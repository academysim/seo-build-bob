# -*- coding: utf-8 -*-
"""Phase 2: give the lounge pages the breadcrumbs the other four properties have.

Events, Builds, Driver and Health all shipped with a visible crumb trail. Lounge
shipped without one on all 16 pages, so shared/tools/add_breadcrumbs.py had
nothing to derive BreadcrumbList schema from. This adds the visible trail; run
add_breadcrumbs.py afterwards to emit the matching schema.

Two details specific to this property:

- The stylesheet is INLINED into every page, so the rule is appended to each
  page's own <style> block rather than to a shared file.
- `:link` and `:visited` are named explicitly. A bare `.crumbs a` loses to the
  sheet's own `a, a:visited` rule, and getComputedStyle masks `:visited`, which
  is exactly how the prose links on this site shipped browser-default blue on a
  near-black background and stayed that way through several checks.

/tracks/sebring/ and the homepage predate the rest of the build and use
<body> + <div class="lp"> with no <main>, so the insertion point is found from
whichever wrapper the page actually has.
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')

# leaf labels, written out rather than derived from slugs so the trail reads
# the way a person would say it ("Stock Car", not "Nascar Simulator Tampa")
LABEL = {
    'racing': 'Racing',
    'racing/gt3-simulator-tampa': 'GT3',
    'racing/formula-simulator-tampa': 'Formula',
    'racing/nascar-simulator-tampa': 'Stock Car',
    'racing/drift-simulator-tampa': 'Drift',
    'racing/imsa-endurance-simulator-tampa': 'Endurance',
    'racing/rally-simulator-tampa': 'Rally',
    'racing/manual-transmission-simulator-tampa': 'Manual',
    'tracks': 'Tracks',
    'tracks/sebring': 'Sebring',
    'tracks/daytona': 'Daytona',
    'cars': 'Car Classes',
    'cars/classic-race-cars': 'Classic Race Cars',
    'cars-and-tracks': 'What Can I Race',
    'things-to-do-in-tampa': 'Things To Do In Tampa',
    # Added 2026-09-09. Both pages shipped on 09-02 with hand-written crumbs but
    # were never added here, and the missing-label check below runs BEFORE the
    # already-has-crumbs check, so this script hard-failed on two pages that
    # needed nothing done to them. build_all.py died on its first step from
    # 09-02 onward, after clearing every upload/. Labels match the crumbs those
    # two pages already carry.
    'league': 'League',
    'membership': 'Membership',
}

CSS = (
    "\n.lp .crumbs{padding-left:max(24px,calc(50% - 550px));"
    "padding-right:max(24px,calc(50% - 550px));padding-top:16px;"
    "font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.18em;"
    "text-transform:uppercase;color:#71717a;}\n"
    ".lp .crumbs a:link,.lp .crumbs a:visited{color:#a1a1aa;text-decoration:none;}\n"
    ".lp .crumbs a:hover{color:#fbbf24;}\n"
)


def crumb_html(rel):
    parts = rel.split('/')
    trail = ['<a href="/">The Lounge</a>']
    if len(parts) > 1:
        parent = parts[0]
        trail.append('<a href="/%s/">%s</a>' % (parent, LABEL[parent]))
    trail.append(LABEL[rel])
    return '<div class="crumbs">%s</div>\n' % ' / '.join(trail)


def main():
    changed = 0
    for f in sorted(glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(f, SITE).replace(os.sep, '/')[:-len('/index.html')]
        if rel == 'index.html' or rel == '':
            continue
        h = io.open(f, encoding='utf-8').read()
        # Order matters: a page that already carries crumbs needs nothing from
        # this script, so it must not be able to fail the label check.
        if 'class="crumbs"' in h:
            print('  -- %-50s already has crumbs' % rel)
            continue
        if rel not in LABEL:
            print('  !! no label for %s' % rel)
            return 1

        if '</style>' not in h:
            print('  !! %s has no inline <style>' % rel)
            return 1
        h = h.replace('</style>', CSS + '</style>', 1)

        block = crumb_html(rel)
        if '<main>' in h:
            h = h.replace('<main>', '<main>\n' + block, 1)
        elif '</nav>' in h:
            h = h.replace('</nav>', '</nav>\n' + block, 1)
        else:
            print('  !! %s has neither <main> nor </nav>' % rel)
            return 1

        io.open(f, 'w', encoding='utf-8', newline='').write(h)
        txt = re.sub(r'<[^>]+>', ' ', block)
        print('  ok  %-50s %s' % (rel, ' '.join(txt.split())))
        changed += 1
    print('\n  %d lounge page(s) given a visible crumb trail' % changed)
    return 0


if __name__ == '__main__':
    sys.exit(main())
