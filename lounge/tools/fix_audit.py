# -*- coding: utf-8 -*-
"""Codex master-plan audit fixes, the ones that are clearly correct and cheap.

NOT applied here, deliberately, and raised with Malik instead:
  - The Sebring page's "our customers run with them" and "certified HPDE
    instructor who races wheel-to-wheel". Both may well be true (the driver
    coach photo shows HPDE progression kit), and stripping a true claim is
    worse than leaving it. His call.
  - The homepage's driver-ed / schools content straying into Driver intent.
    That is a business positioning decision, not a copy bug.
"""
import io, os, sys

D = sys.argv[1]


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def edit(rel, pairs, quiet=False):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-46s MISSING' % rel)
        return
    s = rd(p)
    n = 0
    for o, x in pairs:
        c = s.count(o)
        if c == 0:
            continue
        assert c == 1, 'NOT ONCE in %s (%d): %r' % (rel, c, o[:60])
        s = s.replace(o, x, 1)
        n += 1
    wr(p, s)
    print('  %-46s %d edits' % (rel, n))


EVENTS_LINE = ('  <p>Need simulators brought to a corporate day, party or team event? '
               'See <a href="https://events.academysim.com">Academy Events</a>.</p>')

# ---- Rule 5: missing Events links -----------------------------------------
edit('cars/index.html', [
    ('  <p>Browse everything you can drive on the <a href="/cars-and-tracks/">cars and tracks</a> page, or see all our <a href="/racing/">racing experiences</a>.</p>',
     '  <p>Browse everything you can drive on the <a href="/cars-and-tracks/">cars and tracks</a> page, or see all our <a href="/racing/">racing experiences</a>.</p>\n' + EVENTS_LINE),
])

edit('cars/classic-race-cars/index.html', [
    ('  <p>Not sure this is the one? Compare it against the other <a href="/cars/">car classes</a>, or see all our <a href="/racing/">racing experiences</a>.</p>',
     '  <p>Not sure this is the one? Compare it against the other <a href="/cars/">car classes</a>, or see all our <a href="/racing/">racing experiences</a>.</p>\n' + EVENTS_LINE),
])

# ---- Rule 9: the one page naming all three series without the disclaimer ---
edit('things-to-do-in-tampa/index.html', [
    ('  <p class="note">Hours and prices can change.',
     '  <p class="note">Academy Sim Racing is not affiliated with, endorsed by or licensed by Formula 1, NASCAR, IMSA or any racing series, sanctioning body or car manufacturer. Hours and prices can change.'),
])

# ---- time-sensitive fact on the formula page ------------------------------
edit('racing/formula-simulator-tampa/index.html', [
    ('a current Formula 1 car is around 800 kg', 'a 2026 Formula 1 car is around 800 kg'),
    ('A current Formula 1 car is around 800 kg', 'A 2026 Formula 1 car is around 800 kg'),
])

# ---- cannibalisation: pull /cars/ toward informational intent --------------
edit('cars/index.html', [
    ('<title>Which Car Class Should You Drive? | Academy Sim Racing Tampa</title>',
     '<title>Race Car Classes Explained: GT3 vs Formula vs Prototype | Academy Sim Racing</title>'),
    ('<meta property="og:title" content="Which Car Class Should You Drive? | Academy Sim Racing Tampa">',
     '<meta property="og:title" content="Race Car Classes Explained | Academy Sim Racing">'),
    ('<meta name="twitter:title" content="Which Car Class Should You Drive? | Academy Sim Racing Tampa">',
     '<meta name="twitter:title" content="Race Car Classes Explained | Academy Sim Racing">'),
    ('<h1>Which Car Class<br>Should You Drive?</h1>',
     '<h1>Race Car Classes<br>Explained</h1>'),
    ('"name": "Which Car Class Should You Drive?",',
     '"name": "Race Car Classes Explained",'),
])

# ---- sitemap priorities: commercial pages should not rank below guides -----
sp = os.path.join(D, 'sitemap.xml')
sm = rd(sp)
import re
before = len(re.findall(r'<priority>', sm))
sm = re.sub(r'\s*<priority>[^<]*</priority>', '', sm)
wr(sp, sm)
print('  %-46s removed %d <priority> tags' % ('sitemap.xml', before))
