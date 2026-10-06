#!/usr/bin/env python3
"""F4: the /league/ page was written in pre-season voice and read as stale once
Round 1 (2026-09-03) passed.  Season 3 runs Sep 3 to Oct 8 and the $20 entry
product is still available on Shopify (checked 2026-09-09, /products/leagues.js
-> available true, price 2000), and the page's own rules already document late
joiners, so the fix is to move the copy to present tense rather than to retire
the page or hand-stamp per-round status that goes stale again every Thursday.

Second pass, 2026-09-09, after shipcheck. The first pass changed ONE of the eight
places that say what $20 buys, so the page shipped a contradiction on its own
money path: the CTA said "the rest of the season" while the og/twitter
descriptions, the Event JSON-LD Offer name, the hero statline, the lead, the
other CTA card and step 1 all still said "all six rounds", which stopped being
true on 2026-09-03.  All eight now agree, and they agree with what the live rules
page says: "The $20 home entry still covers every remaining round."

Also removed: "a late entry can still post a full scoring record".  It was true
on the day it was written and false from 2026-09-11, because best-5-of-6 with one
drop only absorbs a single missed round.  Writing a claim with a 24-hour shelf
life into the primary conversion card is the exact defect this script exists to
repair.  Replaced with the drop rule itself, which is true on any day of the
season.

Applies to both lounge/site/league/index.html and lounge/upload/league/index.html.
Read and written with newline='' so line endings are preserved: the first pass
used Path.write_text() and converted the whole file to CRLF against an LF live
copy, putting 474 lines of churn into a five-line change.
"""
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGETS = [ROOT / "lounge/site/league/index.html", ROOT / "lounge/upload/league/index.html"]

EDITS = [
    # ---- tense ----
    # meta description led with a date now in the past
    ('$20 for all six rounds from home, or $40 a race at our Tampa lounge. Season 3 opens Sept 3.',
     '$20 for the season from home, or $40 a race at our Tampa lounge. Season 3 is running now.'),
    # hero sub: state that the season is live and still open
    ('Join from home for the whole season, or book a seat at the Tampa lounge and race any round in person.',
     'Season 3 is running now and still taking entries. Join from home, or book a seat at the Tampa '
     'lounge and race any round in person.'),
    # the lead image was captioned as an upcoming round
    ('<figcaption>Round 1: Road Atlanta, September 3</figcaption>',
     '<figcaption>Round 1 at Road Atlanta, in the Porsche 911 GT3 Cup</figcaption>'),
    # closing band announced an opening date that has passed
    ('<h2>Season 3 Opens September 3</h2>',
     '<h2>Season 3 Is Under Way</h2>'),

    # ---- what $20 buys: all eight places, so they cannot disagree ----
    ('<p>$20 covers all six rounds. Buy your entry, then request to join in iRacing under the same name.</p>',
     '<p>$20 covers every remaining round. Your worst round is dropped at the end of the season, '
     'including one you were not in. Buy your entry, then request to join in iRacing under the '
     'same name.</p>'),
    ('content="Season 3: Porsche Cup Pro-Am. $20 for all six rounds from home, or $40 a race at our Tampa lounge."',
     'content="Season 3: Porsche Cup Pro-Am. $20 for the season from home, or $40 a race at our Tampa lounge."'),
    ('"name": "Home season entry, all six rounds, own iRacing account required",',
     '"name": "Home season entry, every remaining round, own iRacing account required",'),
    ('<span><strong>$20</strong> &nbsp;Home season, all six rounds</span>',
     '<span><strong>$20</strong> &nbsp;Home season entry</span>'),
    ('Enter once from home for $20 and run all six rounds on your own rig',
     'Enter once from home for $20 and run every remaining round on your own rig'),
    ('<p>One payment covers your entry to all six rounds.',
     '<p>One payment covers your entry for the rest of the season.'),
    ('covers your whole season, all six rounds, from home.',
     'covers your season entry, every remaining round, from home.'),
    # the WebPage JSON-LD description, which the first pass left disagreeing with
    # the meta description it had just changed
    ("Pro-Am league. $20 for all six rounds from home, or $40 a race at our Tampa lounge.\",",
     "Pro-Am league. $20 for the season from home, or $40 a race at our Tampa lounge.\","),
    ('Racing from home is $20 for the whole season, paid once, using your own iRacing account.',
     'Racing from home is $20 for the season, paid once, using your own iRacing account.'),
]

fail = 0
for path in TARGETS:
    text = io.open(path, encoding="utf-8", newline="").read()
    before = len(text)
    # site/ comes back from git as CRLF under core.autocrlf while upload/ is LF.
    # Match and substitute in whatever the file actually uses; never rewrite it.
    eol = "\r\n" if "\r\n" in text else "\n"
    for old, new in EDITS:
        old = old.replace("\n", eol)
        new = new.replace("\n", eol)
        n = text.count(old)
        if n == 0:
            if new in text:
                continue          # already applied, this script is re-runnable
            print("MISS  {}: {!r}".format(path.name, old[:70]))
            fail = 1
            continue
        text = text.replace(old, new)   # og: and twitter: carry the same string
    io.open(path, "w", encoding="utf-8", newline="").write(text)
    print("wrote {}  {} -> {} chars".format(path.relative_to(ROOT), before, len(text)))

# the meta description has to stay inside a sane SERP length
for path in TARGETS:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith('<meta name="description"'):
            desc = line.split('content="', 1)[1].rsplit('"', 1)[0]
            print("meta description {} chars: {}".format(len(desc), desc))
            break

# Nothing on this page may still tell a buyer that their money covers "all six
# rounds" or "the whole season". shipcheck found seven such statements after the
# first pass changed only one, and a re-sweep found three more, so the sweep is
# now part of the script rather than something a reviewer has to redo.
#
# Scoped to lines that also carry a price or an entitlement word. "All six rounds
# run on Thursdays" in the Season Schedule section is a statement about the
# CALENDAR, is true on any day of the season, and must not be flagged.
import re
STALE = re.compile(r'all six rounds|all 6 rounds|whole season', re.I)
MONEY = re.compile(r'\$20|covers|entry|payment|paid once|price', re.I)
for path in TARGETS:
    for i, line in enumerate(io.open(path, encoding="utf-8", newline="").read().splitlines(), 1):
        m = STALE.search(line)
        if m and MONEY.search(line):
            print("!! %s:%d still promises %r on a money line" % (path.name, i, m.group(0)))
            fail = 1

sys.exit(fail)