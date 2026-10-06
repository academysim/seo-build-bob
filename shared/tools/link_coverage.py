# -*- coding: utf-8 -*-
"""Count how many sitemap paths a homepage (or homepage+footer, sitewide)
links to, for the 03-hub-links RESULTS.md report.
Usage: python link_coverage.py <key>
"""
import io, os, re, sys

key = sys.argv[1]
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', key))
UP = os.path.join(ROOT, 'upload')

sitemap_p = os.path.join(ROOT, 'site', 'sitemap.xml')
sitemap = io.open(sitemap_p, encoding='utf-8').read()
locs = re.findall(r'<loc>([^<]+)</loc>', sitemap)
paths = set()
for u in locs:
    path = re.sub(r'^https?://[^/]+', '', u)
    if path in ('', '/'):
        continue
    paths.add(path.rstrip('/') + '/')

homepage = os.path.join(UP, 'index.html')
s = io.open(homepage, encoding='utf-8').read()
hrefs = re.findall(r'href=["\']([^"\']+)["\']', s)
linked = set()
for h in hrefs:
    if h.startswith('http') or h.startswith('#') or h.startswith('tel:') or h.startswith('mailto:'):
        continue
    p = h.rstrip('/') + '/'
    if p in paths:
        linked.add(p)

print('%s: sitemap subpages (excl. homepage) = %d' % (key, len(paths)))
print('%s: homepage links to %d of them' % (key, len(linked)))
missing = paths - linked
if missing:
    print('  not linked from homepage:')
    for m in sorted(missing):
        print('    ' + m)
