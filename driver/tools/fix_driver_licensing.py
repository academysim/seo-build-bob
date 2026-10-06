# -*- coding: utf-8 -*-
"""Malik confirmed Academy holds no license of any kind.

Two problems with what I published:

1. The s.1003.48(1) note appeared on all seven district pages and the hub. It
   describes districts contracting driver education out to "a licensed
   commercial driving school or instructor", sitting directly alongside
   Academy's offer. Nothing claimed Academy qualifies, but a district reader
   would reasonably infer it. With no license at all that citation is
   misleading by juxtaposition, so it comes out entirely.

2. "does not satisfy state licensing requirements ON ITS OWN" implies partial
   credit. It gets nothing. Made unconditional.

Replaced with a plain statement of what Academy actually is: a supplier of
simulator equipment and staffed programs, not a driving school.
"""
import io, os, sys

D = sys.argv[1]

OLD_STATUTE_START = '  <div class="note"><p><strong>The statutory picture.</strong>'

WHAT_WE_ARE = (
    '  <div class="note"><p><strong>What Academy is, and is not.</strong> Academy Sim Racing supplies '
    'racing and driving simulators and runs staffed programs with them. <strong>We are not a licensed '
    'driving school and we do not employ state-certified driver education instructors.</strong> Nothing we '
    'provide counts toward Florida licensing requirements, the supervised driving hours a learner must '
    'complete, or any state-required driver education course. Districts should deliver those through their '
    'own certified staff or an appropriately licensed provider. What we offer is supplementary practice '
    'and hazard exposure alongside them.</p></div>')


def strip_block(s, start_marker):
    """Remove one <div class="note">...</div> block beginning at start_marker."""
    i = s.find(start_marker)
    if i < 0:
        return s, False
    j = s.find('</div>', i)
    if j < 0:
        return s, False
    return s[:i] + s[j + len('</div>'):], True


changed = 0
for root, _, files in os.walk(D):
    for f in sorted(files):
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, D).replace(os.sep, '/')
        s = io.open(p, encoding='utf-8', newline='').read()
        before = s
        n = []

        # 1. drop the contracting-statute note, put the honest one in its place
        s, hit = strip_block(s, OLD_STATUTE_START)
        if hit:
            n.append('removed s.1003.48 note')
            # place the replacement immediately after the no-installs disclosure
            anchor = 'not an existing installation or partnership.</p></div>'
            if anchor in s and 'not a licensed driving school' not in s:
                s = s.replace(anchor, anchor + '\n\n' + WHAT_WE_ARE, 1)
                n.append('+ not-a-driving-school note')

        # 2. remove the "on its own" weasel
        for o, x in [
            ('it does not satisfy any state licensing requirement on its own',
             'it does not satisfy any state licensing or driver education requirement'),
            ('No, and it does not satisfy state licensing requirements on its own.',
             'No. It also does not satisfy any state licensing or driver education requirement.'),
            ('a simulator does not make a student road-ready and does not satisfy licensing requirements',
             'a simulator does not make a student road-ready and does not satisfy any licensing or driver '
             'education requirement'),
            ('Treat it as a supplement to your existing course and confirm any requirement with '
             'your district and the state.',
             'It counts for nothing toward state requirements. Treat it purely as a supplement to your '
             'existing course, which must be delivered by appropriately certified staff.'),
        ]:
            if o in s:
                s = s.replace(o, x)
                n.append('unweaseled')

        if s != before:
            io.open(p, 'w', encoding='utf-8', newline='').write(s)
            print('  %-50s %s' % (rel, ', '.join(sorted(set(n)))))
            changed += 1

print('  --- %d pages changed ---' % changed)
