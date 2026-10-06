# -*- coding: utf-8 -*-
"""Builds batch 1: /simulators/ hub plus nine configuration pages.

Every spec quoted here comes from the published homepage lineup. No invented
equipment, no new SKUs, no promised real-world performance gains. Each page
ends by routing into one of the five real builds.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builds_prices as P
from builds_pages import (write, section, prose, faq, linkgrid, figure,
                          build_table, CROSS, ld, SITE, LOUNGE)

PAGES = []

NO_PROMISE = (
    '  <div class="callout"><p>A simulator builds familiarity, repetition and consistency. It is practice, '
    'not a substitute for real seat time or instruction, and we do not claim it will make you faster on '
    'track.</p></div>')


def simpage(slug, eyebrow, title, desc, h1, lede, why, seating, wheel, pedals, display,
            software, tactile, builds, note, who, faqs, img=None, imgalt='', imgcap='',
            extra_links=()):
    # the photo sits at the top of the opening section, above the prose
    opening = []
    if img:
        opening.append(figure(img, imgalt, imgcap))
    opening.append('    <div class="prose">')
    opening += ['      ' + b for b in why]
    opening.append('    </div>')

    body = [
        section('The Discipline', 'What this setup <span class="accent">has to do.</span>', '',
                '\n'.join(opening)),
        prose('Configuration', 'How we <span class="accent">spec it.</span>', '', [
            '<h3>Seating position</h3><p>%s</p>' % seating,
            '<h3>Wheelbase</h3><p>%s</p>' % wheel,
            '<h3>Pedals</h3><p>%s</p>' % pedals,
            '<h3>Display</h3><p>%s</p>' % display,
            '<h3>Software</h3><p>%s</p>' % software,
            '<h3>Tactile and motion</h3><p>%s</p>' % tactile,
        ]),
        section('The Lineup', 'Which build <span class="accent">suits it.</span>',
                'These are our existing builds, not special editions. The table is the published spec.',
                build_table(builds, note)),
        prose('Who It Suits', 'Is this <span class="accent">you?</span>', '', who),
        NO_PROMISE,
        linkgrid('Related', 'Keep <span class="accent">reading.</span>', '', list(extra_links) + [
            ('/simulators/', 'ALL SIMULATOR TYPES', 'Compare configurations by the racing you actually do.'),
            ('/for/', 'BY WHO IT IS FOR', 'Track drivers, race teams, collectors, businesses and more.'),
        ]),
        CROSS,
        faq(faqs),
    ]
    return dict(
        slug=slug, url='/simulators/%s/' % slug, ctype='simulator_type',
        title=title, desc=desc,
        crumbs='<a href="/">Builds</a> / <a href="/simulators/">Simulator Types</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede,
        final_h='Build it <span class="accent">properly.</span>',
        final_p='Tell us the racing you do and the space you have. We will spec it against the real lineup.',
        ld=ld('WebPage', title.split(' | ')[0], desc, '/simulators/%s/' % slug),
        body='\n\n'.join(body),
    )


# ---------------------------------------------------------------- HUB ------
PAGES.append(dict(
    slug='simulators', url='/simulators/', ctype='simulator_hub',
    title='Racing Simulator Types And Configurations | Academy Sim Racing Builds',
    desc='How to spec a racing simulator for formula, GT3, stock car, endurance, drift, rally or track day use. Configuration guidance routed into five real Academy builds.',
    crumbs='<a href="/">Builds</a> / Simulator Types',
    eyebrow='Simulator Types',
    h1='Spec it for the racing<br><span class="accent">you actually do.</span>',
    lede='A rig built for endurance racing and a rig built for drifting want different things from the '
         'same budget. This section is about matching the configuration to the discipline, then routing '
         'you into whichever of our five builds fits.',
    final_h='Not sure <span class="accent">which one?</span>',
    final_p='Tell us what you race and where it goes. We will spec it against the real lineup.',
    ld=ld('CollectionPage', 'Racing Simulator Types And Configurations',
          'Configuration guidance for formula, GT3, stock car, endurance, drift, rally, track day, triple screen and motion racing simulators.',
          '/simulators/'),
    body='\n\n'.join([
        prose('Start Here', 'The spec follows <span class="accent">the discipline.</span>', '', [
            '<p>Most people shop for a simulator by price tier, then find out afterwards that the '
            'configuration does not suit what they actually drive. A drifter and an endurance racer can spend '
            'the same money and both end up with the wrong rig.</p>',
            '<h3>What actually changes between disciplines</h3>',
            '<ul>'
            '<li><strong>Field of view.</strong> Wheel-to-wheel racing and drifting need peripheral vision, '
            'which is a triple-screen problem. Time attack and hot lapping do not.</li>'
            '<li><strong>Pedal feel.</strong> Braking-heavy disciplines justify load cell or active pedals '
            'far more than throttle-heavy ones.</li>'
            '<li><strong>Torque.</strong> Higher wheelbase torque buys detail, not difficulty. It matters '
            'most where the front axle is doing subtle things you need to feel.</li>'
            '<li><strong>Controls.</strong> Rally and drift want a handbrake and a shifter. Formula and GT3 '
            'do not use either.</li>'
            '<li><strong>Motion and tactile.</strong> Useful everywhere, decisive in endurance, where you are '
            'reading the car over hours rather than minutes.</li>'
            '</ul>',
            '<p>The pages below cover each discipline and end with the build we would actually put you in.</p>',
        ]),
        linkgrid('By Discipline', 'Pick your <span class="accent">racing.</span>', '', [
            ('/simulators/gt3-racing-simulator/', 'GT3 SIMULATOR',
             'The most common request, and the easiest to spec well.'),
            ('/simulators/formula-racing-simulator/', 'FORMULA SIMULATOR',
             'Open-wheel seating, high torque, and why the pedals matter most here.'),
            ('/simulators/nascar-racing-simulator/', 'STOCK CAR SIMULATOR',
             'Oval racing, close-quarters awareness and sustained loads.'),
            ('/simulators/imsa-endurance-racing-simulator/', 'ENDURANCE SIMULATOR',
             'Multi-class awareness, long stints and why comfort becomes a spec item.'),
            ('/simulators/drift-racing-simulator/', 'DRIFT SIMULATOR',
             'Handbrake, shifter, fast wheel response and a wide field of view.'),
            ('/simulators/rally-racing-simulator/', 'RALLY SIMULATOR',
             'Handbrake, sequential shifting and surfaces that never settle.'),
            ('/simulators/track-day-racing-simulator/', 'TRACK DAY SIMULATOR',
             'For HPDE and club drivers preparing for real events.'),
            ('/simulators/triple-screen-racing-simulator/', 'TRIPLE SCREEN',
             'When peripheral vision is worth more than pixel density.'),
            ('/simulators/motion-racing-simulator/', 'MOTION SIMULATOR',
             'What a motion platform adds, and when it is worth it.'),
        ]),
        section('The Lineup', 'Five builds, <span class="accent">real specs.</span>',
                'Every recommendation on these pages routes into one of these. Nothing on this site is a '
                'special edition invented for a landing page.',
                build_table(['rookie', 'base', 'club-oled', 'club-triple', 'pole-position'],
                            'Published lineup as shown on our homepage. Displays scale with the tier; '
                            'the wheelbase and pedal philosophy is what changes the driving.')),
        CROSS,
        faq([
            ('Do I need a different simulator for each discipline?',
             'No. Every build here runs every discipline. What changes is how well the configuration suits '
             'the one you spend most of your time in, and which optional controls you add.'),
            ('Is more wheelbase torque always better?',
             'No. Past a point extra torque buys detail rather than difficulty, and the pedals usually do '
             'more for lap time than the wheel does. We would rather put you on better pedals than more Nm '
             'you will never use.'),
            ('Triples or a single ultrawide?',
             'Triples for wheel-to-wheel racing and drifting, where peripheral vision does real work. A '
             'single 49 inch ultrawide is excellent for hot lapping and takes less space. That is the Club '
             'Triple versus Club OLED decision.'),
            ('Can I add a shifter and handbrake later?',
             'Yes. Drift and rally controls are additions rather than a different chassis, so a build can '
             'grow into them.'),
            ('Can I try one before buying?',
             'Yes, and we would encourage it. The components in these builds are the ones we run daily in '
             'the Tampa lounge, so you can drive the wheelbase and pedals before you commit.'),
            ('Do you ship outside Florida?',
             'Yes. Nationwide shipping, with a two to four week build time.'),
        ]),
    ]),
))

# ------------------------------------------------------------------ GT3 ----
PAGES.append(simpage(
    'gt3-racing-simulator', 'GT3',
    'GT3 Racing Simulator Build | Academy Sim Racing',
    'How to spec a GT3 racing simulator: seating, wheelbase, pedals, triple screens and tactile. Routed into five real Academy builds from %s.' % P.ENTRY,
    'GT3 simulator<br><span class="accent">done properly.</span>',
    'GT3 is the most requested configuration we build, and the easiest to get right, because the cars are '
    'forgiving enough that the spec can be balanced rather than specialized.',
    ['<p>GT3 cars carry traction control and anti-lock brakes, shift with paddles and generate real '
     'downforce. That combination means the rig does not have to compensate for a twitchy car. What it does '
     'have to do is give you enough field of view to race other people closely, and enough pedal feel to '
     'brake consistently lap after lap.</p>',
     '<p>Almost everyone who buys a rig for GT3 racing is doing it to race online against other drivers. '
     'That is a wheel-to-wheel discipline, and it changes the priorities: awareness of what is beside you '
     'matters more than raw torque.</p>'],
    'Upright and close to a road car. GT3 seating is the most comfortable configuration we build, which '
    'matters if you are racing hour-long stints.',
    'A 15Nm base is genuinely enough for GT3. Stepping to 25Nm buys detail rather than capability. If your '
    'budget has to choose between wheelbase torque and pedals, choose the pedals.',
    'This is where the money goes. GT3 braking is heavy and repeatable, so a load cell is the floor and '
    'active pedals are the meaningful upgrade. Consistency in the braking zone is what separates lap times.',
    'Triples if you race other cars. A single 49 inch ultrawide is excellent for hot lapping but you will '
    'feel the missing peripheral vision the first time somebody puts a nose up your inside.',
    'iRacing is where most competitive GT3 racing happens. Assetto Corsa Competizione is the other common '
    'choice. Both run on every build here.',
    'A Buttkicker is on every build from Base upward and does more for GT3 than most people expect, because '
    'it tells you about curb strikes and wheelspin you would otherwise only see.',
    ['base', 'club-oled', 'club-triple'],
    'For GT3 specifically we would point most people at Club Triple. The field of view is worth more in '
    'wheel-to-wheel racing than the OLED panel is.',
    ['<p>This configuration suits you if you race online in organized series, run endurance events with a '
     'team, or want one rig that does everything competently rather than one discipline brilliantly.</p>',
     '<p>It is probably not the right starting point if you mainly drift or rally, where a shifter and '
     'handbrake change the specification meaningfully.</p>'],
    [('Do I need triple screens for GT3?',
      'For racing other people, they earn their place. For hot lapping alone, a 49 inch ultrawide is '
      'excellent and takes less room. Club Triple and Club OLED are the same money and that is the choice.'),
     ('Is 15Nm enough, or do I need 25Nm?',
      'Fifteen is genuinely enough for GT3. Twenty-five gives you more detail, not more capability. We would '
      'rather see the budget go into pedals.'),
     ('Which pedals matter most?',
      'The brake. GT3 braking is heavy and has to be repeatable, so a load cell is the minimum and active '
      'pedals are the upgrade that actually shows up in your consistency.'),
     ('Can I use the same rig for endurance racing?',
      'Yes. GT3 and endurance specs overlap almost entirely. See the endurance page for the differences '
      'that matter over long stints.'),
     ('Which build do most GT3 buyers choose?',
      'Base and Club Triple are the two most common. Base if this is a first serious rig, Club Triple if you '
      'are already racing regularly.'),
     ('Can I try GT3 on your rigs first?',
      'Yes. Book a session at the Tampa lounge and drive the wheelbase and pedals before committing.')],
    img='club-triple.jpg', imgalt='Academy Club Triple simulator build with three curved displays',
    imgcap='Club Triple, the common GT3 choice',
    extra_links=(('/simulators/imsa-endurance-racing-simulator/', 'ENDURANCE SIMULATOR',
                  'Where the GT3 spec changes for long stints and multi-class traffic.'),),
))

# -------------------------------------------------------------- FORMULA ----
PAGES.append(simpage(
    'formula-racing-simulator', 'Formula',
    'Formula Racing Simulator Build | Open-Wheel | Academy Sim Racing',
    'How to spec a formula-style open-wheel racing simulator: seating angle, wheelbase torque, pedal pressure and display. Five real Academy builds from %s.' % P.ENTRY,
    'Formula simulator<br><span class="accent">for open-wheel.</span>',
    'Open-wheel is the configuration people ask for by name and the one where the seating position and the '
    'brake pedal matter most. Get those two right and the rest follows.',
    ['<p>Formula-style cars are light, generate a great deal of aerodynamic load and in most classes have no '
     'traction control. What you feel through the wheel is more detailed and arrives faster than in a GT car, '
     'which is why wheelbase quality shows up here more than in any other discipline.</p>',
     '<p>The braking is the other half. Open-wheel braking is extremely high pressure and extremely short, '
     'so the pedal has to give you the same feedback every single time or you will lock a wheel.</p>'],
    'Reclined, legs up, close to a real single-seater. This is the configuration where seating position '
    'changes the driving most, because your relationship to the pedals is completely different from a road '
    'car. Every build here can be set up this way.',
    'This is the one discipline where we would say the higher torque option earns its money. The front axle '
    'in an open-wheel car communicates constantly, and 25Nm resolves detail that 15Nm smooths over.',
    'Pressure-based, always. Open-wheel drivers brake with far more force than they expect, and a load cell '
    'is the minimum. Active pedals are the genuine upgrade here rather than a luxury.',
    'Either works. Open-wheel racing is more about precision on a known circuit than about peripheral '
    'awareness, so a single 49 inch ultrawide is a defensible choice. Triples still help in traffic.',
    'iRacing has the deepest open-wheel competition. Assetto Corsa is the common alternative. Both run on '
    'every build here.',
    'A Buttkicker helps you feel wheelspin, which matters more with no traction control. Motion is a genuine '
    'step for open-wheel because the braking and cornering forces are so much higher than in a road car.',
    ['club-oled', 'club-triple', 'pole-position'],
    'For open-wheel we would steer toward the 25Nm builds. This is the discipline where the wheelbase is '
    'doing the most work.',
    ['<p>This suits you if you race open-wheel online, if you follow single-seater racing closely, or if you '
     'want the most demanding thing a home rig can give you.</p>',
     '<p>If most of your driving is GT3 or endurance, spec for that instead. Open-wheel will still run '
     'perfectly well on a GT3-focused rig.</p>'],
    [('Is this an official Formula 1 simulator?',
      'No. We are not affiliated with, endorsed by or licensed by Formula 1 or any racing series. We build '
      'simulators that run commercially available racing software.'),
     ('Do I really need 25Nm?',
      'For open-wheel it is the one place we would argue yes. The front axle communicates constantly and the '
      'extra torque resolves detail that gets smoothed away at 15Nm.'),
     ('Why do the pedals matter so much here?',
      'Open-wheel braking is very high pressure and very short. Without a pressure-based pedal you are '
      'guessing, and you will lock a wheel.'),
     ('Can I set the seat up like a real single-seater?',
      'Yes. Every build can be configured reclined with the pedals raised. Tell us that is your intent when '
      'you order and we will set it up that way.'),
     ('Triples or ultrawide for open-wheel?',
      'Either is defensible. Open-wheel rewards precision on a known circuit more than peripheral awareness, '
      'so an ultrawide is a genuine option here in a way it is not for drifting.'),
     ('Which build do open-wheel drivers choose?',
      'Club OLED and Club Triple most often, and Pole Position where motion is part of the brief.')],
    img='pole-position.jpg', imgalt='Academy Pole Position simulator build with triple OLED displays and motion',
    imgcap='Pole Position, the flagship',
))

# ------------------------------------------------------------ STOCK CAR ----
PAGES.append(simpage(
    'nascar-racing-simulator', 'Stock Car',
    'Stock Car Racing Simulator Build | Oval Racing | Academy Sim Racing',
    'How to spec a stock car and oval racing simulator: field of view, sustained wheel loads, pedal feel and tactile. Five real Academy builds from %s.' % P.ENTRY,
    'Stock car simulator<br><span class="accent">for oval racing.</span>',
    'Oval racing looks simple and is not. The car moves around underneath you constantly, you run inches '
    'from other cars for a long time, and the spec that suits it is not the one that suits road racing.',
    ['<p>Stock cars are heavy, powerful and short on aerodynamic help, so the car is always moving. Small '
     'corrections, held for a long time, are the whole discipline. That puts sustained load through the '
     'wheel rather than the sharp transitions a road course produces.</p>',
     '<p>The other defining feature is proximity. You spend an entire race within a car length of somebody, '
     'which makes peripheral vision genuinely functional rather than a nice-to-have.</p>'],
    'Upright and stable. Oval racing is long-duration, so comfort over a full race matters more than an '
    'aggressive position.',
    'Sustained rather than peak load is what you are feeling, so headroom matters less here than in '
    'open-wheel. A 15Nm base handles oval racing comfortably.',
    'Less braking-critical than road racing, but throttle modulation is everything on an oval. A load cell '
    'brake is still the sensible floor.',
    'Triples make a real difference here. Racing three-wide is the discipline, and you cannot do it if you '
    'cannot see beside you.',
    'iRacing is where organized oval racing happens, by a wide margin. It runs on every build here.',
    'A Buttkicker is genuinely useful on ovals because it tells you when the rear is starting to go, which '
    'on an oval is a slow build rather than a sudden snap.',
    ['base', 'club-triple'],
    'For oval racing specifically, Club Triple over Club OLED. The field of view does more for three-wide '
    'racing than panel quality does.',
    ['<p>This suits you if you race ovals online, if you follow stock car racing, or if you want a '
     'configuration built around close-quarters racing rather than lap time alone.</p>',
     '<p>Oval-focused buyers are also the group most likely to be happy at the Base tier, because the '
     'discipline asks less of the wheelbase than open-wheel does.</p>'],
    [('Is this an official NASCAR simulator?',
      'No. We are not affiliated with, endorsed by or licensed by NASCAR or any racing series. We build '
      'simulators that run commercially available racing software.'),
     ('Do I need triples for oval racing?',
      'More than for almost anything else. Racing three-wide is the point, and you need to see beside you '
      'to do it.'),
     ('Is 15Nm enough for stock cars?',
      'Yes. Oval racing is about sustained load rather than sharp peaks, so wheelbase headroom matters less '
      'here than in open-wheel.'),
     ('Do I need a shifter?',
      'Not for oval racing. If you also run road courses in stock cars, a shifter can be added.'),
     ('What does the Buttkicker actually do on an oval?',
      'It tells you the rear is going before you can see it. On an oval that is a gradual build rather than '
      'a snap, so feeling it early is genuinely useful.'),
     ('Which build suits an oval racer?',
      'Base is a very reasonable stopping point. Club Triple if you want the field of view for three-wide '
      'racing.')],
    img='triple.jpg', imgalt='Academy triple screen simulator setup',
    imgcap='Triple screens for close-quarters racing',
))

# ------------------------------------------------------------ ENDURANCE ----
PAGES.append(simpage(
    'imsa-endurance-racing-simulator', 'Endurance',
    'Endurance Racing Simulator Build | Multi-Class | Academy Sim Racing',
    'How to spec an endurance racing simulator: comfort over long stints, multi-class awareness, active pedals and motion. Five real Academy builds from %s.' % P.ENTRY,
    'Endurance simulator<br><span class="accent">for the long ones.</span>',
    'Endurance is the discipline where the rig stops being a toy and starts being equipment. Anything that '
    'is slightly uncomfortable in a twenty minute race becomes the reason you make a mistake at hour four.',
    ['<p>Endurance racing asks two things nothing else does. You have to be consistent for hours rather than '
     'minutes, and you have to share a circuit with cars of very different speed.</p>',
     '<p>Both change the spec. Comfort becomes a performance item rather than a luxury, and field of view '
     'becomes safety-critical, because a large part of the job is knowing what is beside you and what class '
     'it is.</p>',
     '<h3>Why motion earns its place here</h3>',
     '<p>Over a long stint you are reading small changes in the car as the tires go off and the fuel load '
     'drops. A motion platform gives you another channel for that information, which is worth more across '
     'four hours than across four laps.</p>'],
    'This is the configuration where seat comfort is a genuine spec decision. Upright, supported, and set '
    'up so you are not compensating for the seat after the first hour.',
    'Either 15Nm or 25Nm works. Detail matters over a long stint, but so does not fighting the wheel, and '
    'the difference is smaller here than in open-wheel.',
    'Active pedals earn their money in endurance more than anywhere. Repeatability across hundreds of '
    'braking events is exactly what they are for.',
    'Triples, without much argument. Multi-class racing means constant awareness of faster and slower '
    'traffic, and that is a peripheral vision problem.',
    'iRacing runs the deepest organized endurance racing, including team events with driver swaps. Assetto '
    'Corsa Competizione is the other common choice.',
    'A Buttkicker on every build from Base upward. Motion is the meaningful step, and endurance is the '
    'discipline where we would most readily recommend it.',
    ['club-triple', 'pole-position'],
    'Club Triple is the sensible endurance build. Pole Position adds D-BOX motion, which is the upgrade '
    'this discipline benefits from most.',
    ['<p>This suits you if you run team endurance events, multi-class racing, or long stints of any kind. '
     'It also suits anyone who simply spends a lot of hours in the seat, because the same comfort argument '
     'applies.</p>',
     '<p>If your racing is twenty minute sprints, spec for GT3 instead and save the money.</p>'],
    [('Is this an official IMSA simulator?',
      'No. We are not affiliated with, endorsed by or licensed by IMSA or any racing series. We build '
      'simulators that run commercially available racing software.'),
     ('Is motion worth it for endurance?',
      'It is the discipline where we would most readily say yes. Over hours you are reading small changes in '
      'the car, and motion is another channel for that information.'),
     ('Why do active pedals matter more here?',
      'Repeatability across hundreds of braking events. That is precisely what they are built for, and over '
      'a long stint it compounds.'),
     ('Do I need triples for multi-class racing?',
      'Effectively yes. Knowing what is beside you and what class it is is a large part of the job, and that '
      'is peripheral vision.'),
     ('Can two drivers share the rig for team events?',
      'Yes. Seat and pedal position adjust, and driver swaps are part of how organized endurance racing '
      'works.'),
     ('Which build for endurance?',
      'Club Triple, or Pole Position if motion is in budget.')],
    img='club-oled.jpg', imgalt='Academy Club OLED simulator build',
    imgcap='Comfort becomes a spec item over long stints',
    extra_links=(('/simulators/gt3-racing-simulator/', 'GT3 SIMULATOR',
                  'The overlapping spec, and where the two differ.'),),
))

# ---------------------------------------------------------------- DRIFT ----
PAGES.append(simpage(
    'drift-racing-simulator', 'Drift',
    'Drift Simulator Build | Handbrake And Shifter | Academy Sim Racing',
    'How to spec a drift simulator: handbrake, H-pattern shifter, fast wheel response and wide field of view. Five real Academy builds from %s.' % P.ENTRY,
    'Drift simulator<br><span class="accent">built for angle.</span>',
    'Drifting is the one discipline where the controls change the build rather than the tier. A handbrake '
    'and a shifter are not accessories here, they are the point.',
    ['<p>Everything else on this site is judged on lap time. Drifting is judged on angle, line and '
     'commitment, and that changes what the rig has to do. You are holding the car in a sustained slide and '
     'making constant corrections, which puts a completely different demand on the wheel.</p>',
     '<p>What matters is how fast the wheel returns, not how hard it pulls. A wheelbase that responds '
     'quickly lets you catch a slide. One that is merely strong does not.</p>'],
    'Upright and fairly close, so you can work the wheel through large, fast movements without running out '
    'of arm.',
    'Response speed over raw torque. A 15Nm base is entirely sufficient for drifting, and we would rather '
    'see the money go into the handbrake, shifter and screens.',
    'Load cell brake is fine. Drifting is throttle-led, and pedal spend matters less here than in almost any '
    'other discipline.',
    'Triples, clearly. You are pointing the car somewhere other than where it is travelling, so peripheral '
    'vision is not optional. This is the strongest triple-screen argument of any discipline.',
    'Assetto Corsa is where most serious drift content lives, with a large community. It runs on every '
    'build here.',
    'A Buttkicker helps you feel the rear breaking traction. Motion is less critical here than in endurance, '
    'because the information you need is mostly in the wheel.',
    ['base', 'club-triple'],
    'Base with a handbrake and shifter added is a strong drift rig. Club Triple if the field of view '
    'matters, which for drifting it does.',
    ['<p>This suits you if drifting is what you actually do, rather than something you try occasionally. '
     'The handbrake and shifter are the difference between practicing the discipline and approximating it.</p>',
     '<p>If you race circuits and want to drift sometimes, spec for the racing and add the controls.</p>'],
    [('Do I need a handbrake to drift?',
      'To practice it properly, yes. Initiating and adjusting with the handbrake is part of the discipline, '
      'and without one you are approximating it.'),
     ('Do I need an H-pattern shifter?',
      'Most drift cars use a manual gearbox, so a shifter makes the practice realistic. It is an addition '
      'rather than a different chassis.'),
     ('Is more torque better for drifting?',
      'No. Response speed matters more than strength. A 15Nm base is entirely sufficient and the money is '
      'better spent on controls and screens.'),
     ('Why do triples matter so much here?',
      'You are pointing the car somewhere other than where it is going. Without peripheral vision you cannot '
      'see where you are actually headed.'),
     ('Which software for drifting?',
      'Assetto Corsa, where most of the serious drift community and content lives.'),
     ('Can I add drift controls to a rig later?',
      'Yes. The handbrake and shifter are additions, so a build can grow into drifting.')],
    img='handbrake.jpg', imgalt='Handbrake fitted to an Academy simulator build',
    imgcap='The handbrake is the discipline, not an accessory',
    extra_links=(('/simulators/rally-racing-simulator/', 'RALLY SIMULATOR',
                  'The other discipline where the handbrake changes the build.'),),
))

# ---------------------------------------------------------------- RALLY ----
PAGES.append(simpage(
    'rally-racing-simulator', 'Rally',
    'Rally Simulator Build | Handbrake And Sequential | Academy Sim Racing',
    'How to spec a rally simulator: handbrake, sequential shifting, loose-surface feel and field of view. Five real Academy builds from %s.' % P.ENTRY,
    'Rally simulator<br><span class="accent">for loose surfaces.</span>',
    'Rally is the discipline where the car is never settled. The rig has to communicate a surface that '
    'changes under you constantly, and give you the controls to react to it.',
    ['<p>On a circuit you learn a fixed piece of road and refine it. On a stage you work from a co-driver '
     'calling corners you cannot see yet, on a surface with far less grip than tarmac, and the car spends '
     'most of the run slightly out of shape.</p>',
     '<p>That puts a premium on feeling the surface through the wheel and on being able to place the car '
     'with the handbrake. It puts far less premium on outright wheelbase torque.</p>'],
    'Upright and supported. Rally is physically busy, with constant correction, so you want to be braced '
    'rather than reclined.',
    'Detail over strength. Loose surfaces communicate through small, fast changes, so response matters more '
    'than peak torque. A 15Nm base is genuinely sufficient.',
    'Load cell brake. Rally braking is less about maximum pressure than about modulation on a surface that '
    'keeps changing.',
    'Triples help, because stages are narrow and your eyes need to be a long way down the road. A single '
    'ultrawide is workable if space is limited.',
    'Rally titles vary and change more often than circuit racing software. Tell us what you intend to run '
    'and we will confirm compatibility rather than guess.',
    'A Buttkicker is genuinely valuable on loose surfaces because so much of what you need to know is '
    'surface texture. Motion adds to that.',
    ['base', 'club-triple'],
    'Base with a handbrake is a capable rally rig. Club Triple if you want the field of view for narrow '
    'stages.',
    ['<p>This suits you if rally is your main discipline, or if you want something genuinely different from '
     'circuit racing. It is also the configuration that overlaps most with drifting, so the two can share '
     'a build.</p>'],
    [('Do I need a handbrake for rally?',
      'For tighter corners it is genuinely useful, though technique varies with the car and the surface. '
      'Most people who rally seriously want one.'),
     ('Sequential or H-pattern for rally?',
      'Depends on the era and car you want to drive. Modern rally cars are sequential, older ones use an '
      'H-pattern. Tell us what you intend to run.'),
     ('Do I need high wheelbase torque?',
      'No. Loose surfaces communicate through small fast changes, so response matters more than strength. '
      'Fifteen Nm is genuinely sufficient.'),
     ('Which software should I run?',
      'Rally titles change more often than circuit racing software, so we would rather confirm compatibility '
      'against what you actually want to run than name something that may have moved on.'),
     ('Can one rig do rally and drifting?',
      'Yes, and they overlap more than any other pair. Both want a handbrake, both are about car control '
      'past the limit.'),
     ('Which build for rally?',
      'Base with a handbrake covers it well. Club Triple for the field of view on narrow stages.')],
    img='rally-spec.jpg', imgalt='Academy rally spec simulator build',
    imgcap='Rally spec, built around the handbrake',
    extra_links=(('/simulators/drift-racing-simulator/', 'DRIFT SIMULATOR',
                  'The closest configuration, and where they differ.'),),
))

# ------------------------------------------------------------ TRACK DAY ----
PAGES.append(simpage(
    'track-day-racing-simulator', 'Track Day',
    'Track Day Simulator Build For HPDE Drivers | Academy Sim Racing',
    'How to spec a simulator for HPDE and track day drivers: circuit familiarity, braking repetition and the builds that suit. From %s.' % P.ENTRY,
    'Track day simulator<br><span class="accent">for real drivers.</span>',
    'If you already drive on track, a simulator is not a substitute for seat time. It is the thing that '
    'stops you spending your first paid session working out which way the circuit goes.',
    ['<p>Track time is expensive and there is never enough of it. The part a simulator genuinely takes off '
     'your hands is orientation: knowing the sequence of corners, which way they go, what follows what, and '
     'which ones matter because they lead onto a straight.</p>',
     '<p>What does not transfer is the feel of your real car, the grip on the day, or your braking '
     'references. Those you build on site with an instructor. Anyone selling you more than that is '
     'overselling.</p>',
     '<h3>What actually helps</h3>',
     '<ul>'
     '<li><strong>Learning the circuit before you arrive.</strong> The single biggest return.</li>'
     '<li><strong>Braking repetition.</strong> Hundreds of braking events you could never afford on track.</li>'
     '<li><strong>Recovering from mistakes.</strong> Practicing a slide costs nothing here.</li>'
     '<li><strong>Traffic and racecraft.</strong> If you are moving toward club racing.</li>'
     '</ul>'],
    'Set it up like your actual car rather than like a race car. If you drive a road-based track car, an '
    'upright position transfers better than a reclined one.',
    'Fifteen Nm is plenty. You are practicing sequence and consistency rather than chasing the last tenth, '
    'and the money is better spent on pedals.',
    'The most important component for this use case. Braking repetition is the thing you cannot practice '
    'anywhere else, and a load cell is the minimum for it to mean anything.',
    'Either. A single 49 inch ultrawide is entirely adequate for learning circuits. Triples help if you are '
    'moving toward wheel-to-wheel club racing.',
    'iRacing and Assetto Corsa between them cover the circuits you are most likely to be running in Florida '
    'and nationally.',
    'A Buttkicker helps you feel curbs and wheelspin, which is useful when learning a circuit. Motion is a '
    'genuine benefit but not necessary for this use case.',
    ['rookie', 'base', 'club-oled'],
    'For most track day drivers, Base is the sensible build. Rookie is a real entry point if this is your '
    'first rig.',
    ['<p>This suits you if you run HPDE days, club events or an occasional track weekend and want to arrive '
     'already knowing the circuit. It is the most common reason people who already drive on track buy a '
     'rig.</p>',
     '<p>Our <a href="%s/tracks/">track guides</a> cover specific Florida circuits in more detail.</p>' % LOUNGE],
    [('Will a simulator make me faster on track?',
      'We will not claim that. What it reliably does is remove orientation from your first session, so your '
      'paid track time goes on driving rather than learning which way the circuit goes.'),
     ('Should I practice my braking points at home?',
      'Learn where the corners are, not where to brake. Real braking references depend on your car, your '
      'tires and the conditions, and your instructor sets them on the day.'),
     ('Do I need triples?',
      'Not for learning circuits. A single 49 inch ultrawide does that job well. Triples matter more if you '
      'are moving toward wheel-to-wheel racing.'),
     ('Which build should a track day driver get?',
      'Base for most people. Rookie is a genuine entry point if this is a first rig and the budget is tight.'),
     ('Can I practice the specific circuit I am running?',
      'If it is in the software, yes. Tell us which circuits matter to you and we will confirm before you '
      'buy rather than after.'),
     ('Can I try one before I commit?',
      'Yes. The components in these builds are the ones we run daily in the Tampa lounge.')],
    img='lifestyle-driver.jpg', imgalt='Driver seated in an Academy simulator build',
    imgcap='Built for people who already drive on track',
))

# -------------------------------------------------------- TRIPLE SCREEN ----
PAGES.append(simpage(
    'triple-screen-racing-simulator', 'Triple Screen',
    'Triple Screen Racing Simulator Build | Academy Sim Racing',
    'When triple screens are worth it versus a single ultrawide, and how we spec them. Club Triple at %s and Pole Position at %s.' % (P.PRICE['club-triple'], P.PRICE['pole-position']),
    'Triple screen<br><span class="accent">or ultrawide?</span>',
    'This is the question we get asked most, and the honest answer is that it depends entirely on whether '
    'you race other people.',
    ['<p>Triple screens buy peripheral vision. That is the whole argument. They do not make the car faster '
     'or the physics better, and a good single ultrawide will often look sharper.</p>',
     '<h3>When triples are clearly right</h3>',
     '<ul>'
     '<li><strong>Wheel-to-wheel racing.</strong> You need to see the car alongside you, not guess.</li>'
     '<li><strong>Oval racing.</strong> Three-wide is the discipline.</li>'
     '<li><strong>Drifting.</strong> You are pointing the car somewhere other than where it is going.</li>'
     '<li><strong>Multi-class endurance.</strong> Knowing what is closing on you is most of the job.</li>'
     '</ul>',
     '<h3>When an ultrawide is the better buy</h3>',
     '<ul>'
     '<li><strong>Hot lapping and time attack.</strong> No traffic to see.</li>'
     '<li><strong>Limited space.</strong> One panel has a much smaller footprint.</li>'
     '<li><strong>You want the best image quality per dollar.</strong> A 49 inch QD-OLED is a better panel '
     'than three good LCDs.</li>'
     '</ul>'],
    'Unchanged either way. What changes is how far you sit from the displays and how the side panels are '
    'angled, which we set during installation.',
    'Unchanged. Display choice and wheelbase are independent decisions.',
    'Unchanged. Do not let the display decision eat the pedal budget.',
    'This is the decision. Club OLED gives you a 49 inch QD-OLED at 240Hz. Club Triple gives you three 32 '
    'inch curved panels at 165Hz. Same money, different priority.',
    'Both configurations run everything. Triple screen support is standard in iRacing and Assetto Corsa.',
    'Independent of display choice. Both Club builds include a Buttkicker.',
    ['club-oled', 'club-triple', 'pole-position'],
    'Club OLED and Club Triple are a thousand dollars apart and represent the two answers to this question. '
    'Pole Position gives you triple OLED and does not make you choose.',
    ['<p>Choose triples if you race other people. Choose the ultrawide if you mostly drive alone or space is '
     'tight. If you cannot decide, come and drive both at the lounge, which is the fastest way to settle '
     'it.</p>'],
    [('Are triples better than an ultrawide?',
      'Not universally. They are better for racing other people and worse for image quality per dollar. It '
      'is a genuine trade, not an upgrade.'),
     ('How much more space do triples need?',
      'Meaningfully more width. If your room is tight, that alone can settle the decision. Tell us your '
      'space and we will tell you what fits.'),
     ('Does a triple setup need a more powerful computer?',
      'Driving three panels is more demanding than driving one. We spec the machine to the display '
      'configuration so this is handled as part of the build.'),
     ('Can I start with one screen and add two later?',
      'It is possible but not free, because the mounting and the machine both change. If you know you want '
      'triples, buying them once is cheaper.'),
     ('Which do most buyers choose?',
      'It splits fairly evenly, which is why both Club builds exist at nearly the same price.'),
     ('Can I compare them before deciding?',
      'Yes, and for this decision we would strongly suggest it. Both configurations are running in the '
      'Tampa lounge.')],
    img='triple.jpg', imgalt='Academy triple screen simulator build',
    imgcap='Club Triple, three 32 inch curved panels',
))

# --------------------------------------------------------------- MOTION ----
PAGES.append(simpage(
    'motion-racing-simulator', 'Motion',
    'Motion Racing Simulator Build | D-BOX | Academy Sim Racing',
    'What a motion platform actually adds to a racing simulator, when it is worth it, and the Academy build that includes D-BOX motion.',
    'Motion simulator<br><span class="accent">and when it is worth it.</span>',
    'Motion is the most misunderstood thing we sell. It does not simulate g-force, and anyone telling you '
    'it does is selling something. What it does is give you another channel of information.',
    ['<p>A motion platform cannot reproduce sustained cornering load. Nothing in a home simulator can, '
     'because you are not actually accelerating. What a platform does reproduce is the transitions: the '
     'pitch under braking, the roll into a corner, the moment the rear starts to rotate.</p>',
     '<p>Those transitions are exactly the information you use to catch a slide, and getting them through '
     'your body rather than only through your eyes and hands is a genuine difference. It is also why motion '
     'matters most over long stints, where you are reading small changes in the car over hours.</p>',
     '<h3>Be honest about whether you need it</h3>',
     '<p>Motion is the largest single cost step in the lineup. For most buyers, better pedals and a better '
     'display will do more for their driving than a platform will. We would rather tell you that than sell '
     'you the flagship.</p>'],
    'Unchanged, but the whole seating structure moves, so installation is more involved and the space '
    'requirement is larger.',
    'Unchanged. Pole Position carries the same 25Nm options as the Club builds.',
    'Unchanged, and still where we would send the budget first if motion is a stretch.',
    'Pole Position pairs motion with triple OLED. The two upgrades are independent in principle but this is '
    'how the flagship is configured.',
    'Motion support is handled at the platform level and works with the racing software these builds run.',
    'This is the page. D-BOX actuators on Pole Position, with a Buttkicker alongside on every build from '
    'Base upward. Tactile and motion do different jobs and complement each other.',
    ['club-triple', 'pole-position'],
    'Pole Position is the motion build. Club Triple is what we would suggest if motion is not in budget, '
    'because it puts the money into field of view instead.',
    ['<p>Motion suits you if you run long stints, if you race at a level where catching slides early '
     'matters, or if the rig is a centerpiece as much as a tool.</p>',
     '<p>It does not suit you if the budget is tight. Pedals and display do more for most drivers.</p>'],
    [('Does motion simulate g-force?',
      'No. Nothing in a home simulator can reproduce sustained cornering load, because you are not actually '
      'accelerating. Motion reproduces transitions: pitch, roll and rotation.'),
     ('Will motion make me faster?',
      'We will not claim that. It gives you another channel of information, particularly for catching slides '
      'and for reading the car over long stints.'),
     ('Is motion worth it over better pedals?',
      'For most buyers, no. Pedals and display do more for your driving. Motion is the right call when '
      'those are already sorted.'),
     ('How much space does a motion rig need?',
      'More than a static build, because the whole seating structure moves. Tell us your room and we will '
      'confirm before you order.'),
     ('Which build has motion?',
      'Pole Position, at %s, with D-BOX actuators and triple OLED.' % P.PRICE['pole-position']),
     ('Can I feel the difference before buying?',
      'Yes, and for this decision we would insist on it. There is a motion rig in the Tampa lounge.')],
    img='pole-position.jpg', imgalt='Academy Pole Position motion simulator build',
    imgcap='Pole Position, with D-BOX motion',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-56s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
