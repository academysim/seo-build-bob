# -*- coding: utf-8 -*-
"""Codex review fixes for the events pages.

The critical one is mine and embarrassing: a shared "we have no branch here"
note was templated onto every city page including Tampa, where it produced
"Academy Sim Racing is based in Tampa at 1421 Massaro Blvd. We do not have an
office, showroom or branch in Tampa."

NOT fixed here, because they are on Malik's pre-existing homepage which cannot
be safely redeployed without the source: the client/partner claims ("partner
with us", "Fortune 500 boardrooms", NDA clients) and the capacity figures
("15-30 racers per hour per simulator", "10' x 10' footprint"). Raised with him.
"""
import io, os, sys

D = sys.argv[1]


def edit(rel, pairs, must=True):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-42s MISSING' % rel)
        return
    s = io.open(p, encoding='utf-8', newline='').read()
    n = 0
    for o, x in pairs:
        c = s.count(o)
        if c == 0:
            continue
        s = s.replace(o, x)
        n += c
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-42s %d replacements' % (rel, n))


CITIES = ['locations/tampa/index.html', 'locations/orlando/index.html',
          'locations/daytona-beach/index.html', 'locations/sarasota/index.html']
ALL = []
for root, _, files in os.walk(D):
    for f in files:
        if f == 'index.html':
            ALL.append(os.path.relpath(os.path.join(root, f), D).replace(os.sep, '/'))
ALL.sort()

# ---- 1 CRITICAL: Tampa is our home. The no-branch note is nonsense there ----
edit('locations/tampa/index.html', [
    ('Academy Sim Racing is based in Tampa at 1421 Massaro Blvd. We do not have '
     'an office, showroom or branch in Tampa. We deliver mobile simulator events there from our Tampa base, '
     'and travel and staffing are quoted per event.',
     'Academy Sim Racing is based in Tampa at 1421 Massaro Blvd. This is the one market where we are '
     'physically located, which is why coming to us is an option here and nowhere else. Everywhere else '
     'in Florida is served by mobile delivery from this address.'),
])

# ---- 2 Tampa page must hand off to the Lounge, not sell it ------------------
edit('locations/tampa/index.html', [
    ('<p>It also means Tampa is the only city where you can skip the delivery entirely. Our lounge at 1421 '
     'Massaro Blvd has eight simulators permanently installed, and for groups up to a certain size a full '
     'lounge buyout is simpler and cheaper than a mobile setup. For anything larger, or anything that needs '
     'to happen at your venue, we deliver.</p>',
     '<p>It also means Tampa is the only city where you can skip the delivery entirely. Academy has a '
     'simulator lounge at the same address, which for some groups is an alternative to a mobile setup. '
     'That is a separate service with its own booking, covered on the '
     '<a href="https://lounge.academysim.com">Academy Lounge site</a>. Everything on this page is about '
     'us bringing simulators to your venue.</p>'),
    ('<li><strong>Come to us</strong> if the group fits, the date is flexible, and you do not need the event '
     'tied to a specific venue. It is the least logistics and the lowest cost.</li>',
     '<li><strong>The lounge</strong> may suit smaller groups with a flexible date and no fixed venue. '
     'See the Academy Lounge site for that.</li>'),
    ('<li><strong>We come to you</strong> if the event is part of something bigger, the venue is fixed, you '
     'need branding, or the guest count is beyond what one room holds.</li>',
     '<li><strong>A mobile event</strong> is what you want if the event is part of something bigger, the '
     'venue is fixed, you need the rigs branded, or the guest count is beyond what one room holds. That is '
     'what we quote for here.</li>'),
    ('<h3>The lounge as a fallback</h3>'
     '<p>If a venue turns out not to work, or plans change late, having a fixed venue with eight rigs a short '
     'drive away is a genuine safety net that we do not have in any other city.</p>',
     '<h3>A fallback venue exists here</h3>'
     '<p>If your venue turns out not to work, or plans change late, Tampa is the one market where there is '
     'an Academy venue nearby as an alternative. That is not something we can offer anywhere else.</p>'),
    ('Can our group come to you instead?',
     'Is there an Academy venue in Tampa?'),
    ('Yes. Our lounge at 1421 Massaro Blvd has eight simulators and can be booked out entirely for a group. For '
     'smaller groups that is usually simpler and cheaper than a mobile setup.',
     'Yes. Academy has a simulator lounge at the same Tampa address, which is a separate service with its own '
     'booking. For some groups it is an alternative to a mobile event. Details are on the Academy Lounge site.'),
    ('<div class="lc-desc">Eight simulators at 1421 Massaro Blvd. Book an hour, bring a group, '
     'or take the whole room.</div>',
     '<div class="lc-desc">Academy&rsquo;s simulator venue in Tampa, booked separately from event rentals.</div>'),
    ("'The only city where coming to us is also an option.'",
     "'Our home market, and the only one with an Academy venue nearby.'"),
])

# ---- 4 manufactured operating history -> conditional planning language ------
edit('locations/orlando/index.html', [
    ('<p>Almost everything we are asked to do in Orlando sits in one of two buckets: a trade show or convention '
     'stand, or a corporate group staying at a hotel or resort.',
     '<p>Orlando event work tends to fall into one of two buckets: a trade show or convention stand, or a '
     'corporate group staying at a hotel or resort.'),
    ('Yes, and it is most of what we do in Orlando. Send us the venue and the exhibitor or event kit and we '
     'will confirm what fits and what the venue requires.',
     'Yes. Send us the venue and the exhibitor or event kit and we will confirm what fits and what the venue '
     'requires.'),
])

edit('locations/daytona-beach/index.html', [
    ('Yes, and we do. Race weeks need more lead time and more slack in the schedule because access and traffic '
     'change across the area, so book as early as you can.',
     'Yes. Race weeks need more lead time and more slack in the schedule, because access and traffic change '
     'across the area, so book as early as you can.'),
    ('<p>At a corporate event in most cities, a racing simulator is a novelty and the job is to make it '
     'approachable. In Daytona, particularly around a race weekend, a meaningful share of the room follows '
     'motorsport properly.',
     '<p>At a corporate event in most cities, a racing simulator is a novelty and the job is to make it '
     'approachable. In Daytona, particularly around a race weekend, you should expect a meaningful share of '
     'the room to follow motorsport properly.'),
    # 9 lap comparison
    ('<li><strong>Run the right circuit.</strong> Guests who have just watched a session have a direct '
     'reference, and comparing their lap to the real one is the conversation.</li>',
     '<li><strong>Run the right circuit.</strong> Guests who have just watched a session recognize every '
     'corner, which is what makes the activation land. Simulator times are not comparable with real ones, '
     'and it is worth saying so rather than inviting the comparison.</li>'),
])

edit('locations/sarasota/index.html', [
    ('<p>The events we are asked to do in Sarasota look different from the ones an hour north. There is less '
     'convention and trade show work and considerably more private hire: club functions, fundraisers, '
     'corporate retreats and events at private homes.</p>',
     '<p>Sarasota has far less convention and trade show infrastructure than Tampa or Orlando, so the events '
     'that make sense here tend to be private rather than public: club functions, fundraisers, corporate '
     'retreats and events at private homes and smaller venues.</p>'),
    ('<p>That changes the setup. Smaller venues mean access matters more than floor space, guest counts are '
     'lower so throughput is rarely the constraint, and the format usually wants to be sociable rather than '
     'competitive.',
     '<p>That changes the setup. At smaller venues access matters more than floor space, and where guest '
     'counts are lower the format usually wants to be sociable rather than competitive.'),
    ('<p>Southwest Florida is busier in the winter months, and the private and club events we get asked about '
     'cluster accordingly. If your date falls in season, treat lead time the way you would for a holiday '
     'party rather than a quiet Tuesday.</p>',
     '<p>Southwest Florida is busier in the winter months, and private and club calendars fill accordingly. '
     'If your date falls in season, treat lead time the way you would for a holiday party rather than a quiet '
     'Tuesday.</p>'),
    ('<p>For most Sarasota bookings we would suggest open racing rather than a structured competition, so guests '
     'drift between the rigs and the rest of the event rather than queueing for a scheduled slot.</p>',
     '<p>For a private or club event we would usually suggest open racing rather than a structured competition, '
     'so guests drift between the rigs and the rest of the event rather than queueing for a scheduled slot.</p>'),
])

# ---- 5 my own unqualified performance claims -------------------------------
for rel in ALL:
    edit(rel, [
        ('Each driver is seated, set up and briefed. First-timers are driving properly in under a minute.',
         'Each driver is seated, set up and briefed before they start, so first-time drivers are not left to '
         'work it out in front of an audience.'),
        ('Most guests are driving competently within a lap or two, which is the point.',
         'Guests are set up and briefed before they start, so first-timers are not left to work it out alone.'),
        ('people are usually lapping competently within a lap or two',
         'most people settle in quickly'),
        ('Yes. That is the main reason we recommend GT3. Driver aids are on by default and our staff set each '
         'person up, so people are lapping properly very quickly.',
         'Yes. That is the main reason we recommend GT3. Driver aids are on by default and our staff set each '
         'person up, so guests are not left struggling.'),
        # 10 contractual absolutes
        ('Delivery, setup, calibration, staffing for the duration and teardown are part of every booking.',
         'Delivery, setup, calibration, staffing and teardown are included as standard, and your quote sets '
         'out exactly what is covered for your event.'),
        ('Delivery, setup, staffing for the duration and teardown are part of every booking.',
         'Delivery, setup, staffing and teardown are included as standard, and your quote confirms the detail.'),
        ('Delivery, setup, staffing for the duration and teardown are included in every booking.',
         'Delivery, setup, staffing and teardown are included as standard, and your quote confirms the detail.'),
        ('Yes. Staffing for the duration is part of every booking. Our team sets drivers up, resets sessions '
         'and keeps the queue moving.',
         'Yes. Staffing is included as standard. Our team sets drivers up, resets sessions and keeps the queue '
         'moving, and your quote confirms the hours covered.'),
        ('Every booking includes delivery, setup, staffing for the duration and teardown.',
         'Bookings include delivery, setup, staffing and teardown as standard, with the detail confirmed in '
         'your quote.'),
    ])

# ---- 6 broadcast rights ----------------------------------------------------
edit('event-types/watch-parties/index.html', [
    ('We supply simulators and staff. We do not supply the broadcast, and we are '
     'not affiliated with any racing series or broadcaster. Screening rights for a public event are the '
     'venue&rsquo;s responsibility.',
     'We supply simulators and staff. We do not supply the broadcast, and we are not affiliated with any '
     'racing series or broadcaster. Confirming and obtaining any screening or broadcast rights required for '
     'your event is the responsibility of the host and the venue, not Academy.'),
    ('No. We supply the simulators, the staff and the leaderboard. The broadcast and any screening rights '
     'are the venue or host&rsquo;s responsibility.',
     'No. We supply the simulators, the staff and the leaderboard. Arranging the broadcast and confirming any '
     'screening rights it requires is down to you and your venue.'),
])

# ---- 7 the queue line ------------------------------------------------------
edit('event-types/index.html', [
    ('If you want the longest queue on the trade show floor, you run short sessions with a live '
     'leaderboard and a staff member calling times.',
     'If you want to get the most attendees through your stand, you run short sessions with a live '
     'leaderboard and a staff member calling times, so the rig always looks busy without anyone waiting long.'),
])
