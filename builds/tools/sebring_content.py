# -*- coding: utf-8 -*-
"""One new page: the Academy build placed at the Sebring Motor Garages clubhouse.

Fact base, confirmed directly by Malik (2026-09-04) -- do not extend beyond this:
  - The build lives in the Sebring Motor Garages clubhouse.
  - Sebring Motor Garages hosts events there and uses it themselves.
  - All Sebring Motor Garages clubhouse members have access to it.

Explicitly NOT true and must not be implied anywhere on this page:
  - Academy does not own, operate, or have an official partnership/affiliation
    with Sebring International Raceway.
  - This is not an Academy branch or retail location.
  - The public cannot walk in and use it; access runs through Sebring Motor
    Garages (clubhouse members and their events), not Academy directly.

Written standalone (not via builds_content*.py) so running it can never
regenerate or revert any other builds page. write() drops output in
builds/tools/builds_new/tracks/sebring-racing-simulator/index.html; the
promotion to site/ and upload/ is a manual, scoped copy of that one file.

Usage: python sebring_content.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builds_prices as P
from builds_pages import write, section, prose, faq, linkgrid, build_table, ld, LOUNGE, EVENTS

HPDE = 'https://hpdeacademy.com/'

SLUG = 'sebring-racing-simulator'
URL = '/tracks/%s/' % SLUG
TITLE = 'Sim Racing At Sebring: Academy Build At Sebring Motor Garages | Academy Sim Racing Builds'
DESC = ('Academy Sim Racing has a custom simulator build placed at the Sebring Motor Garages '
        'clubhouse, used for member practice and club events. See the same builds available '
        'to order, from %s.' % P.ENTRY)

CTA_ROW = (
    '  <div class="hero-ctas" style="justify-content:center;flex-wrap:wrap;">\n'
    '    <a class="btn btn-primary" href="https://builds.academysim.com/?ref=%s#start">Build My Simulator</a>\n'
    '    <a class="btn btn-secondary" href="tel:+18133559071">Try It At The Sebring Motor Garages Clubhouse</a>\n'
    '    <a class="btn btn-tertiary" href="%s">Visit The Academy Lounge In Tampa</a>\n'
    '  </div>\n' % (SLUG, LOUNGE)
)

BODY = '\n\n'.join([
    prose('Sebring, Florida', 'A Build Placed <span class="accent">At The Clubhouse.</span>', '', [
        '<p>Academy Sim Racing has a custom racing simulator build placed inside the Sebring '
        'Motor Garages clubhouse. Sebring Motor Garages hosts events there and uses the rig '
        'themselves, and clubhouse members have access to it as part of their membership.</p>',
        '<p>This is not an Academy retail location and not a public walk-in demo. Access to the '
        'build at the clubhouse runs through Sebring Motor Garages: their members, and their '
        'events. If you are not a member, the way to try Academy hardware in person is the '
        'Academy Lounge in Tampa, or your own build once it ships.</p>',
        '<h3>What this is not</h3>'
        '<p>Academy Sim Racing is not affiliated with, endorsed by, or partnered with Sebring '
        'International Raceway, and does not operate a branch at the track. Sebring Motor '
        'Garages is an independent clubhouse and garage-condo community near the circuit; the '
        'relationship described on this page is limited to the one build placed there.</p>',
    ]),
    section('Try Before You Buy', 'Three ways to <span class="accent">get to a wheel.</span>', '',
            CTA_ROW),
    section('The Lineup', 'The builds we <span class="accent">actually ship.</span>',
            'The Sebring Motor Garages clubhouse runs one configuration from this lineup. Every '
            'build below ships the same way, to anyone, nationwide.',
            build_table([s for s, _, _ in P.TIERS])),
    linkgrid('Prepping For The Real Track', 'For Sebring And <span class="accent">HPDE drivers.</span>',
             'If the goal is real seat time rather than clubhouse access, these are the two routes '
             'that get you there.', [
                 (HPDE, 'HPDE ACADEMY',
                  'High performance driver education that starts in the simulator and finishes on '
                  'the track. Not an Academy Sim Racing product; linked here because the intent is '
                  'the same.'),
                 (LOUNGE, 'ACADEMY LOUNGE, TAMPA',
                  'Book an hour and drive the exact components you would be ordering, open to the '
                  'public, no membership required.'),
                 (EVENTS, 'BRING A SIMULATOR TO YOUR EVENT',
                  'Academy Events delivers staffed simulators anywhere in Florida, the same way one '
                  'ended up at Sebring Motor Garages.'),
             ]),
    faq([
        ('Is Academy Sim Racing affiliated with Sebring International Raceway?',
         'No. Academy has no partnership, sponsorship, or operating relationship with Sebring '
         'International Raceway. The build described on this page is placed at the Sebring Motor '
         'Garages clubhouse, a separate, independent business near the circuit.'),
        ('Can the public use the simulator at the Sebring Motor Garages clubhouse?',
         'Access is through Sebring Motor Garages, not Academy directly: their clubhouse members, '
         'and the events they run there. It is not an Academy retail location and there is no '
         'public walk-in demo at that address.'),
        ('I am not a Sebring Motor Garages member. How do I try one?',
         'Book a session at the Academy Lounge in Tampa, open to the public, or order your own '
         'build and drive it wherever it ships.'),
        ('Can I get the same build for my own garage or clubhouse?',
         'Yes. The lineup above is exactly what shipped to Sebring Motor Garages and what ships '
         'everywhere else. Start a build and we will help you spec it for the space.'),
    ]),
])

PAGE = dict(
    slug=SLUG, url=URL, ctype='track_venue',
    title=TITLE, desc=DESC,
    crumbs='<a href="/">Builds</a> / Sebring Motor Garages',
    eyebrow='Sebring, Florida',
    h1='A Racing Simulator Build<br><span class="accent">At Sebring Motor Garages.</span>',
    lede='Academy placed one of its builds inside the Sebring Motor Garages clubhouse, where '
         'members and their events run it between track sessions.',
    final_h='Want one <span class="accent">of your own?</span>',
    final_p='Tell us the space and what you want it to do. We will spec a build the same way we '
            'did for Sebring Motor Garages.',
    ld=ld('WebPage', TITLE.split(' | ')[0], DESC, URL),
    body=BODY,
)

if __name__ == '__main__':
    path, n = write(PAGE)
    print('  %-52s %6d bytes' % (PAGE['url'], n))
