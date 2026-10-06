# -*- coding: utf-8 -*-
"""Task 03-hub-links: builds currently links only 3 of 23 sitemap pages from
the homepage (the three hub pages, added in an earlier pass). This adds a
second section listing every leaf page (19 of them: 10 under /for/, 9 under
/simulators/), plus an address and hours line to the footer Contact column
(builds currently has neither).

2026-09-09, F8. This wrote only into upload/ and was not a build step, so a
full rebuild dropped the catalogue section and every footer address+hours
block (182 lines over 20 pages). It now takes `--tree site|source|upload`
(default upload) and runs from build_all.py on source/ (fix_review_counts.py
stages the homepage from there), on site/ (the 19 leaf pages), and again on
upload/ after staging. Every pass is idempotent and says so.

Usage: python add_hub_links.py [--tree site|source|upload]
"""
import os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import ADDRESS, PHONE_E164, PHONE, EMAIL
from shared.tools.hub_links_lib import parse_tree_arg, patch_homepage, patch_footer, patch_template

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TREE = parse_tree_arg(valid=('site', 'source', 'upload'))
UP = os.path.join(ROOT, TREE)
if not os.path.isdir(UP):
    raise SystemExit('!! %s does not exist, nothing to patch' % UP)
print('  tree: %s' % UP)
TEMPLATE = os.path.join(ROOT, 'template')


# ------------------------------------------------------------ 1. homepage --
EXPLORE = '''<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Every Build, Every Buyer</span>
      <h2>The full <span class="accent">spec catalogue.</span></h2>
      <p>Every discipline we build for and every buyer we build for, linked directly rather than left to the sitemap.</p>
    </div>
    <div class="footer-top" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin-bottom:0;">
      <div class="footer-col">
        <h4>By Discipline</h4>
        <ul>
          <li><a href="/simulators/">All Disciplines</a></li>
          <li><a href="/simulators/gt3-racing-simulator/">GT3 Racing Simulator</a></li>
          <li><a href="/simulators/formula-racing-simulator/">Formula Racing Simulator</a></li>
          <li><a href="/simulators/nascar-racing-simulator/">Stock Car Racing Simulator</a></li>
          <li><a href="/simulators/imsa-endurance-racing-simulator/">Endurance Racing Simulator</a></li>
          <li><a href="/simulators/drift-racing-simulator/">Drift Racing Simulator</a></li>
          <li><a href="/simulators/rally-racing-simulator/">Rally Racing Simulator</a></li>
          <li><a href="/simulators/track-day-racing-simulator/">Track Day Simulator</a></li>
          <li><a href="/simulators/triple-screen-racing-simulator/">Triple Screen Simulator</a></li>
          <li><a href="/simulators/motion-racing-simulator/">Motion Simulator</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>By Buyer</h4>
        <ul>
          <li><a href="/for/">Who Buys A Build</a></li>
          <li><a href="/for/race-car-drivers/">Competition Drivers</a></li>
          <li><a href="/for/race-teams/">Race Teams</a></li>
          <li><a href="/for/track-day-drivers/">Track Day &amp; HPDE Drivers</a></li>
          <li><a href="/for/car-collectors/">Car Collectors</a></li>
          <li><a href="/for/luxury-garages/">Luxury Garages</a></li>
          <li><a href="/for/garage-condos/">Garage Condos</a></li>
          <li><a href="/for/car-dealerships/">Car Dealerships</a></li>
          <li><a href="/for/automotive-businesses/">Automotive Businesses</a></li>
          <li><a href="/for/offices/">Offices</a></li>
          <li><a href="/for/hotels-and-clubs/">Hotels &amp; Private Clubs</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>

'''

patch_homepage(UP,
               anchor='<section class="faq" id="faq">',
               section_html=EXPLORE,
               sentinel='Every Build, Every Buyer')

# ------------------------------------------------- 2. footer address+hours --
OLD_CONTACT = (
    '      <div class="footer-col">\n'
    '        <h4>Contact</h4>\n'
    '        <ul>\n'
    '          <li><a href="tel:' + PHONE_E164 + '">' + PHONE + '</a></li>\n'
    '          <li><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></li>\n'
    '          <li><a href="#start">Start a Build</a></li>\n'
    '        </ul>\n'
    '      </div>\n'
)
NEW_CONTACT = (
    '      <div class="footer-col">\n'
    '        <h4>Contact</h4>\n'
    '        <ul>\n'
    '          <li>' + ADDRESS + '</li>\n'
    '          <li><a href="tel:' + PHONE_E164 + '">' + PHONE + '</a></li>\n'
    '          <li><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></li>\n'
    '          <li><a href="#start">Start a Build</a></li>\n'
    '        </ul>\n'
    '        <h4 style="margin-top:1.25rem">Showroom Hours</h4>\n'
    '        <ul>\n'
    '          <li>Fri &amp; Sat 2–10 PM</li>\n'
    '          <li>Mon, Wed, Thu 12–9 PM</li>\n'
    '          <li>Sun 12–6 PM · Tue Closed</li>\n'
    '        </ul>\n'
    '      </div>\n'
)

patch_template(os.path.join(TEMPLATE, '_footer.html'), OLD_CONTACT, NEW_CONTACT)
patch_footer(UP, OLD_CONTACT, NEW_CONTACT)
