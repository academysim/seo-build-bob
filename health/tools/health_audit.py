# -*- coding: utf-8 -*-
"""Audit for health.academysim.com pages.

The critical checks are medical and outcome claims. Academy is not a medical
provider, and the brief forbids guaranteeing cognitive, neurological,
rehabilitation or health outcomes. Every page must also carry the scope
disclaimer.
"""
import io, os, re, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import GA4_TAG
from shared.tools.paths import prop_root
from shared.tools.audit_lib import (
    walk_pages, check_zero_pages, check_ai_phrases, check_british,
    check_tag_balance, check_json_ld, check_ga4, check_internal_links,
    check_sitemap_coverage, print_final, exit_audit,
)

# Default to this property's real output. The old default was the temporary
# scratchpad name from the build session (health_new), which no longer exists, and
# os.walk over a missing directory yields nothing - so the audit printed
# '0 pages, ALL OK' and exited 0. A gate that checks nothing must never pass.
_ROOT = prop_root('health')
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ROOT, 'upload')

OUTCOME_VERB = r'(improve|improves|improving|boost|boosts|enhance|enhances|restore|restores|reverse|reverses|sharpen|sharpens)'
HEALTH_NOUN = r'(cognition|cognitive|memory|brain|neurological|mobility|balance|reaction time|health|wellbeing)'

FORBIDDEN = [
    # `\w+` cannot cross a hyphen, so this missed 'improves higher-order
    # cognitive functions' entirely: the gate could not see the very claim
    # shape it exists to catch. Hyphen and multi-word tolerant, still bounded.
    OUTCOME_VERB + r'[\s\w-]{0,40}?' + HEALTH_NOUN,
    r'(proven|clinically|medically|therapeutic)\s+\w*\s*(benefit|outcome|result)',
    r'helps?\s+(with\s+|treat\s+)?(dementia|alzheimer|parkinson)',
    # Fires on Academy claiming to RUN one, not on 'alongside post-stroke
    # recovery programs', which refers to other providers' clinical programs
    # and is how all 5 live mentions read. Without the guard this flagged
    # correct, already-hedged copy on every run. 'our post-stroke recovery
    # program' is preceded by 'our post-', not 'alongside post-', so it
    # still fires.
    r'(?<!alongside )(?<!alongside post-)stroke recovery program',
    r'(reduces?|lowers?)\s+(the\s+)?risk of',
    r'clinically proven', r'medically proven', r'doctor recommended',
    r'our (facility|community) partners?',
    r'used in \d+ (communities|facilities)',
    r'trusted by \w+ communities',
]

AI = ['delve', 'testament to', 'seamless', 'elevate your', 'cutting-edge',
      'state-of-the-art', 'game-changer', 'in today', 'it is worth noting',
      'ultimately,', 'leverage', 'look no further', 'when it comes to']

BRITISH = ['tyre', 'kerb', 'practise', 'centre', 'organiser', 'colour', 'favour',
           'whilst', 'amongst', 'neighbourhood', 'programme', 'realise', 'behaviour']

paths = {'/'}
LIVE = {'/', '/thank-you'}
pages = walk_pages(D)
for rel, _ in pages:
    paths.add('/' + rel[:-len('index.html')])

fail = 0
for rel, p in pages:
    s = io.open(p, encoding='utf-8', newline='').read()
    probs = []
    authored = re.sub(r'<nav[\s\S]*?</nav>|<footer[\s\S]*?</footer>|'
                      r'<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->', ' ', s)

    # ATTRIBUTED RESEARCH IS NOT ACADEMY'S OWN CLAIM.
    # A research-desc block naming a journal ("Published in ...") summarises someone else's
    # published finding, names its authors and links to the source, on a page that already
    # carries the not-a-medical-provider disclaimer. That is the safest form this content can
    # take, and the scan flagged it hardest: the 2014 Casutt et al. card tripped CLAIM on
    # "improves higher-order cognitive" purely for restating the study's own title ("Driving
    # simulator training increases real driving performance in healthy older drivers").
    # The claim worth blocking is Academy saying it about ITS OWN sessions.
    # Exemptions are COUNTED AND PRINTED, never silently dropped - an exemption nobody can see
    # is how a gate quietly stops being one. An UNattributed research-desc is not exempt, so
    # the hatch cannot be widened by deleting the citation.
    _cited = re.findall(r'<div class="research-desc">([\s\S]*?)</div>', authored)
    _exempt = [c for c in _cited if 'Published in' in c]
    for _c in _exempt:
        authored = authored.replace(_c, ' ')
    _unattributed = len(_cited) - len(_exempt)

    text = ' '.join(re.sub(r'<[^>]+>', ' ', authored).split())
    low = text.lower()

    for pat in FORBIDDEN:
        m = re.search(pat, low)
        if m:
            probs.append('CLAIM: ' + m.group(0)[:48])
    if 'not a medical provider' not in low:
        probs.append('MISSING-SCOPE-DISCLAIMER')
    if re.search(r'&mdash;|—', authored):
        probs.append('EM-DASH')
    probs.extend(check_ai_phrases(low, AI))
    probs.extend(check_british(low, BRITISH))
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
    # Quote-agnostic: the old pattern matched double-quoted hrefs only,
    # so any single-quoted link was invisible to this check. See
    # driver_audit.py for the case that found it (429 unchecked links).
    for h in set(re.findall(r'href=["\'](/[^"\'#?]*)["\']', s)):
        if h.endswith(('.xml', '.txt', '.png', '.svg', '.ico', '.jpg', '.webmanifest')):
            continue
        if h not in paths and h not in LIVE:
            probs.append('BROKEN ' + h)

    _cite = ''
    if _exempt:
        _cite = '   [%d attributed citation(s) exempt%s]' % (
            len(_exempt),
            '' if not _unattributed else ', %d UNattributed still scanned' % _unattributed)
    print('  %-46s %7d  %s%s' % (rel, len(s.encode()),
                                 'OK' if not probs else '*** ' + '; '.join(sorted(set(probs))),
                                 _cite))
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
