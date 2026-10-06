#!/usr/bin/env python3
"""F4: remove the builds site's exclusivity claims and replace the hero one with
Academy-specific proof.

The handoff records that competitor Velocity advertises showroom seat time, so
"no other builder can offer this" is unsupportable however it is phrased.

TWO places said it, 780 lines apart, and the first pass of this script found only
the first. shipcheck caught the second on 2026-09-09, after the ledger had already
recorded the claim as gone. Same lesson the F1 merge learned: a single string
literal is not a sweep. There is now a regex check at the bottom that fails this
script if ANY exclusivity phrasing survives anywhere in the file, so it cannot
report success while a third instance exists.

  1. hero / test-drive section -- replaced with a statement about Academy's own
     venue rather than about a competitor.
  2. FAQ answer -- the comparative clause is simply dropped. That also repairs a
     Google policy problem shipcheck found: the FAQPage JSON-LD copy of this same
     answer never carried the clause, so the visible text and the structured data
     disagreed, and the visible side was the one carrying the bad claim.

What the replacement may and may not assert. A first draft said the ten rigs run
"under paying customers every week we are open". Nothing Academy publishes
evidences per-week utilisation, the booking API exposes no inventory endpoint
(/api/resources, /api/categories and /api/sims are all 404), and the lounge page
explicitly excludes the driver-ed sims from the buyout product, so the claim
overreaches on top of being unreachable. Replacing an unsupportable claim with an
unverifiable one is not a fix. What IS published on lounge.academysim.com, and is
what the copy now says: the count of rigs, that the lounge is open to the public,
and that it is booked by the hour.

A second draft ended "from $40 an hour". builds_audit.py failed it as
UNKNOWN-PRICE $40, correctly: that audit validates every dollar figure on this
site against the build price ladder, and a lounge hourly rate on a page of ex-tax
build prices is exactly what it exists to catch.

All three copies of the homepage are patched. builds/ has source/, site/ AND
upload/, and shared/tools/fix_phase2.py stages the one in source/, so an edit made
only in site/ and upload/ is reverted by the next build_all.py run without ever
looking wrong.

Files are read and written with newline='' so line endings are preserved. The
first pass used Path.write_text(), which on Windows translated every LF to CRLF
and put 1,954 lines of pure line-ending churn into a two-line change.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGETS = [ROOT / "builds/source/index.html",
           ROOT / "builds/site/index.html",
           ROOT / "builds/upload/index.html"]

EDITS = [
    # 1. hero / test-drive section
    ("        No other custom sim builder can offer that.\n",
     "        Eight racing simulators and two driving simulators run in that lounge, open to the\n"
     "        public and booked by the hour. Drive it first, then decide.\n"),
    # 2. FAQ answer. Ends the sentence where the FAQPage JSON-LD copy already ends it.
    ("And you can drive it before you buy it, no one else can offer that.",
     "And you can drive it before you buy it."),
]

# Any of these surviving anywhere in the file fails the script.
BANNED = re.compile(
    r"no other (custom )?(sim )?builder|no one else|nobody else|"
    r"only builder|only custom sim|nowhere else|unmatched|"
    r"the only (sim )?(racing )?(builder|shop|place)", re.I)


def main():
    fail = 0
    for path in TARGETS:
        text = io.open(path, encoding="utf-8", newline="").read()
        # These three files do not agree on line endings: upload/ is LF (it is
        # gitignored and written by the staging tools) while site/ and source/
        # come back from git as CRLF under core.autocrlf. Match and substitute in
        # whichever ending the file actually uses, and never rewrite the others.
        eol = "\r\n" if "\r\n" in text else "\n"
        for old, new in EDITS:
            old = old.replace("\n", eol)
            new = new.replace("\n", eol)
            if old in text:
                text = text.replace(old, new, 1)
            elif new not in text:
                print("!! neither the old claim nor its replacement is in %s" % path)
                print("   looking for: %r" % old[:70])
                fail = 1
        io.open(path, "w", encoding="utf-8", newline="").write(text)

        left = [(i + 1, m.group(0)) for i, line in enumerate(text.splitlines())
                for m in [BANNED.search(line)] if m]
        if left:
            for ln, hit in left:
                print("!! exclusivity phrasing survives at %s:%d -- %r" % (path.name, ln, hit))
            fail = 1
        else:
            print("clean   %-28s no exclusivity phrasing anywhere in the file"
                  % str(path.relative_to(ROOT)))
    return fail


sys.exit(main())
