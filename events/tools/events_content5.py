# -*- coding: utf-8 -*-
"""Events batch 5: the last four event types.

Each has a genuinely different job, which is what keeps them from being the
same page four times:
  employee appreciation - internal, inclusive, no lead capture, shift patterns
  client entertainment  - small, slow, conversation is the point
  private parties       - access and mixed ages, no business objective
  fundraisers           - the rig is the fundraising mechanism, not just a draw

Verified facts available to all of them: frame 26 in x 57 in (Trak Racer
TR160 V5), 49 in ultrawide is the widest part, allow ~10 ft x 10 ft per rig in
operation, 15 to 40 drivers per hour per simulator. No prices, no invented
clients or venues, and no contractual absolutes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events_pages import write
from events_content import prose, cards, faq, linkgrid, CROSS, ld

PAGES = []

STANDARD = ('Delivery, setup, calibration, staffing and teardown are included as standard, and your quote '
            'sets out exactly what is covered for your event.')


def etype(slug, eyebrow, title, desc, h1, lede, final_h, final_p,
          why_h, why, fits, practical, faqs, ldname, related=()):
    return dict(
        slug=slug, url='/event-types/%s/' % slug, ctype='event_type',
        title=title, desc=desc,
        crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede, final_h=final_h, final_p=final_p,
        ld=ld('Service', ldname, desc, '/event-types/%s/' % slug),
        body='\n\n'.join([
            prose('Why It Works', why_h, '', why),
            cards('Where It Fits', 'THE OCCASIONS', '', fits),
            prose('Practical', 'PLANNING IT', '', practical),
            linkgrid('Related', 'ALSO WORTH READING', '', list(related) + [
                ('/experiences/', 'PICK THE RACING',
                 'GT3, Formula-style, stock car, endurance, drift and rally.'),
                ('/locations/', 'WHERE WE DELIVER',
                 'Mobile simulator events from our Tampa base, throughout Florida.'),
            ]),
            CROSS,
            faq(faqs),
        ]),
    )


# --------------------------------------------- EMPLOYEE APPRECIATION -------
PAGES.append(etype(
    'employee-appreciation', 'Employee Appreciation',
    'Racing Simulator Rental For Employee Appreciation Events | Academy Sim Racing',
    'Racing simulator rentals for employee appreciation and recognition events in Florida. An activity people actually want to do, with no pitch attached.',
    'SOMETHING THEY DID<br>NOT HAVE TO SIT THROUGH',
    'Recognition events fail in a specific way: they end up being another meeting with catering. The test '
    'is whether anybody would choose to be there, and this is one of the few formats that passes it.',
    'THANKING YOUR<br><span class="amber">TEAM PROPERLY?</span>',
    'Tell us the headcount, the space you have and the window. We will build something people will actually enjoy.',
    'NO AGENDA, WHICH IS THE POINT',
    ['<p>Almost every other event on this site has a commercial objective sitting behind it. An appreciation '
     'day does not, and that changes what a good setup looks like.</p>',
     '<p>There is no lead capture, no branding requirement and nobody who needs to be impressed. The only '
     'measure is whether your people had a good time, which means the format should be built for '
     'inclusiveness rather than for competition. A leaderboard that one person dominates all afternoon is '
     'the wrong answer here even though it is the right answer at a trade show.</p>',
     '<h3>What we would do differently</h3>',
     '<ul>'
     '<li><strong>Driver aids on, and left on.</strong> Nobody should be embarrassed in front of colleagues. '
     'We turn them down only for people who ask.</li>'
     '<li><strong>Longer sessions, less queueing.</strong> Standing in line is not a reward.</li>'
     '<li><strong>Team formats over individual ones.</strong> A relay gets people mixing across departments. '
     'A fastest lap board gets the same three people at the top.</li>'
     '<li><strong>Something for the people not driving.</strong> Screens showing the current session, so '
     'watching is part of it rather than waiting.</li>'
     '</ul>'],
    [('01 / Recognition', 'RECOGNITION DAYS', 'Annual appreciation events where the whole point is that people enjoy themselves.'),
     ('02 / Milestones', 'COMPANY MILESTONES', 'Anniversaries and targets hit, marked with something better than a speech.'),
     ('03 / Summer', 'SUMMER AND FAMILY DAYS', 'Events where partners and children come too, so the format has to suit everyone.'),
     ('04 / Holidays', 'HOLIDAY PARTIES', 'December events. These book earliest, so raise them well ahead.'),
     ('05 / Onsite', 'ONSITE AT YOUR OFFICE', 'Warehouses, offices and parking lots, where we work around your actual space.'),
     ('06 / Shifts', 'SHIFT-BASED WORKFORCES', 'Longer running so that people on different shifts all get a turn.')],
    ['<h3>Shift patterns are the thing people forget</h3>'
     '<p>If your workforce runs shifts, an activation that only exists between noon and three has excluded a '
     'large part of the people it was meant to thank. It is usually better to run longer with fewer rigs than '
     'to run a short, intense session that half the team cannot attend.</p>',
     '<h3>Onsite is often easier than a venue</h3>'
     '<p>Offices, warehouses and covered outdoor areas all work. The frame is 26 inches wide and 57 inches '
     'long, and the 49 inch ultrawide display is the widest part, so allow around 10 feet by 10 feet per '
     'simulator once you include the driver getting in and out and someone waiting. Mains power at the '
     'setup point is the other constraint.</p>',
     '<h3>Work out how many will actually drive</h3>'
     '<p>Each simulator handles roughly 15 to 40 drivers an hour depending on session length. For an '
     'appreciation event we would lean toward the longer end, so size the rig count with that in mind '
     'rather than assuming maximum throughput.</p>',
     '<div class="note-band"><p>' + STANDARD + '</p></div>'],
    [('Does everyone need to be good at driving?',
      'No, and we set it up so they do not have to be. Driver aids are on by default and our staff get each '
      'person going, so nobody is left struggling in front of colleagues.'),
     ('Can you come to our office or warehouse?',
      'Yes, and for appreciation events it is often the easiest option. We need floor space and mains power '
      'at the setup point. Send photos of the space and we will confirm.'),
     ('We run shifts. Can you cover more than one?',
      'Yes. Running longer with fewer rigs usually serves a shift-based workforce better than a short session '
      'with more. Tell us your shift pattern and we will plan around it.'),
     ('What if people bring their families?',
      'That works well. Driver aids make the cars manageable for children and our staff set each driver up '
      'individually.'),
     ('Do we need a competition?',
      'Not at all, and for appreciation events we often suggest not having one. Open racing where people come '
      'and go tends to produce a better afternoon than a bracket nobody asked for.'),
     ('How far ahead should we book?',
      'The earlier the better, and much earlier for anything in December.')],
    'Racing Simulator Rental For Employee Appreciation Events',
    [('/event-types/corporate-events/', 'CORPORATE EVENTS',
      'Formats for kickoffs, annual meetings and client-facing evenings.')],
))

# ----------------------------------------------- CLIENT ENTERTAINMENT ------
PAGES.append(etype(
    'client-entertainment', 'Client Entertainment',
    'Racing Simulator Rental For Client Entertainment | Academy Sim Racing',
    'Racing simulators for client entertainment and hospitality in Florida. Small-group formats where the racing supports the conversation rather than replacing it.',
    'THE REASON TO BE<br>IN THE ROOM',
    'Client entertainment has a specific failure mode: an activity so absorbing that nobody talks, or so '
    'dull that everyone checks their phone. Racing sits in a useful middle, as long as you do not run it '
    'like a competition.',
    'ENTERTAINING CLIENTS<br><span class="amber">IN FLORIDA?</span>',
    'Tell us the group size and the venue. Small hospitality formats are quoted differently from large activations.',
    'THE RACING IS THE BACKDROP',
    ['<p>At a trade show the simulator is the objective. At a client dinner it is the excuse. That difference '
     'should change almost everything about how it is set up, and usually does not, which is why hospitality '
     'activations often feel like a corporate event that wandered into the wrong room.</p>',
     '<p>The job here is to give people something to do with their hands and something easy to talk about. '
     'It is not to establish who is quickest. A structured competition forces everyone to pay attention to '
     'the same thing at the same time, which is the opposite of what you want when your team is trying to '
     'have four separate conversations.</p>',
     '<h3>What changes for hospitality</h3>',
     '<ul>'
     '<li><strong>Fewer rigs, longer sessions.</strong> Nobody should feel hurried out of the seat because '
     'a queue has formed.</li>'
     '<li><strong>No formal competition.</strong> A quiet leaderboard people can look at if they want, rather '
     'than a scheduled bracket.</li>'
     '<li><strong>Our staff run it entirely.</strong> Your team should be talking to clients, not resetting '
     'sessions or explaining the pedals.</li>'
     '<li><strong>Volume matters.</strong> Headphones or lower audio, so the room stays conversational.</li>'
     '</ul>'],
    [('01 / Dinners', 'CLIENT DINNERS', 'A rig in an adjacent room or corner, running through the evening.'),
     ('02 / Suites', 'HOSPITALITY SUITES', 'Small spaces where one simulator does more than a bigger setup would.'),
     ('03 / Thanks', 'CLIENT APPRECIATION EVENINGS', 'Larger thank-you events where the racing is the draw but not the agenda.'),
     ('04 / Pitches', 'PITCH AND PROPOSAL EVENTS', 'Something memorable attached to a business conversation.'),
     ('05 / Race Days', 'RACE-DAY HOSPITALITY', 'Watch parties with a rig running the circuit on the broadcast.'),
     ('06 / Golf', 'ALTERNATIVES TO THE USUAL', 'For clients who do not play golf and have had enough dinners.')],
    ['<h3>One rig is often the right answer</h3>'
     '<p>For a group of ten to twenty, a single simulator running all evening usually works better than two. '
     'It becomes a focal point people gather around rather than an activity everyone has to take a turn at.</p>',
     '<h3>Where to put it</h3>'
     '<p>Adjacent to the main room rather than in it. People should be able to drift toward it and away again. '
     'Allow around 10 feet by 10 feet per simulator, and remember the 49 inch ultrawide display is the widest '
     'part, so a private dining room or a suite is usually workable.</p>',
     '<h3>Brief your own team</h3>'
     '<p>The most common mistake is your people spending the evening running the simulator because they are '
     'enjoying it. Our staff handle the activation so yours can do the job they came to do.</p>',
     '<div class="note-band"><p>' + STANDARD + '</p></div>'],
    [('What is the smallest group you will do?',
      'There is no fixed minimum. Small hospitality events are quoted differently from large activations, so '
      'tell us the group size and we will give you a sensible number.'),
     ('Will it be too loud for a dinner?',
      'Not if it is set up properly. We can run the simulators on headphones or at low volume so the room '
      'stays conversational.'),
     ('Do we need a competition or prizes?',
      'For hospitality we would usually suggest not. A leaderboard people can glance at works better than a '
      'structured bracket that pulls everyone away from their conversations.'),
     ('Can you set up in a private dining room or suite?',
      'Usually yes. Allow around 10 feet by 10 feet per simulator and check the access route. Send us photos '
      'or dimensions and we will confirm before you commit.'),
     ('Will our team have to run it?',
      'No. Our staff run the activation for the duration so your people can concentrate on your clients.'),
     ('Can it be branded for the evening?',
      'Yes, through rig wraps and on-screen branding, though for a small hospitality event most clients '
      'prefer it understated.')],
    'Racing Simulator Rental For Client Entertainment',
    [('/event-types/watch-parties/', 'WATCH PARTIES',
      'Race-day hospitality with simulators running the circuit on the broadcast.')],
))

# ---------------------------------------------------- PRIVATE PARTIES ------
PAGES.append(etype(
    'private-parties', 'Private Parties',
    'Racing Simulator Rental For Private Parties | Florida | Academy Sim Racing',
    'Racing simulator rentals for private parties, birthdays and milestone celebrations across Florida. Delivered to your home or venue, set up and staffed.',
    'BRING IT TO<br>YOUR PARTY',
    'Birthdays, milestone celebrations and anything where the guest list is people you actually know. '
    'We deliver to homes and private venues, run it all evening, and take it away again.',
    'PLANNING A<br><span class="amber">PARTY IN FLORIDA?</span>',
    'Send us the date, the address and rough numbers. Photos of the space help more than measurements.',
    'THE HOST SHOULD NOT HAVE TO RUN IT',
    ['<p>The difference between a private party and a corporate event is that at a party the organizer is a '
     'guest. If the activity needs supervising, explaining or resetting, the host spends the evening doing '
     'that instead of enjoying their own party.</p>',
     '<p>So the setup here is built around not needing you. Our staff seat each driver, explain it in a '
     'sentence, run the sessions and manage whose turn it is. You should be able to ignore it completely.</p>',
     '<h3>Mixed ages are normal</h3>',
     '<p>Most private parties have a wide age range, and that is fine. Driver aids make the cars manageable '
     'for children and for adults who have never done it, and can come off for anyone who wants a challenge. '
     'It is one of the few activities where a twelve year old and a fifty year old can compete on roughly '
     'even terms.</p>'],
    [('01 / Birthdays', 'BIRTHDAYS', 'Milestone birthdays where you want something people will remember.'),
     ('02 / Milestones', 'ANNIVERSARIES AND CELEBRATIONS', 'Any occasion where the alternative was another dinner.'),
     ('03 / Graduations', 'GRADUATIONS AND SEND-OFFS', 'Mixed-age gatherings that need something for everyone.'),
     ('04 / Groups', 'CAR CLUBS AND ENTHUSIAST GROUPS', 'An audience that already knows what it is looking at.'),
     ('05 / Bachelor', 'BACHELOR AND BACHELORETTE PARTIES', 'Competitive without requiring anyone to be sporty.'),
     ('06 / Holidays', 'HOLIDAY GATHERINGS', 'December dates go first, so ask early.')],
    ['<h3>Access matters more than floor space</h3>'
     '<p>At a private home the question is rarely whether there is room. It is whether we can get the '
     'equipment in. The frame is 26 inches wide, so a standard doorway is fine, but steps, gates, lifts, '
     'narrow hallways and how close a vehicle can park all matter. Photographs of the route from the street '
     'to the room are the single most useful thing you can send us.</p>',
     '<h3>Power</h3>'
     '<p>Domestic supply needs checking properly for anything beyond a single rig. It is the constraint most '
     'likely to change a plan at a house, so raise it when you first get in touch.</p>',
     '<h3>Outdoors is possible with cover</h3>'
     '<p>Garages, covered patios and event tents all work. Open ground does not, because the equipment needs '
     'protection from weather and direct sun on the screens makes them hard to see.</p>',
     '<h3>How many rigs</h3>'
     '<p>Each simulator handles roughly 15 to 40 drivers an hour depending on session length. For a party '
     'you want the longer end, so one or two rigs suits most home events better than trying to get everyone '
     'through quickly.</p>',
     '<div class="note-band"><p>' + STANDARD + '</p></div>'],
    [('Can you set up at a private home?',
      'Yes, subject to access and power. Send photographs of the route in and the space and we will tell you '
      'honestly what is workable before you commit to anything.'),
     ('Will it fit through a normal door?',
      'The frame is 26 inches wide, so a standard doorway is fine. Steps, tight corners and gate access are '
      'the things more likely to cause a problem.'),
     ('Is it suitable for children?',
      'Yes. Driver aids make the cars manageable and our staff set each driver up. Mixed-age parties are one '
      'of the things it does best.'),
     ('Do we have to run it ourselves?',
      'No. Our staff run the whole thing so the host can enjoy their own party.'),
     ('Can it go outside?',
      'Under cover, yes. Garages, covered patios and event tents work. Open ground with no weather protection '
      'does not, and direct sun on the screens is a problem.'),
     ('How many simulators do we need for a house party?',
      'Usually one or two. At a party longer sessions are better than maximum throughput, so more rigs is '
      'rarely the right answer.'),
     ('Do you cover our area?',
      'We deliver throughout Florida from our Tampa base. Travel is quoted per event based on distance.')],
    'Racing Simulator Rental For Private Parties',
    [('/locations/', 'WHERE WE DELIVER',
      'Mobile simulator events across Florida, delivered from Tampa.')],
))

# --------------------------------------------------------- FUNDRAISERS -----
PAGES.append(etype(
    'fundraisers', 'Fundraisers',
    'Racing Simulator Rental For Fundraisers &amp; Charity Events | Academy Sim Racing',
    'Racing simulators for charity fundraisers in Florida. The rig is both the draw and the fundraising mechanism, with sponsor branding and a live leaderboard.',
    'THE RIG IS ALSO<br>THE FUNDRAISER',
    'At most events the simulator draws a crowd and something else does the work. At a fundraiser it can '
    'do both, because paying to race is an easier ask than paying to attend.',
    'RAISING MONEY<br><span class="amber">IN FLORIDA?</span>',
    'Tell us the cause, the date and the format you have in mind. We will tell you what works.',
    'PEOPLE WILL PAY TO RACE',
    ['<p>The hardest part of a charity event is usually the ask. A simulator makes it easier, because '
     'entering a race is a transaction people understand and enjoy rather than a donation they feel obliged '
     'to make.</p>',
     '<p>It also produces something a raffle cannot: a leaderboard that keeps updating all evening, which '
     'gives people a reason to enter more than once. The second and third entries are usually where the '
     'money actually comes from.</p>',
     '<h3>Mechanics that work</h3>',
     '<ul>'
     '<li><strong>Pay per run.</strong> A small amount per attempt, with people re-entering to beat their own '
     'time or somebody else&rsquo;s.</li>'
     '<li><strong>Sponsored rig.</strong> A local business covers the activation cost in exchange for branding '
     'on the wrap and the leaderboard, so more of what is raised goes to the cause.</li>'
     '<li><strong>Challenge the guest.</strong> Someone credible sets a time and people pay to try to beat it.</li>'
     '<li><strong>Team entry.</strong> Companies enter teams for a fixed fee, which turns one donation into '
     'several attendees.</li>'
     '</ul>'],
    [('01 / Galas', 'CHARITY GALAS', 'A rig running alongside the dinner, with entries sold through the evening.'),
     ('02 / Golf', 'GOLF DAYS AND OUTDOOR EVENTS', 'Something for people waiting to tee off, under cover.'),
     ('03 / Community', 'COMMUNITY FUNDRAISERS', 'Broad public audiences where the format has to suit everyone.'),
     ('04 / Schools', 'SCHOOL AND CLUB FUNDRAISERS', 'Events where the audience is mixed-age and the entry price is low.'),
     ('05 / Corporate', 'CORPORATE GIVING DAYS', 'Company charity days where teams compete and the business matches.'),
     ('06 / Auctions', 'AUCTION AND PRIZE TIE-INS', 'A fastest-lap prize that ties into the wider auction.')],
    ['<h3>Decide the mechanic before the format</h3>'
     '<p>How you are collecting money should decide the racing format, not the other way round. Pay per run '
     'wants short sessions and high throughput. Team entry wants a relay. A challenge time wants one circuit '
     'and one car all night.</p>',
     '<h3>Find a sponsor for the activation</h3>'
     '<p>The most effective fundraising setups we see have a local business covering the cost of the rig in '
     'exchange for branding. It removes the activation from your budget entirely, which means everything '
     'taken on the night goes to the cause.</p>',
     '<h3>Keep the entry price low and the queue moving</h3>'
     '<p>Each simulator handles roughly 15 to 40 drivers an hour depending on session length. For a '
     'fundraiser, short runs at a low price usually raise more than long sessions at a high one, because '
     'people enter repeatedly.</p>',
     '<div class="note-band"><p>' + STANDARD + ' We are a commercial supplier, not a charity partner, and we '
     'do not administer donations or handle funds raised at your event.</p></div>'],
    [('How does a simulator raise money?',
      'Usually by selling entries. A small amount per run, with a live leaderboard giving people a reason to '
      'come back and try again. Repeat entries are normally where most of the money comes from.'),
     ('Can a sponsor cover the cost of the simulator?',
      'Yes, and it is the arrangement we would suggest. A local business covers the activation in exchange for '
      'branding on the rig and the leaderboard, so more of what you take on the night goes to the cause.'),
     ('Do you handle the money?',
      'No. We supply and run the simulators. Collecting entries and administering funds is for your team, and '
      'we are a commercial supplier rather than a charity partner.'),
     ('Do you offer a discount for charities?',
      'Tell us about the event and the cause when you get in touch. Pricing is quoted per event and we would '
      'rather have that conversation properly than publish a policy.'),
     ('What format raises the most?',
      'In our experience short paid runs with a live leaderboard, because people enter more than once. Team '
      'entries work well when you are selling to businesses rather than individuals.'),
     ('Can the rig carry our sponsors&rsquo; branding?',
      'Yes, through rig wraps and on-screen branding. Wraps need lead time, so raise it early.'),
     ('Is it suitable for a mixed-age community event?',
      'Yes. Driver aids make the cars manageable for children and first-time adults, and our staff set every '
      'driver up.')],
    'Racing Simulator Rental For Fundraisers And Charity Events',
    [('/event-types/brand-activations/', 'BRAND ACTIVATIONS',
      'How sponsor branding works on a wrapped simulator.')],
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
