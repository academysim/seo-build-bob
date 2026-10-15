# -*- coding: utf-8 -*-
"""Conformity audit for new builds.academysim.com pages.

Checks only the content I author. The inherited <nav> and <footer> carry em
dashes in Malik's own copy (including an aria-label), so they are excluded
rather than rewritten.
"""
import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
import builds_prices as P
from shared.tools.constants import GA4_TAG
from shared.tools.paths import prop_root
from shared.tools.audit_lib import (
    walk_pages, check_zero_pages, check_ai_phrases, check_british,
    check_tag_balance, check_ga4, check_internal_links,
    check_sitemap_coverage, print_final, exit_audit,
)

# Default to this property's real output. The old default was the temporary
# scratchpad name from the build session (builds_new), which no longer exists, and
# os.walk over a missing directory yields nothing - so the audit printed
# '0 pages, ALL OK' and exited 0. A gate that checks nothing must never pass.
_ROOT = prop_root('builds')
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ROOT, 'upload')

AI = ['delve', 'testament to', 'seamless', 'elevate your', 'cutting-edge',
      'state-of-the-art', 'game-changer', 'in today', 'it is worth noting',
      'ultimately,', 'leverage', 'look no further', 'when it comes to',
      'plethora', 'myriad', 'unlock the']

BRITISH = ['tyre', 'kerb', 'practise', 'centre', 'organiser', 'colour', 'favour',
           'whilst', 'amongst', 'neighbourhood', 'programme', 'metre', 'realise',
           'customise', 'behaviour', 'marquee', 'car park']

# The only prices that may appear on a published page.
#
# This list is NOT typed here any more. It used to be, and on 2026-08-31 that
# copy was found holding the pre-2026-08-31 ladder: the gate passed the 22
# pages carrying the old prices and failed the one page carrying the right
# ones, which is how the defect stayed invisible for a day. A gate that holds
# its own copy of the answer is calibrated to whatever the answer was when it
# was written. It now reads the same source the pages are rendered from, so a
# price change cannot make the gate and the site disagree.
PRICES = P.ALL_PRICES

# The same ladder in the format JSON-LD uses: no currency symbol, no grouping.
# Derived, never typed - a second hand-maintained copy of the ladder is the
# exact defect the comment above describes.
BARE_PRICES = set(p.replace('$', '').replace(',', '') for p in P.ALL_PRICES)

paths = {'/'}
pages = walk_pages(D)
for rel, _ in pages:
    paths.add('/' + rel[:-len('index.html')])

# pages that already exist on the live site
LIVE = {'/', '/thank-you'}

fail = 0
for rel, p in pages:
    s = io.open(p, encoding='utf-8', newline='').read()
    probs = []

    # authored content only: strip inherited chrome, code and comments
    authored = re.sub(r'<nav[\s\S]*?</nav>|<footer[\s\S]*?</footer>|'
                      r'<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->', ' ', s)
    text = ' '.join(re.sub(r'<[^>]+>', ' ', authored).split())
    low = text.lower()

    if re.search(r'&mdash;|—', authored):
        probs.append('EM-DASH')
    probs.extend(check_ai_phrases(low, AI))
    probs.extend(check_british(low, BRITISH))

    for m in re.finditer(r'\$\d[\d,]*\d|\$\d', text):
        if m.group(0) not in PRICES:
            probs.append('UNKNOWN-PRICE ' + m.group(0))

    if re.search(r'official (formula 1|nascar|imsa|f1) simulator', low):
        after = low[low.index('official'):]
        if not re.search(r'\b(no\.|not affiliated)', after[:220]):
            probs.append('UNDENIED-OFFICIAL-CLAIM')

    probs.extend(check_ga4(s, GA4_TAG))
    if s.count('<h1') != 1:
        probs.append('h1=%d' % s.count('<h1'))
    if 'rel="canonical"' not in s:
        probs.append('NO-CANONICAL')
    if 'content_view' not in s:
        # NOT 'no analytics'. GA4 (GA4_TAG) is loaded site-wide on every property;
        # this only means the custom content_view event is absent from THIS page. The
        # old NO-TRACKING label was read as a tracking outage on 2026-08-31 and produced
        # a false alarm that the August booking diagnosis had been made blind.
        probs.append('NO-CONTENT-VIEW')
    if '#start' not in s:
        probs.append('NO-QUOTE-CTA')

    probs.extend(check_tag_balance(s))

    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(b)
        except Exception:
            probs.append('BAD-JSON-LD')
        # Prices inside JSON-LD are checked HERE and nowhere else. The visible
        # sweep above runs on `authored`, which has already had every <script>
        # stripped out of it, so a structured-data price has never been compared
        # against the ladder - and it is written bare ("18995") where the visible
        # one is grouped ("$18,995"), so a sweep looking for the grouped form
        # cannot see it even when it is handed the markup. Both halves of that
        # are needed to explain why 2026-08-31 was possible.
        #
        # This is the number Google reads. A page can show the right price to a
        # customer and publish a stale one to the shopping surface, and every
        # gate that existed on 2026-09-01 would have called that page OK.
        for _pm in re.finditer(r'"(?:price|lowPrice|highPrice)"\s*:\s*"?([0-9][0-9,.]*)"?', b):
            _raw = _pm.group(1).replace(',', '')
            if _raw not in BARE_PRICES:
                probs.append('UNKNOWN-JSONLD-PRICE ' + _pm.group(1))

    # Quote-agnostic: the old pattern matched double-quoted hrefs only,
    # so any single-quoted link was invisible to this check. See
    # driver_audit.py for the case that found it (429 unchecked links).
    for h in set(re.findall(r'href=["\'](/[^"\'#?]*)["\']', s)):
        if h.endswith(('.xml', '.txt', '.png', '.svg', '.ico', '.webmanifest', '.jpg')):
            continue
        if h not in paths and h not in LIVE:
            probs.append('BROKEN ' + h)

    print('  %-52s %7d  %s' % (rel, len(s.encode()),
                               'OK' if not probs else '*** ' + '; '.join(sorted(set(probs)))))
    if probs:
        fail += 1

check_zero_pages(pages, D)

# COVERAGE. A page that is live but was never opened here is not a page that
# passed. Until 2026-08-31 this audit had no coverage assertion at all: it
# matched the live sitemap by discipline, not by construction, so a URL added
# live and never added locally would have been audited by nothing and no gate
# would have said so. Same family as the 0-pages guard above, one level out.
_sm = os.path.join(_ROOT, 'site', 'sitemap.xml')
fail = check_sitemap_coverage(pages, _sm, fail)

print_final(pages, fail)
exit_audit(fail)
