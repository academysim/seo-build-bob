# -*- coding: utf-8 -*-
"""Three claim fixes on the events homepage.

Client NAMES all stay. Malik confirmed Academy has run events for every company
listed, and naming who hired you is legitimate. The copy already says
"dealerships" rather than the manufacturer names alone, which is the correct
distinction and was right before I touched it.

1. "partner with us" -> "work with us". Partner is a term of art implying a
   formal ongoing relationship. What exists is a customer relationship, which
   is an equally good story and the true one.
2. "F1 paddocks" -> "F1 sponsor activations". Being in an F1 paddock is a
   specific, checkable location claim; doing an activation for a company that
   sponsors F1 is what the site says everywhere else and is already true.
   EASILY REVERTED if Academy has genuinely worked in a paddock.
3. Add the non-affiliation line the rest of the estate carries. The page uses
   "F1" and "Formula 1" prominently and had no such note.
"""
import io, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events_new', 'index.html')
s = io.open(P, encoding='utf-8', newline='').read()
before = len(s.encode())
report = []

# ---- 1. partner -> work ---------------------------------------------------
old = 'Sebring Motor Garages partner with us to deliver experiences'
new = 'Sebring Motor Garages work with us to deliver experiences'
assert s.count(old) == 1, 'partner anchor x%d' % s.count(old)
s = s.replace(old, new, 1)
report.append('"partner with us" -> "work with us"')

# ---- 2. F1 paddocks -> F1 sponsor activations ------------------------------
old = 'From Fortune 500 boardrooms to F1 paddocks'
new = 'From Fortune 500 boardrooms to F1 sponsor activations'
assert s.count(old) == 1, 'paddock anchor x%d' % s.count(old)
s = s.replace(old, new, 1)
report.append('"F1 paddocks" -> "F1 sponsor activations"')

# ---- 3. non-affiliation note in the footer bottom bar ---------------------
DISCLAIMER = ('<div class="foot-bottom" style="letter-spacing:0.12em; line-height:1.7; '
              'text-transform:none; font-size:10px; border-top:none; padding-top:6px;">'
              'Academy Sim Racing is not affiliated with, endorsed by or licensed by Formula 1, NASCAR, '
              'IMSA or any racing series, sanctioning body or vehicle manufacturer. Client and venue names '
              'identify organizations we have provided services for and do not imply any endorsement or '
              'partnership.</div>')

m = re.search(r'<div class="foot-bottom">.*?</div>', s, re.S)
assert m, 'no foot-bottom div found'
if 'not affiliated with' not in s:
    s = s[:m.end()] + '\n      ' + DISCLAIMER + s[m.end():]
    report.append('non-affiliation note added to footer')

io.open(P, 'w', encoding='utf-8', newline='').write(s)

print('  changes:')
for r in report:
    print('    - %s' % r)
print('\n  %d -> %d bytes' % (before, len(s.encode())))
print('  forms intact          : %d' % s.count('data-netlify="true"'))
print('  client names retained : %s' % all(
    n in s for n in ('Ferrari', 'BMW', 'Toyota', 'Ford', 'Porsche',
                     'The Motor Enclave', 'Sebring Motor Garages', 'Florida Aquarium')))
print('  "partner with us"     : %d  (expect 0)' % s.count('partner with us'))
print('  "F1 paddock"          : %d  (expect 0)' % s.count('F1 paddock'))
