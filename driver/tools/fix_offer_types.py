# -*- coding: utf-8 -*-
"""RETIRED 2026-08-31. Already applied, deployed, and folded into source/.

This was a ONE-SHOT P0 transform: it read the byte-recovered driver/source/
and wrote driver/upload/. Its decisions are live and now live in source/ too,
because source/ was synced to the deployed bytes.

It must never run again. driver/source/ is no longer the raw recovered
original; it IS the deployed copy. Re-running this against it would have
reverted the em dash sweep and 28 hand copy fixes on 6 live pages, measured:
it reintroduced 45 em dashes when tested into a scratch directory.

The reasoning behind each edit is preserved below and in git history. If a
placeholder ever needs re-deciding, read it, then edit driver/source/ directly
and deploy with shared/tools/deploy.py.

ORIGINAL DOCSTRING FOLLOWS
======================================================================

P0: scope the lease offer to organizations, per the audit's offer-type check.

The audit asked: "Confirm whether Academy truly offers purchase, lease, rental,
pilot, permanent installation, or all of the above. Remove any option that is
theoretical rather than operationally available."

Malik confirmed on 2026-08-30: leasing IS real, but **business and organization
leases only** (his example: a dealership leasing a simulator from us). There are
no personal or consumer leases.

So the option stays and gets scoped rather than removed. That matters most in
the interest dropdown, which appears on three forms including
/simulator-rentals, a page a private individual can reach; an unqualified
"Lease" there invites an enquiry Academy will not fulfil.

The meta descriptions on /schools-programs are left alone. They address "high
schools, districts, driving schools and CTE programs", so "lease" is already
scoped to organizations by its own sentence.

Runs after fix_placeholders.py, on that script's output in upload/.
"""
import sys

sys.exit("""fix_offer_types.py is retired and will not run.
Its edits are already live and are folded into driver/source/.
Re-running it would revert the em dash sweep and 28 copy fixes.
Edit driver/source/ directly, then deploy with shared/tools/deploy.py.""")

# ---- the original implementation, kept for its reasoning ----
# import io
# import os
# import re
# import sys
#
# HERE = os.path.dirname(os.path.abspath(__file__))
# SRC = os.path.join(HERE, '..', 'source')
# DST = os.path.join(HERE, '..', 'upload')
#
# DROPDOWN_OLD = u'<option>Lease</option>'
# DROPDOWN_NEW = u'<option>Lease (organizations only)</option>'
#
# EDITS = [
#     # the interest dropdown, on all three institutional forms
#     ('schools-programs.html', DROPDOWN_OLD, DROPDOWN_NEW, 1),
#     ('simulator-rentals.html', DROPDOWN_OLD, DROPDOWN_NEW, 1),
#     ('public-safety.html', DROPDOWN_OLD, DROPDOWN_NEW, 1),
#
#     ('index.html',
#      u"Purchase, lease, rent, or pilot a system based on your program's needs.",
#      u"Purchase, rent, or pilot a system based on your program's needs. "
#      u"Leasing is available to organizations and businesses.", 1),
#
#     ('public-safety.html',
#      u'<li>Rental, pilot, lease and purchase options</li>',
#      u'<li>Rental, pilot and purchase options, plus leasing for organizations</li>',
#      1),
# ]
#
# # an unqualified "lease" in visible copy, outside the scoped forms
# LOOSE = re.compile(r'\blease\b(?!\s*\(organizations only\))', re.I)
#
#
# def main():
#     if not os.path.isdir(DST):
#         os.makedirs(DST)
#     files = {}
#     for f, old, new, want in EDITS:
#         if f not in files:
#             staged = os.path.join(DST, f)
#             src = staged if os.path.exists(staged) else os.path.join(SRC, f)
#             files[f] = io.open(src, encoding='utf-8').read()
#         got = files[f].count(old)
#         if got != want:
#             print('  !! %s: expected %d, found %d for %r' % (f, want, got, old[:70]))
#             return 1
#         files[f] = files[f].replace(old, new)
#         print('  ok  %-24s %s' % (f, ' '.join(old.split())[:60]))
#
#     fail = False
#     for f, h in sorted(files.items()):
#         io.open(os.path.join(DST, f), 'w', encoding='utf-8', newline='').write(h)
#         body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
#         body = re.sub(r'<meta[^>]*>', ' ', body)
#         text = re.sub(r'<[^>]+>', ' ', body)
#         for m in LOOSE.finditer(text):
#             ctx = ' '.join(text[max(0, m.start() - 70):m.end() + 70].split())
#             # "leasing is available to organizations", "leasing for organizations"
#             if re.search(r'leasing (is available to|for) organizations', ctx, re.I):
#                 continue
#             print('  !! %s: unscoped lease reference: %r' % (f, ctx))
#             fail = True
#         print('  wrote %-24s %d bytes' % (f, len(h.encode('utf-8'))))
#     return 1 if fail else 0
#
#
# if __name__ == '__main__':
#     sys.exit(main())
