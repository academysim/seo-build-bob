# -*- coding: utf-8 -*-
"""Driver batch 3: /training/ hub plus six driving skill pages.

Educational topic pages. Their job is to be genuinely useful to a parent,
student or teacher searching the skill, and to route institutional readers to
the school and district pages. No claims about installations, no promises about
outcomes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver_pages import write, sec, prose, cards, faq, linkgrid, NO_INSTALLS, ld

PAGES = []

RELATED = linkgrid('Related', 'Where this is taught', '', [
    ('/training/', 'ALL SKILLS', 'The other driving skills we cover.'),
    ('/schools/', 'SCHOOL PROGRAMS', 'How schools can bring these programs in.'),
    ('/school-districts/', 'FLORIDA DISTRICTS', 'District-level program information.'),
])


def topic(slug, eyebrow, title, desc, h1, lede, why, teach, practice, faqs, ldname):
    return dict(
        slug=slug, url='/training/%s/' % slug, ctype='training_topic',
        title=title, desc=desc,
        crumbs='<a href="/">Home</a> / <a href="/training/">Training</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede,
        cta1='Ask About Training',
        final_h='Work on this properly',
        final_p='Whether you are a parent, a student or a school, tell us what you are trying to improve '
                'and we will tell you honestly whether we can help.',
        ld=ld('WebPage', ldname, desc, '/training/%s/' % slug),
        body='\n\n'.join([
            prose('Why It Matters', 'The problem', '', why),
            prose('The Skill', 'What good looks like', '', teach),
            prose('Practicing It', 'Where a simulator helps, and where it does not', '', practice),
            NO_INSTALLS,
            RELATED,
            faq(faqs),
        ]),
    )


# ---------------------------------------------------------------- HUB -----
PAGES.append(dict(
    slug='training', url='/training/', ctype='training_hub',
    title='Driving Skills and Teen Driver Training Topics | Academy',
    desc='Defensive driving, hazard recognition, wet and night driving, emergency braking and manual transmission. What each skill involves and how simulators can help.',
    crumbs='<a href="/">Home</a> / Training',
    eyebrow='Driving Skills',
    h1='The skills that actually keep new drivers safe',
    lede='Passing a test and being a safe driver are different achievements. These pages cover the skills '
         'that sit in the gap, what each one involves, and how a simulator can and cannot help.',
    cta1='Ask About Training',
    final_h='Want help with any of these?',
    final_p='Parents, students and schools all ask about these. Tell us the situation and we will tell you '
            'what we can do.',
    ld=ld('CollectionPage', 'Driving Skills And Teen Driver Training Topics',
          'Guidance on defensive driving, hazard recognition, wet and night driving, emergency braking and manual transmission.',
          '/training/'),
    body='\n\n'.join([
        prose('Start Here', 'The gap between licensed and safe', '', [
            '<p>Florida gives a learner license from age 15 and a Class E license from 16, provided the '
            'learner license has been held at least 12 months and the driver has completed at least 50 '
            'hours of supervised driving including 10 at night. Sixteen year olds may not drive between '
            '11pm and 6am, and seventeen year olds not between 1am and 5am, with exceptions for work or '
            'when accompanied by a licensed driver aged 21 or over.</p>',
            '<p>Fifty hours is a real requirement and it is also not very much. What those hours contain '
            'depends entirely on what happened to come up, which means most new drivers get licensed '
            'having never experienced the situations that actually cause crashes.</p>',
            '<p>These pages cover those situations. Confirm current licensing requirements with '
            '<a href="https://www.flhsmv.gov/pdf/handbooks/englishdriverhandbook.pdf">FLHSMV</a> rather '
            'than relying on this summary.</p>',
        ]),
        linkgrid('Topics', 'The skills', '', [
            ('/training/hazard-recognition/', 'HAZARD RECOGNITION',
             'Seeing the developing problem rather than the current one.'),
            ('/training/defensive-driving/', 'DEFENSIVE DRIVING',
             'Following distance, positioning and assuming less about other drivers.'),
            ('/training/emergency-braking/', 'EMERGENCY BRAKING',
             'Most drivers do not brake hard enough when it counts.'),
            ('/training/rain-driving/', 'RAIN AND WET ROADS',
             'Florida-specific, and the conditions most new drivers meet unprepared.'),
            ('/training/night-driving/', 'NIGHT DRIVING',
             'Ten of the required 50 hours, and the hardest to arrange.'),
            ('/training/stick-shift/', 'MANUAL TRANSMISSION',
             'Increasingly rare, still occasionally essential.'),
        ]),
        NO_INSTALLS,
        faq([
            ('Are these programs for individuals or schools?',
             'Both. Schools and districts bring these in as programs. Individual teen training is booked '
             'through Academy directly.'),
            ('Does simulator practice count toward the 50 supervised hours?',
             'No. The 50 hours are supervised driving on real roads. Simulator time is preparation for '
             'them, not a substitute.'),
            ('Which skill matters most?',
             'Hazard recognition, in our view. Most of the others are responses to a hazard, and seeing it '
             'earlier makes every one of them easier.'),
            ('Can a nervous teenager start on a simulator?',
             'Yes, and it is one of the better uses. Getting the initial unfamiliarity out of the way '
             'somewhere with no consequences makes the first real drive calmer.'),
            ('Do you work with parents directly?',
             'Yes. Teen training is available through Academy. Contact us and we will explain how it works.'),
            ('Do you have simulators in schools already?',
             'No. Academy does not currently have simulators installed in any school district. These are '
             'programs we offer and can deploy.'),
        ]),
    ]),
))

PAGES.append(topic(
    'hazard-recognition', 'Hazard Recognition',
    'Hazard Recognition For New Drivers | Academy Driver Education',
    'What hazard recognition actually is, why new drivers see hazards late, and how simulator practice can help them see developing problems earlier.',
    'Hazard Recognition',
    'Experienced drivers are not faster at reacting. They are earlier at noticing, which gives them longer '
    'to react. That difference is learnable and it is what hazard recognition training targets.',
    ['<p>Reaction time barely improves with experience. What improves is where a driver is looking and what '
     'they treat as significant. A new driver watches the car in front. An experienced one has already '
     'noticed the pedestrian three cars ahead who is looking at their phone.</p>',
     '<p>That is why new drivers seem to react late. They are not slow. They saw it late, because nobody '
     'ever told them where to look or what a developing problem looks like before it becomes an actual '
     'one.</p>'],
    ['<h3>Eyes up and further ahead</h3>'
     '<p>The single most common fault is looking at the road immediately in front of the car. Scanning '
     'further ahead buys time that no amount of quick reflexes can replace.</p>',
     '<h3>Reading intent, not just position</h3>'
     '<p>A car edging forward at a junction, a head turning, a ball rolling into a road. Hazards announce '
     'themselves before they happen, and recognizing the announcement is the skill.</p>',
     '<h3>Prioritizing</h3>'
     '<p>There is always more than one thing happening. Knowing which one matters most right now is what '
     'stops a driver being overwhelmed.</p>'],
    ['<p><strong>Where it helps.</strong> A simulator can present the same developing hazard repeatedly, '
     'which real roads cannot. It can also make hazards happen on demand rather than waiting for one to '
     'occur naturally during a supervised drive.</p>',
     '<p><strong>Where it does not.</strong> Simulated hazards are staged and a student eventually learns '
     'to expect them. Real hazard recognition has to transfer to roads where nothing is scripted, and that '
     'transfer needs real supervised driving.</p>'],
    [('Why do new drivers see hazards late?',
      'Because of where they are looking, not how fast they react. New drivers watch the road immediately '
      'ahead. Scanning further ahead is a learnable habit.'),
     ('Can hazard recognition really be taught?',
      'The habits behind it can. Where to look, what to treat as significant and how to prioritize are all '
      'teachable, which is why it is worth targeting specifically.'),
     ('Does simulator practice transfer to real roads?',
      'The habits do. What does not transfer is expecting a hazard because you are in a training session, '
      'which is why simulator work supplements supervised driving rather than replacing it.'),
     ('What age should this start?',
      'It is useful from the learner permit stage, and arguably before. A student who has thought about '
      'where to look before their first drive gets more from that drive.'),
     ('Is this part of school programs?',
      'Yes. It is usually the core of a defensive driving or teen safety program because everything else '
      'depends on it.'),
     ('Do you have simulators in schools already?',
      'No. Academy does not currently have simulators installed in any school district.')],
    'Hazard Recognition Training For New Drivers',
))

PAGES.append(topic(
    'defensive-driving', 'Defensive Driving',
    'Defensive Driving For New Drivers | Academy Driver Education',
    'What defensive driving actually means in practice: following distance, road positioning and assuming less about other drivers.',
    'Defensive Driving',
    'Defensive driving is a phrase that has been used so loosely it has almost stopped meaning anything. '
    'In practice it comes down to giving yourself time and assuming less about everyone else.',
    ['<p>Most crashes involving new drivers are not caused by a lack of vehicle control. They happen '
     'because the driver had no time and no options when something went wrong, and they had no time '
     'because of decisions made several seconds earlier.</p>',
     '<p>Defensive driving is the set of habits that preserve time and options. It is unglamorous and it '
     'is the most valuable thing a new driver can learn.</p>'],
    ['<h3>Following distance</h3>'
     '<p>Almost every new driver follows more closely than they think. Following distance is the single '
     'biggest lever on whether a driver has time to respond, and it costs nothing.</p>',
     '<h3>Road position</h3>'
     '<p>Where the car sits in a lane changes what the driver can see and what others can see of them. '
     'Most new drivers have never thought about it.</p>',
     '<h3>Assuming less</h3>'
     '<p>The dangerous assumption is that other road users will do the correct thing. Defensive driving is '
     'largely the habit of leaving room for them not to.</p>',
     '<h3>Having an out</h3>'
     '<p>Experienced drivers are continuously aware of where they would go if they had to. New drivers '
     'usually are not, and it is a teachable habit.</p>'],
    ['<p><strong>Where it helps.</strong> A simulator can show a student what their actual following '
     'distance is and what it costs when the car ahead brakes hard. That is a difficult lesson to arrange '
     'safely any other way.</p>',
     '<p><strong>Where it does not.</strong> Defensive driving is a habit rather than a skill, and habits '
     'form through repetition over months of real driving. A session can start the habit. It cannot '
     'install it.</p>'],
    [('What does defensive driving actually mean?',
      'In practice: following distance, road position, assuming less about other drivers, and always '
      'knowing where you would go if you had to. It is about preserving time and options.'),
     ('Is it worth teaching before a student can drive?',
      'The concepts, yes. The habits need real driving to form, but understanding them first makes those '
      'first hours more productive.'),
     ('Does it satisfy a court or district requirement?',
      'Not that we can claim. If it is meant to meet a specific requirement, confirm that with whoever set '
      'it before planning around our program.'),
     ('How is this different from hazard recognition?',
      'Hazard recognition is seeing the problem. Defensive driving is having arranged things so you have '
      'time and room to deal with it.'),
     ('Can you run this for students who already drive?',
      'Yes, and that is often the better audience, because they have habits to correct rather than none '
      'yet formed.'),
     ('Do you have simulators in schools already?',
      'No. Academy does not currently have simulators installed in any school district.')],
    'Defensive Driving Training For New Drivers',
))

PAGES.append(topic(
    'emergency-braking', 'Emergency Braking',
    'Emergency Braking For New Drivers | Academy Driver Education',
    'Why most drivers do not brake hard enough in a genuine emergency, what anti-lock brakes actually do, and how to practice safely.',
    'Emergency Braking',
    'The most common failure in a real emergency is not braking too late. It is not braking hard enough, '
    'because almost nobody has ever done it.',
    ['<p>A driver who has never performed a genuine emergency stop has no idea how hard the pedal has to '
     'be pressed. In the moment they brake firmly rather than maximally, and the difference is measured in '
     'car lengths.</p>',
     '<p>It is entirely fixable, and the fix is doing it. Once a driver has felt a maximum-effort stop, '
     'they know what it takes. Until then they are guessing.</p>'],
    ['<h3>Press harder than feels reasonable</h3>'
     '<p>In an emergency the pedal should be pressed hard and held. Modern cars are designed for this. '
     'Most drivers are far too gentle.</p>',
     '<h3>What anti-lock brakes do</h3>'
     '<p>ABS pulses the brakes to stop the wheels locking so the driver can still steer. The pedal will '
     'shudder and make noise. That is the system working, and the correct response is to keep pressing, '
     'which is the opposite of what an untrained driver does.</p>',
     '<h3>Look where you want to go</h3>'
     '<p>Under heavy braking drivers fixate on what they are trying to avoid, and tend to steer toward '
     'whatever they are looking at. Looking at the gap matters.</p>'],
    ['<p><strong>Where it helps.</strong> This is one of the clearest cases for a simulator. A student can '
     'perform a dozen maximum-effort stops in ten minutes, feel ABS activate, and learn not to lift. '
     'Arranging that on a public road is not possible and on a closed course it is expensive.</p>',
     '<p><strong>Where it does not.</strong> The physical pedal effort in a real car and the sensation of '
     'genuine deceleration cannot be fully reproduced. A simulator teaches the response. The real thing '
     'still feels different.</p>'],
    [('Why do drivers not brake hard enough?',
      'Because they have never done it. Without having felt a maximum-effort stop, a driver has no '
      'reference for how hard the pedal has to be pressed.'),
     ('What should a driver do when ABS activates?',
      'Keep pressing. The shudder and noise mean the system is working. Lifting off is the instinctive '
      'response and the wrong one.'),
     ('Can this be practiced on a public road?',
      'No, and it should not be attempted. That is precisely why simulator or closed-course practice is '
      'valuable for this particular skill.'),
     ('Does it transfer to a real car?',
      'The response does: press hard, hold, keep looking where you want to go. The physical sensation of '
      'real deceleration is different and we would not claim otherwise.'),
     ('Is this suitable for pre-licensed students?',
      'Yes, and arguably it is best learned before bad habits form.'),
     ('Do you have simulators in schools already?',
      'No. Academy does not currently have simulators installed in any school district.')],
    'Emergency Braking Training For New Drivers',
))

PAGES.append(topic(
    'rain-driving', 'Rain And Wet Roads',
    'Driving In Rain For New Florida Drivers | Academy Driver Education',
    'Wet road driving for new Florida drivers: reduced grip, standing water, aquaplaning and why the first few minutes of rain are the worst.',
    'Rain and Wet Roads',
    'In Florida this is not an edge case. Afternoon storms are a routine part of the year, and a new '
    'driver will meet heavy rain long before they have the experience to handle it.',
    ['<p>Florida gives new drivers two things at once: a lot of sudden heavy rain, and a licensing '
     'timeline that does not guarantee they will have driven in any of it before passing.</p>',
     '<p>A student can complete 50 supervised hours in dry weather and be licensed without ever having '
     'driven on a genuinely wet road. The first time is then unsupervised.</p>'],
    ['<h3>The first few minutes are the worst</h3>'
     '<p>Rain lifts oil and rubber off the surface before washing it away, so grip is lowest shortly after '
     'rain starts, not during sustained downpour. Most drivers assume the opposite.</p>',
     '<h3>Everything takes longer</h3>'
     '<p>Braking distances extend and the car responds more slowly. The correct adjustment is more '
     'following distance and earlier inputs rather than merely driving slower.</p>',
     '<h3>Standing water and aquaplaning</h3>'
     '<p>When tires cannot clear water fast enough the car loses contact with the road. The correct '
     'response is to ease off and hold the wheel steady rather than brake or steer sharply, which is '
     'counterintuitive and worth knowing in advance.</p>',
     '<h3>Being seen</h3>'
     '<p>Florida law requires headlights when windshield wipers are in continuous use. It also genuinely '
     'helps other drivers see you.</p>'],
    ['<p><strong>Where it helps.</strong> A simulator can produce a wet road on demand, which no lesson '
     'plan can. A student can experience reduced grip and practice the counterintuitive aquaplaning '
     'response repeatedly and safely.</p>',
     '<p><strong>Where it does not.</strong> Real rain brings poor visibility, spray from other vehicles '
     'and the physical stress of it. Nothing reproduces that fully, and a driver should still get real '
     'supervised wet-weather practice.</p>'],
    [('When is a wet road most dangerous?',
      'Usually shortly after rain begins, when oil and rubber lift off the surface before being washed '
      'away. Many drivers assume sustained heavy rain is worse.'),
     ('What should a driver do if the car aquaplanes?',
      'Ease off the throttle and hold the wheel steady. Braking or steering sharply makes it worse, which '
      'is why it is worth knowing before it happens.'),
     ('Do headlights have to be on in rain in Florida?',
      'Florida requires headlights when windshield wipers are in continuous use. Confirm current '
      'requirements with FLHSMV.'),
     ('Can a student get real wet-weather practice?',
      'Only if it rains during their supervised hours, which is not something anyone can schedule. That is '
      'the gap a simulator fills.'),
     ('Is this particularly relevant in Florida?',
      'More than in most states. Sudden heavy afternoon rain is routine for much of the year.'),
     ('Do you have simulators in schools already?',
      'No. Academy does not currently have simulators installed in any school district.')],
    'Wet Road And Rain Driving Training For New Drivers',
))

PAGES.append(topic(
    'night-driving', 'Night Driving',
    'Night Driving For New Drivers | Academy Driver Education',
    'Night driving for new Florida drivers: reduced visibility, judging distance, glare and the 10 required night hours.',
    'Night Driving',
    'Florida requires 10 of the 50 supervised hours to be at night, which is an acknowledgment that it is '
    'genuinely different. It is also the requirement families find hardest to arrange.',
    ['<p>Night driving is harder for reasons that are physical rather than attitudinal. Visibility is '
     'limited to what headlights reach, judging distance and speed is measurably harder, and oncoming '
     'headlights cause glare that takes seconds to recover from.</p>',
     '<p>It is also the part of the requirement that gets squeezed. Ten hours at night has to compete with '
     'homework, work schedules and a supervising adult who has already had a long day.</p>'],
    ['<h3>You can only react to what you can see</h3>'
     '<p>At night that is roughly the distance the headlights reach. Speed has to suit that distance, '
     'which for most drivers means slower than they instinctively drive.</p>',
     '<h3>Glare and recovery</h3>'
     '<p>Looking directly at oncoming headlights costs several seconds of useful vision. Looking toward '
     'the right edge of the lane instead preserves it.</p>',
     '<h3>Judging distance is harder</h3>'
     '<p>Without daytime cues, distance and closing speed are much harder to estimate, which makes '
     'following distance and junction decisions less reliable.</p>',
     '<h3>Fatigue</h3>'
     '<p>Night driving usually happens at the end of a day. Tiredness compounds every other factor and new '
     'drivers rarely account for it.</p>'],
    ['<p><strong>Where it helps.</strong> A simulator can run night conditions at any hour, which is a '
     'genuine scheduling advantage given how hard the 10 required hours are to arrange. It can also stage '
     'glare and low-visibility hazards safely.</p>',
     '<p><strong>Where it does not.</strong> Simulator time does not count toward the 10 required night '
     'hours. Those are supervised driving on real roads and nothing here substitutes for them.</p>'],
    [('Does simulator time count toward the 10 night hours?',
      'No. The requirement is supervised driving on real roads. Simulator practice is preparation for '
      'those hours, not a replacement.'),
     ('Why is night driving harder?',
      'Visibility is limited to headlight range, judging distance and closing speed is harder, glare costs '
      'seconds of vision, and fatigue usually compounds all of it.'),
     ('What should a driver do about oncoming headlight glare?',
      'Avoid looking directly at them and look toward the right edge of the lane instead, which preserves '
      'useful vision.'),
     ('Why do families struggle with the night hours?',
      'They compete with school, work and a tired supervising adult. It is the most commonly squeezed part '
      'of the requirement.'),
     ('Can a student practice night driving before doing it for real?',
      'A simulator can run night conditions at any hour, which at least means the first real night drive '
      'is not the first exposure to the conditions.'),
     ('Do you have simulators in schools already?',
      'No. Academy does not currently have simulators installed in any school district.')],
    'Night Driving Training For New Drivers',
))

PAGES.append(topic(
    'stick-shift', 'Manual Transmission',
    'Learning To Drive A Manual Transmission | Academy',
    'Learning stick shift: what the clutch actually does, why stalling happens and how to practice without wearing out a real clutch.',
    'Manual Transmission',
    'Most new drivers will never need this. The ones who do usually need it suddenly, and a parking lot '
    'with a borrowed car is a stressful place to find out how a clutch works.',
    ['<p>Manual transmissions have largely disappeared from American cars, which means a driver can hold a '
     'license for years and have no idea how one works. Then they need to move a friend’s car, drive a '
     'work vehicle, rent something abroad, or buy a car they like that happens to be manual.</p>',
     '<p>It is a small skill with a steep and embarrassing start. Almost everyone stalls repeatedly at '
     'first, and doing that in front of someone whose car it is makes it worse.</p>'],
    ['<h3>What the clutch actually does</h3>'
     '<p>It disconnects the engine from the wheels so gears can be changed and so the car can start moving '
     'from stationary without the engine stopping. Understanding that makes the biting point make sense '
     'rather than being a mystery.</p>',
     '<h3>Why stalling happens</h3>'
     '<p>The clutch is released faster than the engine can pick up the load. The fix is releasing more '
     'slowly through the biting point, and adding a little throttle.</p>',
     '<h3>Finding the biting point</h3>'
     '<p>Every car is slightly different. Finding it is the first thing to learn and the thing that makes '
     'everything else possible.</p>',
     '<h3>Hills</h3>'
     '<p>Starting on an incline is where most learners struggle, because the car rolls back while the '
     'clutch is still engaging.</p>'],
    ['<p><strong>Where it helps.</strong> Stalling costs nothing in a simulator, and a learner can do it a '
     'hundred times without wear, embarrassment or a queue of traffic behind them. It also means the first '
     'attempt in a real car is not the first attempt overall.</p>',
     '<p><strong>Where it does not.</strong> The physical feel of a real clutch pedal, and the sound and '
     'vibration a car makes as it approaches stalling, are things a driver ultimately has to learn in the '
     'car. A simulator shortens that, it does not remove it.</p>'],
    [('Is it worth learning manual if my car is automatic?',
      'For most people it sits somewhere between useful and occasionally essential. The people who need it '
      'usually need it at short notice.'),
     ('Why does a car stall?',
      'The clutch is released faster than the engine can take up the load. Releasing more slowly through '
      'the biting point, with a little throttle, fixes it.'),
     ('Can you really learn stick shift on a simulator?',
      'You can learn the sequence, the biting point concept and the coordination without wearing out a '
      'real clutch. The final feel has to be learned in a car, and we would not pretend otherwise.'),
     ('How long does it take?',
      'Most people can move off and change gear within a session. Doing it smoothly on a hill in traffic '
      'takes longer.'),
     ('Do you offer this to individuals?',
      'Yes. Contact us and we will explain how it works.'),
     ('Do you have simulators in schools already?',
      'No. Academy does not currently have simulators installed in any school district.')],
    'Manual Transmission Driving Training',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
