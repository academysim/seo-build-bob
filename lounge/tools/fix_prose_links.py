# -*- coding: utf-8 -*-
"""The shared stylesheet never styled inline prose links, so every
<p><a href="/..."></a></p> rendered as browser-default blue (and purple once
visited) on a near-black background. Both :link and :visited are named
explicitly, because `a, a:visited` outranks a bare class selector and
getComputedStyle masks :visited so this cannot be caught by measurement alone.
"""
import io, os, sys

target = sys.argv[1]

MARKER = '.lp a:focus-visible,.lp button:focus-visible{outline:2px solid #fbbf24;outline-offset:3px;}'

RULES = (
    '\n.lp p a:not([class]):link,.lp p a:not([class]):visited,'
    '.lp li a:not([class]):link,.lp li a:not([class]):visited,'
    '.lp td a:not([class]):link,.lp td a:not([class]):visited'
    '{color:#fbbf24;text-decoration:underline;text-decoration-color:rgba(251,191,36,.45);text-underline-offset:2px;}'
    '\n.lp p a:not([class]):hover,.lp li a:not([class]):hover,.lp td a:not([class]):hover'
    '{color:#fcd34d;text-decoration-color:#fcd34d;}'
)

SENTINEL = '.lp p a:not([class]):link'

if os.path.isfile(target):
    files = [target]
else:
    files = []
    for root, _, fs in os.walk(target):
        for f in fs:
            if f == 'index.html':
                files.append(os.path.join(root, f))
    files.sort()

done = skipped = 0
for p in files:
    s = io.open(p, encoding='utf-8', newline='').read()
    rel = os.path.relpath(p, target if not os.path.isfile(target) else os.path.dirname(target))
    if SENTINEL in s:
        print('  %-46s already fixed' % rel)
        skipped += 1
        continue
    if MARKER not in s:
        print('  %-46s no marker, skipped' % rel)
        skipped += 1
        continue
    assert s.count(MARKER) == 1, '%s: marker %d times' % (rel, s.count(MARKER))
    s = s.replace(MARKER, MARKER + RULES, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s patched' % rel)
    done += 1

print('\n  patched %d, skipped %d' % (done, skipped))
