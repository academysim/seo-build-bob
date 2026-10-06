# -*- coding: utf-8 -*-
"""Driver batch 1: /schools/ hub + 4 program pages, /training/ + 6 topic pages.

No district-specific claims here, so none of this depends on outside
verification. What it must never do is imply Academy already has simulators in
schools. Every page carries the NO_INSTALLS disclosure.

Deliberately NOT built: individual high school pages. The brief forbids them
outright, and district pages are the lowest geographic level allowed.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver_pages import write, sec, prose, cards, faq, linkgrid, NO_INSTALLS, ld

PAGES = []

# ------------------------------------------------------- SCHOOLS HUB ------
PAGES.append(dict(
    slug='schools', url='/schools/', ctype='schools_hub',
    title='Driving Simulator Programs For Schools | Academy Driver Education',
    desc='Driving simulator programs Florida schools can use for driver education, teen safety weeks and defensive driving. Mobile and longer-term options available.',
    crumbs='<a href="/">Home</a> / Schools',
    eyebrow='For Schools',
    h1='Driving Simulator Programs for Schools',
    lede='Academy offers simulator-based driver education programs that schools and districts can bring in '
         'for a day, a week or a term. Every program is delivered by our staff with our equipment.',
    cta1='Request Program Information',
    final_h='Talk to us about your program',
    final_p='Tell us the school or district, roughly how many students and what you are trying to achieve. '
            'We will come back with options and costs.',
    ld=ld('Service', 'Driving Simulator Programs For Schools',
          'Simulator-based driver education, teen safety and defensive driving programs available to Florida schools and districts.',
          '/schools/'),
    body='\n\n'.join([
        prose('The Case', 'Why a simulator, and why now', '', [
            '<p>Driver education has a practical problem that has nothing to do with willingness. Behind the '
            'wheel instruction needs a car, an instructor and a road, which caps how many students can be '
            'trained and makes some situations impossible to teach at all.</p>',
            '<p>A simulator does not solve all of that. What it does is let a student experience a hazard, a '
            'skid or a wet-road stop without any of the risk, and let them do it repeatedly. It also lets '
            'more students get hands-on time in a fixed window, because a simulator does not need a public '
            'road.</p>',
            '<h3>What a simulator can genuinely do</h3>',
            '<ul>'
            '<li>Expose students to hazards that cannot be staged safely on a road</li>'
            '<li>Let a student repeat the same situation until the response is automatic</li>'
            '<li>Give hands-on time to more students within a school day</li>'
            '<li>Standardize what every student experiences, rather than depending on what came up on the day</li>'
            '<li>Run in a gym, a classroom or a media center, in any weather</li>'
            '</ul>',
            '<h3>What it cannot do</h3>',
            '<p>It does not replace behind the wheel instruction and it does not satisfy any state licensing '
            'requirement on its own. We would rather say that plainly than have a district discover it after '
            'a purchase order.</p>',
        ]),
        NO_INSTALLS,
        linkgrid('Programs', 'What we can bring in', 'Four program shapes, described in detail.', [
            ('/schools/driver-education-simulators/', 'DRIVER EDUCATION SIMULATORS',
             'Simulators as part of an existing driver education course.'),
            ('/schools/teen-driver-safety-programs/', 'TEEN DRIVER SAFETY PROGRAMS',
             'Awareness-focused programs, often tied to a safety week or assembly.'),
            ('/schools/defensive-driving-simulator/', 'DEFENSIVE DRIVING',
             'Hazard recognition and response, for students who already drive.'),
            ('/schools/safety-week-driving-programs/', 'SAFETY WEEK PROGRAMS',
             'Short, high-throughput formats built around a defined week.'),
        ]),
        cards('Delivery', 'Three ways to run it',
              'Which one suits you depends on how many students and how long you have.', [
                  ('Mobile program', 'We bring the simulators to your campus, run the sessions and take '
                   'everything away again. The most common request, and the easiest to arrange.'),
                  ('Short-term placement', 'Equipment on site for a defined period, such as a semester or '
                   'a safety initiative, with our staff supporting it.'),
                  ('Longer-term solutions', 'Where a district wants a permanent capability, we can discuss '
                   'what that looks like. This is a conversation rather than a catalog item.'),
              ]),
        prose('Practical', 'What we need to know', '', [
            '<h3>Numbers and time</h3>'
            '<p>How many students, and over how long. Those two numbers determine everything else, '
            'including how many simulators make sense and whether one day is realistic.</p>',
            '<h3>The space</h3>'
            '<p>A gym, cafeteria, media center or large classroom all work. We need floor space and mains '
            'power at the setup point, and a way to get equipment in from a vehicle.</p>',
            '<h3>Who is running it</h3>'
            '<p>Our staff operate the simulators. Your driver education teacher or SRO usually leads the '
            'instructional side, and we work to their plan rather than replacing it.</p>',
            '<h3>Procurement</h3>'
            '<p>Tell us early how your district buys things. Quotes, W-9s, insurance certificates and vendor '
            'registration all take longer than the scheduling does.</p>',
        ]),
        faq([
            ('Do you have simulators in Florida schools already?',
             'No. Academy does not currently have simulators installed in any school district. These are '
             'programs we offer and can deploy, and we would rather be straight about that.'),
            ('Does this replace behind the wheel instruction?',
             'No, and it does not satisfy state licensing requirements on its own. It supplements classroom '
             'and behind the wheel instruction rather than substituting for either.'),
            ('How many students can go through in a day?',
             'It depends on session length and how many simulators. Tell us your numbers and the window and '
             'we will give you a realistic figure rather than an optimistic one.'),
            ('What space do we need?',
             'A gym, cafeteria, media center or large classroom. We need floor space, mains power and a way '
             'to get equipment in.'),
            ('Who supervises the students?',
             'Our staff run the simulators. School staff supervise students, as they would for any outside '
             'provider on campus.'),
            ('How do we start a conversation?',
             'Contact us with the school or district, rough student numbers and what you are trying to '
             'achieve. We will send options and costs.'),
        ]),
    ]),
))


def program(slug, eyebrow, title, desc, h1, lede, what, fits, practical, faqs, ldname):
    return dict(
        slug=slug, url='/schools/%s/' % slug, ctype='school_program',
        title=title, desc=desc,
        crumbs='<a href="/">Home</a> / <a href="/schools/">Schools</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede,
        cta1='Request Program Information',
        final_h='Bring this to your school',
        final_p='Tell us the school or district, student numbers and your timeframe. We will send options '
                'and costs.',
        ld=ld('Service', ldname, desc, '/schools/%s/' % slug),
        body='\n\n'.join([
            prose('The Program', 'What it actually is', '', what),
            NO_INSTALLS,
            cards('Format', 'How it runs', '', fits),
            prose('Practical', 'Planning it', '', practical),
            linkgrid('Related', 'Other programs', '', [
                ('/schools/', 'ALL SCHOOL PROGRAMS', 'The full picture and how delivery works.'),
                ('/school-districts/', 'BY DISTRICT', 'Florida districts we can serve.'),
                ('/training/', 'SKILLS COVERED', 'The specific driving skills these programs address.'),
            ]),
            faq(faqs),
        ]),
    )


PAGES.append(program(
    'driver-education-simulators', 'Driver Education',
    'Driving Simulators For Driver Education Programs | Academy',
    'Simulators that supplement an existing school driver education course. Hazard exposure and repetition that cannot be staged safely on a road.',
    'Simulators for Driver Education',
    'If your school already runs driver education, a simulator is not a replacement for any part of it. '
    'It is the part you cannot do on a public road with a student who has held a permit for two weeks.',
    ['<p>A driver education course covers rules, procedure and supervised road time. What it struggles to '
     'cover is the situations that matter most and are least safe to stage: a car pulling out, a skid on a '
     'wet surface, an emergency stop from real speed.</p>',
     '<p>Those are exactly what a simulator handles well, because the student can experience them, get them '
     'wrong, and try again.</p>',
     '<h3>Where it fits in an existing course</h3>',
     '<ul>'
     '<li><strong>Before behind the wheel.</strong> Students arrive at their first road session having '
     'already made the obvious mistakes somewhere safe.</li>'
     '<li><strong>Alongside classroom units.</strong> A hazard perception unit lands differently when a '
     'student has just driven it.</li>'
     '<li><strong>For students waiting their turn.</strong> Behind the wheel time is a queue. A simulator '
     'gives the rest of the class something better than a worksheet.</li>'
     '</ul>'],
    [('A day on campus', 'We arrive, set up, run sessions through the school day and remove everything. The '
      'simplest way for a school to try the format.'),
     ('A recurring visit', 'The same program repeated across a semester so every cohort gets a turn.'),
     ('Alongside a defined unit', 'Timed to coincide with the classroom unit it supports, so the two '
      'reinforce each other.')],
    ['<h3>Work out the queue</h3>'
     '<p>The limiting factor is students per hour, not enthusiasm. Tell us the cohort size and the window '
     'and we will tell you how many simulators that actually needs.</p>',
     '<h3>Talk to your driver education teacher first</h3>'
     '<p>The program works far better when it is built around what they are already teaching. We would '
     'rather adapt to their plan than hand you a fixed script.</p>',
     '<h3>State requirements</h3>'
     '<p>Simulator time does not substitute for any state-required instruction. Check what your district '
     'requires before planning around it.</p>'],
    [('Does simulator time count toward state requirements?',
      'Not on its own. Treat it as a supplement to your existing course and confirm any requirement with '
      'your district and the state.'),
     ('Do you provide the instruction, or just the equipment?',
      'Our staff run the simulators. The instructional framing is normally led by your driver education '
      'teacher, and we work to their plan.'),
     ('How much of a class can take part in one period?',
      'That depends on session length and simulator count. Give us your class size and period length and we '
      'will be specific.'),
     ('Can students who have never driven use it?',
      'Yes. That is much of the point, and the settings can be adjusted so a first-time driver is not '
      'overwhelmed.'),
     ('Do you have this running in schools now?',
      'No. Academy does not currently have simulators installed in any school district. This is a program '
      'we offer and can deploy.'),
     ('What does it cost?',
      'It depends on numbers, duration and travel, so we quote rather than list. Tell us the details and '
      'you will get a real figure.')],
    'Driving Simulators For School Driver Education Programs',
))

PAGES.append(program(
    'teen-driver-safety-programs', 'Teen Driver Safety',
    'Teen Driver Safety Programs For Schools | Academy',
    'Teen driver safety programs for Florida schools. Awareness-focused simulator sessions for safety weeks, assemblies and parent nights.',
    'Teen Driver Safety Programs',
    'The hard part of teen driver safety is not information. Students know the rules. The gap is between '
    'knowing that something is dangerous and having felt why.',
    ['<p>Safety messaging aimed at teenagers competes with an assumption that it will not happen to them. '
     'A presentation does not shift that. Experiencing a hazard you did not react to in time gets closer.</p>',
     '<p>These programs are built around that moment rather than around content delivery. The simulator is '
     'a way to make the point land, not a lecture with a steering wheel.</p>',
     '<h3>What we can cover</h3>',
     '<ul>'
     '<li>Reaction time and following distance</li>'
     '<li>Distraction, and what it actually costs in stopping distance</li>'
     '<li>Hazard recognition and how late most people see things</li>'
     '<li>Wet and low-grip conditions</li>'
     '<li>Speed and how it changes everything else</li>'
     '</ul>'],
    [('Safety week', 'A day or several days during a defined safety initiative, with high throughput and '
      'short sessions so the largest number of students take part.'),
     ('Assembly plus simulator', 'A short talk for the whole year group, then simulator sessions for '
      'smaller groups afterwards.'),
     ('Parent and teen night', 'An evening session where parents and teens both drive. Parents finding it '
      'harder than they expected is usually the most useful part.')],
    ['<h3>Decide what you want students to leave with</h3>'
     '<p>One idea, well demonstrated, beats five mentioned. Tell us the message and we will build the '
     'session around it.</p>',
     '<h3>Think about throughput honestly</h3>'
     '<p>If you want every student in a year group to drive, that is a scheduling problem before it is '
     'anything else. Tell us the number and the window.</p>',
     '<h3>Involve your SRO or safety lead</h3>'
     '<p>These programs land better when the school voice on safety is part of them rather than adjacent.</p>'],
    [('Is this a presentation or hands-on?',
      'Hands-on. There can be a talk alongside it, but the simulator time is the point.'),
     ('Can every student in a year group take part?',
      'That depends on numbers and time. Tell us both and we will be honest about whether it is realistic '
      'in the window you have.'),
     ('Do you run parent and teen sessions?',
      'Yes, and they work well. Parents discovering the task is harder than they remember tends to change '
      'the conversation at home.'),
     ('Is it suitable for students who do not drive yet?',
      'Yes. For pre-permit students the value is awareness rather than skill.'),
     ('Do you have this running in schools now?',
      'No. Academy does not currently have simulators installed in any school district. This is a program '
      'we offer and can deploy.'),
     ('Can it tie into an existing safety campaign?',
      'Yes, and it works better when it does. Tell us the campaign and we will build around it.')],
    'Teen Driver Safety Simulator Programs For Schools',
))

PAGES.append(program(
    'defensive-driving-simulator', 'Defensive Driving',
    'Defensive Driving Simulator Programs For Schools | Academy',
    'Defensive driving simulator programs for students who already drive. Hazard recognition, following distance and emergency response.',
    'Defensive Driving Programs',
    'For students who already have a license, the useful work is not learning to drive. It is unlearning '
    'the habits that six months of unsupervised driving has already built.',
    ['<p>New drivers develop bad habits quickly and privately. Following too closely, checking mirrors too '
     'rarely, and a general assumption that other road users will behave predictably.</p>',
     '<p>A defensive driving program targets those specifically, by putting a student in situations where '
     'the habit fails and letting them feel the consequence safely.</p>',
     '<h3>What we work on</h3>',
     '<ul>'
     '<li><strong>Following distance.</strong> Almost everyone runs shorter than they think.</li>'
     '<li><strong>Hazard recognition.</strong> Seeing the developing problem rather than the current one.</li>'
     '<li><strong>Emergency braking.</strong> Most drivers do not brake hard enough in a genuine emergency.</li>'
     '<li><strong>Recovery.</strong> What to do when the car is already doing something you did not ask for.</li>'
     '<li><strong>Distraction.</strong> Demonstrated rather than described.</li>'
     '</ul>'],
    [('Single session', 'A focused session on one or two behaviors, which is usually more effective than '
      'covering everything shallowly.'),
     ('Program across a term', 'Repeat visits building on each other, for schools that want more than a '
      'one-off.'),
     ('Targeted groups', 'For students identified by staff as needing it, or for a driving club or CTE '
      'cohort.')],
    ['<h3>Pick a small number of behaviors</h3>'
     '<p>A session aimed at following distance and hazard recognition will change more than one that tries '
     'to cover the whole syllabus.</p>',
     '<h3>These students think they can drive</h3>'
     '<p>That is the useful part. The program works because the simulator can demonstrate otherwise without '
     'anybody getting hurt or embarrassed in front of a class.</p>',
     '<h3>Confirm what your district expects</h3>'
     '<p>If this is meant to satisfy a specific requirement, check that with your district first. Simulator '
     'time does not substitute for state-required instruction.</p>'],
    [('Is this for students who already drive?',
      'Primarily, yes. The value is in addressing habits that have already formed.'),
     ('Does it satisfy any court or district requirement?',
      'Not that we can claim. If it is meant to meet a specific requirement, confirm that with your district '
      'before planning around it.'),
     ('How many behaviors can you cover in a session?',
      'Two, properly, beats six in passing. Tell us what concerns you most about your students and we will '
      'focus there.'),
     ('Can staff observe what a student did?',
      'Yes. What happened in a session is visible and can be discussed afterwards, which is often where the '
      'learning actually happens.'),
     ('Do you have this running in schools now?',
      'No. Academy does not currently have simulators installed in any school district. This is a program '
      'we offer and can deploy.'),
     ('Can this run alongside a driver education course?',
      'Yes, and it complements it well, because the audiences are different stages of the same journey.')],
    'Defensive Driving Simulator Programs For Schools',
))

PAGES.append(program(
    'safety-week-driving-programs', 'Safety Week',
    'Safety Week Driving Simulator Programs | Academy',
    'High-throughput simulator programs built around a school safety week. Short sessions, maximum student participation, delivered and staffed.',
    'Safety Week Programs',
    'A safety week has a fixed window and a fixed student body, which makes it a throughput problem before '
    'it is anything else.',
    ['<p>Most safety weeks fail quietly the same way: a good activity that only forty students actually '
     'experienced, while the rest saw a poster.</p>',
     '<p>So the format changes. Short sessions, several simulators, staff managing the queue, and a single '
     'clear message rather than a curriculum. The aim is that most of the year group actually drives '
     'rather than a lucky subset.</p>',
     '<h3>How we plan it</h3>',
     '<ul>'
     '<li>Start from the number of students and the hours available</li>'
     '<li>Work back to how many simulators that requires</li>'
     '<li>Keep sessions short enough that the queue keeps moving</li>'
     '<li>Pick one message and demonstrate it well</li>'
     '</ul>'],
    [('One day, high throughput', 'Several simulators running continuously through the school day.'),
     ('Across the week', 'Fewer simulators over more days, which suits schools that cannot free a whole '
      'day of scheduling.'),
     ('Paired with an assembly', 'A short whole-group session to frame it, then simulator time in rotation.')],
    ['<h3>Give us the real numbers</h3>'
     '<p>Year group size and the hours genuinely available, not the optimistic version. It is the only way '
     'to size this correctly.</p>',
     '<h3>Scheduling is the hard part</h3>'
     '<p>Getting students to the simulators in an orderly rotation is usually harder than running the '
     'simulators. Involve whoever builds the schedule early.</p>',
     '<h3>Space and power</h3>'
     '<p>A gym or cafeteria works best for high throughput, because there is room for both the equipment '
     'and the queue. We need mains power at the setup point.</p>'],
    [('How many students can take part in a day?',
      'It depends on session length and simulator count. Give us your year group size and available hours '
      'and we will tell you what is realistic.'),
     ('Can you run across several days instead?',
      'Yes, and for many schools that is easier to schedule than freeing a whole day.'),
     ('What space works best?',
      'A gym or cafeteria, because you need room for the equipment and for the students waiting.'),
     ('Do you handle the rotation?',
      'We run the simulators and keep the queue moving. Getting students to the room in order is normally '
      'the school schedule, and it is worth planning early.'),
     ('Do you have this running in schools now?',
      'No. Academy does not currently have simulators installed in any school district. This is a program '
      'we offer and can deploy.'),
     ('How far in advance should we book?',
      'As early as you can. Safety weeks cluster in the calendar and districts often need lead time for '
      'procurement anyway.')],
    'Safety Week Driving Simulator Programs For Schools',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
