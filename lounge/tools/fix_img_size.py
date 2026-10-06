# -*- coding: utf-8 -*-
"""A portrait photo rendered at the full 1100px content width came out 1375px
tall, taller than the viewport. Constrain the figure by width rather than
cropping, so nothing important is cut out of frame: 760px for landscape (which
aligns with the 720px text column) and 460px for portrait.
"""
import io, os, sys

D = sys.argv[1]
OLD = ".lp figure{margin:0;}"
NEW = (".lp figure{margin:0;max-width:760px;}"
       "\n.lp figure.tall{max-width:460px;}")

PORTRAIT = ('asr-hpde-daytona.jpg', 'florida-blue-lounge-event-racing.jpg')

n = 0
for root, _, files in os.walk(D):
    for f in files:
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        s = io.open(p, encoding='utf-8', newline='').read()
        if 'media-band' not in s:
            continue
        rel = os.path.relpath(p, D).replace(os.sep, '/')
        if OLD in s:
            s = s.replace(OLD, NEW, 1)
        if any(x in s for x in PORTRAIT) and '<figure class="tall">' not in s:
            s = s.replace('  <figure>\n', '  <figure class="tall">\n', 1)
            tag = 'tall (460px)'
        else:
            tag = 'wide (760px)'
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print('  %-46s %s' % (rel, tag))
        n += 1
print('  --- %d pages ---' % n)
