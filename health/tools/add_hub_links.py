# -*- coding: utf-8 -*-
"""Task 03-hub-links: add an "Explore" section to the health homepage linking
all 12 subpages (grouped Programs / Locations, matching how the site already
groups them), and add an hours line to the footer's Contact column, which is
identical across every page (homepage included -- unlike lounge, health's
homepage footer has no hours either).

2026-09-09, F8. This wrote only into upload/ and was not a build step, so a
full rebuild dropped the Explore section and every footer hours block (124
lines over 13 pages). It now takes `--tree site|source|upload` (default
upload) and runs from build_all.py on source/ (fix_health_claims.py stages the
homepage from there), on site/ (the 12 leaf pages), and again on upload/ after
staging. Every pass is idempotent and says so.

Usage: python add_hub_links.py [--tree site|source|upload]
"""
import os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import STREET, CITY_STATE_ZIP, PHONE_E164, PHONE, EMAIL
from shared.tools.paths import prop_root
from shared.tools.hub_links_lib import parse_tree_arg, patch_homepage, patch_footer, patch_template

ROOT = prop_root('health')
TREE = parse_tree_arg(valid=('site', 'source', 'upload'))
UP = os.path.join(ROOT, TREE)
if not os.path.isdir(UP):
    raise SystemExit('!! %s does not exist, nothing to patch' % UP)
print('  tree: %s' % UP)
TEMPLATE = os.path.join(ROOT, 'template')


# ------------------------------------------------------------ 1. homepage --
EXPLORE = '''<section style="background:var(--bg-tint2);border-top:1px solid var(--line);">
<div class="section" style="max-width:1100px;margin:0 auto;">
  <div class="section-head" style="text-align:center;">
    <div class="eyebrow" style="display:inline-block;">Explore Academy Health</div>
    <h2 class="h2">PROGRAMS &amp; LOCATIONS</h2>
    <p class="section-intro" style="margin:0 auto;">Every program we run and every Florida community we serve, in one place.</p>
  </div>
  <div class="foot-grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-top:8px;">
    <div class="foot-col">
      <h4>Programs</h4>
      <ul>
        <li><a href="/programs/">All Senior Programs</a></li>
        <li><a href="/programs/55-plus-community-activities/">55+ Community Activities</a></li>
        <li><a href="/programs/retirement-community-events/">Retirement Community Events</a></li>
        <li><a href="/programs/senior-community-race-night/">Senior Community Race Night</a></li>
        <li><a href="/programs/senior-living-racing-simulator/">Senior Living Programs</a></li>
        <li><a href="/programs/senior-wellness-activities/">Senior Wellness Activities</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4>Locations We Serve</h4>
      <ul>
        <li><a href="/locations/">All Florida Locations</a></li>
        <li><a href="/locations/tampa/">Tampa Senior Communities</a></li>
        <li><a href="/locations/clearwater/">Clearwater Communities</a></li>
        <li><a href="/locations/st-petersburg/">St. Petersburg Communities</a></li>
        <li><a href="/locations/orlando/">Orlando Communities</a></li>
        <li><a href="/locations/sarasota/">Sarasota Communities</a></li>
      </ul>
    </div>
  </div>
</div>
</section>

'''

patch_homepage(UP,
               anchor='<!-- FAQ -->\n<section class="faq">',
               section_html=EXPLORE,
               sentinel='Explore Academy Health')

# ------------------------------------------------------- 2. footer hours --
OLD_CONTACT = (
    '    <div class="foot-col">\n'
    '      <h4>Contact</h4>\n'
    '      <ul>\n'
    '        <li>' + STREET + '</li>\n'
    '        <li>' + CITY_STATE_ZIP + '</li>\n'
    '        <li><a href="tel:' + PHONE_E164 + '">' + PHONE + '</a></li>\n'
    '        <li><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></li>\n'
    '      </ul>\n'
    '    </div>\n'
)
NEW_CONTACT = (
    '    <div class="foot-col">\n'
    '      <h4>Contact</h4>\n'
    '      <ul>\n'
    '        <li>' + STREET + '</li>\n'
    '        <li>' + CITY_STATE_ZIP + '</li>\n'
    '        <li><a href="tel:' + PHONE_E164 + '">' + PHONE + '</a></li>\n'
    '        <li><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></li>\n'
    '      </ul>\n'
    '      <h4 style="margin-top:16px">Hours</h4>\n'
    '      <ul>\n'
    '        <li>Fri &amp; Sat 2–10 PM</li>\n'
    '        <li>Mon, Wed, Thu 12–9 PM</li>\n'
    '        <li>Sun 12–6 PM</li>\n'
    '        <li>Tue Closed</li>\n'
    '      </ul>\n'
    '    </div>\n'
)

patch_template(os.path.join(TEMPLATE, '_footer.html'), OLD_CONTACT, NEW_CONTACT)
patch_footer(UP, OLD_CONTACT, NEW_CONTACT)
