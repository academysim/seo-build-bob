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

P0: strip every visible builder placeholder from the live driver pages.

The post-implementation audit flagged one placeholder section on
/schools-programs. A sweep of the whole property found fourteen, across six
pages. Builder notes ("supply verified credentials before publishing",
"PHASE 2", "add real photographs") were shipping to parents and school
districts.

Rule applied, from the audit: replace only with VERIFIED terms, otherwise
remove the field. Where a real source exists the placeholder becomes a fact:
teen pricing comes from the booking API (Driver's Ed class hourly_rate_cents
5000, min_duration_minutes 60, "Driver's Ed Coaching Session" addon 5000).
Where no source exists (founder credentials, coach certifications, pilot
purchase-credit terms, case studies) the element is deleted outright rather
than softened, because an unverifiable claim to a school district is the one
thing this property cannot afford.

Reads  <property>/source/  (byte-recovered from live by shared/tools/recover.py)
Writes <property>/upload/  (what shared/tools/deploy.py ships)
"""
import sys

sys.exit("""fix_placeholders.py is retired and will not run.
Its edits are already live and are folded into driver/source/.
Re-running it would revert the em dash sweep and 28 copy fixes.
Edit driver/source/ directly, then deploy with shared/tools/deploy.py.""")

# ---- the original implementation, kept for its reasoning ----
# import io, os, re, sys
#
# HERE = os.path.dirname(os.path.abspath(__file__))
# SRC = os.path.join(HERE, '..', 'source')
# DST = os.path.join(HERE, '..', 'upload')
#
# PRICE = ('<p class="lead" style="margin:0 0 14px">From $50 per hour, '
#          '60-minute minimum. Add a coach for the whole session for $50.</p>')
#
# COACHES = ('<p>Sessions are run by Academy simulator coaches. Academy is not a '
#            'state-licensed driving school and does not employ state-certified '
#            'driving instructors, so simulator time supplements the '
#            'behind-the-wheel instruction Florida requires rather than counting '
#            'toward it.</p>')
#
# REPORTING = ('<p>Every session ends with a verbal debrief with the parent: what '
#              'went well, what to practice next, and where to go from here.</p>')
#
# # (file, old, new). Empty new = delete. Every old must match exactly once.
# EDITS = [
#     # ---- about: unverifiable founder credentials -------------------------
#     ('about.html',
#      '      <p style="margin-top:10px"><span class="ph">PLACEHOLDER: founder bio, '
#      'certifications and verified credentials \u2014 supply final wording before '
#      'publishing.</span></p>\n', ''),
#
#     # ---- public-safety: case studies that do not exist -------------------
#     ('public-safety.html',
#      '      <div class="note"><strong>Case studies:</strong> <span class="ph">'
#      'PLACEHOLDER</span> \u2014 public-sector program results, participant counts '
#      'and customer quotations will be published here once verified.</div>\n', ''),
#
#     # ---- resources: internal roadmap note --------------------------------
#     ('resources.html',
#      '  <div class="note" style="margin-top:18px"><span class="ph">PHASE 2</span> '
#      '\u2014 each guide above becomes its own indexable page. Ask if you want one '
#      'prioritized.</div>\n', ''),
#
#     # ---- schools-programs -------------------------------------------------
#     # pilot length is negotiated, so say that instead of inventing a term
#     ('schools-programs.html',
#      '<td><span class="ph">PLACEHOLDER</span></td><td>Permanent</td>',
#      '<td>Set with the district</td><td>Permanent</td>'),
#     # purchase-credit terms are unconfirmed: drop the row entirely
#     ('schools-programs.html',
#      '      <tr><th>Purchase credit</th><td>Not applicable</td><td><span class="ph">'
#      'PLACEHOLDER: confirm credit terms</span></td><td>Not applicable</td></tr>\n', ''),
#     # no school has ever installed one, so the section cannot exist yet
#     ('schools-programs.html',
#      '<section class="sec"><div class="sec-in">\n'
#      '  <div class="sec-head"><div class="eyebrow">Case Studies</div>'
#      '<h2>SCHOOL INSTALLATIONS</h2></div>\n'
#      '  <div class="note"><span class="ph">PLACEHOLDER \u2014 CASE STUDIES</span>'
#      '<br><br>\n'
#      '  This section will carry verified school installations only: organization, '
#      'problem, simulator configuration, implementation, number of students, '
#      'training scenarios, results, a customer quotation, and photographs. No '
#      'customers, statistics or outcomes will be published here until they are '
#      'supplied and verified.</div>\n'
#      '</div></section>\n', ''),
#
#     # ---- simulator-rentals ------------------------------------------------
#     ('simulator-rentals.html',
#      '      <p style="margin-top:6px"><span class="ph">PLACEHOLDER: publish '
#      'starting rental price once confirmed.</span></p>\n', ''),
#     ('simulator-rentals.html',
#      '  <div class="note" style="margin-top:18px"><span class="ph">PHOTO / VIDEO '
#      'PLACEHOLDER</span> \u2014 add real photographs and video of the simulator '
#      'deployed at an event.</div>\n', ''),
#
#     # ---- teen-training ----------------------------------------------------
#     ('teen-training.html',
#      '      <p><span class="ph">PLACEHOLDER: duration &amp; package price</span></p>\n',
#      '      ' + PRICE + '\n', 3),
#     ('teen-training.html',
#      '        <p><span class="ph">PLACEHOLDER: coach names, certifications and '
#      'qualifications \u2014 supply verified credentials before publishing.</span></p>',
#      '        ' + COACHES),
#     ('teen-training.html',
#      '        <p><span class="ph">PLACEHOLDER: describe what parents receive after '
#      'a session (verbal debrief, written summary, or performance report).</span></p>',
#      '        ' + REPORTING),
#     ('teen-training.html',
#      '  <div class="note" style="margin-top:18px"><span class="ph">PHOTO '
#      'PLACEHOLDER</span> \u2014 add real photographs of students training on the '
#      'simulator. Photography is the highest-impact remaining improvement to this '
#      'page.</div>\n', ''),
#     # ---- simulator-rentals: the purchase-credit FAQ outlived the table row
#     # that was supposed to document its terms. It appears twice, in visible
#     # copy and in the FAQPage JSON-LD, and structured data left behind keeps
#     # asserting a claim the page no longer makes.
#     ('simulator-rentals.html',
#      'Pilot programs are designed for organizations evaluating a permanent installation. Ask about purchase credit when you request pricing.',
#      'Pilot programs are designed for organizations evaluating a permanent installation. Tell us your timeline when you request pricing and we will quote the pilot and the system together.', 2),
# ]
#
#
# def main():
#     if not os.path.isdir(DST):
#         os.makedirs(DST)
#     files = {}
#     for e in EDITS:
#         f, old, new = e[0], e[1], e[2]
#         want = e[3] if len(e) > 3 else 1
#         if f not in files:
#             files[f] = io.open(os.path.join(SRC, f), encoding='utf-8').read()
#         got = files[f].count(old)
#         if got != want:
#             raise SystemExit('  %s: expected %d match(es), found %d for:\n    %r'
#                              % (f, want, got, old[:90]))
#         files[f] = files[f].replace(old, new)
#         print('  %-24s %s %s' % (f, 'removed' if not new else 'replaced',
#                                  (old[:60].replace('\n', ' ') + '...')))
#
#     fail = False
#     for f, h in sorted(files.items()):
#         left = len(re.findall(r'class="ph"', h))
#         if left:
#             print('  !! %s still has %d .ph placeholder(s)' % (f, left)); fail = True
#         io.open(os.path.join(DST, f), 'w', encoding='utf-8', newline='').write(h)
#         print('  wrote %-24s %d bytes' % (f, len(h.encode())))
#     return 1 if fail else 0
#
#
# if __name__ == '__main__':
#     sys.exit(main())
