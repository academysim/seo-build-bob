# -*- coding: utf-8 -*-
"""`.lp{overflow:hidden}` was authored for pages where .lp is a <div> inside
<body>. On my pages .lp IS the <body>, and per CSS the root/body overflow
propagates to the viewport, so user scrolling was disabled entirely.
Programmatic scrolling (scrollTo/scrollIntoView) still works, which is why every
automated check passed and only a human with a mouse could find it.

overflow-x:hidden keeps the original intent (no sideways scroll) and restores
vertical scrolling on both skeletons.
"""
import io, os, sys

target = sys.argv[1]
OLD = "font-family:'Inter',sans-serif;overflow:hidden;"
NEW = "font-family:'Inter',sans-serif;overflow-x:hidden;"

files = []
if os.path.isfile(target):
    files = [target]
else:
    for root, _, fs in os.walk(target):
        for f in fs:
            if f.endswith(('.html', '.css')):
                files.append(os.path.join(root, f))
files.sort()

n = 0
for p in files:
    s = io.open(p, encoding='utf-8', errors='strict', newline='').read()
    if OLD not in s:
        continue
    c = s.count(OLD)
    s = s.replace(OLD, NEW)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-52s %d' % (os.path.relpath(p, target if os.path.isdir(target) else '.'), c))
    n += 1
print('  --- %d files fixed ---' % n)
