# -*- coding: utf-8 -*-
"""F8 mechanisms 3 and 4: push into the tree each property actually stages from
the content that currently exists only in upload/ (hand-applied) or only in
site/ (while the step stages from source/).

Every edit is exact-match, count-checked, and written back with the file's own
line endings (newline=''), so nothing gains mixed endings.
"""
import io, os, sys

os.chdir('D:/AcademySimRacing/03-SEO-Build')

EDITS = []   # (path, old, new, expected_count, label)


def add(path, old, new, n, label):
    EDITS.append((path, old, new, n, label))


# ---------------------------------------------------------- mechanism 3 ----
# builds: the Task 10 mobile breakpoint was committed to site/, but
# fix_review_counts.py stages builds/index.html from source/. source/ is the
# tree that step reads, so the fix belongs there.
add('builds/source/index.html',
    '@media (max-width: 768px) {\n'
    '  .value-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }\n'
    '}\n',
    '@media (max-width: 768px) {\n'
    '  .value-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }\n'
    '}\n'
    '@media (max-width: 480px) {\n'
    '  .value-grid { grid-template-columns: 1fr; }\n'
    '}\n',
    1, 'builds: .value-grid 480px breakpoint into source/')

# health: same class. fix_health_claims.py stages health/index.html from
# source/; these three lines were committed to site/ only.
add('health/source/index.html',
    '  .lp .pad-mobile { padding-bottom:66px; }\n',
    '  .lp .pad-mobile { padding-bottom:66px; }\n'
    '  .lp.pad-mobile { padding-bottom:66px; }\n'
    '  .lp .nav .btn-amber { font-size:11px; padding:14px 13px; '
    'letter-spacing:0.08em; white-space:nowrap; }\n',
    1, 'health: .lp.pad-mobile + .nav .btn-amber into source/')

add('health/source/index.html',
    "background-image:url('images/sim-cockpit-bg.jpg')",
    "background-image:url('/images/sim-cockpit-bg.jpg')",
    1, 'health: absolute /images/sim-cockpit-bg.jpg into source/')

# ---------------------------------------------------------- mechanism 4 ----
# The unified Google reviews link, applied live 2026-09-02 and never pushed to
# any tree (RESULTS.md:1173).
GP = 'https://g.page/r/CSLLKCLuh-RlEBM'
add('lounge/site/index.html',
    'href="https://www.google.com/search?q=Academy+Sim+Racing+Tampa+reviews"',
    'href="%s"' % GP, 1, 'lounge: g.page reviews link into site/')
add('builds/source/index.html',
    'href="https://share.google/AO3xoIfkyWWBPGs0j"',
    'href="%s"' % GP, 2, 'builds: g.page reviews link x2 into source/')
add('health/source/index.html',
    'href="https://www.google.com/search?q=academy+sim+racing+tampa"',
    'href="%s"' % GP, 1, 'health: g.page reviews link into source/')

# lounge footer: Membership + Thursday Night League, hand-added to staging.
add('lounge/site/index.html',
    '        <li><a href="https://booking.academysim.com">Lockouts</a></li>\n'
    '      </ul>\n',
    '        <li><a href="https://booking.academysim.com">Lockouts</a></li>\n'
    '        <li><a href="/membership/">Membership</a></li>\n'
    '        <li><a href="/league/">Thursday Night League</a></li>\n'
    '      </ul>\n',
    1, 'lounge: Membership + Thursday Night League footer links into site/')

# lounge manual-transmission page: the three booking CTAs must carry the
# lessons_manual category. RESULTS.md:1249 predicted exactly this revert.
add('lounge/site/racing/manual-transmission-simulator-tampa/index.html',
    'href="https://booking.academysim.com/?category=racing"',
    'href="https://booking.academysim.com/?category=lessons_manual"',
    3, 'lounge: 3 lessons_manual booking CTAs into site/')

# driver: the canonical .html hrefs and the footer Hours block that
# fix_canonical_nav.py wrote into upload/ only. Pushed into source/ for the
# TWO pages the verified staging actually carries them on -- see the report;
# the other six are deliberately left alone because adding them would be a
# live content change, not a rebuild fix.
OLD_VISIT = (
    '        <li><a href="mailto:info@academysim.com">info@academysim.com</a></li>\n'
    '      </ul>\n'
    '    </div>\n'
)
NEW_VISIT = (
    '        <li><a href="mailto:info@academysim.com">info@academysim.com</a></li>\n'
    '      </ul>\n'
    '      <h4 style="margin-top:16px">Hours</h4>\n'
    '      <ul>\n'
    '        <li>Fri &amp; Sat 2\u201310 PM</li>\n'
    '        <li>Mon, Wed, Thu 12\u20139 PM</li>\n'
    '        <li>Sun 12\u20136 PM \u00b7 Tue Closed</li>\n'
    '      </ul>\n'
    '    </div>\n'
)
for f in ('schools-programs.html', 'teen-training.html'):
    add('driver/source/' + f,
        "href='/schools-programs#demo'", "href='/schools-programs.html#demo'",
        2, 'driver/%s: canonical .html#demo hrefs' % f)
    add('driver/source/' + f, OLD_VISIT, NEW_VISIT, 1,
        'driver/%s: footer Hours block' % f)


def main():
    fail = False
    by_file = {}
    for path, old, new, n, label in EDITS:
        by_file.setdefault(path, []).append((old, new, n, label))
    for path, edits in by_file.items():
        raw = io.open(path, encoding='utf-8', newline='').read()
        eol = '\r\n' if '\r\n' in raw else '\n'
        if eol == '\r\n' and '\n' in raw.replace('\r\n', ''):
            print('  !! %s has MIXED line endings; refusing to edit' % path)
            fail = True
            continue
        s = raw.replace('\r\n', '\n')
        before = s
        for old, new, n, label in edits:
            # `new` usually CONTAINS `old` (these are additive blocks), so
            # "old is gone" is the wrong test: it never fires, and a second run
            # inserts the block again. Testing `new` alone is the right one.
            if s.count(new) >= n:
                print('  -- %-70s already applied' % label)
                continue
            got = s.count(old)
            if got != n:
                print('  !! %-70s expected %d, found %d' % (label, n, got))
                fail = True
                continue
            s = s.replace(old, new)
            print('  ok  %-70s x%d' % (label, n))
        if fail:
            continue
        if s != before:
            io.open(path, 'w', encoding='utf-8', newline='').write(
                s.replace('\n', eol))
            print('      wrote %s (%s)' % (path, 'CRLF' if eol == '\r\n' else 'LF'))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
