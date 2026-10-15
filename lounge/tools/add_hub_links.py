# -*- coding: utf-8 -*-
"""Task 03-hub-links: add an Explore section to the homepage linking all 15
subpages, and add an hours line to the compact subpage footer (the homepage
footer already has hours; the shared subpage footer does not).

Operates on a tree (site/ or upload/) and on template/ (the source assemble.py
expands into every subpage).

2026-09-09, F8. This script used to write only into upload/, and was not a step
in shared/tools/build_all.py. build_all.py clears upload/ before it runs, so the
next full rebuild would have silently dropped the homepage's 16-link Explore
grid and the hours line from every subpage footer -- the README's own
"generators revert post-generation patches" warning, live. Two changes:

  * `--tree site|upload` (default upload), so the patch can be pushed back into
    the SOURCE tree and survive on its own rather than depending on a step order.
  * section 3, which fetches missing subpages from the live site, is now behind
    `--fetch-missing` and off by default. It was written as one-off recovery for
    the 2026-09-02 incident that emptied upload/. Inside a build it would make
    the build depend on the network and quietly launder live HTML back into a
    deploy as though it had been generated, which is the provenance trap F8 is
    about.

Usage: python add_hub_links.py [--tree site|upload] [--fetch-missing]
"""
import io, os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import ADDRESS_LOUNGE, PHONE_E164, PHONE, EMAIL, HOSTS
from shared.tools.paths import prop_root
from shared.tools.hub_links_lib import rd, wr, parse_tree_arg, patch_homepage, patch_footer

ROOT = prop_root('lounge')
TREE = parse_tree_arg(valid=('site', 'upload'))
UP = os.path.join(ROOT, TREE)
if not os.path.isdir(UP):
    raise SystemExit('!! %s does not exist, nothing to patch' % UP)
print('  tree: %s' % UP)
TEMPLATE = os.path.join(ROOT, 'template')


# ------------------------------------------------------------ 1. homepage --
EXPLORE = '''<section style="background:#0f0f12;border-top:1px solid rgba(255,255,255,0.08);border-bottom:1px solid rgba(255,255,255,0.08);">
<div class="section" style="max-width:1100px;margin:0 auto;">
  <div class="section-head" style="text-align:center;">
    <div class="eyebrow" style="display:inline-block;">Explore The Lounge</div>
    <h2 class="h2">EVERYTHING WE COVER IN TAMPA</h2>
    <p class="section-intro" style="margin:0 auto 8px;">Every racing format, every track guide and every car class, in one place.</p>
  </div>
  <div class="foot-grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-top:8px;">
    <div class="foot-col">
      <h4>Racing Formats</h4>
      <ul>
        <li><a href="/racing/">All Racing Formats</a></li>
        <li><a href="/racing/gt3-simulator-tampa/">GT3 Racing In Tampa</a></li>
        <li><a href="/racing/formula-simulator-tampa/">Formula &amp; Open-Wheel Racing</a></li>
        <li><a href="/racing/nascar-simulator-tampa/">Stock Car &amp; Oval Racing</a></li>
        <li><a href="/racing/drift-simulator-tampa/">Drift Simulator</a></li>
        <li><a href="/racing/imsa-endurance-simulator-tampa/">Endurance Racing</a></li>
        <li><a href="/racing/rally-simulator-tampa/">Rally Stages</a></li>
        <li><a href="/racing/manual-transmission-simulator-tampa/">Manual Transmission Racing</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4>Track Guides</h4>
      <ul>
        <li><a href="/tracks/">All Track Guides</a></li>
        <li><a href="/tracks/daytona/">Daytona Track Guide</a></li>
        <li><a href="/tracks/sebring/">Sebring Track Guide</a></li>
      </ul>
      <h4 style="margin-top:16px">Car Classes</h4>
      <ul>
        <li><a href="/cars/">Race Car Classes Explained</a></li>
        <li><a href="/cars/classic-race-cars/">Classic Race Cars</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4>More To Explore</h4>
      <ul>
        <li><a href="/cars-and-tracks/">Full Cars &amp; Tracks Catalogue</a></li>
        <li><a href="/things-to-do-in-tampa/">Indoor Things To Do In Tampa</a></li>
      </ul>
    </div>
  </div>
</div>
</section>

'''

patch_homepage(UP,
               anchor='<section class="faq">',
               section_html=EXPLORE,
               sentinel='Explore The Lounge')

# ---------------------------------------------------- 2. subpage footers --
OLD_FOOTER = (
    '<footer class="footer">\n'
    '  <div>Academy Sim Racing · ' + ADDRESS_LOUNGE + ' · '
    '<a href="tel:' + PHONE_E164 + '">' + PHONE + '</a></div>\n'
    '  <div>Veteran Owned · <a href="/">The Lounge</a> · '
    '<a href="' + HOSTS['builds'] + '">Builds</a></div>\n'
    '</footer>'
)
NEW_FOOTER = (
    '<footer class="footer">\n'
    '  <div>Academy Sim Racing · ' + ADDRESS_LOUNGE + ' · '
    '<a href="tel:' + PHONE_E164 + '">' + PHONE + '</a></div>\n'
    '  <div>Fri &amp; Sat 2–10 PM · Mon, Wed, Thu 12–9 PM · '
    'Sun 12–6 PM · Tue Closed</div>\n'
    '  <div>Veteran Owned · <a href="/">The Lounge</a> · '
    '<a href="' + HOSTS['builds'] + '">Builds</a></div>\n'
    '</footer>'
)

# template source, so the next assemble.py run does not revert this
tpath = os.path.join(TEMPLATE, '_footer.html')
ts = rd(tpath)
if ts.strip() == OLD_FOOTER:
    wr(tpath, NEW_FOOTER + '\n')
    print('template/_footer.html: hours line added')
elif ts.strip() == NEW_FOOTER:
    print('template/_footer.html: already updated, skipped')
else:
    print('template/_footer.html: !! does not match expected OLD_FOOTER, left untouched -- check by hand')

# already-built subpages
patch_footer(UP, OLD_FOOTER, NEW_FOOTER)

if '--fetch-missing' not in sys.argv:
    print('section 3 (fetch missing subpages from live): SKIPPED, pass --fetch-missing')
    raise SystemExit(0)

# --------------------------------------------- 3. fetch any missing subpages --
# A concurrent session (08-memberships) held/removed most of upload/'s subpage
# files mid-session on 2026-09-02. deploy.py only overlays what's in upload/,
# so a file missing here is simply carried over from live untouched -- no data
# loss -- but it also means this script can't patch a file that isn't present.
# Fetch any of the 15 sitemap subpages still missing locally (verified first to
# carry no <form>; the racing/tracks/cars pages are pure content pages).
import urllib.request

ALL_SUBPAGES = [
    'racing/', 'racing/gt3-simulator-tampa/', 'racing/formula-simulator-tampa/',
    'racing/nascar-simulator-tampa/', 'racing/drift-simulator-tampa/',
    'racing/imsa-endurance-simulator-tampa/', 'racing/rally-simulator-tampa/',
    'racing/manual-transmission-simulator-tampa/',
    'tracks/', 'tracks/daytona/', 'tracks/sebring/',
    'cars/', 'cars/classic-race-cars/',
    'cars-and-tracks/', 'things-to-do-in-tampa/',
]
SITE = 'https://lounge.academysim.com'
fetched = []
for rel_dir in ALL_SUBPAGES:
    rel = rel_dir + 'index.html'
    local_p = os.path.join(UP, *rel.split('/'))
    if os.path.exists(local_p):
        continue
    url = SITE + '/' + rel_dir
    with urllib.request.urlopen(url) as r:
        s = r.read().decode('utf-8')
    if '<form' in s.lower():
        print('!! %s HAS A <form>, refusing to fetch-and-redeploy. Skipped.' % rel)
        continue
    if OLD_FOOTER not in s:
        print('!! %s fetched but OLD_FOOTER not found verbatim (page may already differ from what this script expects). Skipped -- check by hand.' % rel)
        continue
    s = s.replace(OLD_FOOTER, NEW_FOOTER, 1)
    os.makedirs(os.path.dirname(local_p), exist_ok=True)
    io.open(local_p, 'w', encoding='utf-8', newline='').write(s)
    fetched.append(rel)

print('subpages fetched from live + patched: %d' % len(fetched))
for rel in fetched:
    print('  ' + rel)
