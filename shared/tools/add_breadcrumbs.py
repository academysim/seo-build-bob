# -*- coding: utf-8 -*-
"""Phase 2: emit BreadcrumbList schema from the breadcrumbs already on the page.

The discovery audit found visible breadcrumbs on 76 of the built pages and
BreadcrumbList markup on none of them, so Google was shown a flat site with no
hierarchy. Section 14 of the handoff asks for both.

The trail is DERIVED from the visible markup rather than rebuilt from the URL.
That matters: if the two ever disagree, structured data that contradicts the
visible page is a markup violation, and deriving it makes disagreement
impossible. It also means the labels stay whatever the page actually says
("Who It Is For", "Service Areas") instead of something regenerated from a slug.

The final crumb has no link, so its item is the canonical URL of the page
itself. Positions are 1-based and include every crumb, which is what Google's
BreadcrumbList documentation expects.

Reads and rewrites <property>/site/**/index.html in place, then the property's
own deploy step picks them up. Homepages are skipped: a breadcrumb list on the
root of a site points only at itself.

Usage: python add_breadcrumbs.py [property ...]
"""
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)
from shared.tools.constants import HOSTS

BASE = HOSTS

CRUMB = re.compile(
    r'<div class="crumbs?">(?:<div class="crumb-in">)?(.*?)</div>', re.S)
PART = re.compile(r'<a href="([^"]*)">(.*?)</a>|([^<>/][^<>]*)')
MARKER = 'BreadcrumbList'


def trail(block, base, canon):
    """[(name, url), ...] from the visible crumb markup."""
    out = []
    for m in PART.finditer(block):
        if m.group(1) is not None:
            name = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            href = m.group(1)
            url = base.rstrip('/') + href if href.startswith('/') else href
        else:
            name = re.sub(r'<[^>]+>', '', m.group(3)).strip(' / ')
            url = canon
        if name:
            out.append((name, url))
    return out


def build(key):
    base = BASE[key]
    changed = skipped = 0
    for f in sorted(glob.glob(os.path.join(ROOT, key, 'site', '**', 'index.html'),
                              recursive=True)):
        h = io.open(f, encoding='utf-8').read()
        rel = os.path.relpath(f, os.path.join(ROOT, key, 'site')).replace(os.sep, '/')
        if rel == 'index.html':
            skipped += 1
            continue
        if MARKER in h:
            skipped += 1
            continue
        m = CRUMB.search(h)
        if not m:
            print('  -- %-52s no visible breadcrumb, skipped' % rel)
            skipped += 1
            continue
        canon = re.search(r'rel="canonical" href="([^"]*)"', h)
        canon = canon.group(1) if canon else base + '/' + rel.replace('index.html', '')
        items = trail(m.group(1), base, canon)
        if len(items) < 2:
            print('  -- %-52s only %d crumb(s), skipped' % (rel, len(items)))
            skipped += 1
            continue
        data = {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u}
                for i, (n, u) in enumerate(items)],
        }
        block = ('<script type="application/ld+json">\n%s\n</script>\n'
                 % json.dumps(data, indent=2, ensure_ascii=False))
        if '</head>' not in h:
            print('  !! %s has no </head>' % rel)
            return -1
        h = h.replace('</head>', block + '</head>', 1)
        io.open(f, 'w', encoding='utf-8', newline='').write(h)
        print('  ok  %-52s %s' % (rel, ' > '.join(n for n, _ in items)))
        changed += 1
    print('  %s: %d written, %d skipped' % (key, changed, skipped))
    return changed


if __name__ == '__main__':
    total = 0
    for k in (sys.argv[1:] or list(BASE)):
        n = build(k)
        if n < 0:
            sys.exit(1)
        total += n
    print('\n%d page(s) given BreadcrumbList schema' % total)
