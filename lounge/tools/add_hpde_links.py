# -*- coding: utf-8 -*-
"""Section 12: give HPDE Academy its lane, and link to it.

The audit adds a ninth property, hpdeacademy.com, and sets the ownership rule:

    HPDE Academy owns "Sebring HPDE training" and real-world track preparation.
    Builds owns "Sebring racing simulator build".
    Lounge owns "Race Sebring on a simulator in Tampa".
    Events owns simulator rentals for Sebring-area events.

A sweep of all 103 built pages found ZERO references to hpdeacademy.com. The
boundary existed only in the strategy document, which is the state that lets two
properties drift into competing for the same terms. It also asks specifically to
"cross-link Sebring track page to Builds (buy) and HPDE Academy (real-world
training)". The Builds half was already there; this adds the other half.

Copy is taken from what HPDE Academy says about itself ("Sim Trained. Race
Ready.", "powered by Academy Sim Racing and Alliance Racing", tracks named:
Sebring, Daytona, Homestead), so nothing here asserts a relationship that site
does not already assert itself.

Tracking goes in the shared content_view block rather than beside each link, so
cross_domain_hpde fires from anywhere on the property, matching how
cross_domain_events and cross_domain_builds already work.
"""
import glob
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')

CARD = (
    '    <div class="cta-card">\n'
    '      <h3>Take It To The Real Track</h3>\n'
    '      <p>HPDE Academy runs high performance driver education that starts in '
    'the simulator and finishes on the track, {tracks}. It is powered by Academy '
    'Sim Racing and Alliance Racing, and it is where to go when the goal is a '
    'real track day rather than lap practice in Tampa.</p>\n'
    '      <a class="btn-ghost" href="https://hpdeacademy.com/">HPDE ACADEMY '
    '&rarr;</a>\n'
    '    </div>\n'
)

CARDS = {
    'tracks/sebring': 'at Sebring, Daytona and Homestead',
    'tracks/daytona': 'at Daytona, Sebring and Homestead',
}

# /tracks/sebring/ predates the rest of the build and writes the arrow as a
# literal character where the newer pages use the entity, so both spellings of
# the same anchor have to be accepted.
ANCHORS = [('      <a class="btn-ghost" href="https://builds.academysim.com">'
            'EXPLORE BUILDS %s</a>\n    </div>\n' % arrow)
           for arrow in (u'&rarr;', u'→')]

HUB_OLD = ('<p>Need simulators brought to a corporate day, party or team event? '
           'See <a href="https://events.academysim.com">Academy Events</a>.</p>')
HUB_NEW = ('<p>Preparing for a real track day rather than practicing laps? '
           '<a href="https://hpdeacademy.com/">HPDE Academy</a>, powered by '
           'Academy Sim Racing, runs high performance driver education that '
           'starts in the simulator and finishes on the track.</p>\n  ') + HUB_OLD

TRACK_OLD = """  document.querySelectorAll('a[href*="events.academysim.com"]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'cross_domain_events', { content_type: type, content_id: id });
    });
  });
"""
TRACK_NEW = TRACK_OLD + """  document.querySelectorAll('a[href*="hpdeacademy.com"]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'cross_domain_hpde', { content_type: type, content_id: id });
    });
  });
"""


def main():
    cards = tracked = hubs = 0
    for f in sorted(glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(f, SITE).replace(os.sep, '/')
        key = rel[:-len('/index.html')] if rel != 'index.html' else ''
        h = io.open(f, encoding='utf-8').read()
        before = h

        if key in CARDS and 'hpdeacademy.com' not in h:
            hit = [a for a in ANCHORS if h.count(a) == 1]
            if len(hit) != 1:
                print('  !! %s: found %d usable cta anchor(s)' % (rel, len(hit)))
                return 1
            h = h.replace(hit[0], hit[0] + CARD.format(tracks=CARDS[key]), 1)
            cards += 1
            print('  card    %s' % rel)

        if key == 'tracks' and 'hpdeacademy.com' not in h:
            if h.count(HUB_OLD) != 1:
                print('  !! %s: hub anchor found %d times' % (rel, h.count(HUB_OLD)))
                return 1
            h = h.replace(HUB_OLD, HUB_NEW, 1)
            hubs += 1
            print('  hub     %s' % rel)

        if TRACK_OLD in h and 'cross_domain_hpde' not in h:
            h = h.replace(TRACK_OLD, TRACK_NEW, 1)
            tracked += 1

        if h != before:
            io.open(f, 'w', encoding='utf-8', newline='').write(h)

    # gates
    fail = False
    for key in list(CARDS) + ['tracks']:
        h = io.open(os.path.join(SITE, key, 'index.html'), encoding='utf-8').read()
        if 'hpdeacademy.com' not in h:
            print('  !! %s has no HPDE link' % key)
            fail = True
        if h.count('<div') != h.count('</div>'):
            print('  !! %s: %d <div> vs %d </div>'
                  % (key, h.count('<div'), h.count('</div>')))
            fail = True
        # house rule: no em dashes in authored copy
        prose = h.split('<script')[0]
        if u'—' in prose:
            print('  !! %s: em dash in visible copy' % key)
            fail = True
    n = sum(1 for f in glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True)
            if 'cross_domain_hpde' in io.open(f, encoding='utf-8').read())
    print('\n  %d card(s), %d hub link(s), %d page(s) now tracking cross_domain_hpde'
          % (cards, hubs, n))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
