# -*- coding: utf-8 -*-
"""Task 03-hub-links: events currently links only 3 of 24 sitemap pages from
the homepage (the three hub pages, added in an earlier pass). This adds a
second section listing every leaf page (20 of them), grouped the way the
site already groups them (event-types / experiences / locations), plus
hours in the footer (address + phone already present).

2026-09-09, F8. This wrote only into upload/ and was not a build step, so a
full rebuild dropped the whole section and the hours block (56 lines). It now
takes `--tree site|source|upload` (default upload) and runs from build_all.py
on source/ (where fix_events_p0.py stages the homepage from) and again on
upload/ after staging. Every pass is idempotent and says so.

Usage: python add_hub_links.py [--tree site|source|upload]
"""
import os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import STREET, CITY_STATE_ZIP, PHONE_E164, PHONE, EMAIL
from shared.tools.hub_links_lib import parse_tree_arg, patch_homepage, patch_footer, patch_template

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TREE = parse_tree_arg(valid=('site', 'source', 'upload'))
UP = os.path.join(ROOT, TREE)
if not os.path.isdir(UP):
    raise SystemExit('!! %s does not exist, nothing to patch' % UP)
print('  tree: %s' % UP)
TEMPLATE = os.path.join(ROOT, 'template')


# ------------------------------------------------------------ 1. homepage --
EXPLORE = '''<section style="background:#fafafa;">
<div class="section" style="max-width:1100px;margin:0 auto;">
  <div class="section-head" style="text-align:center;">
    <div class="eyebrow" style="display:inline-block;">Every Format, Every City</div>
    <h2 class="h2">THE FULL LINEUP</h2>
    <p class="section-intro" style="margin:0 auto;">Every event type, every racing experience and every Florida city we deliver to.</p>
  </div>
  <div class="foot-grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-top:8px;">
    <div class="foot-col">
      <h4>Event Types</h4>
      <ul>
        <li><a href="/event-types/">All Event Types</a></li>
        <li><a href="/event-types/corporate-events/">Corporate Events</a></li>
        <li><a href="/event-types/trade-shows/">Trade Shows &amp; Expos</a></li>
        <li><a href="/event-types/conventions/">Conventions</a></li>
        <li><a href="/event-types/brand-activations/">Brand Activations</a></li>
        <li><a href="/event-types/car-dealership-events/">Car Dealership Events</a></li>
        <li><a href="/event-types/watch-parties/">Race Watch Parties</a></li>
        <li><a href="/event-types/employee-appreciation/">Employee Appreciation</a></li>
        <li><a href="/event-types/client-entertainment/">Client Entertainment</a></li>
        <li><a href="/event-types/private-parties/">Private Parties</a></li>
        <li><a href="/event-types/fundraisers/">Fundraisers &amp; Charity Events</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4>Racing Experiences</h4>
      <ul>
        <li><a href="/experiences/">All Racing Experiences</a></li>
        <li><a href="/experiences/gt3-racing-simulator/">GT3 Racing</a></li>
        <li><a href="/experiences/formula-racing-simulator/">Formula-Style Racing</a></li>
        <li><a href="/experiences/nascar-racing-simulator/">Stock Car Racing</a></li>
        <li><a href="/experiences/imsa-endurance-racing/">Endurance-Style Racing</a></li>
        <li><a href="/experiences/drift-racing-simulator/">Drift Racing</a></li>
        <li><a href="/experiences/rally-racing-simulator/">Rally Racing</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4>Where We Deliver</h4>
      <ul>
        <li><a href="/locations/">All Locations</a></li>
        <li><a href="/locations/tampa/">Tampa</a></li>
        <li><a href="/locations/orlando/">Orlando</a></li>
        <li><a href="/locations/daytona-beach/">Daytona Beach</a></li>
        <li><a href="/locations/sarasota/">Sarasota</a></li>
      </ul>
    </div>
  </div>
</div>
</section>

'''

patch_homepage(UP,
               anchor='<section class="faq">',
               section_html=EXPLORE,
               sentinel='Every Format, Every City')

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
