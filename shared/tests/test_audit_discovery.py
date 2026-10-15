# -*- coding: utf-8 -*-
"""Tests for shared/tools/audit_discovery.py — HTTP logic, offline.

Import strategy
---------------
audit_discovery.py is guarded with ``if __name__ == '__main__'``, so it is
safe to import directly.  The two HTTP entry-points are:

  * sitemap(base)  — subprocess.run(['curl.exe', '-s', base + '/sitemap.xml'])
  * fetch(url)     — subprocess.run(['curl.exe', '-s', '-L', url])

Both are patched with unittest.mock so no real network traffic is produced.

The audit() function is also exercised end-to-end through the mocked HTTP
layer to cover the four scenarios:

  1. Healthy site  — sitemap returns URLs; every page returns 200 with good HTML.
  2. 404 page      — sitemap has one URL that returns an empty body (curl's
                     behaviour when the server returns 404 and -s is used; the
                     function guards against empty responses and returns NO_INPUT).
  3. Redirect      — sitemap fetch returns a 301-like response (empty body);
                     treated the same as an unreachable sitemap → NO_INPUT.
  4. Timeout       — subprocess.run returns empty bytes; treated as empty →
                     NO_INPUT.

Run:
    python -m unittest shared/tests/test_audit_discovery.py
    python -m unittest discover -s shared/tests
"""
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _ROOT)

import shared.tools.audit_discovery as _ad  # noqa: E402


# ---------------------------------------------------------------------------
# Minimal valid HTML for a single page that passes all checks in audit().
# Base URL is always http://example.invalid so PREMISES_OK never matches it.
# ---------------------------------------------------------------------------

_BASE = 'https://example.invalid'

def _good_html(url):
    """Return a minimal page body that satisfies every check in audit()."""
    return (
        '<!DOCTYPE html>'
        '<html><head>'
        '<title>Unique Title For %s</title>'
        '<meta name="description" content="Unique description for %s.">'
        '<link rel="canonical" href="%s">'
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"WebPage",'
        '"name":"Test","breadcrumb":{"@type":"BreadcrumbList","itemListElement":[]}}'
        '</script>'
        '</head><body>'
        '<h1>Unique H1 For %s</h1>'
        '<p>BreadcrumbList is in the JSON-LD above.</p>'
        '<a href="https://booking.academysim.com/">book</a>'
        '<a href="%s/other/">internal link back</a>'
        '</body></html>'
    ) % (url, url, url, url, _BASE)


def _sitemap_xml(urls):
    locs = ''.join('<url><loc>%s</loc></url>' % u for u in urls)
    return ('<?xml version="1.0"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + locs + '</urlset>').encode('utf-8')


def _proc(stdout_bytes):
    """Return a mock subprocess.CompletedProcess."""
    r = MagicMock()
    r.stdout = stdout_bytes
    return r


# ---------------------------------------------------------------------------
# Tests for audit_discovery.fetch()
# ---------------------------------------------------------------------------

class TestAuditDiscoveryFetch(unittest.TestCase):
    """Unit tests for the low-level fetch() that wraps curl."""

    def setUp(self):
        # Use a real temp directory so the cache path logic is exercised
        # without hitting the file system in unexpected places.
        self._tmpdir = tempfile.mkdtemp()
        self._orig_cache = _ad.CACHE
        _ad.CACHE = self._tmpdir

    def tearDown(self):
        _ad.CACHE = self._orig_cache
        # Clean up temp files (best-effort).
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    # ------------------------------------------------------------------
    # 1. Healthy 200
    # ------------------------------------------------------------------

    def test_healthy_200_returns_body(self):
        """fetch() returns the decoded HTML body on a normal 200 response."""
        html = b'<html><h1>Hello</h1></html>'
        with patch('subprocess.run', return_value=_proc(html)):
            body = _ad.fetch('https://example.invalid/good')
        self.assertIn('<h1>Hello</h1>', body)

    # ------------------------------------------------------------------
    # 2. 404 page
    # ------------------------------------------------------------------

    def test_404_empty_response_returns_empty_string(self):
        """When curl returns an empty body (e.g. 404 with -s), fetch returns ''."""
        with patch('subprocess.run', return_value=_proc(b'')):
            body = _ad.fetch('https://example.invalid/missing')
        self.assertEqual('', body)

    # ------------------------------------------------------------------
    # 3. Redirect
    # ------------------------------------------------------------------

    def test_redirect_empty_body_returns_empty_string(self):
        """A redirect response whose body is whitespace-only returns ''."""
        with patch('subprocess.run', return_value=_proc(b'   \n')):
            body = _ad.fetch('https://example.invalid/redirect')
        self.assertEqual('', body)

    # ------------------------------------------------------------------
    # 4. Timeout
    # ------------------------------------------------------------------

    def test_timeout_zero_bytes_returns_empty_string(self):
        """When subprocess.run gives back b'' (timeout/error), fetch returns ''."""
        with patch('subprocess.run', return_value=_proc(b'')):
            body = _ad.fetch('https://example.invalid/slow')
        self.assertEqual('', body)


# ---------------------------------------------------------------------------
# Tests for audit_discovery.sitemap()
# ---------------------------------------------------------------------------

class TestAuditDiscoverySitemap(unittest.TestCase):

    def test_healthy_sitemap_returns_urls(self):
        """sitemap() extracts <loc> URLs from a well-formed sitemap."""
        xml = _sitemap_xml(['https://example.invalid/', 'https://example.invalid/page/'])
        with patch('subprocess.run', return_value=_proc(xml)):
            urls = _ad.sitemap('https://example.invalid')
        self.assertEqual(
            ['https://example.invalid/', 'https://example.invalid/page/'],
            urls,
        )

    def test_404_empty_body_returns_empty_list(self):
        """sitemap() returns [] when curl gives back empty bytes (404/timeout)."""
        with patch('subprocess.run', return_value=_proc(b'')):
            urls = _ad.sitemap('https://example.invalid')
        self.assertEqual([], urls)

    def test_redirect_whitespace_body_returns_empty_list(self):
        """sitemap() returns [] when the response body has no <loc> elements."""
        with patch('subprocess.run', return_value=_proc(b'\n\r\n')):
            urls = _ad.sitemap('https://example.invalid')
        self.assertEqual([], urls)

    def test_timeout_zero_bytes_returns_empty_list(self):
        """sitemap() returns [] on a zero-byte (timeout) response."""
        with patch('subprocess.run', return_value=_proc(b'')):
            urls = _ad.sitemap('https://example.invalid')
        self.assertEqual([], urls)


# ---------------------------------------------------------------------------
# End-to-end tests for audit_discovery.audit()
# ---------------------------------------------------------------------------

class TestAuditDiscoveryAudit(unittest.TestCase):
    """Drive audit() through the four HTTP scenarios via mocked subprocess.run."""

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._orig_cache = _ad.CACHE
        _ad.CACHE = self._tmpdir
        # Inject a test key into SITES so audit() can look up the base URL.
        self._orig_sites = dict(_ad.SITES)
        _ad.SITES['_test'] = _BASE

    def tearDown(self):
        _ad.CACHE = self._orig_cache
        _ad.SITES.clear()
        _ad.SITES.update(self._orig_sites)
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _sitemap_call(self, urls):
        """A subprocess mock result that returns a well-formed sitemap."""
        return _proc(_sitemap_xml(urls))

    def _page_call(self, url):
        """A subprocess mock result returning good HTML for url."""
        return _proc(_good_html(url).encode('utf-8'))

    # ------------------------------------------------------------------
    # 1. Healthy site — audit returns 0 issues
    # ------------------------------------------------------------------

    def test_healthy_site_returns_zero_issues(self):
        """A site where every page is well-formed should return 0 findings."""
        urls = [_BASE + '/']
        # Two subprocess calls: sitemap fetch + one page fetch.
        side_effects = [
            self._sitemap_call(urls),
            self._page_call(urls[0]),
        ]
        with patch('subprocess.run', side_effect=side_effects):
            result = _ad.audit('_test')
        self.assertEqual(0, result)

    # ------------------------------------------------------------------
    # 2. 404 page — audit returns NO_INPUT (empty body from curl)
    # ------------------------------------------------------------------

    def test_404_page_returns_no_input(self):
        """When fetched pages come back empty (404), audit returns NO_INPUT."""
        urls = [_BASE + '/missing/']
        side_effects = [
            self._sitemap_call(urls),
            _proc(b''),   # empty body for the "404" page
        ]
        with patch('subprocess.run', side_effect=side_effects):
            result = _ad.audit('_test')
        self.assertEqual(_ad.NO_INPUT, result)

    # ------------------------------------------------------------------
    # 3. Redirect — sitemap is unreachable (redirect body is empty/unparseable)
    # ------------------------------------------------------------------

    def test_redirect_sitemap_returns_no_input(self):
        """When the sitemap fetch returns no parseable <loc> elements (redirect),
        audit returns NO_INPUT."""
        side_effects = [
            _proc(b'\n'),   # sitemap → no <loc> tags
        ]
        with patch('subprocess.run', side_effect=side_effects):
            result = _ad.audit('_test')
        self.assertEqual(_ad.NO_INPUT, result)

    # ------------------------------------------------------------------
    # 4. Timeout — sitemap subprocess returns zero bytes
    # ------------------------------------------------------------------

    def test_timeout_returns_no_input(self):
        """When subprocess.run returns b'' for the sitemap, audit returns NO_INPUT."""
        side_effects = [
            _proc(b''),   # timeout on sitemap
        ]
        with patch('subprocess.run', side_effect=side_effects):
            result = _ad.audit('_test')
        self.assertEqual(_ad.NO_INPUT, result)


if __name__ == '__main__':
    unittest.main()
