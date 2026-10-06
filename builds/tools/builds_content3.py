# -*- coding: utf-8 -*-
"""Builds batch 3: the /network/ hub.

Malik's framing: these are separate companies that BOUGHT simulators from
Academy. They are customers, not partners and not branches.

His goal is mutual: send traffic to owners who want it, and grow Academy's
network of places where a prospective buyer can see a rig in person.

So this page is built as a hub and an INVITATION. The brief is explicit: "Do
not publish incomplete partner pages" and "Do not imply every Academy customer
is a public demo location." Naming any company needs its details confirmed
and its owner's consent.

As of 2026-09-04, Malik confirmed three businesses by name with consent to be
listed, and gave the facts below directly (do not extend beyond them). Public
details (city, site URL, general business category) were confirmed by
checking each business's own website:

  - Kaizen Garage Studio (Sarasota, FL, kaizengaragestudio.com) - a luxury
    garage design studio and showroom. Two Academy-built sims are on site;
    customers come in to customize their garage design and look at
    renders/models with the team.
  - Sim to Grid, run by Ovik (Stuart, FL, simtogrid.com) - located inside a
    higher-end car shop. Two Academy-built sims are on site; Ovik runs track
    days and racing and uses the sims the way Academy does: coaching, and
    rentals for fun. He also runs events at his location and mobile events.
  - Superior Autohaus (Bonita Springs, FL, superiorautohaus.com) - a
    high-end performance shop, mostly European cars. One Academy-built sim
    is on site; customers use it while waiting on service, and Superior
    runs "fastest lap of the day" competitions on it during its car shows
    and parties.

Every other business that owns an Academy build remains unnamed until it
gives the same permission.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from builds_pages import (write, section, prose, faq, linkgrid, build_table,
                          CROSS, ld, SITE, LOUNGE, EVENTS)

PAGES = []

PAGES.append(dict(
    slug='network', url='/network/', ctype='network_hub',
    title='See An Academy Simulator In Person | Academy Sim Racing Builds',
    desc='Where you can see and drive an Academy simulator in the real world: our Tampa lounge, and independent businesses across Florida that own Academy builds.',
    crumbs='<a href="/">Builds</a> / Network',
    eyebrow='The Network',
    h1='See one in person<br><span class="accent">before you buy.</span>',
    lede='A spec sheet cannot tell you whether a wheelbase feels right or whether triples are worth the '
         'space. Driving one can. Here is where that is possible.',
    final_h='Find one <span class="accent">near you.</span>',
    final_p='Tell us roughly where you are and what you want to try. We will tell you what is realistic.',
    ld=ld('WebPage', 'See An Academy Simulator In Person',
          'Where to see and drive an Academy simulator: the Tampa lounge, and independent businesses across Florida that own Academy builds.',
          '/network/'),
    body='\n\n'.join([
        prose('Start Here', 'Two <span class="accent">different things.</span>', '', [
            '<p>There are two ways to get in front of an Academy simulator, and they are not the same '
            'thing. It is worth being precise about the difference, because plenty of companies in this '
            'industry are not.</p>',
            '<h3>1. Our lounge in Tampa</h3>',
            '<p>Academy has one place of its own: the lounge at 1421 Massaro Blvd in Tampa. Eight '
            'simulators, open to the public, bookable by the hour. Every component in the builds we sell is '
            'running there daily, which is the whole reason we can say drive it before you buy it and mean '
            'it.</p>',
            '<h3>2. Businesses around Florida that own Academy builds</h3>',
            '<p>Beyond that, independent companies across the state have bought Academy simulators for '
            'their own premises. Some are automotive businesses, some are venues, some run their own '
            'rentals and events.</p>',
            '<p><strong>Those are their businesses, not ours.</strong> They are customers who bought '
            'equipment from us. They are not Academy branches, they are not showrooms, and most of them '
            'are private premises with no obligation to show a simulator to anybody. Three have agreed to '
            'be named publicly below. We are not going to imply otherwise about the rest, and we are not '
            'going to publish an unlisted company&rsquo;s name and address without asking them first.</p>',
        ]),
        linkgrid('Where To Drive', 'The one place <span class="accent">that is ours.</span>',
                 'Open to the public, bookable by the hour, with every build component running daily.', [
                     (LOUNGE, 'ACADEMY LOUNGE, TAMPA',
                      '1421 Massaro Blvd. Eight simulators including motion, triple screen and '
                      'manual-shifter rigs. Book an hour and drive the exact components you would be buying.'),
                     (EVENTS, 'AT YOUR OWN EVENT',
                      'Academy Events delivers staffed simulators anywhere in Florida. If you want a group '
                      'to try before a purchase decision, that is often the simplest route.'),
                 ]),
        linkgrid('Also In The Network', 'Three businesses <span class="accent">that said yes.</span>',
                 'Independent companies that bought Academy builds and agreed to be named here. They are '
                 'customers running their own premises, not Academy branches or showrooms.', [
                     ('https://www.kaizengaragestudio.com/', 'KAIZEN GARAGE STUDIO · SARASOTA, FL',
                      'A luxury garage design studio and showroom with two Academy-built sims on site. '
                      'Customers come in to customize their own garage design and review renders and models '
                      'with the team.'),
                     ('https://simtogrid.com/', 'SIM TO GRID · STUART, FL',
                      'Run by Ovik inside a higher-end car shop, with two Academy-built sims on site. Ovik '
                      'races and runs track days himself, and uses the sims the way Academy does: coaching '
                      'and rentals for fun, at his location and at mobile events.'),
                     ('https://superiorautohaus.com/', 'SUPERIOR AUTOHAUS · BONITA SPRINGS, FL',
                      'A high-end performance shop specializing mostly in European cars, with one '
                      'Academy-built sim in the lobby. Customers use it while their car is serviced, and '
                      'Superior runs a "fastest lap of the day" competition on it at their car shows and '
                      'parties.'),
                 ]),
        prose('If You Are Buying', 'Ask us <span class="accent">what is near you.</span>', '', [
            '<p>If you are seriously considering a build and you are not near Tampa, ask. We know where our '
            'simulators are, and in some cases the owner is happy to let a genuine prospective buyer come '
            'and look.</p>',
            '<p>That is entirely at their discretion and always by arrangement. Some businesses welcome it, '
            'some have no interest, and both answers are fine. What we will not do is send you to a private '
            'address on the assumption that you will be welcome.</p>',
            '<div class="callout"><p><strong>What to tell us:</strong> roughly where you are, which build '
            'you are considering, and what you specifically want to feel. Wheelbase torque, triple screens '
            'versus a single ultrawide, and motion are the three things worth travelling for. Everything '
            'else can be settled on a call.</p></div>',
        ]),
        section('The Decisions', 'What is <span class="accent">worth travelling for.</span>',
                'Three things genuinely need to be felt. The rest of a build can be decided on a call.',
                build_table(['base', 'club-oled', 'club-triple', 'pole-position'],
                            'Club OLED against Club Triple is the single most common thing people come to '
                            'settle in person, because they are a thousand dollars apart and represent '
                            'opposite answers to the same question.')),
        prose('If You Own One', 'Want to be <span class="accent">on this page?</span>', '', [
            '<p>If your business owns an Academy build and you would be happy to host prospective buyers, '
            'tell us. There is a straightforward mutual case for it.</p>',
            '<h3>What you get</h3>',
            '<ul>'
            '<li>A page here about your business, linking to your site</li>'
            '<li>Referrals from people who want to see a simulator in your area</li>'
            '<li>Traffic from an audience already interested in what your simulator does</li>'
            '</ul>',
            '<h3>What we would need</h3>',
            '<ul>'
            '<li>Your explicit permission to name your business publicly</li>'
            '<li>Which build you have, and how you use it</li>'
            '<li>Whether visits are possible, and on what terms. Appointment only is completely fine and is '
            'the usual answer</li>'
            '<li>Anything you want said, and anything you want left out</li>'
            '</ul>',
            '<p>Nothing goes on this site without you agreeing to it first, and we will take it down the '
            'day you ask us to. If you would rather not be listed at all, that is the default and we will '
            'never publish your details.</p>',
        ]),
        CROSS,
        faq([
            ('Does Academy have showrooms around Florida?',
             'No. We have one location, the lounge in Tampa. Kaizen Garage Studio, Sim to Grid and '
             'Superior Autohaus are independent companies that bought equipment from us and agreed to be '
             'named here; they are not Academy branches or showrooms. Other businesses own Academy builds '
             'too, and remain unnamed until they give the same permission.'),
            ('Can I visit a business near me that owns one?',
             'Kaizen Garage Studio, Sim to Grid and Superior Autohaus are listed above with what you can '
             'do at each. For any other business with an Academy simulator, visiting is entirely at the '
             'owner&rsquo;s discretion and always by arrangement; ask us where you are and we will tell you '
             'honestly whether that is realistic.'),
            ('Why are only three businesses named on this page?',
             'Because those three gave us permission to name them and confirmed what visitors can actually '
             'do there. We have not asked every business that owns an Academy build, and publishing a '
             'company&rsquo;s name and address without asking would be wrong. Owners who want to be listed '
             'can tell us and we will add them.'),
            ('What is actually worth travelling to feel?',
             'Wheelbase torque, triple screens against a single ultrawide, and motion. Those three are hard '
             'to judge from a spec sheet. Everything else can be settled on a call.'),
            ('Can you bring a simulator to me instead?',
             'For a group or a business, often the simplest answer is Academy Events delivering a staffed '
             'setup. For an individual buyer, the Tampa lounge is usually more practical.'),
            ('I own an Academy build and want referrals. What do I do?',
             'Get in touch. We would need your permission to name you, which build you have and whether '
             'visits are possible. Appointment only is the usual and completely acceptable answer.'),
        ]),
    ]),
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
