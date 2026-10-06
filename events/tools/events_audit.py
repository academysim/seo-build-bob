# -*- coding: utf-8 -*-
"""Conformity audit for the new events.academysim.com pages."""
import io, os, re, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import GA4_TAG
from shared.tools.audit_lib import (
    walk_pages, check_zero_pages, check_ai_phrases, check_tag_balance,
    check_json_ld, check_ga4, check_internal_links, check_sitemap_coverage,
    print_final, exit_audit,
)

# Default to this property's real output. The old default was the temporary
# scratchpad name from the build session (events_new), which no longer exists, and
# os.walk over a missing directory yields nothing - so the audit printed
# '0 pages, ALL OK' and exited 0. A gate that checks nothing must never pass.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ROOT, 'events', 'upload')

AI = ['delve', 'testament to', 'seamless', 'elevate your', 'cutting-edge',
      'state-of-the-art', 'game-changer', 'in today', 'it is worth noting',
      'ultimately,', 'robust', 'leverage', 'look no further', 'when it comes to',
      'plethora', 'myriad']

# The brief forbids CLAIMING these. Asking "Is this an official X simulator?"
# and answering "No, we are not affiliated" is the required treatment, so a
# match only counts when it is not immediately denied.
OFFICIAL = re.compile(r'official (formula 1|nascar|imsa|f1) simulator', re.I)
DENIAL = re.compile(r'\b(no\.|not affiliated|are not affiliated)', re.I)

# Wording the brief requires for cities with no Academy presence.
BRANCHY = re.compile(r'academy (orlando|sarasota|miami|daytona|jacksonville)\s+'
                     r'(location|showroom|office|branch)', re.I)

paths = {'/'}
pages = walk_pages(D)
for rel, _ in pages:
    paths.add('/' + rel[:-len('index.html')])

fail = 0
for rel, p in pages:
    s = io.open(p, encoding='utf-8', newline='').read()
    probs = []

    body = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', ' ', s, flags=re.S)
    text = ' '.join(re.sub(r'<[^>]+>', ' ', body).split())
    low = text.lower()

    if re.search(r'&mdash;|—', body):
        probs.append('EM-DASH')
    probs.extend(check_ai_phrases(low, AI))

    for m in OFFICIAL.finditer(text):
        after = text[m.end():m.end() + 140]
        if not DENIAL.search(after):
            probs.append('UNDENIED-OFFICIAL-CLAIM')

    if BRANCHY.search(text):
        probs.append('IMPLIES-A-BRANCH')

    # a location page must say plainly that there is no branch there
    # Tampa is the actual location, so the no-branch disclaimer must NOT appear
    # there. It said 'we do not have a branch in Tampa' once. Never again.
    if rel == 'locations/tampa/index.html':
        if 'branch in tampa' in low or 'showroom or branch in tampa' in low:
            probs.append('DENIES-OWN-HOME-CITY')
    elif rel.startswith('locations/') and rel != 'locations/index.html':
        if 'do not have' not in low and 'one facility' not in low:
            probs.append('NO-BRANCH-DISCLAIMER')

    if '<body class=' in s:
        probs.append('BODY-CLASS-SCROLL-RISK')
    if '<div class="lp">' not in s:
        probs.append('NO-LP-WRAPPER')
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

    probs.extend(check_tag_balance(s))
    probs.extend(check_json_ld(s))
    probs.extend(check_internal_links(s, paths))

    print('  %-46s %7d  %s' % (rel, len(s.encode()),
                               'OK' if not probs else '*** ' + '; '.join(sorted(set(probs)))))
    if probs:
        fail += 1

check_zero_pages(pages, D)

# COVERAGE. A page that is live but was never opened here is not a page that
# passed. Until 2026-08-31 this audit had no coverage assertion at all: it
# matched the live sitemap by discipline, not by construction, so a URL added
# live and never added locally would have been audited by nothing and no gate
# would have said so. Same family as the 0-pages guard above, one level out.
_sm = os.path.join(_ROOT, 'events', 'site', 'sitemap.xml')
fail = check_sitemap_coverage(pages, _sm, fail)

print_final(pages, fail)
exit_audit(fail)
