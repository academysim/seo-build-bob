# -*- coding: utf-8 -*-
"""Tests for shared/tools/live_audit.py.

All tests serve fixture pages from a local http.server on 127.0.0.1.
No real internet requests are made.

Covered scenarios:
  1. A good page (GA4, canonical, JSON-LD, exactly one h1) → passes.
  2. A page missing the GA4 tag → fails with NO-GA4.
  3. A URL that returns 404 → fails.
  4. An empty sitemap (no <loc> URLs) → sitemap error, host fails.
  5. main() returns exit 1 when zero pages are checked (all sitemaps empty).

Run:
  python -m unittest shared/tests/test_live_audit.py
  python -m unittest discover -s shared/tests
"""
import http.server
import io
import os
import sys
import threading
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _ROOT)

from shared.tools import live_audit       # noqa: E402
from shared.tools import audit_lib        # noqa: E402
from shared.tools.constants import GA4_TAG  # noqa: E402


# ---------------------------------------------------------------------------
# Fixture HTML
# ---------------------------------------------------------------------------

_GOOD_HTML = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    # GA4 tag: embed the real measurement ID so check_ga4(html, GA4_TAG) passes.
    '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
    '<script>\n'
    '  window.dataLayer = window.dataLayer || [];\n'
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    "  gtag('config', '%s');\n"
    '</script>\n'
    '<link rel="canonical" href="https://example.com/good">\n'
    '<script type="application/ld+json">'
    '{"@context":"https://schema.org","@type":"WebPage"}'
    '</script>\n'
    '<title>Good Page</title>\n'
    '</head>\n'
    '<body>\n'
    '<h1>Good Page</h1>\n'
    '<p>All checks should pass.</p>\n'
    '</body>\n'
    '</html>\n'
) % (GA4_TAG, GA4_TAG)

_NO_GA4_HTML = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    '<link rel="canonical" href="https://example.com/no-ga4">\n'
    '<script type="application/ld+json">'
    '{"@context":"https://schema.org","@type":"WebPage"}'
    '</script>\n'
    '<title>No GA4</title>\n'
    '</head>\n'
    '<body>\n'
    '<h1>No GA4 Page</h1>\n'
    '</body>\n'
    '</html>\n'
)

_EMPTY_SITEMAP = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '</urlset>\n'
)


def _sitemap_for(port, paths):
    """Return a sitemap XML string with one <loc> per path."""
    locs = ''.join(
        '<url><loc>http://127.0.0.1:%d%s</loc></url>\n' % (port, p)
        for p in paths
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + locs +
        '</urlset>\n'
    )


# ---------------------------------------------------------------------------
# Minimal fixture HTTP server
# ---------------------------------------------------------------------------

class _FixtureHandler(http.server.BaseHTTPRequestHandler):
    """Serve responses from ``self.server.routes`` dict.

    routes: { path_str: (status_int, content_type_str, body_str) }
    Anything not in routes returns 404.
    """

    def log_message(self, fmt, *args):   # suppress request logs
        pass

    def do_GET(self):   # noqa: N802
        routes = self.server.routes     # type: ignore[attr-defined]
        if self.path in routes:
            code, ctype, body = routes[self.path]
        else:
            code, ctype, body = 404, 'text/plain', 'Not Found'
        encoded = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(encoded)))
        self.send_header('Connection', 'close')   # don't hold keep-alive sockets
        self.end_headers()
        self.wfile.write(encoded)


def _start_server(routes):
    """Start a fixture server on a free port.  Returns (server, port)."""
    server = http.server.HTTPServer(('127.0.0.1', 0), _FixtureHandler)
    server.routes = routes              # type: ignore[attr-defined]
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, port


# ---------------------------------------------------------------------------
# Unit tests for the two new audit_lib functions
# ---------------------------------------------------------------------------

class TestCheckCanonical(unittest.TestCase):

    def test_present_returns_empty(self):
        html = '<link rel="canonical" href="https://example.com/">'
        self.assertEqual([], audit_lib.check_canonical(html))

    def test_absent_returns_error(self):
        self.assertEqual(['NO-CANONICAL'], audit_lib.check_canonical('<html></html>'))

    def test_single_quotes_not_matched(self):
        # The check looks for the exact string rel="canonical" (double quotes).
        # Single-quoted canonical is considered absent (matches offline audit logic).
        html = "<link rel='canonical' href='https://example.com/'>"
        self.assertEqual(['NO-CANONICAL'], audit_lib.check_canonical(html))


class TestCheckH1(unittest.TestCase):

    def test_exactly_one_returns_empty(self):
        self.assertEqual([], audit_lib.check_h1('<h1>Hello</h1>'))

    def test_zero_returns_error(self):
        self.assertEqual(['h1=0'], audit_lib.check_h1('<h2>Nope</h2>'))

    def test_two_returns_error(self):
        self.assertEqual(['h1=2'], audit_lib.check_h1('<h1>A</h1><h1>B</h1>'))

    def test_h1_with_attributes_counted(self):
        self.assertEqual([], audit_lib.check_h1('<h1 class="big">Title</h1>'))


# ---------------------------------------------------------------------------
# Unit tests for parse_sitemap_urls
# ---------------------------------------------------------------------------

class TestParseSitemapUrls(unittest.TestCase):

    def test_extracts_locs(self):
        xml = (
            '<urlset>'
            '<url><loc>https://example.com/a</loc></url>'
            '<url><loc>https://example.com/b</loc></url>'
            '</urlset>'
        )
        urls = live_audit.parse_sitemap_urls(xml)
        self.assertEqual(urls, ['https://example.com/a', 'https://example.com/b'])

    def test_empty_sitemap_returns_empty_list(self):
        self.assertEqual([], live_audit.parse_sitemap_urls(_EMPTY_SITEMAP))


# ---------------------------------------------------------------------------
# Integration tests using a local HTTP server
# ---------------------------------------------------------------------------

class _ServerMixin(unittest.TestCase):
    """Base class that starts a fixture HTTP server and shuts it down cleanly."""

    def _start(self, routes):
        """Start a fixture server; must be called from the test method body."""
        server = http.server.HTTPServer(('127.0.0.1', 0), _FixtureHandler)
        server.timeout = 0.5             # max time blocked in select() per loop
        port = server.server_address[1]
        server.routes = routes           # type: ignore[attr-defined]
        t = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.1))
        t.daemon = True
        t.start()
        self._server = server
        self._thread = t
        return port

    def setUp(self):
        self._server = None
        self._thread = None

    def tearDown(self):
        if self._server:
            self._server.shutdown()   # blocks until serve_forever exits
            self._server.server_close()
        # _thread is daemon; shutdown() already ensured it finished.


class TestLiveAuditGoodPage(_ServerMixin):
    """A sitemap with one good page must pass (audit_host returns failed=0)."""

    def test_good_page_passes(self):
        port = self._start({})         # placeholder; routes need the port
        # Now set the real routes that reference the port we just got.
        self._server.routes = {
            '/sitemap.xml': (200, 'application/xml',
                             _sitemap_for(port, ['/good'])),
            '/good': (200, 'text/html', _GOOD_HTML),
        }
        lines = []
        passed, failed, sitemap_ok = live_audit._audit_host(
            'fixture', 'http://127.0.0.1:%d' % port, lines
        )
        self.assertTrue(sitemap_ok, 'sitemap should be fetchable')
        self.assertEqual(0, failed,
                         'Expected 0 failures.\n' + '\n'.join(lines))
        self.assertEqual(1, passed)


class TestLiveAuditMissingGA4(_ServerMixin):
    """A page missing the GA4 tag must fail with NO-GA4."""

    def test_missing_ga4_fails(self):
        port = self._start({})
        self._server.routes = {
            '/sitemap.xml': (200, 'application/xml',
                             _sitemap_for(port, ['/no-ga4'])),
            '/no-ga4': (200, 'text/html', _NO_GA4_HTML),
        }
        lines = []
        passed, failed, sitemap_ok = live_audit._audit_host(
            'fixture', 'http://127.0.0.1:%d' % port, lines
        )
        self.assertTrue(sitemap_ok)
        self.assertEqual(1, failed)
        self.assertEqual(0, passed)
        self.assertIn('NO-GA4', '\n'.join(lines))


class TestLiveAudit404(_ServerMixin):
    """A URL in the sitemap that returns 404 must be counted as a failure."""

    def test_404_page_fails(self):
        port = self._start({
            # /missing intentionally absent → handler returns 404
        })
        self._server.routes = {
            '/sitemap.xml': (200, 'application/xml',
                             _sitemap_for(port, ['/missing'])),
        }
        lines = []
        passed, failed, sitemap_ok = live_audit._audit_host(
            'fixture', 'http://127.0.0.1:%d' % port, lines
        )
        self.assertTrue(sitemap_ok)
        self.assertEqual(1, failed)
        self.assertEqual(0, passed)


class TestLiveAuditEmptySitemap(_ServerMixin):
    """An empty sitemap (no <loc> elements) must be treated as a sitemap error."""

    def test_empty_sitemap_is_error(self):
        port = self._start({
            '/sitemap.xml': (200, 'application/xml', _EMPTY_SITEMAP),
        })
        lines = []
        passed, failed, sitemap_ok = live_audit._audit_host(
            'fixture', 'http://127.0.0.1:%d' % port, lines
        )
        self.assertFalse(sitemap_ok,
                         'empty sitemap should set sitemap_ok=False')
        self.assertEqual(0, passed)
        self.assertEqual(0, failed)


class TestMainZeroPages(_ServerMixin):
    """main() must return exit code 1 when zero pages are checked."""

    def test_zero_pages_exits_1(self):
        port = self._start({
            '/sitemap.xml': (200, 'application/xml', _EMPTY_SITEMAP),
        })

        # Patch the HOSTS dict that live_audit.main() reads at call time.
        # live_audit imports `constants` as `_constants` and reads
        # _constants.HOSTS each call, so we patch the attribute on that
        # module object — which is the same object as live_audit._constants.
        original_hosts = live_audit._constants.HOSTS
        live_audit._constants.HOSTS = {'fixture': 'http://127.0.0.1:%d' % port}

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exit_code = live_audit.main([])
        finally:
            sys.stdout = old_stdout
            live_audit._constants.HOSTS = original_hosts

        self.assertEqual(1, exit_code,
                         'expected exit code 1 when zero pages are checked')


if __name__ == '__main__':
    unittest.main()
