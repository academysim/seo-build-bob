# -*- coding: utf-8 -*-
"""Whole-site conformity audit over the deploy tree."""
import io, os, re, json, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import GA4_TAG
from shared.tools.audit_lib import (
    walk_pages, check_zero_pages, check_ai_phrases, check_ga4,
)

# 'lounge_deploy' was the temporary session scratchpad directory and has not
# existed since the work moved into this repo. Bare, this crashed with
# FileNotFoundError on lounge_deploy/sitemap.xml - loudly, unlike the other
# four audits which passed silently, but still never auditing anything.
#
# Points at site/ rather than upload/ because sitemap.xml lives in site/ and
# this audit cross-checks every sitemap URL against a file on disk. Note the
# consequence: patches that fix_*.py writes only into upload/ are NOT seen
# here. Pass the directory explicitly to audit something else.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ROOT, 'lounge', 'site')

AI = ['delve', 'testament to', 'seamless', 'elevate your', 'cutting-edge',
      'state-of-the-art', 'game-changer', 'in today', 'it is worth noting',
      'ultimately,', 'robust', 'leverage', 'look no further', 'when it comes to',
      'dive in', 'unlock the', 'a myriad', 'plethora']

# lounge walks index.html only (not all .html)
pages = [(rel, p) for rel, p in walk_pages(D) if rel.endswith('index.html')]

# A gate that checked nothing is not a pass.
check_zero_pages(pages, D)

sitemap = io.open(os.path.join(D, 'sitemap.xml'), encoding='utf-8').read()
locs = set(re.findall(r'<loc>(.*?)</loc>', sitemap))

fails = 0
print('  %-44s %7s %4s %4s %4s %s' % ('page', 'bytes', 'GA', 'h1', 'ld', 'issues'))
for rel, p in pages:
    s = io.open(p, encoding='utf-8', newline='').read()
    probs = []

    # Only judge prose on what a visitor actually reads: strip style, script
    # and HTML comments first. Em dashes inside CSS/JS comments are not copy.
    prose = re.sub(r'<style[\s\S]*?</style>|<script[\s\S]*?</script>|<!--[\s\S]*?-->', ' ', s)

    if re.search(r'__[A-Z_]+__', s):
        probs.append('placeholder')
    if re.search(r'&mdash;|—', prose):
        probs.append('EM-DASH')
    low = prose.lower()
    probs.extend(check_ai_phrases(low, AI))
    probs.extend(check_ga4(s, GA4_TAG))
    if s.count('<h1') != 1:
        probs.append('h1=%d' % s.count('<h1'))
    # <p[ >] so <pre>/<picture> are not counted as paragraphs
    op = len(re.findall(r'<p[ >]', s))
    if op != s.count('</p>'):
        probs.append('p%d/%d' % (op, s.count('</p>')))
    if s.count('<div') != s.count('</div>'):
        probs.append('div%d/%d' % (s.count('<div'), s.count('</div>')))
    if 'rel="canonical"' not in s:
        probs.append('no-canonical')

    # A class applied to <body> that sets overflow:hidden propagates to the
    # viewport and kills user scrolling. Programmatic scrolling still works, so
    # only a human with a mouse notices. Shipped once; never again.
    import re as _re
    for m in _re.finditer(r'<body[^>]*class="([^"]+)"', s):
        for cls in m.group(1).split():
            for rule in _re.findall(r'(?:^|[},])\s*\.' + _re.escape(cls) + r'\s*\{([^}]*)\}', s):
                if _re.search(r'overflow\s*:\s*hidden', rule):
                    probs.append('BODY-OVERFLOW-HIDDEN(.%s)' % cls)
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(blk)
        except Exception as e:
            probs.append('ld-json')

    # canonical should match the path, and be in the sitemap
    m = re.search(r'rel="canonical" href="([^"]+)"', s)
    if m:
        want = 'https://lounge.academysim.com/' + (rel[:-10] if rel.endswith('index.html') else rel)
        if m.group(1) != want:
            probs.append('canonical!=path')
        elif m.group(1) not in locs:
            probs.append('not-in-sitemap')

    ld = len(re.findall(r'application/ld\+json', s))
    ga = s.count(GA4_TAG)
    print('  %-44s %7d %4d %4d %4d %s' % (rel, len(s.encode()), ga, s.count('<h1'), ld,
                                          'OK' if not probs else '*** ' + ' '.join(probs)))
    if probs:
        fails += 1

# links
print('\n  internal links:')
allpaths = set('/' + (r[:-10] if r.endswith('index.html') else r) for r, _ in pages)
broken = 0
for rel, p in pages:
    s = io.open(p, encoding='utf-8', newline='').read()
    # Quote-agnostic: the old pattern matched double-quoted hrefs only,
    # so any single-quoted link was invisible to this check. See
    # driver_audit.py for the case that found it (429 unchecked links).
    for href in set(re.findall(r'href=["\'](/[^"\'#?]*)["\']', s)):
        if href.endswith(('.xml', '.txt', '.ico', '.svg', '.png', '.jpg')):
            continue
        if href not in allpaths:
            print('    BROKEN %s -> %s' % (rel, href))
            broken += 1
print('    %d broken' % broken)

print('\n  sitemap urls: %d   pages on disk: %d' % (len(locs), len(pages)))
for l in sorted(locs):
    pth = l.replace('https://lounge.academysim.com/', '')
    f = os.path.join(D, *(pth.split('/') if pth else []), 'index.html')
    if not os.path.isfile(f):
        print('    SITEMAP URL WITH NO FILE: %s' % l)
        fails += 1

print('\n%s' % ('FAILURES: %d' % fails if (fails or broken) else 'ALL PAGES CONFORM'))
sys.exit(1 if (fails or broken) else 0)
