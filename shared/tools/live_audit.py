# -*- coding: utf-8 -*-
"""Read-only audit of the live Academy web estate.

For each host in shared.tools.constants.HOSTS:
  1. Fetch <host>/sitemap.xml.
  2. Parse every <loc> URL from it.
  3. Fetch each page URL and run the standard per-page checks from audit_lib.

Output: one line per page (URL, HTTP status, OK or problems), a per-host
summary, then a grand total.

Exit codes:
  0  all pages passed all checks
  1  any page failed, any sitemap could not be fetched, or zero pages checked

Options:
  --report <path>   write the full output to <path> in addition to stdout
                    (the ONLY way this script ever writes to a file)

Usage:
  python shared/tools/live_audit.py
  python shared/tools/live_audit.py --report out.txt
"""
import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _ROOT)

from shared.tools import constants as _constants            # noqa: E402
from shared.tools.constants import GA4_TAG                  # noqa: E402
from shared.tools.audit_lib import (                        # noqa: E402
    check_ga4, check_json_ld, check_canonical, check_h1,
)

# ---------------------------------------------------------------------------
# HTTP settings
# ---------------------------------------------------------------------------

_USER_AGENT = 'academy-live-audit/1.0'
_TIMEOUT    = 15     # seconds
_PAUSE      = 0.5    # seconds between requests
_RE_LOC     = re.compile(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', re.IGNORECASE)


# ---------------------------------------------------------------------------
# HTTP helpers  (stdlib urllib, GET only, one at a time)
# ---------------------------------------------------------------------------

def _get(url):
    """Fetch *url* with GET.  Returns (status_code, body_text).

    On network / timeout errors returns (0, error_message_string).
    """
    req = urllib.request.Request(
        url,
        headers={'User-Agent': _USER_AGENT, 'Connection': 'close'},
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            charset = resp.headers.get_content_charset() or 'utf-8'
            return resp.status, resp.read().decode(charset, errors='replace')
    except urllib.error.HTTPError as exc:
        body = ''
        try:
            body = exc.read().decode('utf-8', errors='replace')
        except Exception:
            pass
        return exc.code, body
    except Exception as exc:
        return 0, str(exc)


def _fetch(url):
    """Fetch *url* then sleep _PAUSE seconds.  Returns (status, body)."""
    result = _get(url)
    time.sleep(_PAUSE)
    return result


# ---------------------------------------------------------------------------
# Sitemap parsing
# ---------------------------------------------------------------------------

def parse_sitemap_urls(xml):
    """Return list of <loc> URL strings from *xml*."""
    return _RE_LOC.findall(xml)


# ---------------------------------------------------------------------------
# Per-page checks  (reuse audit_lib functions)
# ---------------------------------------------------------------------------

def _check_page(html):
    """Run every audit_lib check and return a combined list of problem strings."""
    probs = []
    probs.extend(check_ga4(html, GA4_TAG))
    probs.extend(check_canonical(html))
    probs.extend(check_json_ld(html))
    probs.extend(check_h1(html))
    return probs


# ---------------------------------------------------------------------------
# Per-host audit
# ---------------------------------------------------------------------------

def _audit_host(name, origin, out):
    """Audit all pages for one host.

    Appends formatted text to *out* (list of str) and also prints each line.
    Returns (pages_passed, pages_failed, sitemap_ok).
    """
    def emit(line):
        out.append(line)
        print(line)

    sitemap_url = origin + '/sitemap.xml'
    emit('')
    emit('=' * 72)
    emit('HOST: %s  (%s)' % (name, origin))
    emit('sitemap: %s' % sitemap_url)
    emit('')

    status, body = _fetch(sitemap_url)
    if status != 200:
        emit('  ERROR  sitemap fetch failed (HTTP %d)' % status)
        return 0, 0, False

    page_urls = parse_sitemap_urls(body)
    if not page_urls:
        emit('  ERROR  sitemap returned 0 <loc> URLs (empty sitemap)')
        return 0, 0, False

    emit('  %d URL(s) in sitemap' % len(page_urls))
    emit('')

    passed = 0
    failed = 0
    for url in page_urls:
        pg_status, pg_body = _fetch(url)
        if pg_status != 200:
            emit('  FAIL  [%d]  %s' % (pg_status, url))
            emit('          * HTTP %d' % pg_status)
            failed += 1
            continue

        probs = _check_page(pg_body)
        if probs:
            emit('  FAIL  [200]  %s' % url)
            for p in probs:
                emit('          * %s' % p)
            failed += 1
        else:
            emit('  ok    [200]  %s' % url)
            passed += 1

    emit('')
    emit('  %s: %d passed, %d failed  (%d pages checked)'
         % (name, passed, failed, passed + failed))
    return passed, failed, True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Read-only audit of the live Academy web estate.',
    )
    parser.add_argument(
        '--report', metavar='PATH', default=None,
        help='Write full output to PATH in addition to stdout.',
    )
    args = parser.parse_args(argv)

    out = []

    def emit(line):
        out.append(line)
        print(line)

    emit('academy-live-audit/1.0')
    emit('Hosts: %s' % list(_constants.HOSTS.keys()))

    total_passed     = 0
    total_failed     = 0
    any_sitemap_err  = False

    for name, origin in _constants.HOSTS.items():
        passed, failed, sitemap_ok = _audit_host(name, origin, out)
        total_passed    += passed
        total_failed    += failed
        if not sitemap_ok:
            any_sitemap_err = True

    total_pages = total_passed + total_failed
    emit('')
    emit('=' * 72)
    emit('GRAND TOTAL')
    emit('  pages checked : %d' % total_pages)
    emit('  passed        : %d' % total_passed)
    emit('  failed        : %d' % total_failed)

    if total_pages == 0:
        emit('')
        emit('RESULT: FAIL  (zero pages were checked)')
        exit_code = 1
    elif any_sitemap_err or total_failed > 0:
        emit('')
        emit('RESULT: FAIL')
        exit_code = 1
    else:
        emit('')
        emit('RESULT: PASS')
        exit_code = 0

    # Write report only when --report was explicitly supplied.
    if args.report:
        try:
            with open(args.report, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(out) + '\n')
            print('Report written to: %s' % args.report)
        except OSError as exc:
            print('WARNING: could not write report to %s: %s' % (args.report, exc),
                  file=sys.stderr)

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
