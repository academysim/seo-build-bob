# -*- coding: utf-8 -*-
"""Events batch 4: /locations/ hub plus four city pages.

Four, not the ten the brief lists. Codex and I agreed the ten-city version is
the biggest doorway-page risk in the whole handoff, and the README forbids
mass-generating thin city pages. Tampa, Orlando, Daytona Beach and Sarasota
each have genuinely different event economies. The rest wait for Search Console
demand.

Every page states plainly that Academy has no branch in that city. Wording is
taken from the brief: "serving", "available for events in", "delivered to",
"mobile simulator events in". No invented venues, venue relationships,
distances, travel times or prices.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events_pages import write
from events_content import prose, cards, faq, linkgrid, CROSS, ld

PAGES = []

TURNKEY = cards('What Is Included', 'FULLY TURNKEY',
    'Everything from the truck leaving Tampa to the room being clear at the end.', [
        ('01 / Transport', 'TRANSPORT AND DELIVERY',
         'We bring the simulators, screens, seating and power distribution to your venue.'),
        ('02 / Install', 'SETUP AND CALIBRATION',
         'Installed, wired and calibrated before doors, inside your load-in window.'),
        ('03 / Staff', 'STAFFING',
         'Our team runs the activation for the duration. Nobody on your side has to learn the software.'),
        ('04 / Guests', 'GUEST ONBOARDING',
         'Each driver is seated, set up and briefed. First-timers are driving properly in under a minute.'),
        ('05 / Running', 'EVENT OPERATION',
         'Sessions, queue management and timing, with a live leaderboard if you want one.'),
        ('06 / Out', 'TEARDOWN',
         'Removed inside your load-out window, leaving the space as we found it.'),
    ])

NOT_A_BRANCH = (
    '<div class="note-band"><p>Academy Sim Racing is based in Tampa at 1421 Massaro Blvd. We do not have '
    'an office, showroom or branch in %s. We deliver mobile simulator events there from our Tampa base, '
    'and travel and staffing are quoted per event.</p></div>'
)


def city(slug, city_name, title, desc, h1, lede, context_h, context, mix,
         local_notes, faqs, ldname):
    return dict(
        slug=slug, url='/locations/%s/' % slug, ctype='location',
        title=title, desc=desc,
        crumbs='<a href="/">Events</a> / <a href="/locations/">Locations</a> / ' + city_name,
        eyebrow='Serving ' + city_name,
        h1=h1, lede=lede,
        cta1='REQUEST %s %s QUOTE &rarr;' % (
            'AN' if city_name[0].upper() in 'AEIOU' else 'A',
            city_name.upper().split(',')[0]),
        cta2='CHECK YOUR DATE', cta2_href='/?ref=%s#quote' % slug,
        final_h='BRING THE RACE<br><span class="amber">TO %s.</span>' % city_name.upper(),
        final_p='Send us the venue, the date, your guest count and what the event is for. '
                'If you know how many simulators you want, tell us that too.',
        ld=ld('Service', ldname, desc, '/locations/%s/' % slug),
        body='\n\n'.join([
            prose('Local Context', context_h, '', context),
            cards('What We Run There', 'THE EVENT MIX', '', mix),
            TURNKEY,
            prose('Practical', 'WHAT TO KNOW LOCALLY', '', local_notes + [NOT_A_BRANCH % city_name]),
            linkgrid('Related', 'PLAN THE FORMAT', '', [
                ('/event-types/', 'BY EVENT TYPE',
                 'Corporate, trade show, convention, brand activation and dealership formats.'),
                ('/experiences/', 'BY RACING TYPE',
                 'GT3, Formula-style, stock car, endurance, drift and rally.'),
                ('/locations/', 'OTHER FLORIDA MARKETS',
                 'Where else we deliver mobile simulator events.'),
            ]),
            CROSS,
            faq(faqs),
        ]),
    )


# ------------------------------------------------------------- HUB ---------
PAGES.append(dict(
    slug='locations', url='/locations/', ctype='location_hub',
    title='Racing Simulator Rentals Across Florida | Academy Sim Racing',
    desc='Mobile racing simulator rentals delivered across Florida from our Tampa base. Corporate events, conventions, dealerships, brand activations and private events.',
    crumbs='<a href="/">Events</a> / Locations',
    eyebrow='Florida Service Area',
    h1='RACING SIMULATOR RENTALS<br>ACROSS FLORIDA',
    lede='Academy Sim Racing is based in Tampa and delivers fully staffed, turnkey simulator events '
         'throughout the state. We bring the rigs to your venue, run the activation, and take it all away again.',
    cta1='REQUEST A QUOTE &rarr;', cta2='CHECK YOUR DATE', cta2_href='/?ref=locations#quote',
    final_h='TELL US WHERE<br><span class="amber">AND WHEN.</span>',
    final_p='Send the venue, the city, the date and your guest count. We will tell you what it takes.',
    ld=ld('Service', 'Racing Simulator Rentals Across Florida',
          'Mobile racing simulator rentals delivered across Florida from a Tampa base, fully staffed and turnkey.',
          '/locations/'),
    body='\n\n'.join([
        prose('How It Works', 'ONE BASE, THE WHOLE STATE', '', [
            '<p>We operate from one place. Everything we bring to an event in Orlando, Daytona Beach or '
            'Sarasota leaves from our Tampa facility, arrives with our staff, and goes back the same way.</p>',
            '<p>That is worth being clear about, because service-area pages often imply a branch network that '
            'does not exist. <strong>Academy has one location. Everywhere else on this page is somewhere we '
            'deliver to, not somewhere we have an office.</strong></p>',
            '<p>Practically it means two things. Travel and staffing are quoted per event rather than baked '
            'into a list price, and lead time matters more the further you are from Tampa, particularly for '
            'multi-day installs.</p>',
        ]),
        linkgrid('Florida Markets', 'WHERE WE DELIVER MOST',
                 'Each of these has a different event economy, so the guidance is different.', [
                     ('/locations/tampa/', 'TAMPA',
                      'Our home market. The only city where coming to us is also an option.'),
                     ('/locations/orlando/', 'ORLANDO',
                      'Conventions, hotel conferences, resort events and trade shows.'),
                     ('/locations/daytona-beach/', 'DAYTONA BEACH',
                      'Motorsports, race-week activations, automotive brands and sponsor events.'),
                     ('/locations/sarasota/', 'SARASOTA',
                      'Private events, corporate retreats and club functions south of Tampa Bay.'),
                 ]),
        prose('Elsewhere', 'THE REST OF FLORIDA', '', [
            '<p>We take bookings across the state, including St. Petersburg, Clearwater, Wesley Chapel, '
            'Bradenton, Lakeland, Ocala, Jacksonville, Fort Myers, Naples and the South Florida markets. '
            'Those do not have their own pages yet, which is deliberate. We would rather write a genuinely '
            'useful page for a market once we have enough to say about it than publish a page that is this '
            'one with the city name swapped out.</p>',
            '<p>If your event is somewhere not listed, ask. The answer is usually yes.</p>',
            '<div class="note-band"><p>Academy Sim Racing operates from 1421 Massaro Blvd, Tampa, FL 33619. '
            'We do not have offices, showrooms or branches in any other city. Every other market listed here '
            'is served by mobile delivery from Tampa.</p></div>',
        ]),
        TURNKEY,
        CROSS,
        faq([
            ('Do you have locations outside Tampa?',
             'No. We have one facility, in Tampa. Everywhere else in Florida is served by mobile delivery from '
             'there, with our own staff travelling to the event.'),
            ('How far will you travel?',
             'Throughout Florida. Travel and staffing are quoted per event based on distance and duration.'),
            ('Is staff included?',
             'Yes, always. Delivery, setup, calibration, staffing for the duration and teardown are part of '
             'every booking.'),
            ('How much does a simulator rental cost?',
             'It depends on the number of rigs, the length of the event, the venue and the distance, so we quote '
             'rather than list. Send us the details and you will get a real number.'),
            ('How much space does a simulator need?',
             'It varies by rig and by how much queue space you want around it. Send us your floor plan or venue '
             'dimensions and we will tell you what fits.'),
            ('Can we use several simulators at one event?',
             'Yes. Multi-rig setups are common, and they are what you need if you want everyone through in a '
             'defined window.'),
            ('How far ahead should we book?',
             'The earlier the better, especially for branded wraps, multi-day installs, race weekends and dates '
             'in the lead-up to the holidays.'),
        ]),
    ]),
))

# ------------------------------------------------------------ TAMPA --------
PAGES.append(city(
    'tampa', 'Tampa',
    'Racing Simulator Rental Tampa | Corporate &amp; Private Events | Academy Sim Racing',
    'Racing simulator rentals in Tampa for corporate events, conventions, dealerships and private events. Our home market, with a fixed lounge as an alternative venue.',
    'RACING SIMULATOR RENTALS<br>IN TAMPA, FLORIDA',
    'Tampa is where we are based, which makes it the one market where you have a choice: we bring the '
    'simulators to your venue, or your group comes to ours.',
    'OUR HOME MARKET',
    ['<p>Everything Academy owns is in Tampa. That has practical consequences for events here that do not '
     'apply anywhere else in the state: shorter lead times are workable, last-minute changes are easier to '
     'absorb, and if something needs swapping mid-event we are not several hours away from a spare.</p>',
     '<p>It also means Tampa is the only city where you can skip the delivery entirely. Our lounge at 1421 '
     'Massaro Blvd has eight simulators permanently installed, and for groups up to a certain size a full '
     'lounge buyout is simpler and cheaper than a mobile setup. For anything larger, or anything that needs '
     'to happen at your venue, we deliver.</p>',
     '<h3>Which to choose</h3>',
     '<ul>'
     '<li><strong>Come to us</strong> if the group fits, the date is flexible, and you do not need the event '
     'tied to a specific venue. It is the least logistics and the lowest cost.</li>'
     '<li><strong>We come to you</strong> if the event is part of something bigger, the venue is fixed, you '
     'need branding, or the guest count is beyond what one room holds.</li>'
     '</ul>'],
    [('01 / Corporate', 'CORPORATE EVENTS', 'Tampa headquarters and regional offices running kickoffs, annual meetings and client nights.'),
     ('02 / Convention', 'CONVENTION DISTRICT', 'Shows and conferences in the downtown convention area, where load-in windows are tight and planning matters.'),
     ('03 / Dealerships', 'DEALERSHIP EVENTS', 'Grand openings, VIP nights and weekend family events across the Bay area.'),
     ('04 / Private', 'PRIVATE EVENTS', 'Birthdays, milestone celebrations and private hire, at your venue or at ours.'),
     ('05 / Community', 'COMMUNITY AND PUBLIC SAFETY', 'Community days and programs with local departments and civic organisations.'),
     ('06 / Lounge', 'AT OUR LOUNGE', 'Full lounge buyouts for groups, with all eight simulators and nobody else in the room.')],
    ['<h3>Lead time</h3>'
     '<p>Tampa is the one market where short notice is often workable, because nothing has to travel far. It is '
     'still worth booking ahead for anything in December or anything needing branded wraps.</p>',
     '<h3>Venues</h3>'
     '<p>We work in hotel ballrooms, convention space, offices, showrooms, warehouses and private homes across '
     'the Bay area. The constraints that decide what is possible are the same everywhere: door and lift access, '
     'floor space and available power.</p>',
     '<h3>The lounge as a fallback</h3>'
     '<p>If a venue turns out not to work, or plans change late, having a fixed venue with eight rigs a short '
     'drive away is a genuine safety net that we do not have in any other city.</p>'],
    [('Do you deliver racing simulators in Tampa?',
      'Yes. Tampa is our home market and where we are based, so it is the easiest and quickest market for us to '
      'deliver into.'),
     ('Can our group come to you instead?',
      'Yes. Our lounge at 1421 Massaro Blvd has eight simulators and can be booked out entirely for a group. For '
      'smaller groups that is usually simpler and cheaper than a mobile setup.'),
     ('Can you set up at hotels and convention centers?',
      'Yes. We work in hotel ballrooms and convention space regularly. Send us the venue and its load-in details '
      'and we will confirm what fits.'),
     ('Is staff included?',
      'Yes. Delivery, setup, calibration, staffing for the duration and teardown are part of every booking.'),
     ('How much space is required?',
      'It depends on the rig and how much queue space you want. Send us the floor plan and we will tell you '
      'exactly what works.'),
     ('Can you do short-notice bookings?',
      'More easily in Tampa than anywhere else, because nothing has to travel. Ask and we will tell you honestly '
      'whether the date is workable.'),
     ('Do you cover the wider Bay area?',
      'Yes, including St. Petersburg, Clearwater, Brandon, Riverview and Wesley Chapel.')],
    'Racing Simulator Rental In Tampa, Florida',
))

# ----------------------------------------------------------- ORLANDO -------
PAGES.append(city(
    'orlando', 'Orlando',
    'Racing Simulator Rental Orlando | Conventions &amp; Corporate Events | Academy Sim Racing',
    'Racing simulator rentals delivered to Orlando for conventions, hotel conferences, trade shows and resort events. Fully staffed and turnkey, from our Tampa base.',
    'RACING SIMULATOR RENTALS<br>IN ORLANDO, FLORIDA',
    'Orlando is a convention town, and convention work is a different discipline from evening events. '
    'Long show days, strict load-in windows, and an activation that has to look as good on day four as day one.',
    'A CONVENTION AND HOSPITALITY MARKET',
    ['<p>Almost everything we are asked to do in Orlando sits in one of two buckets: a trade show or convention '
     'stand, or a corporate group staying at a hotel or resort. Both are longer and more logistically '
     'constrained than the typical evening activation, and both reward planning early.</p>',
     '<p>The difference that catches people out is the venue rules. Large convention and hotel venues have '
     'defined load-in and load-out windows, specified dock access, and their own requirements for power, '
     'insurance and sometimes labour. None of it is difficult, but all of it has to be known in advance, and '
     'it is the reason we ask for the exhibitor kit before quoting rather than after.</p>',
     '<h3>What changes for a convention activation</h3>',
     '<ul>'
     '<li><strong>Show hours are long.</strong> Staffing is planned around the full run, not a three hour '
     'evening, and around the peaks after keynotes rather than the average.</li>'
     '<li><strong>Power is ordered, not assumed.</strong> Show power usually has to be booked through the '
     'organizer well ahead of the event.</li>'
     '<li><strong>The stand is the constraint.</strong> Booth dimensions and ceiling height decide the setup '
     'more than anything else.</li>'
     '<li><strong>Branding needs lead time.</strong> If the rig is being wrapped for the show, that decision '
     'has to happen early.</li>'
     '</ul>'],
    [('01 / Conventions', 'CONVENTIONS AND EXPOS', 'Multi-day shows where the staffing plan matters more than the hardware.'),
     ('02 / Hotels', 'HOTEL CONFERENCES', 'Corporate groups meeting at hotels and resorts, with the activation in a ballroom or breakout space.'),
     ('03 / Resorts', 'RESORT AND HOSPITALITY EVENTS', 'Guest-facing activations where the audience is broad and arriving all day.'),
     ('04 / Corporate', 'CORPORATE MEETINGS', 'Sales kickoffs and annual meetings for teams flown in from elsewhere.'),
     ('05 / Trade Shows', 'TRADE SHOW BOOTHS', 'Booth traffic, dwell time and qualified conversations on a busy floor.'),
     ('06 / Brand', 'BRAND ACTIVATIONS', 'Wrapped rigs as the centrepiece of a launch or campaign presence.')],
    ['<h3>Send us the exhibitor kit</h3>'
     '<p>For any convention or trade show booking this answers most of what we need: booth dimensions, ceiling '
     'height, dock and load-in times, and how power is ordered. We would rather read it before quoting than '
     'discover a constraint on install day.</p>',
     '<h3>Plan around the peaks</h3>'
     '<p>Convention floor traffic is not evenly spread. The setup has to cope with the rush after a keynote '
     'rather than the quiet hour before lunch, which is a staffing decision more than a hardware one.</p>',
     '<h3>Book early for the big weeks</h3>'
     '<p>Orlando has weeks where the whole city is busy. If your event falls in one, lead time matters more '
     'than usual, for us and for every other supplier you are using.</p>'],
    [('Do you deliver racing simulators to Orlando?',
      'Yes. We deliver mobile simulator events to Orlando from our Tampa base, with our own staff travelling to '
      'run the activation.'),
     ('Do you have an Orlando location?',
      'No. Academy has one facility, in Tampa. Orlando is a market we deliver to, not a location we operate from.'),
     ('Can you set up at hotels and convention centers?',
      'Yes, and it is most of what we do in Orlando. Send us the venue and the exhibitor or event kit and we '
      'will confirm what fits and what the venue requires.'),
     ('Can you work within our load-in window?',
      'Yes. Give us the load-in and load-out times and dock access details and we will plan the install around them.'),
     ('Do you staff the stand for the whole show?',
      'Yes. For multi-day bookings our team runs the activation for the full show hours every day.'),
     ('How much does an Orlando rental cost?',
      'It depends on rig count, show length, venue requirements and travel, so we quote rather than list. Send '
      'the details and you will get a real number.'),
     ('How far ahead should we book?',
      'Earlier than for a local evening event, particularly during Orlando&rsquo;s busiest weeks and if the rigs '
      'are being wrapped for the show.')],
    'Racing Simulator Rental In Orlando, Florida',
))

# ----------------------------------------------------- DAYTONA BEACH -------
PAGES.append(city(
    'daytona-beach', 'Daytona Beach',
    'Racing Simulator Rental Daytona Beach | Race Week &amp; Automotive Events | Academy Sim Racing',
    'Racing simulator rentals delivered to Daytona Beach for race-week activations, automotive brands, dealership events and sponsor hospitality.',
    'RACING SIMULATOR RENTALS<br>IN DAYTONA BEACH',
    'Daytona is the one market where your audience already knows what they are looking at. That raises the '
    'bar on format and lowers the amount of explaining anyone has to do.',
    'A MOTORSPORTS AUDIENCE',
    ['<p>At a corporate event in most cities, a racing simulator is a novelty and the job is to make it '
     'approachable. In Daytona, particularly around a race weekend, a meaningful share of the room follows '
     'motorsport properly. They will know the circuit on screen, they will have opinions about the car, and '
     'they will notice if the activation is superficial.</p>',
     '<p>That changes what we recommend. Formula-style and endurance-style racing land far better here than '
     'they would at a general corporate event, and running the circuit that is actually being raced that '
     'weekend is worth doing rather than a nice extra.</p>',
     '<h3>What works with an audience that knows racing</h3>',
     '<ul>'
     '<li><strong>Run the right circuit.</strong> Guests who have just watched a session have a direct '
     'reference, and comparing their lap to the real one is the conversation.</li>'
     '<li><strong>Offer a real challenge.</strong> Driver aids off for anyone who asks. This crowd wants the '
     'difficult version.</li>'
     '<li><strong>Endurance formats suit the calendar.</strong> Team relays and multi-class racing fit an '
     'audience that follows sports car racing.</li>'
     '<li><strong>Do not overclaim.</strong> A knowledgeable crowd notices immediately if a setup pretends to '
     'be something official that it is not.</li>'
     '</ul>'],
    [('01 / Race Week', 'RACE-WEEK ACTIVATIONS', 'Hospitality and brand presence built around a race weekend, when the whole area is focused on one thing.'),
     ('02 / Automotive', 'AUTOMOTIVE BRANDS', 'Manufacturer and aftermarket brands presenting to an audience that already cares.'),
     ('03 / Sponsors', 'SPONSOR HOSPITALITY', 'Client entertainment where the racing has to be credible to the people being entertained.'),
     ('04 / Dealerships', 'DEALERSHIP EVENTS', 'Local dealership events with a customer base that follows the sport.'),
     ('05 / Watch Parties', 'WATCH PARTIES', 'Race-day viewing with simulators running the circuit on the broadcast.'),
     ('06 / Endurance', 'ENDURANCE-STYLE EVENTS', 'Team relays and multi-class formats for an audience that follows sports car racing.')],
    ['<h3>Race weeks are a different planning problem</h3>'
     '<p>During a major race week, accommodation, access and local traffic all change. Load-in timings that '
     'would be routine on a normal week need more slack, and every supplier in the area is busy. Book early '
     'and build in margin.</p>',
     '<h3>Get the format right for the room</h3>'
     '<p>The default corporate recommendation of GT3 for everyone is often the wrong call here. Tell us who is '
     'coming and we will suggest something that respects the audience.</p>',
     '<h3>Be careful with branding claims</h3>'
     '<p>We wrap and brand the simulators we supply, and we do not provide series or manufacturer branding we '
     'are not licensed to use. In this market especially, an audience will spot an implied association that '
     'does not exist.</p>'],
    [('Do you deliver racing simulators to Daytona Beach?',
      'Yes. We deliver mobile simulator events to Daytona Beach from our Tampa base, with our own staff running '
      'the activation.'),
     ('Do you have a Daytona location?',
      'No. Academy has one facility, in Tampa. Daytona Beach is a market we deliver to.'),
     ('Can you set up during a race week?',
      'Yes, and we do. Race weeks need more lead time and more slack in the schedule because access and traffic '
      'change across the area, so book as early as you can.'),
     ('Can guests drive the circuit being raced that weekend?',
      'Where that circuit is in the software we run, yes. Tell us the weekend and we will confirm.'),
     ('Is this an official race series activation?',
      'No. We are not affiliated with, endorsed by or licensed by any racing series, sanctioning body or '
      'manufacturer. We supply simulator experiences and brand them for you within those limits.'),
     ('What format works best for a motorsport crowd?',
      'Usually Formula-style or endurance-style racing rather than the more forgiving formats we recommend for '
      'general corporate audiences. Tell us who is coming and we will advise.'),
     ('Is staff included?',
      'Yes. Delivery, setup, calibration, staffing for the duration and teardown are part of every booking.')],
    'Racing Simulator Rental In Daytona Beach, Florida',
))

# ---------------------------------------------------------- SARASOTA ------
PAGES.append(city(
    'sarasota', 'Sarasota',
    'Racing Simulator Rental Sarasota | Private &amp; Corporate Events | Academy Sim Racing',
    'Racing simulator rentals delivered to Sarasota for private events, corporate retreats, club functions and fundraisers. Fully staffed, from our Tampa base.',
    'RACING SIMULATOR RENTALS<br>IN SARASOTA, FLORIDA',
    'Sarasota work skews smaller and more private than Tampa or Orlando. Fewer trade show stands, more '
    'private venues, clubs and homes, and a season that shapes when things happen.',
    'A PRIVATE AND SEASONAL MARKET',
    ['<p>The events we are asked to do in Sarasota look different from the ones an hour north. There is less '
     'convention and trade show work and considerably more private hire: club functions, fundraisers, '
     'corporate retreats and events at private homes.</p>',
     '<p>That changes the setup. Smaller venues mean access matters more than floor space, guest counts are '
     'lower so throughput is rarely the constraint, and the format usually wants to be sociable rather than '
     'competitive. A leaderboard that dominates the evening is often the wrong call at a private event where '
     'the racing is meant to sit alongside the conversation.</p>',
     '<h3>The seasonal question</h3>',
     '<p>Southwest Florida is busier in the winter months, and the private and club events we get asked about '
     'cluster accordingly. If your date falls in season, treat lead time the way you would for a holiday '
     'party rather than a quiet Tuesday.</p>'],
    [('01 / Private', 'PRIVATE EVENTS', 'Milestone celebrations and private hire at homes and small venues.'),
     ('02 / Clubs', 'CLUB AND MEMBER FUNCTIONS', 'Member events where the activation has to suit a social evening rather than dominate it.'),
     ('03 / Retreats', 'CORPORATE RETREATS', 'Smaller offsites where the group is together for a day or two.'),
     ('04 / Fundraisers', 'FUNDRAISERS', 'Charity events where the simulator is the draw and the leaderboard is the competition.'),
     ('05 / Dealerships', 'DEALERSHIP EVENTS', 'Local dealership weekends and owner nights.'),
     ('06 / Community', 'COMMUNITY EVENTS', 'Public days where the audience is broad and arrives across the whole event.')],
    ['<h3>Access decides more than space</h3>'
     '<p>At private homes and smaller venues the question is rarely whether there is room. It is whether we can '
     'get the equipment in: door widths, steps, lifts, gate access and how close a vehicle can get. Photographs '
     'of the access route are more useful to us than the floor dimensions.</p>',
     '<h3>Power at private venues</h3>'
     '<p>Domestic and older venues need power checking properly, particularly for multi-rig setups. It is the '
     'single thing most likely to change a plan, so raise it early.</p>',
     '<h3>Pick a sociable format</h3>'
     '<p>For most Sarasota bookings we would suggest open racing rather than a structured competition, so guests '
     'drift between the rigs and the rest of the event rather than queueing for a scheduled slot.</p>'],
    [('Do you deliver racing simulators to Sarasota?',
      'Yes. We deliver mobile simulator events to Sarasota and the surrounding area from our Tampa base.'),
     ('Do you have a Sarasota location?',
      'No. Academy has one facility, in Tampa. Sarasota is a market we deliver to, not one we operate from.'),
     ('Can you set up at a private home?',
      'Yes, subject to access and power. Send photographs of the route in and the space and we will tell you '
      'what is workable before you commit.'),
     ('Do you cover Bradenton and Venice?',
      'Yes, and the surrounding area. Travel is quoted per event based on distance.'),
     ('What is the smallest event you will do?',
      'There is no fixed minimum, but very small events are usually better served by fewer rigs and a longer '
      'session length. Tell us the guest count and we will suggest what makes sense.'),
     ('Is staff included?',
      'Yes, always. Delivery, setup, calibration, staffing for the duration and teardown are part of every '
      'booking.'),
     ('When should we book for a winter date?',
      'As early as you can. The season is busier and the good dates go first.')],
    'Racing Simulator Rental In Sarasota, Florida',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
