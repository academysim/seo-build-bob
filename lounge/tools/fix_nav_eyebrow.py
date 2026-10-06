# -*- coding: utf-8 -*-
"""The shared nav was lifted from the Sebring track page, so every page built
from it says "TRACK GUIDE" in the brand eyebrow, including the racing pages
and the cars library. Set it per section."""
import io, os, sys, re

D = sys.argv[1]

SECTION = [
    ('cars-and-tracks/index.html', 'CARS &amp; TRACKS'),
    ('racing/index.html', 'RACING'),
    ('racing/gt3-simulator-tampa/index.html', 'RACING'),
    ('racing/formula-simulator-tampa/index.html', 'RACING'),
    ('racing/nascar-simulator-tampa/index.html', 'RACING'),
    ('racing/drift-simulator-tampa/index.html', 'RACING'),
    ('racing/imsa-endurance-simulator-tampa/index.html', 'RACING'),
    ('racing/rally-simulator-tampa/index.html', 'RACING'),
    ('racing/manual-transmission-simulator-tampa/index.html', 'RACING'),
    ('tracks/index.html', 'TRACK GUIDES'),
    ('tracks/daytona/index.html', 'TRACK GUIDE'),
    ('tracks/sebring/index.html', 'TRACK GUIDE'),
]

PAT = re.compile(r'(brand-dot"></span>)([^<]*)')

for rel, label in SECTION:
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-46s SKIP (not present)' % rel)
        continue
    s = io.open(p, encoding='utf-8', newline='').read()
    found = PAT.findall(s)
    assert len(found) == 1, '%s: %d eyebrow matches' % (rel, len(found))
    old = found[0][1]
    if old == label:
        print('  %-46s already %s' % (rel, label))
        continue
    s = PAT.sub(lambda m: m.group(1) + label, s, count=1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s %-12s -> %s' % (rel, old, label))
