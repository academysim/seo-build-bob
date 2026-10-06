# -*- coding: utf-8 -*-
"""Content for the first events.academysim.com pages.

Every claim here is either generic and verifiable, or already published on the
events homepage. No prices (the site quotes rather than lists), no invented
venues, clients, travel times or case studies.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events_pages import write, SITE

LOUNGE = 'https://lounge.academysim.com'
BUILDS = 'https://builds.academysim.com'


def faq(items):
    out = ['<section class="section faq">',
           '  <div class="section-head"><div class="eyebrow">Questions</div>'
           '<h2 class="h2">WHAT PLANNERS ASK</h2></div>',
           '  <div class="faq-list">']
    for q, a in items:
        out.append('    <div class="faq-item">')
        out.append('      <div class="faq-q">%s</div>' % q)
        out.append('      <div class="faq-a"><div class="faq-a-inner">%s</div></div>' % a)
        out.append('    </div>')
    out += ['  </div>', '</section>']
    return '\n'.join(out)


def prose(eyebrow, h2, intro, blocks):
    out = ['<section class="section">',
           '  <div class="section-head">',
           '    <div class="eyebrow">%s</div>' % eyebrow,
           '    <h2 class="h2">%s</h2>' % h2]
    if intro:
        out.append('    <p class="section-intro">%s</p>' % intro)
    out.append('  </div>')
    out.append('  <div class="prose">')
    out += ['    ' + b for b in blocks]
    out += ['  </div>', '</section>']
    return '\n'.join(out)


def cards(eyebrow, h2, intro, items):
    """items: (num, name, desc)"""
    out = ['<section class="section">',
           '  <div class="section-head">',
           '    <div class="eyebrow">%s</div>' % eyebrow,
           '    <h2 class="h2">%s</h2>' % h2]
    if intro:
        out.append('    <p class="section-intro">%s</p>' % intro)
    out += ['  </div>', '  <div class="types-grid">']
    for num, name, desc in items:
        out.append('    <div class="type-card">')
        out.append('      <div class="type-num">%s</div>' % num)
        out.append('      <div class="type-name">%s</div>' % name)
        out.append('      <div class="type-desc">%s</div>' % desc)
        out.append('    </div>')
    out += ['  </div>', '</section>']
    return '\n'.join(out)


def linkgrid(eyebrow, h2, intro, links):
    """links: (href, name, desc)"""
    out = ['<section class="section">',
           '  <div class="section-head">',
           '    <div class="eyebrow">%s</div>' % eyebrow,
           '    <h2 class="h2">%s</h2>' % h2]
    if intro:
        out.append('    <p class="section-intro">%s</p>' % intro)
    out += ['  </div>', '  <div class="linkgrid">']
    for href, name, desc in links:
        out.append('    <a class="linkcard" href="%s">' % href)
        out.append('      <div class="lc-name">%s</div>' % name)
        out.append('      <div class="lc-desc">%s</div>' % desc)
        out.append('    </a>')
    out += ['  </div>', '</section>']
    return '\n'.join(out)


CROSS = (
    '<section class="section">\n'
    '  <div class="section-head"><div class="eyebrow">Elsewhere at Academy</div>'
    '<h2 class="h2">TWO OTHER WAYS TO RACE</h2></div>\n'
    '  <div class="linkgrid">\n'
    '    <a class="linkcard" href="%s">\n'
    '      <div class="lc-name">DRIVE AT OUR TAMPA LOUNGE</div>\n'
    '      <div class="lc-desc">Eight simulators at 1421 Massaro Blvd. Book an hour, bring a group, '
    'or take the whole room.</div>\n'
    '    </a>\n'
    '    <a class="linkcard" href="%s">\n'
    '      <div class="lc-name">WANT A PERMANENT SYSTEM?</div>\n'
    '      <div class="lc-desc">Academy builds custom simulators for offices, showrooms and '
    'private clients.</div>\n'
    '    </a>\n'
    '  </div>\n'
    '</section>' % (LOUNGE, BUILDS)
)

LD_ORG = """{
  "@context": "https://schema.org",
  "@type": "%s",
  "name": "%s",
  "description": "%s",
  "url": "%s%s",
  "isPartOf": { "@type": "WebSite", "name": "Academy Sim Racing Events", "url": "%s/" },
  "provider": {
    "@type": "Organization",
    "name": "Academy Sim Racing",
    "telephone": "+1-813-355-9071",
    "areaServed": { "@type": "State", "name": "Florida" },
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1421 Massaro Blvd",
      "addressLocality": "Tampa",
      "addressRegion": "FL",
      "postalCode": "33619",
      "addressCountry": "US"
    }
  }
}"""


def ld(kind, name, desc, url):
    return LD_ORG % (kind, name, desc, SITE, url, SITE)


PAGES = []

# ---------------------------------------------------------------- HUB -------
PAGES.append(dict(
    slug='event-types', url='/event-types/', ctype='event_type_hub',
    title='Racing Simulator Rentals By Event Type | Academy Sim Racing',
    desc='Racing simulator rentals for corporate events, trade shows, conventions, brand activations and dealership events across Florida. Turnkey, staffed and delivered.',
    crumbs='<a href="/">Events</a> / Event Types',
    eyebrow='Event Types',
    h1='RACING SIMULATORS,<br>BUILT AROUND YOUR EVENT',
    lede='The rigs are the same. What changes is how they are staffed, branded, laid out and run. '
         'A trade show booth needs throughput. A client dinner needs conversation. A dealership night needs both.',
    final_h='TELL US ABOUT<br><span class="amber">YOUR EVENT.</span>',
    final_p='Send us the date, the venue and roughly how many people. We will come back with a plan and a price.',
    ld=ld('CollectionPage', 'Racing Simulator Rentals By Event Type',
          'Racing simulator rentals for corporate events, trade shows, conventions, brand activations and dealership events across Florida.',
          '/event-types/'),
    body='\n\n'.join([
        prose('Start Here', 'THE THING MOST PLANNERS GET WRONG', '', [
            '<p>Booking a simulator is easy. Getting the right result out of it is a question of format, '
            'and format depends entirely on what the event is for.</p>',
            '<p>If you want the longest queue on the trade show floor, you run short sessions with a live '
            'leaderboard and a staff member calling times. If you want your sales team to actually talk to '
            'people, you slow it down and let the rig be the reason someone stops rather than the whole '
            'interaction. If you are entertaining clients over dinner, the racing works better as something '
            'happening in the room than as a competition anyone has to take seriously.</p>',
            '<p>Same hardware. Completely different setup. The pages below cover what changes for each kind '
            'of event, and what to tell us when you ask for a quote.</p>',
        ]),
        linkgrid('Choose Your Format', 'BROWSE BY EVENT TYPE',
                 'Detailed guidance for the formats we run most often.', [
                     ('/event-types/corporate-events/', 'CORPORATE EVENTS',
                      'Sales kickoffs, annual meetings, team building, holiday parties and client appreciation nights.'),
                     ('/event-types/trade-shows/', 'TRADE SHOWS &amp; EXPOS',
                      'Booth traffic, dwell time and qualified conversations on a show floor.'),
                     ('/event-types/conventions/', 'CONVENTIONS',
                      'Multi-day shows where the staffing plan matters more than the hardware.'),
                     ('/event-types/brand-activations/', 'BRAND ACTIVATIONS',
                      'Custom-wrapped simulators for product launches and brand experiences.'),
                     ('/event-types/car-dealership-events/', 'DEALERSHIP EVENTS',
                      'Grand openings, VIP nights, test drive events and service waiting areas.'),
                     ('/event-types/watch-parties/', 'WATCH PARTIES',
                      'Race-day viewing with simulators running the circuit on the broadcast.'),
                     ('/event-types/employee-appreciation/', 'EMPLOYEE APPRECIATION',
                      'Recognition days built for inclusiveness rather than competition.'),
                     ('/event-types/client-entertainment/', 'CLIENT ENTERTAINMENT',
                      'Small-group hospitality where the racing supports the conversation.'),
                     ('/event-types/private-parties/', 'PRIVATE PARTIES',
                      'Birthdays and celebrations, delivered to your home or venue.'),
                     ('/event-types/fundraisers/', 'FUNDRAISERS',
                      'Charity events where the simulator is the fundraising mechanism.'),
                 ]),
        prose('What Is Included', 'TURNKEY MEANS TURNKEY', '', [
            '<p>Every booking includes delivery, setup, staffing for the duration and teardown. We bring the '
            'simulators, the screens, the seating and the power distribution, and we run the activation while '
            'we are there. Nobody on your team has to learn the software or reset a rig.</p>',
            '<h3>What we need from you</h3>',
            '<ul>'
            '<li>Date, venue and load-in access</li>'
            '<li>Roughly how many people, and over how long</li>'
            '<li>Available power at the activation point</li>'
            '<li>Whether you want the rigs branded, and with what</li>'
            '<li>What a good outcome looks like: traffic, conversations, leads or entertainment</li>'
            '</ul>',
            '<div class="note-band"><p>We are based in Tampa and deliver mobile simulator events throughout '
            'Florida. We do not operate branches in other cities. Travel and staffing outside the Tampa area '
            'are quoted per event.</p></div>',
        ]),
        CROSS,
        faq([
            ('How many simulators do we need?',
             'It depends on how many people you want through the rigs and how long you have. A booth running '
             'five minute sessions moves far more people than a dinner where guests drift over between courses. '
             'Tell us the headcount and the window and we will size it.'),
            ('Do you brand the simulators?',
             'Yes. Simulators can be custom wrapped for the event, and the on-screen leaderboard can carry your '
             'branding. Wraps need lead time, so raise it early.'),
            ('Does someone stay to run it?',
             'Yes. Staffing for the duration is part of every booking. Our team sets drivers up, resets sessions '
             'and keeps the queue moving.'),
            ('What about first-time drivers?',
             'Most guests at a corporate event have never driven a simulator. Driver aids are turned on by default '
             'and staff get people going in under a minute, so nobody is embarrassed in front of colleagues.'),
            ('How far in advance should we book?',
             'The earlier the better, particularly for branded wraps and for dates in the lead-up to the holidays. '
             'We do take short-notice bookings when the calendar allows.'),
            ('Do you travel outside Tampa?',
             'Yes, throughout Florida. Travel and staffing are quoted per event based on distance and duration.'),
        ]),
    ]),
))

# ------------------------------------------------------- CORPORATE ----------
PAGES.append(dict(
    slug='corporate-events', url='/event-types/corporate-events/', ctype='event_type',
    title='Racing Simulator Rental For Corporate Events | Florida | Academy Sim Racing',
    desc='Racing simulator rentals for corporate events across Florida. Sales kickoffs, annual meetings, team building and client appreciation. Turnkey, staffed and branded.',
    crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / Corporate Events',
    eyebrow='Corporate Events',
    h1='THE ACTIVITY PEOPLE<br>ACTUALLY REMEMBER',
    lede='Most corporate entertainment is endured politely. Racing simulators are the rare thing that gets '
         'competitive on its own, across every level of the org chart, without anyone being told to participate.',
    final_h='PLANNING A CORPORATE<br><span class="amber">EVENT IN FLORIDA?</span>',
    final_p='Send the date, the venue and your headcount. We will come back with a format and a price.',
    ld=ld('Service', 'Racing Simulator Rental For Corporate Events',
          'Turnkey racing simulator rentals for corporate events throughout Florida, including delivery, staffing and branding.',
          '/event-types/corporate-events/'),
    body='\n\n'.join([
        prose('Why It Works', 'IT LEVELS THE ROOM', '', [
            '<p>The reason simulators work at corporate events is that almost nobody is good at them. A '
            'graduate hire and a managing director start from roughly the same place, and the leaderboard '
            'does not care about titles. That produces the kind of mixing that team building exercises are '
            'supposed to produce and usually do not.</p>',
            '<p>It also gives people something to do with their hands and their attention. Standing around '
            'with a drink is hard work for a lot of people. Watching a colleague try to keep a car on the '
            'road is not.</p>',
            '<h3>The formats that work</h3>',
            '<ul>'
            '<li><strong>Open racing.</strong> Rigs run continuously, people come and go. Best for receptions '
            'and evening events where nothing should feel scheduled.</li>'
            '<li><strong>Leaderboard competition.</strong> One circuit, one car, everyone gets the same '
            'conditions, fastest lap of the night wins. This is the format that gets loud.</li>'
            '<li><strong>Bracket racing.</strong> Head to head elimination. Takes longer and needs a defined '
            'window, but it produces a proper finale.</li>'
            '<li><strong>Team relay.</strong> Departments against each other over a set number of laps. Good '
            'when the goal is cross team contact rather than individual glory.</li>'
            '</ul>',
        ]),
        cards('Where It Fits', 'THE EVENTS WE RUN MOST', '', [
            ('01 / Kickoffs', 'SALES KICKOFFS',
             'Break up a day of presentations with something physical. Works well as an afternoon reset or an evening close.'),
            ('02 / Annual', 'ANNUAL MEETINGS',
             'Multi-day meetings where the rigs run through breaks and receptions and give people a reason to leave the room.'),
            ('03 / Holidays', 'HOLIDAY PARTIES',
             'The alternative to another dinner. December books up early, so raise it well ahead.'),
            ('04 / Clients', 'CLIENT APPRECIATION',
             'Slower format, fewer rigs, more conversation. The racing is the reason to be there, not the agenda.'),
            ('05 / Teams', 'TEAM BUILDING',
             'Structured competition with mixed teams. Genuinely competitive without being physical or exposing.'),
            ('06 / Recognition', 'EMPLOYEE APPRECIATION',
             'Recognition events where the point is that people enjoy themselves rather than sit through a program.'),
        ]),
        prose('Practical', 'WHAT TO WORK OUT BEFORE YOU BOOK', '', [
            '<h3>Space and power</h3>',
            '<p>Each rig needs a footprint and mains power at the activation point. Ballrooms and conference '
            'centers are usually straightforward. Older venues and outdoor spaces need checking early, because '
            'power is the constraint that most often changes a plan.</p>',
            '<h3>Throughput</h3>',
            '<p>Work backwards from your headcount. If you want everyone to drive, session length multiplied by '
            'guests divided by rigs has to fit inside your window. If you only need the rigs as atmosphere, far '
            'fewer will do.</p>',
            '<h3>Branding</h3>',
            '<p>Simulators can be wrapped for the event and the leaderboard can carry your branding. Wraps need '
            'lead time. If the event is a launch or has a campaign attached, raise it in the first conversation.</p>',
            '<h3>Who is coming</h3>',
            '<p>A room of car enthusiasts and a room of people who have never played a driving game want different '
            'settings. We default to driver aids on so that first timers are not humiliated, and turn them off for '
            'anyone who asks.</p>',
            '<div class="note-band"><p>Academy Sim Racing is based in Tampa and delivers mobile simulator events '
            'throughout Florida. We do not operate offices or branches in other cities. Travel and staffing are '
            'quoted per event.</p></div>',
        ]),
        CROSS,
        faq([
            ('How many people can you get through in an evening?',
             'That is a function of rigs, session length and window rather than a fixed number. Short sessions '
             'with staff running the queue move a lot of people. Tell us the headcount and how long you have and '
             'we will size the setup to it.'),
            ('Will people who have never done this be able to drive?',
             'Yes. Driver aids are on by default and our staff set each person up. Most guests are driving '
             'competently within a lap or two, which is the point.'),
            ('Can you run it as a competition with prizes?',
             'Yes. A single circuit with identical conditions and a live leaderboard is the most popular format. '
             'We can run brackets or team relays if you want a defined finale.'),
            ('Do you supply everything?',
             'Yes. Delivery, setup, simulators, screens, seating, power distribution, staffing for the duration '
             'and teardown. Your team does not have to run anything.'),
            ('Can the simulators carry our branding?',
             'Yes, through custom wraps and on-screen branding. Wraps need lead time, so mention it early.'),
            ('Do you cover events outside Tampa?',
             'Yes, throughout Florida. Travel and staffing are quoted per event based on distance and duration.'),
        ]),
    ]),
))

# ------------------------------------------------------ TRADE SHOWS ---------
PAGES.append(dict(
    slug='trade-shows', url='/event-types/trade-shows/', ctype='event_type',
    title='Racing Simulator Rental For Trade Shows &amp; Expos | Academy Sim Racing',
    desc='Racing simulator rentals for trade show booths and expos in Florida. Draw traffic, increase dwell time and give your team more qualified conversations.',
    crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / Trade Shows',
    eyebrow='Trade Shows &amp; Expos',
    h1='THE BUSIEST BOOTH<br>ON THE FLOOR',
    lede='A trade show booth has one job before it has any other job: make people stop. A racing simulator '
         'does that from across the hall, and it holds them long enough for your team to start a conversation.',
    final_h='EXHIBITING IN<br><span class="amber">FLORIDA THIS YEAR?</span>',
    final_p='Send us the show, your booth size and your dates. We will tell you what fits and what it costs.',
    ld=ld('Service', 'Racing Simulator Rental For Trade Shows And Expos',
          'Turnkey racing simulator rentals for trade show booths and expos in Florida, including delivery, staffing and branding.',
          '/event-types/trade-shows/'),
    body='\n\n'.join([
        prose('The Problem', 'FOOTFALL IS NOT THE HARD PART', '', [
            '<p>Getting people past your booth is the show organizer&rsquo;s job. Getting them to stop, stay, '
            'and talk to someone is yours, and it is where most booths lose.</p>',
            '<p>A simulator solves the stopping problem structurally. It is tall, it is loud, it has a screen '
            'with motion on it, and there is usually a small crowd around it. People walk toward that without '
            'being asked. More usefully, a driver is stationary for the length of a session, and the people '
            'waiting are stationary too, which gives your team a queue of people who are standing still and '
            'have nothing else to do.</p>',
            '<h3>Dwell time is the metric that matters</h3>',
            '<p>A booth that people glance at as they pass converts almost nobody. A booth where someone spends '
            'four minutes in a seat and another few minutes waiting gives your sales team a real window. That is '
            'the difference a simulator makes, and it is why the format of the activation matters more than the '
            'hardware.</p>',
        ]),
        prose('Format', 'RUN IT FOR LEADS, NOT FOR FUN', '', [
            '<h3>Keep sessions short</h3>',
            '<p>Long sessions feel generous and perform badly. Short timed runs keep the queue moving, keep the '
            'leaderboard competitive, and mean more people through the booth over the day.</p>',
            '<h3>Put the leaderboard where the hall can see it</h3>',
            '<p>A live leaderboard turns a one off go into a reason to come back. People check whether they have '
            'been knocked off, which brings them past your team a second time.</p>',
            '<h3>Make the prize worth returning for</h3>',
            '<p>An end of day or end of show prize for the fastest lap gives people a reason to return on day two '
            'and a natural reason to leave contact details.</p>',
            '<h3>Brief your team on the handoff</h3>',
            '<p>The simulator creates the opportunity. Your team still has to take it. Decide in advance who talks '
            'to the person in the seat, who works the queue, and what the qualifying question is.</p>',
            '<div class="note-band"><p>Booth space, ceiling height, power drop and load-in windows all affect what '
            'we can install. Send us the exhibitor kit and we will tell you what fits before you commit.</p></div>',
        ]),
        cards('Logistics', 'WHAT WE HANDLE', '', [
            ('01 / Delivery', 'LOAD IN AND SETUP',
             'We deliver, install and test inside your load-in window, and tear down at the end of the show.'),
            ('02 / Staffing', 'STAFFED ALL SHOW',
             'Our team runs the activation for the duration so your people can sell rather than reset rigs.'),
            ('03 / Branding', 'WRAPPED TO MATCH',
             'Custom simulator wraps and on-screen branding so the rig reads as your booth, not as ours.'),
            ('04 / Capture', 'LEADERBOARD AND PRIZES',
             'A live leaderboard, running through the show, with a fastest lap prize if you want one.'),
        ]),
        CROSS,
        faq([
            ('How much booth space does a simulator need?',
             'It varies with the rig and how much queue space you want around it. Send us your booth dimensions and '
             'the exhibitor kit and we will tell you what fits.'),
            ('What power do you need?',
             'Mains power at the booth. Requirements depend on the setup, and show power has to be ordered from the '
             'organizer in advance, so raise it early.'),
            ('Can you install inside our load-in window?',
             'Yes. Give us the load-in and load-out times from the exhibitor kit and we will work to them.'),
            ('Can it be branded for the show?',
             'Yes, through custom wraps and on-screen branding. Wraps need lead time.'),
            ('Do you staff the booth for the whole show?',
             'Yes. Staffing for the duration is included, so your team can focus on conversations rather than '
             'running the activation.'),
            ('How do we capture leads from it?',
             'Most exhibitors tie entry to the leaderboard, or run a fastest lap prize that requires contact '
             'details. We will run the activation around whatever capture method you use.'),
        ]),
    ]),
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
