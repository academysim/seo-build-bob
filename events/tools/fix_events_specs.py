# -*- coding: utf-8 -*-
"""Add real, verified rig dimensions and Malik's throughput figure.

Sources:
  * Frame: Trak Racer TR160 V5, published assembled dimensions
    660 mm x 1445 mm (26 in x 57 in). Verified from the manufacturer's spec table.
  * Widest point: the 49 inch ultrawide display, per Malik.
  * Operating allowance: about 10 ft x 10 ft per simulator. This already appears
    on the existing homepage FAQ and is an allowance including driver access and
    someone waiting, not the rig footprint. The two are consistent.
  * Throughput: 15 to 40 drivers per hour per simulator, per Malik.

NOTE: the existing homepage FAQ says "15-30 racers per hour". Malik's figure is
15-40. That homepage line needs updating too and cannot be edited without the
original source folder. Flagged.
"""
import io, os, sys

D = sys.argv[1]

SPACE = ('The frame is 26 inches wide and 57 inches long, and the widest point is the 49 inch '
         'ultrawide display. In practice, allow around 10 feet by 10 feet per simulator once you '
         'include the driver getting in and out and somebody waiting. Send us your floor plan or '
         'booth dimensions and we will confirm exactly what fits.')

THROUGHPUT = ('Depending on session length, expect roughly 15 to 40 drivers per hour per simulator. '
              'Short runs at a busy stand sit at the top of that range, longer sessions at an evening '
              'reception at the bottom. Running several rigs in parallel scales it from there.')


def edit(rel, pairs):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p):
        return 0
    s = io.open(p, encoding='utf-8', newline='').read()
    n = 0
    for o, x in pairs:
        c = s.count(o)
        if c:
            s = s.replace(o, x)
            n += c
    if n:
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
    return n


ALL = []
for root, _, files in os.walk(D):
    for f in files:
        if f == 'index.html':
            ALL.append(os.path.relpath(os.path.join(root, f), D).replace(os.sep, '/'))
ALL.sort()

# ---- space answers ---------------------------------------------------------
SPACE_PAIRS = [
    ('It depends on the rig and how much queue space you want. Send us the floor plan and we will tell you '
     'exactly what works.', SPACE),
    ('It varies by rig and by how much queue space you want around it. Send us your floor plan or venue '
     'dimensions and we will tell you what fits.', SPACE),
    ('It varies with the rig and how much queue space you want around it. Send us your booth dimensions and '
     'the exhibitor kit and we will tell you what fits.',
     SPACE + ' For a trade show, send the exhibitor kit as well so we can check ceiling height and dock access.'),
    ('It depends on how many people you want through the rigs and how long you have. A booth running '
     'five minute sessions moves far more people than a dinner where guests drift over between courses. '
     'Tell us the headcount and the window and we will size it.',
     'Work it back from throughput. Expect roughly 15 to 40 drivers per hour per simulator depending on '
     'session length, then divide your headcount by the window you have. Tell us both and we will size it.'),
]

# ---- throughput answers ----------------------------------------------------
THRU_PAIRS = [
    ('That is a function of rigs, session length and window rather than a fixed number. Short sessions '
     'with staff running the queue move a lot of people. Tell us the headcount and how long you have and '
     'we will size the setup to it.', THROUGHPUT),
    ('It depends on your space and expected traffic at peak rather than on total attendance. Send us your '
     'stand dimensions and the show and we will size it.',
     'Size it on peak traffic rather than total attendance. Each simulator handles roughly 15 to 40 drivers '
     'an hour depending on session length. Send us your stand dimensions and the show and we will size it.'),
    ('It depends on headcount and how long you have. Send us both and we will size it.',
     'Roughly 15 to 40 drivers per hour per simulator, depending on session length. Divide your headcount by '
     'the window you have and that gives you the rig count. Send us both and we will confirm.'),
]

# ---- richer planning copy where a section already discusses space ----------
PROSE_PAIRS = [
    ('<h3>Space and power</h3>\n'
     '    <p>Each rig needs a footprint and mains power at the activation point. Ballrooms and conference '
     'centers are usually straightforward. Older venues and outdoor spaces need checking early, because '
     'power is the constraint that most often changes a plan.</p>',
     '<h3>Space and power</h3>\n'
     '    <p>The frame is 26 inches wide and 57 inches long, and the 49 inch ultrawide display is the widest '
     'part. Allow around 10 feet by 10 feet per simulator in operation, which covers the driver getting in '
     'and out and someone waiting their turn. Each rig also needs mains power at the activation point. '
     'Ballrooms and conference centers are usually straightforward. Older venues and outdoor spaces need '
     'checking early, because power is the constraint that most often changes a plan.</p>'),
    ('<h3>Throughput</h3>\n'
     '    <p>Work backwards from your headcount. If you want everyone to drive, session length multiplied by '
     'guests divided by rigs has to fit inside your window. If you only need the rigs as atmosphere, far '
     'fewer will do.</p>',
     '<h3>Throughput</h3>\n'
     '    <p>Work backwards from your headcount. A simulator handles roughly 15 to 40 drivers an hour '
     'depending on how long you set the sessions, so divide your guest count by the window you have to get '
     'the rig count. If you only need the rigs as atmosphere rather than wanting everyone to drive, far '
     'fewer will do.</p>'),
    ('<li>Available power at the activation point</li>',
     '<li>Available power at the activation point, and roughly 10 feet by 10 feet of floor per simulator</li>'),
    ('<h3>Access decides more than space</h3>'
     '<p>At private homes and smaller venues the question is rarely whether there is room. It is whether we can '
     'get the equipment in: door widths, steps, lifts, gate access and how close a vehicle can get. Photographs '
     'of the access route are more useful to us than the floor dimensions.</p>',
     '<h3>Access decides more than space</h3>'
     '<p>At private homes and smaller venues the question is rarely whether there is room. It is whether we can '
     'get the equipment in. The frame is 26 inches wide, so a standard doorway is fine, but door widths, steps, '
     'lifts, gate access and how close a vehicle can get all matter. Photographs of the access route are more '
     'useful to us than the floor dimensions.</p>'),
]

total = 0
for rel in ALL:
    n = edit(rel, SPACE_PAIRS + THRU_PAIRS + PROSE_PAIRS)
    if n:
        print('  %-46s %d' % (rel, n))
        total += n
print('  --- %d replacements ---' % total)
