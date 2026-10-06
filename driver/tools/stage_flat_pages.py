# -*- coding: utf-8 -*-
"""Stage driver's eight flat pages from source/ into upload/.

Why this exists, and why it is a plain copy rather than a transform.

driver.academysim.com has two kinds of page. The pages under /school-districts/,
/schools/ and /training/ are GENERATED into driver/site/ and staged by
shared/tools/stage.py. The eight flat pages at the root (index, about, contact,
public-safety, resources, schools-programs, simulator-rentals, teen-training)
have no generator: the site was built by drag-and-drop, so they were byte
recovered from live into driver/source/.

Until 2026-08-31 they reached upload/ as a side effect of two one-shot P0
transforms, fix_placeholders.py and fix_offer_types.py. Those have been retired.
Their edits are live and are now folded into source/, so re-running them against
the current source/ would have REVERTED the em dash sweep and 28 hand copy fixes
on six live pages. Measured, not assumed: run into a scratch directory, they
reintroduced 45 em dashes.

Because build_all.py clears upload/ before it runs, removing those two steps
without replacing them would have left driver's eight flat pages out of the
build altogether. This step is that replacement.

driver/source/ is therefore no longer a raw recovered archive. It IS the
deployable copy, it is what git tracks (upload/ is gitignored), and it is where
these eight pages should be edited. One copy, so nothing can silently disagree
with anything else.

Usage: python stage_flat_pages.py
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'source'))
DST = os.path.normpath(os.path.join(HERE, '..', 'upload'))

# A named set rather than a bare count. The count was 8, thanks.html was added
# in bc1af0e and nobody updated it, so from that commit on this step returned 2
# and killed build_all.py -- after upload/ had already been cleared. A count
# also cannot tell an added page from a deleted one; a set can, and it names
# which file moved. Adding or removing a flat page is meant to be a deliberate
# edit here.
EXPECTED = {
    'about.html', 'contact.html', 'index.html', 'public-safety.html',
    'resources.html', 'schools-programs.html', 'simulator-rentals.html',
    'teen-training.html',
    'thanks.html',   # form action target, live 200, deliberately not in the sitemap
}


def main():
    if not os.path.isdir(SRC):
        raise SystemExit('  !! %s is missing; nothing to stage' % SRC)
    if not os.path.isdir(DST):
        os.makedirs(DST)

    pages = sorted(f for f in os.listdir(SRC) if f.endswith('.html'))

    # A stage step that finds nothing must fail, not quietly succeed. This
    # property has been bitten three times by a tool reporting success over an
    # empty or missing directory.
    if not pages:
        raise SystemExit('  !! no .html in %s - staging nothing is not success' % SRC)
    found = set(pages)
    if found != EXPECTED:
        for f in sorted(found - EXPECTED):
            print('  !! %s is in source/ but not in EXPECTED; add it here on purpose' % f)
        for f in sorted(EXPECTED - found):
            print('  !! %s is EXPECTED but missing from source/' % f)
        return 2

    fail = False
    for f in pages:
        s = io.open(os.path.join(SRC, f), encoding='utf-8', newline='').read()

        # source/ is the deployable copy now, so the things the audit forbids
        # must not be in it. Catch them here rather than on the live site.
        left = len(re.findall(r'class="ph"', s)) + s.count('PLACEHOLDER')
        dashes = len(re.findall(r'&mdash;|—', s)) + s.count('\\u2014')
        if left:
            print('  !! %-24s %d placeholder(s)' % (f, left)); fail = True
        if dashes:
            print('  !! %-24s %d em dash(es)' % (f, dashes)); fail = True

        shutil.copyfile(os.path.join(SRC, f), os.path.join(DST, f))
        print('  staged %-24s %d bytes' % (f, len(s.encode('utf-8'))))

    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
