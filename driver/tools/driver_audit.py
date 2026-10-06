# -*- coding: utf-8 -*-
"""Audit for driver.academysim.com pages.

The critical check is FORBIDDEN CLAIMS. Academy has no simulators in any
school, and the brief lists the exact phrasings that must never appear.
"""
import io, os, re, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import GA4_TAG
from shared.tools.audit_lib import (
    walk_pages, check_zero_pages, check_ai_phrases, check_british,
    check_tag_balance, check_json_ld, check_ga4,
    check_sitemap_coverage, print_final, exit_audit,
)

# Default to this property's real output. The old default was the temporary
# scratchpad name from the build session (driver_new), which no longer exists, and
# os.walk over a missing directory yields nothing - so the audit printed
# '0 pages, ALL OK' and exited 0. A gate that checks nothing must never pass.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ROOT, 'driver', 'upload')

FORBIDDEN = [
    r'currently used in (florida )?schools',
    r'our school installations?',
    r'schools using academy',
    r'proven across (florida )?school districts',
    r'trusted by (florida )?school districts',
    r'installed in [a-z ]+ county schools',
    r'we have simulators in',
    r'already in \d+ schools',
    r'our (district|school) partners',
]

AI = ['delve', 'testament to', 'seamless', 'elevate your', 'cutting-edge',
      'state-of-the-art', 'game-changer', 'in today', 'it is worth noting',
      'ultimately,', 'leverage', 'look no further', 'when it comes to']

BRITISH = ['tyre', 'kerb', 'practise', 'centre', 'organiser', 'colour', 'favour',
           'whilst', 'amongst', 'neighbourhood', 'programme', 'realise', 'behaviour']

paths = {'/'}
LIVE = {'/', '/contact', '/about', '/resources', '/teen-training',
        '/simulator-rentals', '/schools-programs', '/public-safety'}
pages = walk_pages(D)
# EVERY .html, not just index.html. Until 2026-08-30 this loop matched only
# 'index.html', so six pages that are live - about, public-safety, resources,
# schools-programs, simulator-rentals, teen-training - were audited by nothing.
# Fetched live, none of them carried the no-install disclosure or the
# not-a-state-licensed-provider line, and /schools-programs.html is the page
# most exposed to exactly that question. The audit could not have caught it
# because the audit never opened the file.
for rel, _ in pages:
    if rel.endswith('index.html'):
        paths.add('/' + rel[:-len('index.html')])
    else:
        # Netlify's pretty URLs serve /about.html at /about too, so an
        # internal link to either form has to resolve.
        paths.add('/' + rel)
        paths.add('/' + rel[:-len('.html')])

# Resolve a site path back to the file that serves it, so a #fragment can be
# checked against the ids that page actually defines.
_by_path = {}
for _rel, _p in pages:
    if _rel.endswith('index.html'):
        _by_path['/' + _rel[:-len('index.html')]] = _p
    else:
        _by_path['/' + _rel] = _p
        _by_path['/' + _rel[:-len('.html')]] = _p

_src_cache = {}
def anchor_src(path):
    """Contents of the page serving `path`, or None if it is not ours to check."""
    p = _by_path.get(path) or _by_path.get(path.rstrip('/')) or _by_path.get(path + '/')
    if p is None:
        return None
    if p not in _src_cache:
        _src_cache[p] = io.open(p, encoding='utf-8', newline='').read()
    return _src_cache[p]


fail = 0
for rel, p in pages:
    s = io.open(p, encoding='utf-8', newline='').read()
    probs = []
    authored = re.sub(r'<header[\s\S]*?</header>|<footer[\s\S]*?</footer>|'
                      r'<script[\s\S]*?</script>|<!--[\s\S]*?-->', ' ', s)
    text = ' '.join(re.sub(r'<[^>]+>', ' ', authored).split())
    low = text.lower()

    for pat in FORBIDDEN:
        if re.search(pat, low):
            probs.append('FORBIDDEN-CLAIM: ' + pat)
    if 'does not currently have simulators installed' not in low:
        probs.append('MISSING-NO-INSTALL-DISCLOSURE')
    if re.search(r'&mdash;|\u2014', authored):
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
    # Quote-agnostic on purpose. Until 2026-09-01 this matched href="..." only, so
    # every single-quoted link was invisible to it - on driver that was 429 hrefs
    # across 27 pages, including the entire top nav, which is emitted with single
    # quotes. Nothing was broken, but nothing was checking either, and that is the
    # same defect as the 0-pages pass and the 26-of-27 coverage gap above: the
    # output described what was looked at and said nothing about what was not.
    # A link nothing resolves is not a link that works.
    #
    # The fragment is now kept and checked rather than stripped by the pattern. A
    # nav pointing at /page#anchor where the anchor was renamed is a dead link that
    # returns HTTP 200, so no status-code check will ever find it.
    for h in set(re.findall(r'href=["\'](/[^"\'?]*)["\']', s)):
        base, _, frag = h.partition('#')
        base = base or '/'
        if base.endswith(('.xml', '.txt', '.png', '.svg', '.ico', '.jpg', '.css', '.js')):
            continue
        if base not in paths and base not in LIVE:
            probs.append('BROKEN ' + h)
        elif frag:
            tgt = anchor_src(base)
            if tgt is None:
                probs.append('ANCHOR-UNCHECKED ' + h)
            elif not re.search(r'id=["\']%s["\']' % re.escape(frag), tgt):
                probs.append('DEAD-ANCHOR ' + h)

    print('  %-52s %7d  %s' % (rel, len(s.encode()),
                               'OK' if not probs else '*** ' + '; '.join(sorted(set(probs)))))
    if probs:
        fail += 1

check_zero_pages(pages, D)
# COVERAGE. Auditing 26 of 27 live pages and reporting on the 26 is the same
# family of defect as auditing 0 and reporting ALL OK: the output describes what
# was looked at, and says nothing about what was not. /contact.html is live
# (HTTP 200, in the sitemap) and exists only in driver/source/, never in
# driver/upload/ - so it was invisible to this audit even after it was widened
# to every .html. It carries neither disclosure.
_sm = os.path.join(_ROOT, 'driver', 'site', 'sitemap.xml')
fail = check_sitemap_coverage(pages, _sm, fail)

print_final(pages, fail)
exit_audit(fail)
