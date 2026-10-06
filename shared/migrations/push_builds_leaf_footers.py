# -*- coding: utf-8 -*-
"""Push builds' footer address+hours block into builds/site/ for exactly the 19
leaf pages the VERIFIED staging carries it on.

Why a scoped list rather than running builds/tools/add_hub_links.py --tree site:
that tool walks every index.html in the tree, and builds/site also holds
for/index.html and simulators/index.html, which the live site does NOT have the
block on. Running it wholesale would add a footer block to two live pages, which
is a content change, not a rebuild fix. The homepage is handled separately by
the --tree source step in build_all.py (fix_review_counts.py stages it from
source/). network/ and tracks/sebring-racing-simulator/ already carry the block
in site/, because they were generated after the patch.

Idempotent: a page that already has the block is reported and skipped.
"""
import io, os, re, sys

os.chdir('D:/AcademySimRacing/03-SEO-Build')

LEAVES = [
    'for/automotive-businesses/index.html', 'for/car-collectors/index.html',
    'for/car-dealerships/index.html', 'for/garage-condos/index.html',
    'for/hotels-and-clubs/index.html', 'for/luxury-garages/index.html',
    'for/offices/index.html', 'for/race-car-drivers/index.html',
    'for/race-teams/index.html', 'for/track-day-drivers/index.html',
    'simulators/drift-racing-simulator/index.html',
    'simulators/formula-racing-simulator/index.html',
    'simulators/gt3-racing-simulator/index.html',
    'simulators/imsa-endurance-racing-simulator/index.html',
    'simulators/motion-racing-simulator/index.html',
    'simulators/nascar-racing-simulator/index.html',
    'simulators/rally-racing-simulator/index.html',
    'simulators/track-day-racing-simulator/index.html',
    'simulators/triple-screen-racing-simulator/index.html',
]

# Take the two blocks from the tool itself, so they cannot drift apart.
src = io.open('builds/tools/add_hub_links.py', encoding='utf-8',
              newline='').read().replace('\r\n', '\n')
OLD = eval('(' + re.search(r'^OLD_CONTACT = \((.*?)^\)$', src, re.S | re.M).group(1) + ')')
NEW = eval('(' + re.search(r'^NEW_CONTACT = \((.*?)^\)$', src, re.S | re.M).group(1) + ')')

fail = patched = already = 0
for rel in LEAVES:
    p = os.path.join('builds', 'site', *rel.split('/'))
    raw = io.open(p, encoding='utf-8', newline='').read()
    eol = '\r\n' if '\r\n' in raw else '\n'
    s = raw.replace('\r\n', '\n')
    if NEW in s:
        already += 1
        continue
    if s.count(OLD) != 1:
        print('  !! %s: expected 1 Contact block, found %d' % (rel, s.count(OLD)))
        fail += 1
        continue
    s = s.replace(OLD, NEW, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', eol))
    patched += 1

print('builds/site leaf footers: %d patched, %d already present, %d failed'
      % (patched, already, fail))
sys.exit(1 if fail else 0)
