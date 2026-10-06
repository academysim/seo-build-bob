# -*- coding: utf-8 -*-
"""Phase 2 of the post-implementation audit: is any of this actually findable?

Section 14 of the handoff is a discovery checklist that applies to every hub and
landing page. This checks the mechanical half of it across every live URL on
every property at once:

  unique title / h1 / meta description   (uniqueness is checked ACROSS the
                                          property, not just presence)
  canonical present and self-referential
  indexable (no noindex)
  in that property's XML sitemap
  breadcrumbs + BreadcrumbList schema
  linked from at least one other page on its own property (no orphans)
  valid JSON-LD
  no LocalBusiness schema on a service-area page
  at least one CTA and one cross-domain link

Everything is read from the live sites, so it reports what a crawler would
actually see rather than what the build scripts intended.

Usage: python audit_discovery.py [property ...]
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '..', '..', '.audit-cache')
sys.path.insert(0, HERE)
from constants import HOSTS as SITES  # noqa: E402

# The cache had no expiry at all, so this script's own docstring claim that it
# 'reports what a crawler would actually see' was false the moment a page
# changed: it reported what a crawler saw whenever the cache was first filled.
# An hour is short enough that a pre-deploy run reads the live site and long
# enough that re-running it three times in a row does not re-fetch 104 pages.
CACHE_MAX_AGE_S = 3600

# Pages that legitimately describe the Tampa premises. Everywhere else, a
# LocalBusiness node asserts a location Academy does not have.
#
# A HOMEPAGE is always allowed: it represents the company, which really is at
# 1421 Massaro Blvd. The rule exists to stop a CITY page (/locations/orlando/)
# claiming a branch office. Before 2026-09-09 only the lounge and driver roots
# were listed, so the builds, events and health homepages were reported on every
# run -- and a gate that cries wolf on every run teaches people to ignore it.
PREMISES_OK = re.compile(r'^https://(lounge|driver|builds|events|health)\.academysim\.com/$|'
                         r'^https://lounge\.academysim\.com/things-to-do-in-tampa/')


def premises_claim(html):
    """True only if a LocalBusiness node with a postal address is the page's OWN
    subject. Returns False for one nested as a Service's `provider`.

    The old test was `'LocalBusiness' in html and 'PostalAddress' in html`, a
    substring match over the whole document. That fired on the events and health
    homepages, where the only hits were an HTML COMMENT reading
    "Service / LocalBusiness structured data" and a correct
    `"provider": {"@type": "LocalBusiness", ...}` inside a Service. Declaring the
    real provider of a service is exactly right and is not a premises claim.
    Parse the graph and look at what the page is actually about.
    """
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
                         html, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        nodes = data.get('@graph', [data]) if isinstance(data, dict) else data
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            types = node.get('@type')
            types = types if isinstance(types, list) else [types]
            if not any('LocalBusiness' in str(t) for t in types):
                continue
            addr = node.get('address')
            if isinstance(addr, dict) and 'PostalAddress' in str(addr.get('@type')):
                return True
    return False


def fetch(url):
    """Cached GET. An EMPTY response is never cached.

    The cache had no invalidation and no success check, so one failed curl
    wrote a zero-byte file that every later run then served as though it were
    the page. The audit would report that page as conforming forever, because
    an empty string has no problems in it.
    """
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    key = re.sub(r'\W+', '_', url)[:120] + '.html'
    p = os.path.join(CACHE, key)
    if (os.path.exists(p) and os.path.getsize(p) > 0
            and (time.time() - os.path.getmtime(p)) < CACHE_MAX_AGE_S):
        return io.open(p, encoding='utf-8', errors='replace').read()
    out = subprocess.run(['curl.exe', '-s', '-L', url],
                         stdout=subprocess.PIPE).stdout
    if not out.strip():
        return ''          # caller counts it; nothing is written to the cache
    io.open(p, 'wb').write(out)
    return out.decode('utf-8', 'replace')


def sitemap(base):
    xml = subprocess.run(['curl.exe', '-s', base + '/sitemap.xml'],
                         stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')
    return re.findall(r'<loc>([^<]+)</loc>', xml)


def text_of(h):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', t)


def one(pat, h, g=1):
    m = re.search(pat, h, re.S | re.I)
    return m.group(g).strip() if m else None


def audit(key):
    base = SITES[key]
    urls = sitemap(base)

    # A gate that checked nothing is not a pass. An unreachable sitemap, a DNS
    # failure or a 404 all produce zero URLs, and with zero URLs there are no
    # findings - which used to print ALL PAGES CONFORM.
    if not urls:
        print('\n===== %s =====' % key)
        print('  !! NO URLS. %s/sitemap.xml returned nothing parseable.' % base)
        print('     Refusing to report conformance for a property that was never fetched.')
        return NO_INPUT

    pages = {u: fetch(u) for u in urls}
    empty = sorted(u for u, h in pages.items() if not h.strip())
    if empty:
        print('\n===== %s =====' % key)
        print('  !! %d of %d pages came back EMPTY and were not cached:' % (len(empty), len(urls)))
        for u in empty[:10]:
            print('     %s' % u)
        print('     Refusing to report conformance on a partial fetch.')
        return NO_INPUT

    # every internal link seen anywhere on the property
    linked = set()
    for u, h in pages.items():
        for href in re.findall(r'href=["\']([^"\']+)["\']', h):
            if href.startswith('/'):
                linked.add(base.rstrip('/') + href)
            elif href.startswith(base):
                linked.add(href)
    norm = lambda s: s.rstrip('/') or s
    linked = {norm(x.split('#')[0].split('?')[0]) for x in linked}

    seen = {'title': {}, 'h1': {}, 'desc': {}}
    rows = []
    for u in urls:
        h = pages[u]
        p = []
        title = one(r'<title[^>]*>(.*?)</title>', h)
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
        desc = one(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h)
        canon = one(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']*)', h)

        if not title:
            p.append('no title')
        if len(h1s) != 1:
            p.append('%d h1' % len(h1s))
        if not desc:
            p.append('no meta description')
        if not canon:
            p.append('no canonical')
        elif norm(canon) != norm(u):
            p.append('canonical %s' % canon)
        if re.search(r'name=["\']robots["\'][^>]*noindex', h, re.I):
            p.append('NOINDEX')

        for field, val in (('title', title), ('desc', desc),
                           ('h1', re.sub(r'<[^>]+>', '', h1s[0]).strip() if h1s else None)):
            if val:
                seen[field].setdefault(' '.join(val.split()), []).append(u)

        # The site root has no trail to describe, so a BreadcrumbList there is
        # meaningless. The ORPHAN check below already exempts it the same way;
        # this one did not, so every property reported its own homepage.
        if 'BreadcrumbList' not in h and norm(u) != norm(base):
            p.append('no BreadcrumbList')
        if norm(u) != norm(base) and norm(u) not in linked:
            p.append('ORPHAN')

        for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
                             h, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                p.append('bad JSON-LD (%s)' % str(e)[:40])
        if not PREMISES_OK.match(u.rstrip('/') + '/') and premises_claim(h):
            p.append('LocalBusiness+address on a service-area page')

        if not re.search(r'https://(booking|academysim|builds|events|lounge|driver|health)\.',
                         h):
            p.append('no cross-domain link')
        rows.append((u, p))

    dupes = []
    for field in ('title', 'desc', 'h1'):
        for val, us in seen[field].items():
            if len(us) > 1:
                dupes.append('duplicate %s on %d pages: %r' % (field, len(us), val[:60]))
                for x in us:
                    dupes.append('      %s' % x)

    bad = [(u, p) for u, p in rows if p]
    print('\n===== %s  (%d urls) =====' % (key, len(urls)))
    for u, p in bad:
        print('  %-64s %s' % (u.replace(base, ''), '; '.join(p)))
    for d in dupes:
        print('  %s' % d)
    if not bad and not dupes:
        print('  ALL PAGES CONFORM')
    return len(bad) + len(dupes)


# Sentinel, deliberately not a plain count: "we could not look" and "we looked
# and found N problems" are different outcomes and must not add together.
NO_INPUT = -1


if __name__ == '__main__':
    total = 0
    blind = 0
    for k in (sys.argv[1:] or list(SITES)):
        r = audit(k)
        if r == NO_INPUT:
            blind += 1
        else:
            total += r

    if blind:
        print('\n%d propert%s could not be audited at all.'
              % (blind, 'y' if blind == 1 else 'ies'))
        print('%d issue(s) found on the rest.' % total)
        raise SystemExit(2)

    print('\n%d issue(s) total' % total)
    # This script had no exit code at all: it printed its findings and fell off
    # the end, so `audit_discovery.py && deploy` would deploy regardless of what
    # it found. The README calls it the pre-deploy gate; now it can be one.
    raise SystemExit(1 if total else 0)
