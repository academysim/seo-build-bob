# -*- coding: utf-8 -*-
"""Events batch 2: conventions, brand activations, dealership events.

Same rules as batch 1. The only client names used are ones already published on
the events homepage, and no prices, venues, travel times or case studies are
invented.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events_pages import write
from events_content import prose, cards, faq, CROSS, ld

PAGES = []

# ------------------------------------------------------- CONVENTIONS -------
PAGES.append(dict(
    slug='conventions', url='/event-types/conventions/', ctype='event_type',
    title='Racing Simulator Rental For Conventions | Florida | Academy Sim Racing',
    desc='Racing simulator rentals for multi-day conventions in Florida. Staffed for the full run, built for continuous throughput, delivered and operated by our team.',
    crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / Conventions',
    eyebrow='Conventions',
    h1='BUILT TO RUN<br>ALL WEEK',
    lede='A one night activation and a four day convention are different problems. Over a long run the '
         'hardware stops being the hard part and the staffing plan becomes everything.',
    final_h='EXHIBITING AT A<br><span class="amber">FLORIDA CONVENTION?</span>',
    final_p='Send the show, the dates and your space. We will tell you what a full run needs.',
    ld=ld('Service', 'Racing Simulator Rental For Conventions',
          'Turnkey racing simulator rentals for multi-day conventions in Florida, staffed and operated for the full run.',
          '/event-types/conventions/'),
    body='\n\n'.join([
        prose('The Difference', 'LENGTH CHANGES EVERYTHING', '', [
            '<p>At a single evening event a simulator either works or it does not, and you find out inside an '
            'hour. Across a multi-day convention the things that decide whether it worked are duller and more '
            'operational: whether the queue was managed at peak, whether the rigs were reset between drivers '
            'without a gap, whether anyone was left standing at a rig with nobody to help them.</p>',
            '<p>We have run simulators non-stop through multi-day corporate events, and the lesson is always '
            'the same. Throughput is a staffing question, not a hardware question.</p>',
            '<h3>What we plan around</h3>',
            '<ul>'
            '<li><strong>Peak versus average.</strong> Hall traffic is not evenly spread. The setup has to '
            'survive the rush after a keynote, not the quiet hour before lunch.</li>'
            '<li><strong>Session length across the day.</strong> Shorter sessions at peak, longer when the '
            'floor is quiet, so the queue never becomes a deterrent.</li>'
            '<li><strong>Continuous operation.</strong> Staff work the full show hours so there is never a rig '
            'sitting idle because nobody is there to restart it.</li>'
            '<li><strong>Overnight.</strong> Rigs stay in place between days and are checked and ready before '
            'doors open.</li>'
            '</ul>',
        ]),
        cards('Across The Run', 'WHAT A MULTI-DAY BOOKING INCLUDES', '', [
            ('01 / Install', 'LOAD IN AND TEST',
             'Delivered and installed inside your load-in window, tested, and ready before doors.'),
            ('02 / Operation', 'STAFFED EVERY HOUR',
             'Our team runs the activation for the full show hours, every day, so your people can work the floor.'),
            ('03 / Continuity', 'READY EACH MORNING',
             'Rigs are checked and reset before each day opens. Leaderboards can carry across the whole show or reset daily.'),
            ('04 / Out', 'TEARDOWN',
             'Removed inside your load-out window without your team having to manage it.'),
        ]),
        prose('Planning', 'WHAT TO SEND US', '', [
            '<p>The exhibitor kit answers most of what we need. Beyond that, the useful things to know early are '
            'your space and its ceiling height, the power drop available at your stand, your load-in and load-out '
            'windows, and the show hours for each day.</p>',
            '<p>If you want the simulators wrapped for the show, raise it in the first conversation. Wraps need '
            'lead time and cannot be turned around at short notice.</p>',
            '<div class="note-band"><p>Academy Sim Racing is based in Tampa and delivers mobile simulator events '
            'throughout Florida. We do not operate offices or branches in other cities. Travel, staffing and '
            'multi-day rates are quoted per event.</p></div>',
        ]),
        CROSS,
        faq([
            ('Do the rigs stay in place overnight?',
             'Yes. They stay installed for the run of the show and are checked and reset before each day opens.'),
            ('Do you staff every day of the convention?',
             'Yes. Staffing for the full show hours is part of a multi-day booking, so nobody on your team has to '
             'run the activation.'),
            ('Can the leaderboard run across the whole show?',
             'Yes. It can carry across all days for an overall fastest lap, or reset daily so each day has its own '
             'winner. Daily resets give people a reason to come back.'),
            ('How many simulators does a convention stand need?',
             'It depends on your space and expected traffic at peak rather than on total attendance. Send us your '
             'stand dimensions and the show and we will size it.'),
            ('Can you work to our load-in window?',
             'Yes. Send the exhibitor kit with load-in and load-out times and we will plan to them.'),
            ('Do you cover conventions outside Tampa?',
             'Yes, throughout Florida. Travel and staffing are quoted per event.'),
        ]),
    ]),
))

# --------------------------------------------------- BRAND ACTIVATIONS ------
PAGES.append(dict(
    slug='brand-activations', url='/event-types/brand-activations/', ctype='event_type',
    title='Racing Simulator Brand Activations &amp; Product Launches | Academy Sim Racing',
    desc='Custom-wrapped racing simulators for brand activations and product launches in Florida. Your branding on the rig, on the screen and on the leaderboard.',
    crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / Brand Activations',
    eyebrow='Brand Activations',
    h1='PUT YOUR BRAND<br>IN THE DRIVER&rsquo;S SEAT',
    lede='A branded simulator is not a banner people walk past. It is a thing they queue for, sit inside, '
         'and photograph, with your logo on every surface they are looking at.',
    final_h='LAUNCHING SOMETHING<br><span class="amber">IN FLORIDA?</span>',
    final_p='Tell us the campaign, the date and the venue. Wraps need lead time, so the earlier the better.',
    ld=ld('Service', 'Racing Simulator Brand Activations And Product Launches',
          'Custom-wrapped racing simulators for brand activations and product launches in Florida, delivered and staffed.',
          '/event-types/brand-activations/'),
    body='\n\n'.join([
        prose('Why A Simulator', 'ATTENTION YOU CAN MEASURE', '', [
            '<p>Most activation formats buy you a glance. A simulator buys you a seat, a queue and a photograph.</p>',
            '<p>The person driving is inside your branding for the length of a session, looking at a screen you '
            'control. The people waiting are standing next to it. And because a racing rig looks like something, '
            'it gets photographed and posted without anyone being asked to.</p>',
            '<h3>What can carry your brand</h3>',
            '<ul>'
            '<li><strong>The rig itself.</strong> Custom vinyl wraps across the chassis and seat area.</li>'
            '<li><strong>The screen.</strong> Branded leaderboard and on-screen graphics.</li>'
            '<li><strong>The car.</strong> Liveries in the simulator can be matched to the campaign.</li>'
            '<li><strong>The format.</strong> Prizes, challenges and capture mechanics built around what you want '
            'the activation to produce.</li>'
            '</ul>',
        ]),
        prose('Getting It Right', 'THE PART THAT NEEDS LEAD TIME', '', [
            '<h3>Wraps are not a last minute item</h3>',
            '<p>Custom wraps have to be designed, printed and fitted. If the activation has a campaign attached, '
            'bring us in while the creative is still being decided rather than after it is locked, so the artwork '
            'is built for the surfaces it is going on.</p>',
            '<h3>Decide what the activation is for</h3>',
            '<p>Reach, dwell time, data capture and social content are different goals and they pull the format in '
            'different directions. A fast-moving queue maximises how many people touch the brand. A slower format '
            'with a prize maximises how many leave details. Pick one to optimize for.</p>',
            '<h3>Think about the photograph</h3>',
            '<p>If social content is part of the brief, the rig needs to be lit and placed so that a phone photo '
            'looks good, with branding in frame from the angle people will actually shoot from.</p>',
            '<div class="note-band"><p>We produce branding for the simulators we supply. We are not affiliated with '
            'and do not represent any racing series, sanctioning body or car manufacturer, and we do not provide '
            'licensed series branding.</p></div>',
        ]),
        cards('Formats', 'ACTIVATIONS WE RUN', '', [
            ('01 / Launch', 'PRODUCT LAUNCHES',
             'The simulator as the centrepiece, wrapped in the campaign, with the product alongside it.'),
            ('02 / Retail', 'RETAIL AND MALL ACTIVATIONS',
             'High footfall spaces where the rig has to draw people in from a distance.'),
            ('03 / Sponsorship', 'SPONSOR ACTIVATIONS',
             'Simulators as the interactive element of a wider sponsorship presence.'),
            ('04 / Roadshow', 'MULTI-STOP TOURS',
             'The same activation delivered across several Florida dates with consistent setup and staffing.'),
        ]),
        CROSS,
        faq([
            ('How far ahead do you need artwork for a wrap?',
             'As early as possible. Wraps have to be designed, printed and fitted, so raise it in the first '
             'conversation rather than close to the date.'),
            ('Can you match the simulator car to our brand?',
             'On-screen liveries can be customized. We do not provide branding for racing series or manufacturers '
             'we are not licensed to represent.'),
            ('Can we capture leads through the activation?',
             'Yes. Most brands tie entry or the prize to contact details. We build the format around whatever '
             'capture method you are using.'),
            ('Can you run the same activation in several cities?',
             'Yes, across Florida. Multi-stop tours are quoted per event based on dates and distances.'),
            ('Do you provide the staff?',
             'Yes. Delivery, setup, staffing for the duration and teardown are part of every booking.'),
            ('Can the leaderboard carry our branding?',
             'Yes. The on-screen leaderboard and graphics can be branded for the activation.'),
        ]),
    ]),
))

# ---------------------------------------------------------- DEALERSHIPS -----
PAGES.append(dict(
    slug='car-dealership-events', url='/event-types/car-dealership-events/', ctype='event_type',
    title='Racing Simulator Rental For Car Dealership Events | Academy Sim Racing',
    desc='Racing simulator rentals for dealership events in Florida. Grand openings, VIP nights, test drive events and service waiting areas. Delivered, branded and staffed.',
    crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / Dealership Events',
    eyebrow='Dealership Events',
    h1='GIVE PEOPLE A REASON<br>TO STAY ON THE LOT',
    lede='Dealership events live or die on dwell time. A racing simulator keeps families occupied, gives '
         'enthusiasts something to talk about, and buys your sales team the minutes they need.',
    final_h='PLANNING A<br><span class="amber">DEALERSHIP EVENT?</span>',
    final_p='Send the date and what the event is for. We will suggest a format and quote it.',
    ld=ld('Service', 'Racing Simulator Rental For Car Dealership Events',
          'Turnkey racing simulator rentals for dealership grand openings, VIP nights, test drive events and service areas in Florida.',
          '/event-types/car-dealership-events/'),
    body='\n\n'.join([
        prose('The Fit', 'THE AUDIENCE IS ALREADY THERE FOR CARS', '', [
            '<p>Most event activations have to work to connect themselves to the brand in the room. At a '
            'dealership that problem does not exist. People came to look at cars, and a racing simulator is the '
            'most obvious possible extension of that.</p>',
            '<p>Practically, it solves the two problems dealership events actually have. It occupies the people '
            'who are not the decision maker, which is usually what cuts a visit short. And it gives a salesperson '
            'a reason to stand next to someone for five minutes without it being a pitch.</p>',
            '<h3>Where it goes</h3>',
            '<ul>'
            '<li><strong>Showroom floor.</strong> Visible from the entrance, next to the cars.</li>'
            '<li><strong>Under a event tent outside.</strong> For grand openings and larger weekend events, subject '
            'to power and weather cover.</li>'
            '<li><strong>Service waiting area.</strong> A longer-term option for the people with the least to do '
            'and the most time to do it in.</li>'
            '</ul>',
        ]),
        cards('Occasions', 'WHEN DEALERSHIPS BOOK US', '', [
            ('01 / Openings', 'GRAND OPENINGS',
             'The launch weekend, where the job is getting people through the door and keeping them there.'),
            ('02 / VIP', 'VIP AND OWNER NIGHTS',
             'Invitation evenings for existing customers, where the simulator is the entertainment rather than the pitch.'),
            ('03 / Test Drives', 'TEST DRIVE EVENTS',
             'Something for people to do while they wait their turn, and for whoever came with them.'),
            ('04 / Service', 'SERVICE WAITING AREAS',
             'Longer placements that change how a service visit feels.'),
            ('05 / Launch', 'MODEL LAUNCHES',
             'A branded rig alongside the new model, wrapped for the campaign.'),
            ('06 / Community', 'FAMILY AND COMMUNITY DAYS',
             'Weekend events where the audience is broader than buyers.'),
        ]),
        prose('Practical', 'WHAT MAKES IT WORK ON A LOT', '', [
            '<h3>Put it where it is seen from outside</h3>',
            '<p>A simulator visible through the showroom glass does work before anyone walks in. Tucked in a back '
            'corner it only entertains people who already came.</p>',
            '<h3>Set the difficulty for the audience</h3>',
            '<p>A dealership crowd is broad. Driver aids stay on by default so that a first-time driver is not '
            'embarrassed in the middle of your showroom, and go off for anyone who asks.</p>',
            '<h3>Decide what happens with the leaderboard</h3>',
            '<p>A fastest lap prize gives people a reason to come back on day two of a weekend event, and a '
            'natural reason to leave contact details.</p>',
            '<div class="note-band"><p>We supply and brand the simulators we bring. We are not affiliated with and '
            'do not represent any vehicle manufacturer, and we do not provide manufacturer branding.</p></div>',
        ]),
        CROSS,
        faq([
            ('Can it go outside for a weekend event?',
             'Yes, with weather cover and power. Event tents and covered forecourts both work. Send us photos of the '
             'space and we will tell you what is workable.'),
            ('What power do you need?',
             'Mains power at the setup point. Requirements depend on the number of rigs, so confirm it early '
             'if the placement is outdoors.'),
            ('Can the simulator be branded for a model launch?',
             'The rig can be custom wrapped for your campaign. We do not provide manufacturer branding we are not '
             'licensed to use.'),
            ('Is it suitable for children at a family day?',
             'Yes. Driver aids make the cars manageable, and our staff set each driver up. It is one of the more '
             'popular things at dealership family events.'),
            ('Can we keep one in the service area longer term?',
             'Longer placements are possible. Tell us the duration you have in mind and we will quote it.'),
            ('Do you cover dealerships across Florida?',
             'Yes. We are based in Tampa and deliver statewide. Travel and staffing are quoted per event.'),
        ]),
    ]),
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
