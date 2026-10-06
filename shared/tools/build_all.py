# -*- coding: utf-8 -*-
"""Run every fix in the one order that is correct, then stage for deploy.

Ordering is not cosmetic here. fix_review_counts.py and fix_phase2.py read from
upload/ when a file is already staged there, so anything that edits site/ must
run BEFORE them. Running the review-count fix first is exactly how the lounge
Tampa page shipped to a draft without the breadcrumbs that had just been added
to site/: the stale staged copy won.

upload/ is cleared first so a stale file from a previous run can never survive.

Usage: python build_all.py
"""
import os, shutil, subprocess, sys

# The CHILD's encoding was fixed below with PYTHONIOENCODING and the same trap was left
# standing on THIS side: when build_all's own stdout is a pipe or a file, Python picks the
# locale encoding (cp1252 on this box), so re-printing a child's decoded tick kills the
# PARENT -- again mid-run, again after upload/ has already been cleared, leaving a
# half-staged upload/ that looks like a finished build. Fixing one end of a pipe is not
# fixing the pipe. Hit 2026-08-31 on fix_health_claims.py's check mark, exactly the failure
# the comment below says it already solved.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

STEPS = [
    ('lounge/tools/add_crumbs.py',      []),   # site/ : visible trail
    ('lounge/tools/add_hpde_links.py',  []),   # site/ : the ninth property
    # F8, 2026-09-09. This wrote only into upload/ and was NOT a step here, so a
    # full rebuild silently stripped the homepage's 16-link Explore grid and the
    # hours line from every subpage footer. It runs on site/ FIRST, which is what
    # makes the patch survive on its own rather than depending on step order, and
    # again on upload/ after staging as a belt-and-braces pass. Both runs are
    # idempotent ("already present, skipped").
    ('lounge/tools/add_hub_links.py',   ['--tree', 'site']),
    # F8, 2026-09-09, the same failure class as lounge's above: these three
    # wrote only into upload/ and were not steps here, so a rebuild stripped
    # 362 lines of hub sections and footer hours across events, builds and
    # health. Each now takes --tree site|source|upload and runs against the
    # tree its property actually stages the homepage FROM:
    #   events  homepage <- source/ (fix_events_p0.py)
    #   builds  homepage <- source/ (fix_review_counts.py)
    #   health  homepage <- source/ (fix_health_claims.py)
    # SCOPE, deliberately narrow. events and builds get the source pass only.
    # Their tools walk EVERY index.html in whatever tree they are handed, and a
    # site/ or upload/ pass would newly patch pages the LIVE site does not have
    # the block on: 23 events leaf pages, and builds' for/index.html and
    # simulators/index.html. That is a content change, not a rebuild fix, so it
    # is out of scope here. builds' 19 leaf pages already carry the block in
    # site/ (pushed there 2026-09-09) and reach upload/ through stage.py.
    # health is the one property where every page the tool would touch is a
    # page the verified staging already has, so it gets the site pass too, and
    # the belt-and-braces upload pass after staging. Every pass is idempotent.
    ('events/tools/add_hub_links.py',   ['--tree', 'source']),
    ('builds/tools/add_hub_links.py',   ['--tree', 'source']),
    ('health/tools/add_hub_links.py',   ['--tree', 'source']),
    ('health/tools/add_hub_links.py',   ['--tree', 'site']),
    ('shared/tools/add_breadcrumbs.py', []),   # site/ : schema from that trail
    ('health/tools/fix_health_claims.py', []), # source/ -> upload/
    ('events/tools/fix_events_p0.py',   []),   # source/ -> upload/
    # Both P0 transforms that used to sit here are RETIRED: their edits are
    # live and folded into driver/source/, so re-running them would revert
    # the em dash sweep and 28 copy fixes. source/ is now the deployable
    # copy, so the eight flat pages are simply staged.
    ('driver/tools/stage_flat_pages.py', []),  # source/ -> upload/ (copy)
    ('shared/tools/fix_review_counts.py', []), # site|source -> upload/
    ('shared/tools/fix_phase2.py',      []),   # site|upload -> upload/
    ('shared/tools/stage.py', ['lounge', 'events', 'builds', 'driver', 'health']),
    ('lounge/tools/add_hub_links.py', ['--tree', 'upload']),  # after staging
    ('health/tools/add_hub_links.py', ['--tree', 'upload']),  # after staging
    # driver/tools/fix_canonical_nav.py is deliberately NOT a step. Two reasons,
    # both fatal: it FETCHES pages it cannot find locally straight from the live
    # site, which would make the build network-dependent and launder live HTML
    # back into a deploy (the same trap section 3 of lounge's tool was put
    # behind a flag for); and it rewrites hrefs on ALL EIGHT flat pages, while
    # the live site carries that patch on only two (schools-programs.html and
    # teen-training.html). Running it here would change six live pages. Its two
    # pages' worth of output is instead folded into driver/source/, which is
    # what stage_flat_pages.py copies, so a rebuild reproduces it exactly.
    ('shared/tools/gen_llms.py', []),          # upload/ : llms.txt, LAST on purpose
    # The loss gate. Runs LAST, on the finished artefact, because that is the only
    # place asset loss is visible: the five property audits read the HTML they find,
    # so losing every non-HTML file makes them pass faster. Reverting stage.py's
    # DEPLOYABLE allowlist used to leave this build exit 0.
    ('shared/tools/check_staged.py', []),
]

if '--dry-run' in sys.argv:
    print('  dry-run: STEPS (nothing will be run or cleared)\n')
    for script, args in STEPS:
        print('  %s%s' % (script, ('  ' + ' '.join(args)) if args else ''))
    print('\n  %d step(s)' % len(STEPS))
    sys.exit(0)

for key in ('lounge', 'events', 'builds', 'driver', 'health'):
    up = os.path.join(ROOT, key, 'upload')
    if os.path.isdir(up):
        shutil.rmtree(up)
print('  cleared every upload/\n')

for script, args in STEPS:
    print('== %s' % script)
    # PYTHONIOENCODING is load-bearing. stdout here is a PIPE, so a child
    # picks the locale encoding (cp1252 on this box) rather than UTF-8, and
    # any script printing a tick or a dash dies with UnicodeEncodeError
    # mid-run - after upload/ has already been cleared. That is how this
    # whole build stopped completing: fix_health_claims.py prints a check mark.
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    r = subprocess.run([sys.executable, os.path.join(ROOT, script)] + args,
                       cwd=ROOT, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode('utf-8', 'replace')
    tail = out.strip().splitlines()
    for line in tail:
        if '!!' in line or line.strip().startswith(('  ', '=', 'lounge', 'events',
                                                    'builds', 'driver', 'health')):
            pass
    print('\n'.join(tail[-4:]))
    if r.returncode != 0:
        print('\n'.join(l for l in tail if '!!' in l))
        raise SystemExit('  %s FAILED' % script)
print('\n  all steps clean')
