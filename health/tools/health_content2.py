# -*- coding: utf-8 -*-
"""Health: /locations/ hub + 5 Florida service areas.

These target activity directors at senior communities. The Events property has
location pages for Tampa, Orlando and Sarasota aimed at corporate event
planners. Titles and copy here are explicitly senior-community focused so the
two do not compete for the same query.

No invented communities, no named facilities, no partnerships, and no claim of
any existing installation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from health_pages import (write, sec, prose, cards, faq, linkgrid,
                          SCOPE, ACCESS, CROSS, ld)

PAGES = []

NOT_A_BRANCH = (
    '  <div class="disclaimer"><p>Academy Sim Racing is based at 1421 Massaro Blvd in Tampa. We do not '
    'operate an office or facility in %s, and we have no affiliation with any community named or unnamed '
    'in that area. We travel there to run programs, and travel is quoted per booking.</p></div>')


def area(slug, city, title, desc, h1, lede, context, mix, notes, faqs, ldname):
    return dict(
        slug=slug, url='/locations/%s/' % slug, ctype='health_location',
        title=title, desc=desc,
        crumbs='<a href="/">Home</a> / <a href="/locations/">Service Areas</a> / ' + city,
        eyebrow='Serving ' + city,
        h1=h1, lede=lede,
        cta1='Plan a Program',
        final_h='BRING IT TO<br><span class="amber">%s.</span>' % city.upper(),
        final_p='Tell us the community, roughly how many residents and the kind of program you have in '
                'mind. We will come back with formats and costs.',
        ld=ld('Service', ldname, desc, '/locations/%s/' % slug),
        body='\n\n'.join([
            prose('Local Context', 'SENIOR COMMUNITIES IN %s' % city.upper(), '', context),
            SCOPE,
            cards('What We Run', 'PROGRAMS THAT SUIT THE AREA', '', mix),
            prose('Accessibility', 'WHO CAN TAKE PART', '', ACCESS),
            prose('Practical', 'WHAT TO KNOW LOCALLY', '', notes + [NOT_A_BRANCH % city]),
            linkgrid('Related', 'PROGRAMS AND OTHER AREAS', '', [
                ('/programs/', 'ALL PROGRAMS', 'The five program formats in detail.'),
                ('/locations/', 'OTHER SERVICE AREAS', 'Where else in Florida we travel.'),
            ]),
            CROSS,
            faq(faqs),
        ]),
    )


# ---------------------------------------------------------------- HUB ----
PAGES.append(dict(
    slug='locations', url='/locations/', ctype='health_location_hub',
    title='Senior Community Simulator Programs Across Florida | Academy',
    desc='Racing simulator programs delivered to senior living, 55+ and retirement communities across Florida from our Tampa base. Staffed, seated and accessible.',
    crumbs='<a href="/">Home</a> / Service Areas',
    eyebrow='Florida Service Areas',
    h1='SENIOR COMMUNITY PROGRAMS<br>ACROSS FLORIDA',
    lede='We are based in Tampa and travel across Florida to run simulator programs in senior living, 55+ '
         'and retirement communities. We bring everything, run the session and take it away again.',
    cta1='Plan a Program',
    final_h='WHERE IS YOUR<br><span class="amber">COMMUNITY?</span>',
    final_p='Tell us the community and roughly how many residents. We will confirm what a visit involves.',
    ld=ld('Service', 'Senior Community Simulator Programs Across Florida',
          'Racing simulator programs for senior living, 55+ and retirement communities across Florida.',
          '/locations/'),
    body='\n\n'.join([
        prose('How It Works', 'ONE BASE, THE WHOLE STATE', '', [
            '<p>Everything we bring to a community leaves from our Tampa facility with our own staff and '
            'goes back the same way. There is no branch network and we are not going to imply one.</p>',
            '<p>Practically that means two things. Travel is quoted per booking rather than built into a '
            'list price, and communities further from Tampa often find a longer single visit works better '
            'than several short ones.</p>',
            '<h3>Whatever the distance, the visit is the same</h3>',
            '<ul>'
            '<li>We arrive ahead of the session and set up in a room you already use</li>'
            '<li>Our staff run the simulators and stay for the whole session</li>'
            '<li>Settings are adjusted per resident rather than set once</li>'
            '<li>We pack down and the room goes back to normal</li>'
            '</ul>',
        ]),
        SCOPE,
        linkgrid('Service Areas', 'WHERE WE TRAVEL MOST', 'Five areas with a dedicated page. We can serve '
                 'anywhere in Florida.', [
                     ('/locations/tampa/', 'TAMPA', 'Our home market, and the shortest travel.'),
                     ('/locations/st-petersburg/', 'ST. PETERSBURG', 'Dense and compact, across the bay.'),
                     ('/locations/clearwater/', 'CLEARWATER', 'Coastal Pinellas and the surrounding area.'),
                     ('/locations/sarasota/', 'SARASOTA', 'A large concentration of retirement communities.'),
                     ('/locations/orlando/', 'ORLANDO', 'Central Florida and the surrounding 55+ growth.'),
                 ]),
        prose('Elsewhere', 'THE REST OF FLORIDA', '', [
            '<p>We take bookings across the state, including Bradenton, Venice, Naples, Fort Myers, Ocala, '
            'The Villages area, Jacksonville and the east coast. Those do not have their own pages, which '
            'is deliberate. We would rather write something genuinely specific than publish the same page '
            'with the city name changed.</p>',
            '<p>If your community is not listed, ask. The answer is usually yes.</p>',
            '<div class="disclaimer"><p>Academy Sim Racing operates from 1421 Massaro Blvd, Tampa, FL '
            '33619. We do not have offices or facilities anywhere else in Florida, and we have no '
            'affiliation with any senior community, operator or facility.</p></div>',
        ]),
        CROSS,
        faq([
            ('Do you have locations outside Tampa?',
             'No. We have one facility, in Tampa. Everywhere else in Florida is served by travelling to '
             'the community with our own staff and equipment.'),
            ('How far will you travel?',
             'Across Florida. Travel is quoted per booking based on distance and the length of the visit.'),
            ('Is staff provided?',
             'Yes. Our team sets up, runs the session and packs down. Your staff handle anything involving '
             'residents personally.'),
            ('Can you serve several communities in one group?',
             'Yes. Operators with multiple communities in a region often rotate visits, which is usually '
             'more efficient than booking each separately.'),
            ('How much space do we need?',
             'An activity room, dining room or common area is normally enough. We need floor space, mains '
             'power and a route in from a vehicle.'),
            ('How does pricing work?',
             'It depends on the number of simulators, the length of the visit, travel and whether it is a '
             'one-off or recurring. We quote per program.'),
        ]),
    ]),
))

PAGES.append(area(
    'tampa', 'Tampa',
    'Senior Community Simulator Programs in Tampa | Academy',
    'Racing simulator programs for senior living, 55+ and retirement communities in Tampa. Our home market, with the shortest travel and the most flexible scheduling.',
    'SIMULATOR PROGRAMS FOR<br>TAMPA SENIOR COMMUNITIES',
    'Tampa is where we are based, which makes it the easiest market for us to serve and the most flexible '
    'to schedule.',
    ['<p>Everything Academy owns is in Tampa, at 1421 Massaro Blvd. For communities in the immediate area '
     'that has practical consequences: shorter lead times are workable, a late change is easier to absorb, '
     'and if something needs swapping we are not hours away from a spare.</p>',
     '<p>It also makes short and recurring visits viable in a way they are not further afield, because the '
     'travel component of a booking is minimal.</p>'],
    [('Recurring calendar slot', 'The most practical arrangement in Tampa, because short travel makes a '
      'regular visit economic rather than a stretch.'),
     ('Short-notice bookings', 'Easier here than anywhere else, since nothing has to travel far.'),
     ('Larger multi-day events', 'For bigger communities wanting more residents to get a turn.'),
     ('Visits to our lounge', 'For mobile residents, a trip to the Tampa lounge is an alternative to us '
      'coming to you.')],
    ['<h3>Short travel changes what is affordable</h3>'
     '<p>A monthly recurring slot is genuinely practical for a Tampa community in a way it may not be for '
     'one three hours away. If you want this as regular programming, being local helps.</p>',
     '<h3>An outing is an option here</h3>'
     '<p>For communities with mobile residents and transport, a visit to our lounge is a change of scene '
     'rather than another activity in the same room. That is only realistic close to Tampa.</p>'],
    [('How quickly can you come out in Tampa?',
      'More quickly than anywhere else, because nothing has to travel far. Ask and we will tell you '
      'honestly whether a date works.'),
     ('Can our residents visit you instead?',
      'For mobile residents with transport, yes. Our lounge is at 1421 Massaro Blvd and a visit is a change '
      'of scene rather than another session in the activity room.'),
     ('Is a recurring monthly visit practical?',
      'In Tampa, very. Short travel is what makes regular programming economic.'),
     ('Do you cover the wider Tampa area?',
      'Yes, including Brandon, Riverview, Valrico, Wesley Chapel and Carrollwood.'),
     ('Is staff provided?',
      'Yes. Our team runs the session throughout. Your staff handle anything involving residents '
      'personally.'),
     ('Do you have a program running in Tampa communities now?',
      'We are not going to name communities or imply relationships we have not been given permission to '
      'describe. Contact us and we will tell you what we can do for yours.')],
    'Senior Community Simulator Programs In Tampa, Florida',
))

PAGES.append(area(
    'st-petersburg', 'St. Petersburg',
    'Senior Community Simulator Programs in St. Petersburg | Academy',
    'Racing simulator programs for senior living and retirement communities in St. Petersburg. Delivered and staffed from our Tampa base.',
    'SIMULATOR PROGRAMS FOR<br>ST. PETERSBURG COMMUNITIES',
    'St. Petersburg is dense, compact and has a long-established older population, which makes it one of '
    'the more practical areas in Florida to run recurring programming.',
    ['<p>Pinellas County is one of the most densely populated counties in Florida and St. Petersburg has a '
     'long history as a retirement destination. For a service that travels, density is the thing that '
     'matters: communities are close together, so a single trip can reasonably serve more than one.</p>',
     '<p>The other practical factor is bridge traffic. Travel from Tampa is short in distance and variable '
     'in time, which affects scheduling more than it affects cost.</p>'],
    [('Recurring visits', 'Practical here because the area is compact and travel is short.'),
     ('Multiple communities in a day', 'Density makes serving two communities in one trip realistic, which '
      'suits operators with several properties.'),
     ('Race nights', 'A defined evening event, which tends to draw better attendance than open sessions.'),
     ('Family and open house events', 'For communities marketing to prospective residents and their adult '
      'children.')],
    ['<h3>Density works in your favor</h3>'
     '<p>If you operate more than one community in the area, tell us. Serving two in a single trip is '
     'usually better value than two separate bookings.</p>',
     '<h3>Scheduling around the bridges</h3>'
     '<p>Travel from Tampa is short but the timing varies. We would rather build a little slack into an '
     'arrival time than turn up late to an activity room full of waiting residents.</p>'],
    [('Do you travel to St. Petersburg regularly?',
      'It is a short trip from our Tampa base and one of the more practical areas for recurring '
      'programming.'),
     ('Can you serve two of our communities in one visit?',
      'Often yes, given how close together they are. Tell us the properties and we will look at it.'),
     ('How is this priced compared to Tampa?',
      'Travel is quoted per booking. St. Petersburg is close enough that the difference is small.'),
     ('Do you cover the rest of Pinellas?',
      'Yes, including Clearwater, Largo, Pinellas Park and the beach communities.'),
     ('What space do we need?',
      'An activity room, dining room or common area with mains power and a route in from a vehicle.'),
     ('Can residents in wheelchairs take part?',
      'Tell us in advance and we will talk it through properly. Some setups work without transferring out '
      'of a chair and some do not.')],
    'Senior Community Simulator Programs In St. Petersburg, Florida',
))

PAGES.append(area(
    'clearwater', 'Clearwater',
    'Senior Community Simulator Programs in Clearwater | Academy',
    'Racing simulator programs for senior living and retirement communities in Clearwater and coastal Pinellas. Delivered and staffed from Tampa.',
    'SIMULATOR PROGRAMS FOR<br>CLEARWATER COMMUNITIES',
    'Clearwater and the coastal Pinellas communities sit slightly further out than St. Petersburg, which '
    'changes the scheduling more than it changes anything else.',
    ['<p>Coastal Pinellas has a substantial concentration of senior living and 55+ communities, many of '
     'them long established. What differs from St. Petersburg is the geography: communities are spread '
     'along the coast rather than concentrated, so a trip serves a narrower area.</p>',
     '<p>That points toward longer single visits rather than short frequent ones. If we are making the '
     'trip, it is usually better for everyone if more residents get a turn while we are there.</p>'],
    [('Longer single visits', 'Better value than short frequent ones given the travel, and more residents '
      'get a turn.'),
     ('Half or full day', 'Suits larger communities where an afternoon would not reach everyone.'),
     ('Seasonal blocks', 'A defined run of visits, which suits communities whose population changes '
      'through the year.'),
     ('Open house and family events', 'For communities marketing to prospective residents.')],
    ['<h3>Fewer, longer visits usually work better</h3>'
     '<p>Given the travel, a half or full day reaches more residents per trip than an hour or two. If you '
     'want recurring programming, a longer session less often is usually the better structure.</p>',
     '<h3>Tell us about seasonal population</h3>'
     '<p>If your community&rsquo;s numbers change through the year, that affects when a visit is worth '
     'making. It is worth mentioning when you get in touch.</p>'],
    [('Do you travel to Clearwater?',
      'Yes, from our Tampa base. It is a straightforward trip and one we make for coastal Pinellas '
      'communities.'),
     ('Is a recurring program practical here?',
      'Yes, though we would usually suggest fewer and longer visits rather than short frequent ones, '
      'given the travel.'),
     ('Do you cover Dunedin, Palm Harbor and Safety Harbor?',
      'Yes, and the surrounding coastal communities.'),
     ('How many residents can take part in a day?',
      'It depends on numbers of simulators and how long each resident wants. Tell us your resident count '
      'and we will size it.'),
     ('Is staff provided?',
      'Yes. Our team runs the whole session. Your staff handle anything involving residents personally.'),
     ('How does travel affect the cost?',
      'Travel is quoted per booking. A longer single visit spreads that across more residents.')],
    'Senior Community Simulator Programs In Clearwater, Florida',
))

PAGES.append(area(
    'sarasota', 'Sarasota',
    'Senior Community Simulator Programs in Sarasota | Academy',
    'Racing simulator programs for senior living, 55+ and retirement communities in Sarasota. Delivered and staffed from our Tampa base.',
    'SIMULATOR PROGRAMS FOR<br>SARASOTA COMMUNITIES',
    'Sarasota has one of the highest concentrations of retirement and 55+ communities in Florida, and an '
    'audience that expects programming to be good rather than merely available.',
    ['<p>Sarasota and the surrounding area have a large, long-established older population and a '
     'correspondingly large number of communities competing for residents. Activity programming is part of '
     'how those communities differentiate, which raises the bar on what counts as interesting.</p>',
     '<p>It is also a market with a pronounced seasonal pattern, which affects when programming lands best '
     'and when a community is at full occupancy.</p>'],
    [('Competitive race nights', 'Active adult communities here tend to want real competition rather than '
      'a gentle activity.'),
     ('Marketing and open house events', 'In a competitive market, something genuinely different is worth '
      'more than another wine and cheese evening.'),
     ('Recurring seasonal programming', 'Aligned to when the community is at fuller occupancy.'),
     ('Operator-wide rotations', 'For groups running several communities in the area.')],
    ['<h3>The bar is higher here</h3>'
     '<p>With this many communities competing, residents and prospective residents have seen a lot of '
     'programming. That works in favor of something genuinely unusual, which this is.</p>',
     '<h3>Plan around the season</h3>'
     '<p>Occupancy and attendance change through the year in this market more than in most. Tell us your '
     'pattern and we will suggest when a visit will land best.</p>',
     '<h3>Several communities, one trip</h3>'
     '<p>If you operate more than one property in the area, serving them in a single trip is usually '
     'better value.</p>'],
    [('Do you travel to Sarasota?',
      'Yes, from our Tampa base. It is a straightforward trip and Sarasota is one of the areas we are '
      'asked about most.'),
     ('Do you cover Bradenton, Venice and Lakewood Ranch?',
      'Yes, and the surrounding communities.'),
     ('What suits an active adult community here?',
      'Usually a competitive format with a leaderboard. This audience tends to want a real contest rather '
      'than a gentle activity.'),
     ('Can this work as a marketing event?',
      'Yes, and in a market this competitive it differentiates well. It also photographs well for '
      'materials.'),
     ('Can you serve several of our properties?',
      'Yes. Tell us the properties and we will look at a rotation, which is usually better value than '
      'separate bookings.'),
     ('When is the best time of year?',
      'That depends on your occupancy pattern. Tell us yours and we will suggest timing.')],
    'Senior Community Simulator Programs In Sarasota, Florida',
))

PAGES.append(area(
    'orlando', 'Orlando',
    'Senior Community Simulator Programs in Orlando | Academy',
    'Racing simulator programs for senior living, 55+ and retirement communities in Orlando and Central Florida. Delivered and staffed from Tampa.',
    'SIMULATOR PROGRAMS FOR<br>ORLANDO COMMUNITIES',
    'Central Florida has seen substantial 55+ community growth, and newer communities tend to want '
    'programming that matches how they market themselves.',
    ['<p>The Orlando area and Central Florida more broadly have a lot of newer active adult development. '
     'Newer communities are generally marketing to a younger, more active resident than a long-established '
     'senior living community is, and their programming reflects that.</p>',
     '<p>For us the practical difference is distance. Orlando is a longer trip than anywhere else on this '
     'list, which points firmly toward fewer, longer visits.</p>'],
    [('Full day visits', 'The sensible structure given the travel. More residents get a turn per trip.'),
     ('Competitive formats', 'Newer active adult communities generally want a real contest.'),
     ('Amenity and clubhouse events', 'Simulators as the draw at an amenity showcase or open house.'),
     ('Multi-community rotations', 'For operators with several Central Florida properties.')],
    ['<h3>Fewer, longer visits</h3>'
     '<p>Given the distance from Tampa, a full day reaches far more residents per trip than a short '
     'session. If you want recurring programming, that is the structure we would suggest.</p>',
     '<h3>Group your properties if you can</h3>'
     '<p>If you run several communities in Central Florida, a rotation across a couple of days is much '
     'better value than separate trips.</p>',
     '<h3>Newer communities, different expectations</h3>'
     '<p>Active adult residents in newer developments generally want competition rather than a gentle '
     'activity. Tell us which you have and we will pitch the session accordingly.</p>'],
    [('Do you travel to Orlando?',
      'Yes, from our Tampa base. It is the longest trip of the areas we have pages for, which affects how '
      'we would structure a visit rather than whether we come.'),
     ('Is a recurring program practical at that distance?',
      'Yes, though we would suggest fewer and longer visits. A full day reaches many more residents per '
      'trip than a short session.'),
     ('Do you cover Kissimmee, Winter Park and the surrounding area?',
      'Yes, and Central Florida more broadly.'),
     ('Can you serve several of our communities in one trip?',
      'Yes, and at this distance we would encourage it. A rotation across a couple of days is far better '
      'value.'),
     ('How does travel affect pricing?',
      'Travel is quoted per booking. Longer visits and grouped properties both spread it across more '
      'residents.'),
     ('What suits a newer active adult community?',
      'Usually a competitive format with a leaderboard rather than an open activity session.')],
    'Senior Community Simulator Programs In Orlando And Central Florida',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
