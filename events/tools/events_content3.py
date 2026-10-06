# -*- coding: utf-8 -*-
"""Events batch 3: /experiences/ hub, six experience pages, plus watch parties
(which the brief names as a required cross-link target from experiences).

The brief is explicit about language here. Never "official Formula 1 / NASCAR /
IMSA simulator". Use Formula-style racing, stock-car racing, GT3 racing,
endurance-style racing, drift experience, rally experience. SEO copy may
address people searching those series names without implying affiliation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events_pages import write
from events_content import prose, cards, faq, linkgrid, CROSS, ld

PAGES = []

DISCLAIMER = (
    '<div class="note-band"><p>Academy Sim Racing is not affiliated with, endorsed by or licensed by '
    'Formula 1, NASCAR, IMSA or any racing series, sanctioning body or car manufacturer. We provide '
    'simulator experiences using commercially available racing software.</p></div>'
)


def xlinks(extra=()):
    base = [
        ('/event-types/corporate-events/', 'CORPORATE EVENTS',
         'How the format changes for kickoffs, annual meetings and client nights.'),
        ('/event-types/watch-parties/', 'WATCH PARTIES',
         'Race-day viewing with simulators running alongside the broadcast.'),
        ('/locations/', 'WHERE WE DELIVER',
         'Mobile simulator events from our Tampa base, throughout Florida.'),
    ]
    return linkgrid('Related', 'WHERE THIS FITS', '', list(extra) + base)


# ------------------------------------------------------------- HUB ---------
PAGES.append(dict(
    slug='experiences', url='/experiences/', ctype='experience_hub',
    title='Racing Simulator Experiences For Events | Academy Sim Racing',
    desc='Formula-style, stock car, GT3, endurance, drift and rally simulator experiences for events across Florida. Pick the racing that suits your audience.',
    crumbs='<a href="/">Events</a> / Experiences',
    eyebrow='Experiences',
    h1='PICK THE RACING<br>THAT SUITS YOUR ROOM',
    lede='The rigs do not change. The cars, the circuits and the competition format do, and that choice '
         'decides whether your guests are gripped or quietly waiting for their turn to end.',
    final_h='NOT SURE WHICH<br><span class="amber">SUITS YOUR EVENT?</span>',
    final_p='Tell us who is coming and what the event is for. We will recommend a format.',
    ld=ld('CollectionPage', 'Racing Simulator Experiences For Events',
          'Formula-style, stock car, GT3, endurance, drift and rally simulator experiences for corporate and brand events in Florida.',
          '/experiences/'),
    body='\n\n'.join([
        prose('Start Here', 'MATCH THE CAR TO THE AUDIENCE', '', [
            '<p>The single most common mistake at a corporate event is putting a room of first-time drivers into '
            'the fastest, least forgiving car in the library because it sounds the most impressive. Everyone '
            'spins, nobody improves, and the queue thins out.</p>',
            '<p>The opposite mistake is real too. Put a room of car enthusiasts in something too tame and they '
            'will be polite about it and then go back to the bar.</p>',
            '<h3>The short version</h3>',
            '<ul>'
            '<li><strong>Mixed corporate audience, most have never done this.</strong> GT3 racing.</li>'
            '<li><strong>You want the biggest spectacle for onlookers.</strong> Drift.</li>'
            '<li><strong>Broad public audience, family day or community event.</strong> Stock car racing.</li>'
            '<li><strong>Enthusiasts, or you want a genuine challenge.</strong> Formula-style.</li>'
            '<li><strong>Long event, team competition, multiple departments.</strong> Endurance-style with a relay.</li>'
            '<li><strong>Something different that stands on its own.</strong> Rally.</li>'
            '</ul>',
        ]),
        linkgrid('Browse', 'THE EXPERIENCES', 'What each one feels like, and the events it suits.', [
            ('/experiences/gt3-racing-simulator/', 'GT3 RACING',
             'The default for mixed audiences. Forgiving, quick to learn, competitive within minutes.'),
            ('/experiences/formula-racing-simulator/', 'FORMULA-STYLE RACING',
             'Open-wheel, low weight, high grip. The one enthusiasts ask for.'),
            ('/experiences/nascar-racing-simulator/', 'STOCK CAR RACING',
             'Oval racing. Simple to understand, close, and loud in the best way.'),
            ('/experiences/imsa-endurance-racing/', 'ENDURANCE-STYLE RACING',
             'Multi-class racing and team relays. Built for longer events.'),
            ('/experiences/drift-racing-simulator/', 'DRIFT EXPERIENCE',
             'No lap times. Judged on angle and commitment, and the best one to watch.'),
            ('/experiences/rally-racing-simulator/', 'RALLY EXPERIENCE',
             'One car, one clock, loose surfaces. Nothing else at an event feels like it.'),
        ]),
        cards('Formats', 'HOW THE COMPETITION IS RUN', '', [
            ('01 / Open', 'OPEN RACING',
             'Rigs run continuously, guests come and go. Best for receptions where nothing should feel scheduled.'),
            ('02 / Leaderboard', 'FASTEST LAP',
             'One circuit, one car, identical conditions. A live leaderboard and a prize at the end of the night.'),
            ('03 / Bracket', 'HEAD TO HEAD',
             'Elimination brackets. Needs a defined window but produces a proper finale.'),
            ('04 / Relay', 'TEAM RELAY',
             'Departments or tables against each other over set laps. The best format for cross-team contact.'),
        ]),
        DISCLAIMER,
        CROSS,
        faq([
            ('Can we run more than one experience at an event?',
             'Yes. Different rigs can run different cars and circuits, or the format can change across the evening. '
             'Tell us the shape of the event and we will plan it.'),
            ('Which is best if most guests have never driven a simulator?',
             'GT3 racing. The cars have driver aids on by default, they shift with paddles, and people are usually '
             'lapping competently within a lap or two.'),
            ('Can guests race against each other directly?',
             'Yes. Multiple rigs can run the same session so guests race wheel to wheel, or you can run a leaderboard '
             'where everyone drives the same circuit and car.'),
            ('Do you provide the leaderboard?',
             'Yes, and it can carry your branding. It is the single most effective way to keep people coming back '
             'to the activation.'),
            ('Are these official Formula 1 or NASCAR simulators?',
             'No. We are not affiliated with or licensed by any racing series or manufacturer. We run commercially '
             'available racing software and describe the experiences by their style of racing.'),
            ('Can the cars be branded?',
             'On-screen liveries can be customized and the rigs can be custom wrapped. We do not supply branding '
             'for series or manufacturers we are not licensed to represent.'),
        ]),
    ]),
))


def experience(slug, title, desc, eyebrow, h1, lede, final_h, final_p,
               why_h, why, suits, formats, extra_faq, ldname, extra_links=()):
    return dict(
        slug=slug, url='/experiences/%s/' % slug, ctype='experience',
        title=title, desc=desc,
        crumbs='<a href="/">Events</a> / <a href="/experiences/">Experiences</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede, final_h=final_h, final_p=final_p,
        ld=ld('Service', ldname, desc, '/experiences/%s/' % slug),
        body='\n\n'.join([
            prose('The Experience', why_h, '', why),
            cards('Where It Fits', 'EVENTS IT SUITS', '', suits),
            prose('Running It', 'COMPETITION FORMATS', '', formats),
            DISCLAIMER,
            xlinks(extra_links),
            CROSS,
            faq(extra_faq),
        ]),
    )


# ------------------------------------------------------------- GT3 ---------
PAGES.append(experience(
    'gt3-racing-simulator',
    'GT3 Racing Simulator Experience For Events | Academy Sim Racing',
    'GT3 racing simulator experiences for corporate events, trade shows and activations in Florida. The most accessible format for mixed audiences.',
    'GT3 Racing', 'GT3 RACING<br>FOR EVENTS',
    'If you only book one format, book this one. GT3 cars are quick enough to feel serious and forgiving '
    'enough that a room of people who have never done it will be racing properly inside a few minutes.',
    'BRING GT3 RACING<br><span class="amber">TO YOUR EVENT.</span>',
    'Send us the date, the venue and your headcount. We will size the setup and quote it.',
    'THE FORMAT THAT ALWAYS WORKS',
    ['<p>GT3 cars are production-based racing cars built to a balanced ruleset. In practice, for an event, '
     'what matters is that they carry traction control and anti-lock brakes, they shift with paddles so '
     'there is no gearbox to think about, and they have enough downforce to feel planted without demanding '
     'perfect inputs.</p>',
     '<p>That combination means the gap between your most confident guest and your least confident one stays '
     'narrow. Everybody gets a lap time they are not embarrassed by, which is what keeps the queue full.</p>',
     '<h3>Why it holds a crowd</h3>',
     '<ul>'
     '<li>Guests improve visibly within a single session, which is the thing that makes people want another go.</li>'
     '<li>Lap times cluster closely, so a leaderboard stays competitive all evening rather than being settled early.</li>'
     '<li>The cars are recognisable to enthusiasts without being intimidating to anyone else.</li>'
     '</ul>'],
    [('01 / Corporate', 'CORPORATE EVENTS', 'The default choice for sales kickoffs, annual meetings and client nights.'),
     ('02 / Trade Shows', 'TRADE SHOW BOOTHS', 'Short sessions and a live leaderboard keep the queue moving all day.'),
     ('03 / Dealerships', 'DEALERSHIP EVENTS', 'Broad audiences, families included, with nobody left out.'),
     ('04 / Brand', 'BRAND ACTIVATIONS', 'The most photogenic format that is still easy for anyone to drive.')],
    ['<h3>Fastest lap</h3>'
     '<p>One circuit, one car, identical conditions for everyone, live leaderboard, prize at the end. This is '
     'the format we run most often with GT3 and the one that produces the most repeat visits to the rig.</p>',
     '<h3>Head to head</h3>'
     '<p>Two or more rigs running the same session so guests race each other directly. Better for smaller groups '
     'and for events with a defined competition window.</p>',
     '<h3>Open racing</h3>'
     '<p>Rigs run continuously and guests drive when they feel like it. Best for receptions where a scheduled '
     'competition would feel forced.</p>'],
    [('How long does a GT3 session take?',
      'Session length is a dial we set to suit your throughput. Short runs at a busy trade show booth, longer '
      'sessions at an evening reception. Tell us your headcount and window and we will set it.'),
     ('Will guests who have never raced be able to do it?',
      'Yes. That is the main reason we recommend GT3. Driver aids are on by default and our staff set each '
      'person up, so people are lapping properly very quickly.'),
     ('Can experienced drivers be challenged?',
      'Yes. Driver aids can be reduced or turned off for anyone who asks, and a harder circuit raises the '
      'difficulty without changing the setup for everyone else.'),
     ('Which circuits do you use?',
      'Well-known real-world road courses, chosen for how quickly a first-time driver can learn them. For a '
      'leaderboard we keep everyone on one circuit so the times are comparable.'),
     ('Can the cars carry our branding?',
      'On-screen liveries can be customized and the rigs can be wrapped. We do not supply branding for series '
      'or manufacturers we are not licensed to represent.'),
     ('How many rigs do we need?',
      'It depends on headcount and how long you have. Send us both and we will size it.')],
    'GT3 Racing Simulator Experience For Events',
))

# --------------------------------------------------------- FORMULA ---------
PAGES.append(experience(
    'formula-racing-simulator',
    'Formula-Style Racing Simulator Experience For Events | Academy Sim Racing',
    'Formula-style open-wheel racing simulator experiences for corporate events and activations in Florida. The format enthusiasts ask for by name.',
    'Formula-Style Racing', 'FORMULA-STYLE<br>RACING FOR EVENTS',
    'Open-wheel cars are the ones guests ask for by name. Very little weight, a great deal of aerodynamic '
    'grip, and in most classes no traction control to catch a mistake with the throttle.',
    'BRING FORMULA-STYLE<br><span class="amber">RACING TO YOUR EVENT.</span>',
    'Tell us who is coming. If it is an enthusiast crowd, this is usually the right call.',
    'THE ONE PEOPLE ASK FOR',
    ['<p>Open-wheel single seaters are the most demanding thing we put guests in, and for the right audience '
     'that is exactly the appeal. The cars are light, the grip is high, and the margin for error is small.</p>',
     '<p>Be honest with yourself about the room. For a crowd that follows motorsport, this format lands better '
     'than anything else we offer and the conversation around the rig is completely different. For a general '
     'corporate audience it can be frustrating, and GT3 will produce a better evening.</p>',
     '<h3>What makes it hard</h3>',
     '<ul>'
     '<li>Aerodynamic load rises sharply with speed, so the car has most grip exactly where it is least '
     'comfortable to trust it.</li>'
     '<li>In most classes there is no traction control, so throttle discipline out of slow corners matters.</li>'
     '<li>The braking is far stronger than road-car instinct expects, which is where most first laps go wrong.</li>'
     '</ul>',
     '<p>Driver aids can be turned up for guests who want the experience without the difficulty, which is the '
     'usual compromise when the audience is mixed.</p>'],
    [('01 / Enthusiasts', 'ENTHUSIAST AUDIENCES', 'Car clubs, motorsport sponsors and any room that follows racing.'),
     ('02 / Race Weekends', 'RACE-DAY WATCH PARTIES', 'Guests drive the circuit they are watching, on the day.'),
     ('03 / Sponsors', 'SPONSOR ACTIVATIONS', 'Motorsport-adjacent brands where the format has to be credible.'),
     ('04 / VIP', 'VIP AND HOSPITALITY', 'Smaller groups where a genuine challenge is the point.')],
    ['<h3>Fastest lap, with aids available</h3>'
     '<p>The usual setup. Everyone runs the same circuit and car, and guests choose how much assistance they '
     'want. Times are still comparable and nobody is stuck.</p>',
     '<h3>Head to head</h3>'
     '<p>Two rigs, same session, direct racing. Works well with an enthusiast crowd who will take it seriously.</p>',
     '<h3>Circuit of the day</h3>'
     '<p>For a watch party, run the circuit that is being raced that weekend. It gives guests a direct reference '
     'for what they are watching on screen.</p>'],
    [('Is this an official Formula 1 simulator?',
      'No. We are not affiliated with, endorsed by or licensed by Formula 1 or any racing series. We run '
      'commercially available racing software and describe this as Formula-style racing.'),
     ('Is it too hard for a corporate audience?',
      'For a general corporate room, often yes, and GT3 is the better choice. For an enthusiast audience it is '
      'the best thing we offer. Driver aids can be increased if the room is mixed.'),
     ('Can we run it alongside an easier format?',
      'Yes, and for mixed audiences we often recommend it. One rig set up for enthusiasts, the others in GT3.'),
     ('Which circuits work best?',
      'For events we favor circuits that are quick to learn so guests are not still finding their way round at '
      'the end of a short session.'),
     ('Can we brand it?',
      'The rigs can be wrapped and the on-screen leaderboard branded. We do not supply Formula 1 or team '
      'branding, which we are not licensed to use.'),
     ('Do you supply the staff?',
      'Yes. Delivery, setup, staffing for the duration and teardown are included in every booking.')],
    'Formula-Style Racing Simulator Experience For Events',
))

# ------------------------------------------------------- STOCK CAR ---------
PAGES.append(experience(
    'nascar-racing-simulator',
    'Stock Car Racing Simulator Experience For Events | Academy Sim Racing',
    'Stock car and oval racing simulator experiences for events in Florida. Simple to grasp, close racing, and the easiest format for a broad public audience.',
    'Stock Car Racing', 'STOCK CAR RACING<br>FOR EVENTS',
    'Oval racing is the easiest kind of motorsport to explain to somebody who does not follow motorsport. '
    'Turn left, stay flat, do not touch the wall. That simplicity is exactly why it works on a crowd.',
    'BRING STOCK CAR RACING<br><span class="amber">TO YOUR EVENT.</span>',
    'Tell us the venue and the audience. For broad public events this is usually the format we recommend.',
    'THE MOST ACCESSIBLE FORMAT WE RUN',
    ['<p>A road course has to be learned. An oval does not, which is why stock car racing works so well at '
     'events where guests are not motorsport fans and will only get one short session.</p>',
     '<p>Stock cars are heavy and powerful with very little aerodynamic help, so the car moves around under the '
     'driver. That sounds like a drawback and is actually the appeal: it feels dramatic at speeds that are still '
     'manageable, and the racing stays close because everyone is on the same line.</p>',
     '<h3>Why crowds like watching it</h3>',
     '<ul>'
     '<li>Cars stay near each other, so a head-to-head session actually looks like a race.</li>'
     '<li>There is no complicated circuit to follow, so onlookers can see who is winning.</li>'
     '<li>Lap times are short, which keeps the leaderboard turning over quickly.</li>'
     '</ul>'],
    [('01 / Community', 'FAMILY AND COMMUNITY DAYS', 'Broad audiences of all ages and no motorsport knowledge required.'),
     ('02 / Dealerships', 'DEALERSHIP EVENTS', 'Weekend events where the crowd is wide and the sessions are short.'),
     ('03 / Trade Shows', 'TRADE SHOW BOOTHS', 'Short laps mean high throughput and a leaderboard that keeps moving.'),
     ('04 / Fundraisers', 'FUNDRAISERS', 'Easy to enter, easy to explain, and competitive for everyone.')],
    ['<h3>Fastest lap</h3>'
     '<p>Short laps make this format especially good on an oval. The leaderboard changes constantly and guests '
     'can see their name move after a single run.</p>',
     '<h3>Head to head</h3>'
     '<p>Two rigs on the same oval produces the closest racing of any format we run, because there is nowhere '
     'for a faster driver to disappear to.</p>',
     '<h3>Bracket racing</h3>'
     '<p>Short sessions make elimination brackets practical even at a busy event, and they build to a final that '
     'draws a crowd.</p>'],
    [('Is this an official NASCAR simulator?',
      'No. We are not affiliated with, endorsed by or licensed by NASCAR or any racing series. We run '
      'commercially available racing software and describe this as stock car racing.'),
     ('Is oval racing boring on a simulator?',
      'It is the opposite at an event. Short laps, close racing and a constantly changing leaderboard make it '
      'the format that holds a general audience best.'),
     ('Do guests need any experience?',
      'None. An oval is the quickest layout to learn, which is why we recommend it when guests get one short go.'),
     ('Can you run road courses as well?',
      'Yes. Many ovals also have road course configurations, and we can switch during an event if the audience '
      'changes through the day.'),
     ('Is it suitable for children?',
      'Yes, at family and community events. Driver aids make the cars manageable and staff set each driver up.'),
     ('Can it be branded?',
      'Yes, through rig wraps and on-screen branding. We do not supply series or manufacturer branding.')],
    'Stock Car Racing Simulator Experience For Events',
))

# ------------------------------------------------------- ENDURANCE ---------
PAGES.append(experience(
    'imsa-endurance-racing',
    'Endurance-Style Racing Simulator Experience For Events | Academy Sim Racing',
    'Endurance-style and multi-class racing simulator experiences for longer events in Florida. Team relays, driver changes and leaderboards that run all day.',
    'Endurance-Style Racing', 'ENDURANCE-STYLE<br>RACING FOR EVENTS',
    'Most event formats are built around one person doing one lap. Endurance racing is built around a team '
    'sharing a car, which makes it the only format that produces genuine group competition.',
    'RUN A TEAM<br><span class="amber">ENDURANCE EVENT.</span>',
    'Tell us how many teams and how long you have. We will build the format around it.',
    'THE ONLY TRUE TEAM FORMAT',
    ['<p>Endurance racing puts several drivers in one car across a longer race, with driver changes along the '
     'way. Translated to an event, that means departments or tables enter as teams, each member drives a stint, '
     'and the result belongs to the group rather than the individual.</p>',
     '<p>It changes the social dynamic completely. In a fastest-lap competition the strongest driver wins and '
     'everyone else watches. In a relay the weakest driver matters just as much, so teams coach each other, and '
     'that is usually the actual point of the exercise.</p>',
     '<h3>Multi-class racing</h3>'
     '<p>Endurance racing runs faster and slower classes on track together. On a simulator that gives you a way '
     'to put confident and nervous drivers in the same race without either being spoiled, because they are '
     'competing within their own class.</p>'],
    [('01 / Team Building', 'TEAM BUILDING', 'The format built for it. Groups share a car and a result.'),
     ('02 / Conventions', 'MULTI-DAY EVENTS', 'A leaderboard that runs across the whole show, with a final on the last day.'),
     ('03 / Corporate', 'SALES KICKOFFS', 'Departments against each other, with a finale that closes the day.'),
     ('04 / Fundraisers', 'CHARITY RACES', 'Teams enter, sponsors back them, and the race runs for a set time.')],
    ['<h3>Team relay</h3>'
     '<p>Each team gets a set number of laps or a set time, drivers rotate, and the combined result decides it. '
     'The most popular endurance format at corporate events.</p>',
     '<h3>Timed race</h3>'
     '<p>A fixed clock rather than a lap count, so the event ends when you need it to regardless of pace.</p>',
     '<h3>Multi-class</h3>'
     '<p>Two classes running together, so experienced and inexperienced guests race in the same session without '
     'either group having a bad time.</p>'],
    [('Is this an official IMSA simulator?',
      'No. We are not affiliated with, endorsed by or licensed by IMSA or any racing series. We run commercially '
      'available racing software and describe this as endurance-style racing.'),
     ('How long does a team relay take?',
      'It is set to your window rather than fixed. Tell us how long you have and how many teams and we will '
      'build the format to fit.'),
     ('How many people per team?',
      'Usually three to five, so each driver gets a meaningful stint without anyone waiting too long. Larger '
      'teams work if the race is longer.'),
     ('Can drivers of very different ability be on the same team?',
      'Yes, and that is part of why it works. The format rewards teams that help their least experienced driver '
      'rather than teams with one quick person.'),
     ('Do you handle the timing?',
      'Yes. Timing, stint tracking and the leaderboard are run by our staff, and the leaderboard can carry your '
      'branding.'),
     ('Does it work across a multi-day event?',
      'Yes. Teams can race on different days with a leaderboard carrying across the show and a final on the '
      'last day.')],
    'Endurance-Style Racing Simulator Experience For Events',
))

# ----------------------------------------------------------- DRIFT ---------
PAGES.append(experience(
    'drift-racing-simulator',
    'Drift Simulator Experience For Events | Academy Sim Racing',
    'Drift simulator experiences for brand activations and events in Florida. No lap times, maximum spectacle, and the best format for onlookers and social content.',
    'Drift Experience', 'THE ONE PEOPLE<br>STOP TO WATCH',
    'Every other format is judged on lap time, which means the interesting part is happening to the person in '
    'the seat. Drifting is judged on how it looks, which makes it the only format that performs for the room.',
    'BRING DRIFTING<br><span class="amber">TO YOUR EVENT.</span>',
    'If the brief mentions social content or crowd draw, this is the one to ask about.',
    'BUILT FOR SPECTATORS',
    ['<p>Drifting is scored on angle, line and commitment rather than on speed. There is no clock, which changes '
     'the whole feel of the activation: nobody is quietly failing against a number, and a spectacular attempt '
     'that ends in a spin is more entertaining than a clean one.</p>',
     '<p>That makes it the best format we run for crowd draw. The car is sideways, the screen is dramatic, and '
     'people stop to watch other guests rather than only queueing for their own go.</p>',
     '<h3>Why it suits brand work</h3>',
     '<ul>'
     '<li>It photographs and films better than any other format, which matters when social content is in the brief.</li>'
     '<li>Failure is entertaining, so guests take bigger swings and enjoy themselves more.</li>'
     '<li>It is visually distinct from every other activation on a show floor.</li>'
     '</ul>'],
    [('01 / Brand', 'BRAND ACTIVATIONS', 'The most photogenic format we run, and the easiest to build content around.'),
     ('02 / Trade Shows', 'TRADE SHOW BOOTHS', 'Draws people from across the hall because the screen is dramatic from a distance.'),
     ('03 / Community', 'FAMILY AND COMMUNITY DAYS', 'No lap times means no pressure, which suits a broad audience.'),
     ('04 / Car Clubs', 'CAR CLUB EVENTS', 'An audience that already knows what good looks like.')],
    ['<h3>Judged runs</h3>'
     '<p>Guests get a set number of attempts and are scored on angle and line. Our staff score and call the runs, '
     'which is a large part of what makes it entertaining for onlookers.</p>',
     '<h3>Tandem</h3>'
     '<p>Two rigs, lead and chase, the way real drift competition is judged. Harder, and the best thing to watch '
     'at an event.</p>',
     '<h3>Just play</h3>'
     '<p>No scoring at all. Guests drive, get sideways, and enjoy it. Often the right answer at a busy activation '
     'where a competition would slow the queue.</p>'],
    [('Do guests need experience to drift?',
      'No, and that is the point. It is genuinely hard, so nobody expects to be good at it and everyone enjoys '
      'trying. Our staff coach each driver through it.'),
     ('Is it harder than the other formats?',
      'Yes, in the sense that holding a sustained drift takes practice. But because there is no lap time, being '
      'bad at it is fun rather than discouraging.'),
     ('Is it good for social content?',
      'It is the best format we run for that. The visuals are dramatic and the moments people want to film happen '
      'constantly rather than once a session.'),
     ('Can it be branded?',
      'Yes. Rig wraps and on-screen branding, and the car livery can be customized.'),
     ('Does it work for a general corporate audience?',
      'It works very well as one rig among several. As the only format at a corporate event it can be limiting, '
      'because some guests want a lap time to chase.'),
     ('Do you provide staff to run it?',
      'Yes. Staffing is included, and for drifting it matters more than usual because someone has to coach and '
      'score the runs.')],
    'Drift Simulator Experience For Events',
))

# ----------------------------------------------------------- RALLY ---------
PAGES.append(experience(
    'rally-racing-simulator',
    'Rally Simulator Experience For Events | Academy Sim Racing',
    'Rally simulator experiences for events in Florida. One car against the clock on loose surfaces, with co-driver calls. Unlike anything else at an event.',
    'Rally Experience', 'ONE CAR,<br>ONE CLOCK',
    'Rally is not wheel-to-wheel racing. Guests run alone against a clock on a loose surface, working from a '
    'co-driver calling the road ahead. It is the format nobody expects and the one people remember.',
    'BRING RALLY<br><span class="amber">TO YOUR EVENT.</span>',
    'If you want something that is not another racing activation, ask us about this one.',
    'NOTHING ELSE AT AN EVENT FEELS LIKE IT',
    ['<p>Every other format at your event will be a car on a circuit. Rally is a car on a road, on gravel or '
     'dirt, sliding most of the way, with a voice calling corners the driver cannot see yet.</p>',
     '<p>Acting on a call rather than on what your eyes have confirmed is the genuinely novel part, and it is '
     'what guests talk about afterwards. It is also why rally works as a differentiator when your audience has '
     'seen a racing simulator at three other events this year.</p>',
     '<h3>What guests find surprising</h3>',
     '<ul>'
     '<li>The car spends most of the stage slightly out of shape, which feels alarming and is normal.</li>'
     '<li>There is nobody to race against, so the pressure is entirely against your own previous run.</li>'
     '<li>The co-driver calls make it a listening exercise as much as a driving one.</li>'
     '</ul>'],
    [('01 / Differentiation', 'WHEN CIRCUIT RACING IS EXPECTED', 'Audiences who have seen racing sims before and will not be surprised again.'),
     ('02 / Corporate', 'CORPORATE EVENTS', 'Works well as one rig among several, giving guests a genuine change of pace.'),
     ('03 / Brand', 'OUTDOOR AND ADVENTURE BRANDS', 'A format that fits brands whose world is not tarmac.'),
     ('04 / Community', 'FAMILY AND COMMUNITY DAYS', 'No wheel-to-wheel contact and no way to be held up by another driver.')],
    ['<h3>Stage times</h3>'
     '<p>Everyone runs the same stage and the leaderboard is built from stage times. The closest rally equivalent '
     'to a fastest-lap competition.</p>',
     '<h3>Two runs each</h3>'
     '<p>Guests run the stage twice, and the improvement between runs is the story. It suits rally better than a '
     'single attempt because the first run is largely reconnaissance.</p>',
     '<h3>Open driving</h3>'
     '<p>No timing at all. Guests drive stages and enjoy the surface. Good when rally is one of several rigs.</p>'],
    [('Do guests get co-driver calls?',
      'Yes, and learning to act on them is the part people remember. Our staff explain the system before the '
      'first run.'),
     ('Is it harder than circuit racing?',
      'Different rather than harder. There is no other car to worry about, but the surface offers less grip and '
      'the road is new to the driver.'),
     ('Does it work as the only format at an event?',
      'It can, but it usually works best as one rig among several so guests get a contrast. As a differentiator '
      'alongside circuit racing it is very effective.'),
     ('Is it suitable for a general audience?',
      'Yes. Because there is no wheel-to-wheel racing, nobody gets held up or spun by another guest, which makes '
      'it forgiving in a busy activation.'),
     ('Can it be branded?',
      'Yes, through rig wraps, on-screen branding and the car livery.'),
     ('Do you supply everything?',
      'Yes. Delivery, setup, staffing for the duration and teardown are part of every booking.')],
    'Rally Simulator Experience For Events',
))

# ---------------------------------------------------- WATCH PARTIES --------
PAGES.append(dict(
    slug='watch-parties', url='/event-types/watch-parties/', ctype='event_type',
    title='Race Watch Party Simulator Rental | Florida | Academy Sim Racing',
    desc='Racing simulators for race-day watch parties in Florida. Guests drive the circuit they are watching, on the day, with a live leaderboard alongside the broadcast.',
    crumbs='<a href="/">Events</a> / <a href="/event-types/">Event Types</a> / Watch Parties',
    eyebrow='Watch Parties',
    h1='DRIVE THE CIRCUIT<br>THEY ARE WATCHING',
    lede='A race on a screen is a passive event. Put a simulator running the same circuit next to it and the '
         'room stops being an audience.',
    final_h='HOSTING A<br><span class="amber">RACE WEEKEND?</span>',
    final_p='Tell us the date and the venue. Race weekends book up early, so raise it ahead of time.',
    ld=ld('Service', 'Race Watch Party Simulator Rental',
          'Racing simulator rentals for race-day watch parties in Florida, running the circuit being broadcast, with a live leaderboard.',
          '/event-types/watch-parties/'),
    body='\n\n'.join([
        prose('The Idea', 'THE CIRCUIT ON SCREEN, IN THE ROOM', '', [
            '<p>Watch parties have a structural problem. There is a lot of dead time, and once the running order '
            'settles people stop watching and start talking, which is fine until the interesting part happens '
            'and nobody notices.</p>',
            '<p>A simulator running the same circuit fixes it. Guests who have just driven the track understand '
            'what they are seeing, and the broadcast becomes something to argue about rather than something '
            'playing in the background. The comparison between a guest lap time and the real one is the single '
            'most reliable conversation starter we have seen at these events.</p>',
            '<h3>How it usually runs</h3>',
            '<ul>'
            '<li>Rigs set to the circuit being raced that weekend.</li>'
            '<li>Guests drive between sessions and during the quieter parts of the race.</li>'
            '<li>A leaderboard runs all day, with a prize at the chequered flag.</li>'
            '<li>Driver aids on by default so nobody is stuck while the race is on.</li>'
            '</ul>',
        ]),
        cards('Where It Works', 'VENUES AND HOSTS', '', [
            ('01 / Corporate', 'CLIENT HOSPITALITY',
             'Race weekends as a client entertainment format, where the racing gives everyone something to talk about.'),
            ('02 / Venues', 'BARS AND EVENT SPACES',
             'Venues hosting a race broadcast who want a reason for people to arrive early and stay.'),
            ('03 / Sponsors', 'SPONSOR ACTIVATIONS',
             'Brands with a motorsport tie who want the activation to be credible to an audience that knows the sport.'),
            ('04 / Private', 'PRIVATE PARTIES',
             'Enthusiast groups watching a big race together at a home or private venue.'),
        ]),
        prose('Planning', 'WHAT TO SORT OUT EARLY', '', [
            '<h3>Book ahead of the calendar</h3>',
            '<p>Major race weekends are fixed dates that everyone knows about a year out, so they are the events '
            'that book earliest. If a specific weekend matters to you, raise it well ahead.</p>',
            '<h3>Think about sound</h3>',
            '<p>The broadcast and the simulators compete for the same air. Most hosts run the race audio and keep '
            'the rigs on headphones, which lets both work.</p>',
            '<h3>Decide when people drive</h3>',
            '<p>Free rein all day, or driving only outside the race itself. Both work, but it is worth deciding '
            'in advance so the format is clear to guests.</p>',
            '<div class="note-band"><p>We supply simulators and staff. We do not supply the broadcast, and we are '
            'not affiliated with any racing series or broadcaster. Screening rights for a public event are the '
            'venue&rsquo;s responsibility.</p></div>',
        ]),
        CROSS,
        faq([
            ('Can you set the simulators to the circuit being raced?',
             'Yes, where that circuit is in the software we run. Tell us the weekend and we will confirm.'),
            ('Do you provide the race broadcast?',
             'No. We supply the simulators, the staff and the leaderboard. The broadcast and any screening rights '
             'are the venue or host&rsquo;s responsibility.'),
            ('How do you handle sound?',
             'Most events run the broadcast audio through the room and put the simulators on headphones, so the '
             'race is audible and the drivers still get engine sound.'),
            ('Can guests compare their lap to the real one?',
             'Yes, and it is the thing people enjoy most. It is also a reliable way to get a room talking about '
             'what is happening on the broadcast.'),
            ('How far ahead should we book a race weekend?',
             'Earlier than a normal event. Major race dates are known a long way out and are the first to go.'),
            ('Do you cover venues outside Tampa?',
             'Yes, throughout Florida. Travel and staffing are quoted per event.'),
        ]),
    ]),
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
