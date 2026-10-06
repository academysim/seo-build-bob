# -*- coding: utf-8 -*-
"""Shared audit helpers for all five per-property audits.

Each helper is a pure function that takes explicit inputs and returns a list
of problem strings (empty = no problems found).  The caller accumulates them
and decides how to print and exit.

Extracted from the ~80% identical boilerplate across:
  events/tools/events_audit.py
  builds/tools/builds_audit.py
  health/tools/health_audit.py
  driver/tools/driver_audit.py
  lounge/tools/audit_site.py
"""
import io, json, os, re, sys


def walk_pages(directory, extensions=('.html',)):
    """Return a sorted list of (rel, abspath) for every matching file under *directory*.

    *rel* uses forward slashes regardless of OS.  Returns [] if directory does
    not exist or contains no matching files (the caller must guard against 0
    pages with check_zero_pages).
    """
    pages = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(extensions):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, directory).replace(os.sep, '/')
                pages.append((rel, p))
    pages.sort()
    return pages


def check_zero_pages(pages, directory):
    """Print an error and exit(2) when *pages* is empty.

    Call this after walk_pages() but before the per-page loop so a missing or
    empty directory never produces a silent ALL OK.
    """
    if not pages:
        print('\n  !! 0 pages found under %s' % directory)
        print('     Refusing to report OK: an audit that checked nothing is not a pass.')
        sys.exit(2)


def check_ai_phrases(text_lower, ai_list):
    """Return ['ai:<phrase>', ...] for every AI phrase found in *text_lower*."""
    return ['ai:' + t for t in ai_list if t in text_lower]


def check_british(text_lower, british_list):
    """Return ['british:<word>', ...] for every British spelling found."""
    return ['british:' + t for t in british_list
            if re.search(r'\b%s' % t, text_lower)]


def check_tag_balance(html, tags=('<div', '<section', '<p')):
    """Return ['<tag> N/M', ...] for every tag whose open/close counts differ.

    For *<p* the open count uses ``<p[ >]`` to avoid counting ``<pre>``/
    ``<picture>`` as paragraphs (matching lounge audit's existing logic).
    For all tags the close count uses ``</tag>``.
    """
    probs = []
    for tag in tags:
        o = len(re.findall(re.escape(tag) + r'[ >]', html))
        c = html.count('</' + tag[1:] + '>')
        if o != c:
            probs.append('%s %d/%d' % (tag, o, c))
    return probs


def check_json_ld(html):
    """Return ['BAD-JSON-LD'] if any application/ld+json block is invalid JSON."""
    probs = []
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(b)
        except Exception:
            probs.append('BAD-JSON-LD')
    return probs


def check_ga4(html, tag='G-SQL40ZS59K'):
    """Return ['NO-GA4'] if *tag* does not appear in *html*."""
    if html.count(tag) < 1:
        return ['NO-GA4']
    return []


def check_internal_links(html, known_paths):
    """Return ['BROKEN /path', ...] for internal href links not in *known_paths*.

    Skips asset extensions.  Quote-agnostic (matches both single- and
    double-quoted href values).  Does NOT check fragments (use the driver audit's
    anchor_src pattern for that).
    """
    SKIP = ('.xml', '.txt', '.png', '.svg', '.ico', '.webmanifest', '.jpg',
            '.css', '.js')
    probs = []
    for h in set(re.findall(r'href=["\'](/[^"\'#?]*)["\']', html)):
        if h.endswith(SKIP):
            continue
        if h not in known_paths:
            probs.append('BROKEN ' + h)
    return probs


def check_sitemap_coverage(pages, sitemap_path, fail_count=0):
    """Compare *pages* against the sitemap at *sitemap_path*.

    Prints warnings for uncovered URLs and returns an updated *fail_count*.
    If the sitemap file does not exist, prints an error and returns
    fail_count + 1.

    *pages* is a list of (rel, abspath) as returned by walk_pages().
    """
    if not os.path.exists(sitemap_path):
        print('\n  !! no sitemap.xml at %s' % sitemap_path)
        print('     Coverage NOT verified. Refusing to call that a pass.')
        return fail_count + 1

    xml = io.open(sitemap_path, encoding='utf-8').read()
    live = set()
    for loc in re.findall(r'<loc>\s*(.*?)\s*</loc>', xml):
        live.add(re.sub(r'^https?://[^/]+', '', loc) or '/')
    have = set()
    for rel, _ in pages:
        rel = rel.replace(os.sep, '/')
        have.add('/' + (rel[:-len('index.html')] if rel.endswith('index.html') else rel))
        if not rel.endswith('index.html'):
            have.add('/' + rel[:-len('.html')])
    uncovered = sorted(u for u in live if u not in have)
    if uncovered:
        print('\n  !! %d LIVE url(s) in sitemap.xml that this audit never opened:'
              % len(uncovered))
        for u in uncovered:
            print('     %s' % u)
        print('     A page nothing audits is not a page that passed.')
        fail_count += len(uncovered)
    return fail_count


def parse_sitemap(path):
    """Return a list of URL strings from the <loc> elements in *path*.

    Returns [] if the file does not exist.
    """
    if not os.path.exists(path):
        return []
    xml = io.open(path, encoding='utf-8').read()
    return re.findall(r'<loc>\s*(.*?)\s*</loc>', xml)


def print_final(pages, fail):
    """Print the standard ``N pages, FAILURES: M`` / ``ALL OK`` summary line."""
    print('\n  %d pages, %s' % (len(pages), 'FAILURES: %d' % fail if fail else 'ALL OK'))


def exit_audit(fail):
    """sys.exit(1) on any failure, 0 on clean."""
    sys.exit(1 if fail else 0)
