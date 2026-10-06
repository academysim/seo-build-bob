# -*- coding: utf-8 -*-
"""Builds batch 2: /for/ hub plus ten audience pages.

These are buyer-type pages. The discipline pages under /simulators/ answer
"what should it be", these answer "is this for me". No invented customers, no
case studies, no partner claims. Partner-dependent content is deliberately
absent until Malik confirms the relationships.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builds_prices as P
from builds_pages import (write, section, prose, faq, linkgrid, figure,
                          build_table, CROSS, ld, LOUNGE)

PAGES = []


def forpage(slug, eyebrow, title, desc, h1, lede, why, considerations, builds, note,
            faqs, img=None, imgalt='', imgcap='', extra_links=()):
    opening = []
    if img:
        opening.append(figure(img, imgalt, imgcap))
    opening.append('    <div class="prose">')
    opening += ['      ' + b for b in why]
    opening.append('    </div>')

    body = [
        section('The Fit', 'Why people like you <span class="accent">buy one.</span>', '',
                '\n'.join(opening)),
        prose('What To Think About', 'The decisions <span class="accent">that matter.</span>', '',
              considerations),
        section('The Lineup', 'Where we would <span class="accent">start you.</span>',
                'Our published builds. Nothing here is a special edition invented for this page.',
                build_table(builds, note)),
        linkgrid('Related', 'Keep <span class="accent">reading.</span>', '', list(extra_links) + [
            ('/simulators/', 'BY DISCIPLINE', 'Spec guidance for the racing you actually do.'),
            ('/for/', 'ALL BUYER TYPES', 'Track drivers, teams, collectors, businesses and venues.'),
        ]),
        CROSS,
        faq(faqs),
    ]
    return dict(
        slug=slug, url='/for/%s/' % slug, ctype='buyer_type',
        title=title, desc=desc,
        crumbs='<a href="/">Builds</a> / <a href="/for/">Who It Is For</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede,
        final_h='Start your <span class="accent">build.</span>',
        final_p='Tell us what you drive, what you want it for and where it goes. We will spec it properly.',
        ld=ld('WebPage', title.split(' | ')[0], desc, '/for/%s/' % slug),
        body='\n\n'.join(body),
    )


SPACE = ('<h3>Space and access</h3><p>The chassis needs a footprint and the room needs a door we can get '
         'it through. Send us the room dimensions and a photo of the access route before you order and we '
         'will confirm it fits rather than discover it on install day.</p>')

POWER = ('<h3>Power</h3><p>A single standard outlet covers most builds. Motion and triple-display setups '
         'draw more, so we confirm requirements against your room as part of the build.</p>')


# ---------------------------------------------------------------- HUB ------
PAGES.append(dict(
    slug='for', url='/for/', ctype='buyer_hub',
    title='Who Buys A Custom Racing Simulator | Academy Sim Racing Builds',
    desc='Racing simulators for track day drivers, race teams, car collectors, luxury garages, dealerships, offices, hotels and clubs. Five real builds from %s.' % P.ENTRY,
    crumbs='<a href="/">Builds</a> / Who It Is For',
    eyebrow='Who It Is For',
    h1='Different buyers,<br><span class="accent">different briefs.</span>',
    lede='A race team and a car collector both buy the same hardware for completely different reasons, and '
         'the right specification follows the reason rather than the budget.',
    final_h='Not sure where <span class="accent">you fit?</span>',
    final_p='Tell us what you want it to do. We will tell you which build makes sense.',
    ld=ld('CollectionPage', 'Who Buys A Custom Racing Simulator',
          'Racing simulator builds for track drivers, race teams, collectors, luxury garages, dealerships, offices, hotels and clubs.',
          '/for/'),
    body='\n\n'.join([
        prose('Start Here', 'The brief comes <span class="accent">before the budget.</span>', '', [
            '<p>People arrive at a simulator from very different directions. Some want to prepare for real '
            'track days. Some want the centerpiece of a collection. Some are buying it for a business and '
            'need it to survive strangers using it all day.</p>',
            '<p>Those are different products in every way except the parts list. A rig that lives in a '
            'showroom needs to be robust and idiot-proof. A rig for a race team needs to match the real car '
            'as closely as possible. A rig in a collection is also furniture.</p>',
            '<p>Find yourself below, or tell us the brief and we will place you.</p>',
        ]),
        linkgrid('Individuals', 'For <span class="accent">drivers.</span>', '', [
            ('/for/track-day-drivers/', 'TRACK DAY DRIVERS',
             'HPDE and club drivers who want to arrive knowing the circuit.'),
            ('/for/race-car-drivers/', 'RACE CAR DRIVERS',
             'Competition drivers using the rig as preparation between events.'),
            ('/for/car-collectors/', 'CAR COLLECTORS',
             'Where the rig is part of the collection, not just equipment.'),
        ]),
        linkgrid('Teams And Spaces', 'For <span class="accent">organizations.</span>', '', [
            ('/for/race-teams/', 'RACE TEAMS',
             'Shared rigs, multiple drivers and preparation between rounds.'),
            ('/for/luxury-garages/', 'LUXURY GARAGES',
             'Simulator rooms integrated into a premium automotive space.'),
            ('/for/garage-condos/', 'GARAGE CONDOS',
             'The fastest-growing request we get, and why the spec is specific.'),
        ]),
        linkgrid('Business', 'For <span class="accent">commercial use.</span>', '', [
            ('/for/car-dealerships/', 'CAR DEALERSHIPS',
             'Showroom and service-area installations that run all day.'),
            ('/for/automotive-businesses/', 'AUTOMOTIVE BUSINESSES',
             'Shops, tuners and performance businesses with a waiting area.'),
            ('/for/offices/', 'OFFICES',
             'Break rooms, client entertainment and recruitment differentiators.'),
            ('/for/hotels-and-clubs/', 'HOTELS AND CLUBS',
             'Amenity installations that have to survive guests.'),
        ]),
        section('The Lineup', 'Five builds, <span class="accent">real specs.</span>',
                'Every recommendation routes into these.',
                build_table(['rookie', 'base', 'club-oled', 'club-triple', 'pole-position'])),
        CROSS,
        faq([
            ('Do commercial installations get a different build?',
             'Not a different product, but usually a different specification. Anything used by the public '
             'gets specced for robustness and simple operation rather than for outright capability.'),
            ('Can you install outside Florida?',
             'Yes. Nationwide shipping with a two to four week build time. Tell us where it is going and we '
             'will confirm what installation looks like.'),
            ('Do you handle installation?',
             'Tell us the site and we will confirm what we can do. Access, power and room layout all affect '
             'the answer, which is why we ask for photos before quoting.'),
            ('Can we try one before committing?',
             'Yes, and for a business purchase we would encourage it. The components are the ones we run '
             'daily in the Tampa lounge.'),
            ('What is the lead time?',
             'Two to four weeks for the build itself. Custom finishes and wraps add to that.'),
            ('Can a build be branded or finished to match a space?',
             'Yes. Livery, wraps and finish options are part of what we do, which matters most for '
             'showroom and collection installations.'),
        ]),
    ]),
))

# ------------------------------------------------------- TRACK DAY --------
PAGES.append(forpage(
    'track-day-drivers', 'Track Day Drivers',
    'Racing Simulator For Track Day And HPDE Drivers | Academy Sim Racing',
    'A racing simulator for HPDE and track day drivers who want circuit familiarity and braking repetition before the event. Five real builds from %s.' % P.ENTRY,
    'For drivers who<br><span class="accent">already go on track.</span>',
    'You are not buying this to play a game. You are buying it so your first paid session is spent driving '
    'rather than working out which way the circuit goes.',
    ['<p>Track time is expensive and finite. The part a simulator genuinely gives back is orientation: the '
     'corner sequence, what follows what, where the road falls away, and which corners matter because they '
     'feed a straight.</p>',
     '<p>The second thing is braking repetition. You can practice a hundred braking events in an evening, '
     'which is more than a full day on track gives you and costs nothing in consumables.</p>',
     '<p>What it does not do is replace seat time, instruction or the feel of your actual car on the day. '
     'We are not going to pretend otherwise.</p>'],
    ['<h3>Spec the pedals first</h3><p>For this use case the brake pedal matters more than the wheelbase. '
     'Braking repetition is the thing you cannot get anywhere else, and it only means something on a '
     'pressure-based pedal.</p>',
     '<h3>Do not overbuy the wheelbase</h3><p>A 15Nm base is plenty for learning circuits and building '
     'consistency. Spend the difference on pedals or a better display.</p>',
     '<h3>Check the circuits you actually run</h3><p>Tell us which tracks matter to you before you buy and '
     'we will confirm they are in the software, rather than you finding out afterwards.</p>',
     SPACE],
    ['rookie', 'base', 'club-oled'],
    'Base is where most track day drivers land. Rookie is a genuine entry point rather than a stripped one.',
    [('Will this make me faster on track?',
      'We are not going to claim that. What it reliably does is remove orientation from your first session '
      'so your paid track time goes on driving.'),
     ('Should I practice braking points at home?',
      'Learn where the corners are, not where to brake. Real references depend on your car, your tires and '
      'the conditions, and your instructor sets them on the day.'),
     ('Which build do most track drivers choose?',
      'Base. It has the 15Nm wheelbase and load cell pedals that matter for this use, without paying for '
      'capability you will not use.'),
     ('Do I need triple screens?',
      'Not for learning circuits. A single 49 inch ultrawide does that job well and takes less room.'),
     ('Can I practice the specific circuit I am running?',
      'If it is in the software, yes. Tell us which circuits matter and we will confirm before you buy.'),
     ('Can I drive one before buying?',
      'Yes. Book a session at the Tampa lounge, where the same components are running daily.')],
    img='lifestyle-driver.jpg', imgalt='Driver seated in an Academy simulator build',
    imgcap='Built for people who already drive on track',
    extra_links=(('/simulators/track-day-racing-simulator/', 'TRACK DAY SPEC',
                  'The configuration detail for this use case.'),),
))

# ------------------------------------------------------ RACE DRIVERS ------
PAGES.append(forpage(
    'race-car-drivers', 'Race Car Drivers',
    'Racing Simulator For Competition Drivers | Academy Sim Racing',
    'A racing simulator for competition drivers preparing between rounds: circuit familiarity, racecraft and repetition. Five real builds from %s.' % P.ENTRY,
    'For drivers who<br><span class="accent">actually race.</span>',
    'If you compete, the value is not learning to drive. It is repetition on a circuit you are about to '
    'race, and racecraft you cannot practice anywhere else without risking a car.',
    ['<p>Competition drivers use a rig differently from enthusiasts. The point is not lap time in the '
     'simulator, it is arriving at a round having already run the circuit two hundred times.</p>',
     '<p>The other genuine value is racecraft: starts, restarts, traffic, defending, and the situations '
     'that decide races. Practicing those in a real car means risking a real car.</p>'],
    ['<h3>Match your real car as closely as you can</h3><p>Seating position, pedal spacing and wheel size '
     'all affect how well the practice transfers. Tell us what you race and we will set it up toward that '
     'rather than to a generic position.</p>',
     '<h3>Active pedals are the upgrade that matters</h3><p>Repeatability across hundreds of braking events '
     'is exactly what they exist for, and it is the closest analogue to what you are training.</p>',
     '<h3>Field of view for racecraft</h3><p>If you are practicing traffic and defending, triples are doing '
     'real work rather than looking impressive.</p>',
     SPACE],
    ['club-oled', 'club-triple', 'pole-position'],
    'Club Triple for most competition drivers. Pole Position where motion is part of the preparation.',
    [('Will simulator practice transfer to the real car?',
      'Circuit familiarity and racecraft transfer well. Braking references, grip levels and the feel of your '
      'actual car do not, and we will not claim otherwise.'),
     ('Can you set it up like my race car?',
      'We will get the seating position, pedal spacing and wheel toward your car as far as the hardware '
      'allows. Tell us what you race when you order.'),
     ('Which software do competition drivers use?',
      'iRacing for organized competition and racecraft, Assetto Corsa Competizione for GT racing. Both run '
      'on every build here.'),
     ('Is motion worth it for a competition driver?',
      'It helps most for catching slides early and reading the car over long stints. If the budget is '
      'finite, pedals first.'),
     ('Can two or three drivers share one rig?',
      'Yes. Seat and pedal positions adjust, which matters if you are sharing with teammates.'),
     ('Do you work with teams rather than individuals?',
      'Yes. See the race teams page for how that changes the specification.')],
    img='lifestyle-coaching.jpg', imgalt='Coaching session on an Academy simulator',
    imgcap='Repetition you cannot buy on track',
    extra_links=(('/for/race-teams/', 'RACE TEAMS', 'When the rig is shared across drivers.'),),
))

# -------------------------------------------------------- RACE TEAMS ------
PAGES.append(forpage(
    'race-teams', 'Race Teams',
    'Racing Simulator For Race Teams | Academy Sim Racing',
    'A shared racing simulator for race teams: multiple drivers, preparation between rounds and durability. Five real builds from %s.' % P.ENTRY,
    'For teams, not<br><span class="accent">just drivers.</span>',
    'A team rig has a different problem from a personal one. Several people use it, positions change '
    'constantly, and it has to still be working the week before a round.',
    ['<p>The brief for a team is preparation capacity. Getting every driver on the circuit before a round, '
     'running through setups and race scenarios, and doing it without the rig becoming a bottleneck.</p>',
     '<p>That changes two things. Adjustability matters more than it does on a personal rig, because the '
     'position is changing several times a week. And durability matters, because the thing is in constant '
     'use rather than occasional use.</p>'],
    ['<h3>Adjustability is the spec item</h3><p>Seat and pedal position will be changed constantly. Tell us '
     'how many drivers and their rough size range and we will set the adjustment range accordingly.</p>',
     '<h3>Consider more than one rig</h3><p>If preparation capacity is the problem, two mid-tier builds '
     'often beat one flagship. Tell us the number of drivers and the time available and we will be honest '
     'about which is the better use of the budget.</p>',
     '<h3>Field of view for race scenarios</h3><p>If you are practicing starts, restarts and traffic, '
     'triples are functional rather than decorative.</p>',
     SPACE],
    ['club-triple', 'pole-position'],
    'Club Triple is the sensible team rig. Two of them will often serve a team better than one Pole '
    'Position, and we would rather say so.',
    [('Should we buy one flagship or two mid-tier rigs?',
      'If the constraint is getting every driver prepared, two rigs usually beat one. If the constraint is '
      'fidelity for a lead driver, one better rig wins. Tell us which problem you have.'),
     ('How adjustable are the builds for different drivers?',
      'Seat and pedal positions adjust. Tell us the size range of your drivers when you order so we set the '
      'range up correctly from the start.'),
     ('Can several drivers keep separate settings?',
      'Software profiles handle wheel and pedal settings per driver. The physical position is a manual '
      'adjustment.'),
     ('Do you offer anything for team preparation beyond hardware?',
      'Coaching is available through the Academy lounge. Tell us what you need and we will tell you what we '
      'can actually do rather than overpromise.'),
     ('What is the lead time for multiple rigs?',
      'Two to four weeks for a build. Multiple units may extend that, so tell us your season calendar.'),
     ('Can we try before committing to several?',
      'Yes, and for a multi-rig purchase we would insist on it.')],
    img='lounge.jpg', imgalt='Multiple Academy simulators installed in the Tampa lounge',
    imgcap='Multiple rigs, in daily use',
))

# ---------------------------------------------------- CAR COLLECTORS ------
PAGES.append(forpage(
    'car-collectors', 'Car Collectors',
    'Racing Simulator For Car Collectors | Academy Sim Racing',
    'A racing simulator as part of a collection: finish, presentation and drivability. Custom livery and wrap options. Builds to %s.' % P.TOP,
    'When the rig is part<br><span class="accent">of the collection.</span>',
    'A simulator in a collection has two jobs. It has to drive properly, and it has to look like it belongs '
    'next to the cars.',
    ['<p>Collectors are the one group who care as much about how the rig looks as how it drives, and that '
     'is a legitimate requirement rather than vanity. A rig that looks like gaming furniture next to a '
     'collection is the wrong object, however well it drives.</p>',
     '<p>It is also the group most likely to want the rig to reference something specific: a car in the '
     'collection, a livery, a period. That is what the finish and wrap options are for.</p>'],
    ['<h3>Finish is a real specification</h3><p>Livery, wrap and finish options let the rig sit alongside '
     'the collection rather than in spite of it. Tell us what it is going next to.</p>',
     '<h3>Do not compromise the driving for the look</h3><p>The temptation is to spec for presentation. We '
     'would rather you had the pedals right and the rig looked good than the reverse.</p>',
     '<h3>Think about who else drives it</h3><p>Collections get shown. If guests will drive it, the setup '
     'should be forgiving by default, which is a software decision we can set up for you.</p>',
     SPACE],
    ['club-oled', 'club-triple', 'pole-position'],
    'Club OLED and Pole Position are the usual collector choices, because the display and the motion '
    'platform both read as serious equipment.',
    [('Can the rig be finished to match a specific car?',
      'Livery, wrap and finish options are part of what we do. Tell us the car or the scheme and we will '
      'tell you what is achievable.'),
     ('Which build looks best in a collection?',
      'Club OLED and Pole Position, usually. Both read as equipment rather than furniture, which is what '
      'collectors are after.'),
     ('Will guests be able to drive it?',
      'Yes, and we can set the software up so that driver aids are on by default, which is what you want if '
      'people are trying it at a party.'),
     ('How much space does it need?',
      'It varies by build, particularly for triples and motion. Send us the room and we will confirm before '
      'you order.'),
     ('Can it be moved later?',
      'Yes, though motion builds are more involved. Tell us if relocation is likely and we will factor it '
      'in.'),
     ('Do you install outside Florida?',
      'We ship nationwide. Tell us the site and we will confirm what installation looks like.')],
    img='livery.jpg', imgalt='Custom livery on an Academy simulator build',
    imgcap='Finished to sit alongside the collection',
    extra_links=(('/for/luxury-garages/', 'LUXURY GARAGES',
                  'When the simulator is part of a wider automotive space.'),),
))

# --------------------------------------------------- LUXURY GARAGES -------
PAGES.append(forpage(
    'luxury-garages', 'Luxury Garages',
    'Racing Simulator For Luxury Garages | Academy Sim Racing',
    'Simulator rooms integrated into premium automotive spaces. Finish, layout and drivability for luxury garages. Builds to %s.' % P.TOP,
    'A simulator room<br><span class="accent">that belongs.</span>',
    'A premium automotive space is designed. A simulator dropped into it without thought looks like it was '
    'dropped into it without thought.',
    ['<p>The difference between a simulator in a luxury garage and one in a spare room is that the space '
     'already has an intent. Lighting, materials and sightlines have all been decided, and the rig either '
     'works with them or fights them.</p>',
     '<p>Practically that means the conversation starts with the room rather than the spec sheet. Where it '
     'sits, what is behind it, how it is lit and what people see when they walk in.</p>'],
    ['<h3>Start with the room, not the build</h3><p>Send photos and dimensions. Where the rig sits changes '
     'the display decision more than the budget does.</p>',
     '<h3>Sightlines and lighting</h3><p>A screen facing a window is a problem. So is a rig positioned so '
     'the first thing a visitor sees is the back of it. These are solvable if raised early.</p>',
     '<h3>Finish to match the space</h3><p>Livery, wrap and finish options exist so the rig reads as part '
     'of the room. Tell us the materials and palette you are working with.</p>',
     SPACE, POWER],
    ['club-oled', 'club-triple', 'pole-position'],
    'Club OLED suits a space where the rig is a focal point. Pole Position where the motion platform is '
    'part of the statement.',
    [('Can you work with our designer or builder?',
      'Yes. The earlier we are in the conversation the better, because power and sightlines are much easier '
      'to solve before the room is finished.'),
     ('How much space does a simulator room need?',
      'It depends on the build and whether it is triples or motion. Send dimensions and we will tell you '
      'what fits properly rather than what technically fits.'),
     ('Can the rig be finished to match the space?',
      'Yes, through livery, wrap and finish options. Tell us the materials and palette.'),
     ('What about power?',
      'A single standard outlet covers most builds. Motion and triple-display setups draw more, so we '
      'confirm requirements against your room.'),
     ('Will guests be able to use it?',
      'Yes. We can set the software up so it is forgiving by default, which is what you want when visitors '
      'try it.'),
     ('Do you install outside Florida?',
      'We ship nationwide. Tell us the site and we will confirm what installation looks like.')],
    img='bespoke.jpg', imgalt='Bespoke finished Academy simulator build',
    imgcap='Specified around the room it lives in',
    extra_links=(('/for/garage-condos/', 'GARAGE CONDOS',
                  'The related brief, with different constraints.'),),
))

# ---------------------------------------------------- GARAGE CONDOS -------
PAGES.append(forpage(
    'garage-condos', 'Garage Condos',
    'Racing Simulator For Garage Condos | Academy Sim Racing',
    'Racing simulators for garage condo owners: space-efficient specification, finish and shared use. Five real builds from %s.' % P.ENTRY,
    'For garage condos<br><span class="accent">and private units.</span>',
    'Garage condos have a specific set of constraints that most simulator buyers do not, and they change '
    'the specification more than the budget does.',
    ['<p>A garage condo is usually a finished, social space where cars are stored and people spend time. '
     'That makes it close to ideal for a simulator, and it comes with constraints worth planning around.</p>',
     '<p>Floor space competes directly with cars, which is the real cost. Climate varies more than in a '
     'house. And the rig will be used by visitors far more often than a home rig, because the whole point '
     'of the space is having people in it.</p>'],
    ['<h3>Footprint competes with a car</h3><p>Every square foot the rig takes is square footage not '
     'holding a vehicle. That is the strongest argument for a single ultrawide over triples in this '
     'setting.</p>',
     '<h3>Plan for visitors driving it</h3><p>The rig will be used by people who have never driven one. Set '
     'up with driver aids on by default so it is welcoming rather than frustrating.</p>',
     '<h3>Climate and dust</h3><p>Garage environments are harder on equipment than living rooms. Tell us '
     'about climate control when you order so we can advise properly.</p>',
     SPACE, POWER],
    ['base', 'club-oled', 'club-triple'],
    'Club OLED is often the right answer here specifically because a single 49 inch panel takes less floor '
    'space than triples.',
    [('How much floor space do I lose?',
      'Less with a single ultrawide than with triples, which is the main reason we often suggest Club OLED '
      'for garage condos. Send us the unit dimensions and we will be specific.'),
     ('Is a garage environment bad for the equipment?',
      'Climate and dust are worth planning around. Tell us about your climate control when you order and we '
      'will advise rather than guess.'),
     ('Will guests be able to drive it?',
      'Yes, and in a garage condo they will. We set it up so driver aids are on by default so first-timers '
      'are not put off.'),
     ('Triples or single screen for a condo unit?',
      'Usually single, purely on floor space. If you race wheel-to-wheel seriously, triples may still be '
      'worth the footprint.'),
     ('Can it be moved between units?',
      'Yes, though motion builds are more involved. Tell us if that is likely.'),
     ('Can the finish match the unit?',
      'Yes, through livery, wrap and finish options.')],
    img='club-oled.jpg', imgalt='Academy Club OLED simulator build',
    imgcap='A single 49 inch panel costs less floor space than triples',
    extra_links=(('/for/luxury-garages/', 'LUXURY GARAGES',
                  'The related brief, in a designed space.'),),
))

# ------------------------------------------------------ DEALERSHIPS -------
PAGES.append(forpage(
    'car-dealerships', 'Car Dealerships',
    'Racing Simulator For Car Dealerships | Academy Sim Racing',
    'Racing simulators for dealership showrooms and service areas: robust specification, simple operation and branding. Five real builds from %s.' % P.ENTRY,
    'For showrooms and<br><span class="accent">service areas.</span>',
    'A dealership rig is commercial equipment. It runs all day, gets used by people who have never seen one, '
    'and nobody on staff has time to reset it between customers.',
    ['<p>A simulator solves two dealership problems. It occupies the people who are not the decision maker, '
     'which is usually what cuts a visit short. And in a service area it changes how a two hour wait '
     'feels.</p>',
     '<p>The specification that suits this is not the one an enthusiast would buy. Robustness and simple '
     'operation matter more than outright capability, because the rig is being used by strangers without '
     'supervision.</p>'],
    ['<h3>Spec for strangers, not for you</h3><p>Driver aids on by default, a forgiving car preloaded, and '
     'a setup that returns to a known state. The rig should be usable without a member of staff standing '
     'next to it.</p>',
     '<h3>Put it where it is seen from outside</h3><p>A simulator visible through the showroom glass works '
     'before anyone walks in. In a back corner it only entertains people who already came.</p>',
     '<h3>Branding</h3><p>Livery and wrap options mean the rig can carry your dealership branding. We do '
     'not supply manufacturer branding we are not licensed to use.</p>',
     SPACE, POWER],
    ['base', 'club-oled', 'club-triple'],
    'Base or Club OLED for most dealership installations. The money is better spent on robustness and '
    'presentation than on the last few Nm.',
    [('Will it survive being used all day?',
      'These are the same components we run daily in a commercial lounge, which is the closest test there '
      'is. Tell us the expected usage and we will spec accordingly.'),
     ('Does someone need to operate it?',
      'It should not. We set it up so it returns to a known state and is usable without supervision, which '
      'is the main difference from a home build.'),
     ('Can it carry our dealership branding?',
      'Yes, through livery and wrap options. We do not supply manufacturer branding we are not licensed to '
      'use.'),
     ('Where should it go in the showroom?',
      'Somewhere visible from outside if possible. It does work drawing people in before they walk through '
      'the door.'),
     ('Can we put one in the service waiting area?',
      'Yes, and it is one of the better uses. It changes how a long wait feels.'),
     ('Do you also do temporary event rentals?',
      'For one-off events, Academy Events rents staffed simulators rather than selling you one. That is '
      'often the better answer for a single weekend.')],
    img='lifestyle-coaching.jpg', imgalt='Academy simulator in commercial use',
    imgcap='Specified for people who have never used one',
))

# -------------------------------------------- AUTOMOTIVE BUSINESSES -------
PAGES.append(forpage(
    'automotive-businesses', 'Automotive Businesses',
    'Racing Simulator For Automotive Businesses | Academy Sim Racing',
    'Racing simulators for performance shops, tuners and automotive businesses with a customer waiting area. Five real builds from %s.' % P.ENTRY,
    'For shops with a<br><span class="accent">waiting room.</span>',
    'If your customers already care about cars, a simulator in the waiting area is the rare amenity that is '
    'actually on brand rather than just being a nicer chair.',
    ['<p>Performance shops, tuners and specialist workshops have an advantage most businesses do not: the '
     'customer sitting in your waiting area is already interested in driving. A simulator is not a random '
     'perk in that context, it is the obvious one.</p>',
     '<p>It also gives your staff something to talk to a customer about that is not the invoice, which is '
     'worth more than it sounds.</p>'],
    ['<h3>Durability over capability</h3><p>This is commercial use. Spec for robustness and simple '
     'operation rather than for the last few Nm of torque.</p>',
     '<h3>Unsupervised operation</h3><p>Nobody on your team has time to reset it. We set it up so it '
     'returns to a known state and is usable without help.</p>',
     '<h3>Branding</h3><p>Livery and wrap options let it carry your shop branding, which turns an amenity '
     'into a marketing surface.</p>',
     SPACE, POWER],
    ['rookie', 'base', 'club-oled'],
    'Rookie and Base cover most waiting-area installations well. The audience is casual and the rig is '
    'better robust than maximal.',
    [('Is a simulator too much for a waiting area?',
      'For a general business, maybe. For a performance shop whose customers are already car people, it is '
      'the most on-brand amenity available.'),
     ('Will customers break it?',
      'These are the components we run daily in a commercial lounge. Tell us the expected usage and we will '
      'spec for it.'),
     ('Does staff have to run it?',
      'No. We set it up so it returns to a known state and works without supervision.'),
     ('Can it carry our branding?',
      'Yes, through livery and wrap options.'),
     ('What is the smallest sensible build for this?',
      'Rookie is a genuine option for a waiting area, and the entry price reflects that.'),
     ('Can we finance or expense it as equipment?',
      'That is a question for your accountant rather than us, but it is bought as equipment like anything '
      'else in the shop.')],
    img='sport.jpg', imgalt='Academy Sport simulator build',
    imgcap='Commercial use, specified for it',
))

# ---------------------------------------------------------- OFFICES -------
PAGES.append(forpage(
    'offices', 'Offices',
    'Racing Simulator For Offices | Academy Sim Racing',
    'Racing simulators for offices: break rooms, client entertainment and recruitment. Robust specification and simple operation. From %s.' % P.ENTRY,
    'For offices that want<br><span class="accent">something better.</span>',
    'The office game room is usually a table nobody uses. A simulator is the rare one that people actually '
    'walk past and stop at, including the people you are trying to hire.',
    ['<p>Offices buy simulators for three reasons: something for staff that is genuinely used, something to '
     'do with a client who has arrived early, and something that makes an impression during recruitment.</p>',
     '<p>All three want the same specification, and it is not the enthusiast one. It has to work for '
     'somebody who has never done it, without anybody explaining it first.</p>'],
    ['<h3>Spec for the person who has never driven one</h3><p>Driver aids on by default, a forgiving car '
     'preloaded, and a setup that returns to a known state after every use.</p>',
     '<h3>Think about noise</h3><p>An open-plan office and engine audio are a bad combination. Headphones '
     'are usually the answer and we will set it up that way if you ask.</p>',
     '<h3>Somewhere it can be seen</h3><p>Half the value is that visitors notice it. A rig in a closed room '
     'does less work than one people walk past.</p>',
     SPACE, POWER],
    ['rookie', 'base', 'club-oled'],
    'Rookie or Base covers most office installations. Club OLED where it is also meant to impress '
    'visitors.',
    [('Will people actually use it?',
      'More than a pool table, in our experience of what gets asked for. It helps that it is genuinely hard '
      'and there is a lap time to beat.'),
     ('Is it too loud for an open-plan office?',
      'It can be. Headphones solve it and we will set the rig up that way if you tell us the environment.'),
     ('Does anyone need to manage it?',
      'No. We set it up to return to a known state so it works without supervision.'),
     ('Can we run an internal leaderboard?',
      'Yes. A persistent leaderboard is the single thing that makes an office rig get used repeatedly '
      'rather than once.'),
     ('Which build for an office?',
      'Rookie or Base for staff use. Club OLED if visitors and recruitment are part of the reason.'),
     ('Can we brand it?',
      'Yes, through livery and wrap options.')],
    img='base.jpg', imgalt='Academy Base simulator build',
    imgcap='Specified for people who have never driven one',
))

# ------------------------------------------------- HOTELS AND CLUBS -------
PAGES.append(forpage(
    'hotels-and-clubs', 'Hotels And Clubs',
    'Racing Simulator For Hotels And Private Clubs | Academy Sim Racing',
    'Racing simulators as a hotel or private club amenity: robust specification, unsupervised operation and presentation. From %s.' % P.ENTRY,
    'An amenity that has<br><span class="accent">to survive guests.</span>',
    'A hospitality installation is the hardest brief we get. It runs constantly, it is used entirely by '
    'people who have never seen one, and nobody is standing next to it.',
    ['<p>Hotels and private clubs buy simulators as a differentiating amenity, and the differentiator only '
     'works if the thing is running. A rig that needs resetting or explaining fails within a week of '
     'opening.</p>',
     '<p>So the entire specification bends toward robustness and unattended operation. Outright capability '
     'is the least important thing on the list, which is the opposite of every enthusiast build.</p>'],
    ['<h3>Unattended operation is the whole brief</h3><p>Driver aids on, a forgiving car loaded, and a '
     'setup that returns to a known state after every guest. If it needs a member of staff, it will not get '
     'used.</p>',
     '<h3>Robustness over capability</h3><p>Guests are not careful. Spend on durability rather than on the '
     'top wheelbase.</p>',
     '<h3>Presentation matters here</h3><p>In a hospitality space the rig is part of the room. Finish and '
     'placement are as much of the decision as the spec.</p>',
     '<h3>Think about supervision and age</h3><p>Decide in advance whether children can use it unsupervised '
     'and how that is communicated. That is your policy rather than ours, but it is worth settling before '
     'installation.</p>',
     SPACE, POWER],
    ['base', 'club-oled'],
    'Base or Club OLED for hospitality. We would actively steer away from the flagship here, because the '
    'money is better spent on robustness and finish.',
    [('Will it survive unsupervised guest use?',
      'That is the main thing we spec for in a hospitality build. Tell us the setting and expected usage '
      'and we will be honest about what holds up.'),
     ('Does staff need to operate it?',
      'It should not. We set it up so it returns to a known state after each guest.'),
     ('Which build suits a hotel or club?',
      'Base or Club OLED. We would steer away from the flagship, because durability and finish matter more '
      'than the top wheelbase here.'),
     ('Can children use it?',
      'Physically most can, with driver aids on. Whether they may use it unsupervised is your policy, and '
      'worth deciding before installation.'),
     ('Can it be finished to match our space?',
      'Yes, through livery, wrap and finish options.'),
     ('What about noise in a shared space?',
      'Headphones are usually the answer in hospitality settings. Tell us the environment and we will set '
      'it up accordingly.')],
    img='lounge.jpg', imgalt='Academy simulators installed in a commercial space',
    imgcap='Built to run without supervision',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
