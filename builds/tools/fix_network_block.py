# -*- coding: utf-8 -*-
"""Repair the hand-built HTML block in builds_content3.py.

A heredoc turned escaped newlines into literal ones inside string literals.
Replaced with the existing linkgrid() helper, which is what it should have been.
"""
import io

P = 'builds_content3.py'
lines = io.open(P, encoding='utf-8', newline='').read().split('\n')

start = next(i for i, l in enumerate(lines) if "section('Where To Drive'" in l)
end = next(i for i, l in enumerate(lines) if "prose('If You Are Buying'" in l)

clean = """        linkgrid('Where To Drive', 'The one place <span class="accent">that is ours.</span>',
                 'Open to the public, bookable by the hour, with every build component running daily.', [
                     (LOUNGE, 'ACADEMY LOUNGE, TAMPA',
                      '1421 Massaro Blvd. Eight simulators including motion, triple screen and '
                      'manual-shifter rigs. Book an hour and drive the exact components you would be buying.'),
                     (EVENTS, 'AT YOUR OWN EVENT',
                      'Academy Events delivers staffed simulators anywhere in Florida. If you want a group '
                      'to try before a purchase decision, that is often the simplest route.'),
                 ]),"""

lines[start:end] = clean.split('\n')
io.open(P, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('  repaired lines %d-%d' % (start + 1, end))

# prove it parses
import py_compile
py_compile.compile(P, doraise=True)
print('  compiles clean')
