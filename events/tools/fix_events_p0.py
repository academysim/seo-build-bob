# -*- coding: utf-8 -*-
"""P0: remove the undocumented engagement multiplier from the events homepage.

The audit: "Any numerical claims such as 3-5x dwell time or similar engagement
multipliers must have evidence. If not documented, rewrite as qualitative
benefits."

There is no evidence for 3-5x. It appeared twice on the homepage, once as a
headline stat beside two figures that ARE documented (15-40 racers per hour per
simulator, statewide coverage), which is the worst place for it: a made-up
number sitting between two real ones borrows their credibility.

The ten event-type and location pages built on 2026-08-29 already discuss dwell
time qualitatively with no multiplier, so this brings the homepage in line with
the rest of the property rather than changing the property's story.

The replacement stat is the operating footprint, about 10 ft x 10 ft per
simulator. That is confirmed (it already appears in this site's own FAQ, and it
is consistent with the Trak Racer TR160 V5 frame at 660 x 1445 mm), and it is
the number an event planner actually needs before they can say yes.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source', 'index.html')
DST = os.path.join(HERE, '..', 'upload')

EDITS = [
    # a fabricated multiplier standing between two documented figures
    (u'<div class="aerial-stat"><span class="aerial-stat-big">3–5×</span>'
     u'<span class="aerial-stat-small">Longer Dwell Time</span></div>',
     u'<div class="aerial-stat"><span class="aerial-stat-big">10×10</span>'
     u'<span class="aerial-stat-small">Feet Per Simulator</span></div>'),

    # the same claim as a benefit card: keep the benefit, drop the number
    (u'<div class="why-name">INCREASES DWELL TIME</div>'
     u'<div class="why-desc">Guests stay 3–5x longer waiting for their turn,'
     u' giving your team more time to connect and sell.</div>',
     u'<div class="why-name">HOLDS A CROWD</div>'
     u'<div class="why-desc">People wait for a turn instead of walking past, '
     u'which gives your team more time to talk to them.</div>'),
]

# any surviving engagement multiplier, in visible copy or structured data
MULTIPLIER = re.compile(r'\b\d+\s*[-–]\s*\d+\s*[x×]\b|\b\d+\s*[x×]\s*(?:longer|more|higher)', re.I)


def main():
    h = io.open(SRC, encoding='utf-8').read()
    already = []
    for old, new in EDITS:
        got = h.count(old)
        if got == 0:
            # ALREADY APPLIED, not missing -- same situation as fix_health_claims.py: a
            # one-time migration whose edits have since been folded into source/ by hand.
            # Safe to skip HERE specifically because this script does not depend on the
            # edits having fired: the post-conditions below (no engagement multiplier, the
            # 15-40 throughput figure, balanced forms, exactly 2 data-netlify forms) check
            # the RESULTING page, so the outcome stays gated either way.
            # A wrong COUNT still fails, because that is drift rather than completion.
            already.append(' '.join(old.split())[:74])
            continue
        if got != 1:
            print('  !! expected 1, found %d for %r' % (got, ' '.join(old.split())[:80]))
            return 1
        h = h.replace(old, new)
        print('  ok  %s' % ' '.join(old.split())[:74])
    if already:
        print('  %d edit(s) already applied in source/' % len(already))

    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    left = MULTIPLIER.findall(body)
    if left:
        print('  !! engagement multiplier still present: %s' % left)
        return 1
    if '15–40' not in h:
        print('  !! the documented 15-40 throughput figure went missing')
        return 1
    if h.count('<form') - h.count('</form>') != 0:
        print('  !! unbalanced form tags')
        return 1
    if h.count('data-netlify="true"') != 2:
        print('  !! expected 2 netlify forms, found %d' % h.count('data-netlify="true"'))
        return 1

    if not os.path.isdir(DST):
        os.makedirs(DST)
    out = os.path.join(DST, 'index.html')
    io.open(out, 'w', encoding='utf-8', newline='').write(h)
    print('  clean. wrote %s (%d bytes)' % (out, len(h.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
