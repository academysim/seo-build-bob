# -*- coding: utf-8 -*-
"""Driver batch 2: /school-districts/ hub plus the six phase-1 districts.

Every district fact below was verified against the district's own site or
Florida Statutes, with NOT CONFIRMED treated as "do not publish". That is why
the pages differ genuinely: Hillsborough runs a mature in-school program with
a DMV-approved range at each high school, while Pasco's driver education course
is delivered online through Pasco eSchool. Those are different sales problems
and the pages say so.

Two constraints that shape all of it:
  1. Academy has NO simulators installed in any school. Everything is
     future-facing: offers, can provide, can deploy.
  2. The Dori Slosberg Act requires programs it funds to devote at least 30% of
     student time to behind-the-wheel training. A simulator cannot count toward
     that, and the pages say so plainly rather than letting a district discover
     it after a purchase order.

Deliberately NOT claimed: that Academy is a licensed commercial driving school
under s.1003.48(1). The statute is cited as procurement context only. Flagged
to Malik.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver_pages import write, sec, prose, cards, faq, linkgrid, NO_INSTALLS, ld

PAGES = []

STATUTE = (
    '  <div class="note"><p><strong>The statutory picture.</strong> Florida Statute '
    '<a href="https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&amp;URL=1000-1099/1003/Sections/1003.48.html">'
    's.1003.48(1)</a> requires each district school board to make a course in the safe and lawful '
    'operation of motor vehicles available to secondary students, and allows a district to deliver it with '
    'its own personnel or by contracting it out. Districts should confirm their own procurement route and '
    'any licensing requirements that apply to a given provider.</p></div>')

SLOSBERG = (
    '  <div class="note"><p><strong>If you fund driver education through the Dori Slosberg Act.</strong> '
    '<a href="https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&amp;URL=0300-0399/0318/Sections/0318.1215.html">'
    's.318.1215</a> lets a county add $5 to civil traffic penalties to support driver education, and '
    'requires that programs receiving those funds devote at least 30 percent of student instruction time '
    'to behind-the-wheel training. Simulator time is not behind-the-wheel time and cannot count toward '
    'that 30 percent. We would rather say so now than have it surface during an audit.</p></div>')


def district(slug, name, official, hq, facts, situation, pitch, faqs, enrollment_line=''):
    return dict(
        slug=slug, url='/school-districts/%s/' % slug, ctype='school_district',
        title='Driving Simulator Programs for %s | Academy Driver Education' % official,
        desc='Driving simulator programs available to %s for driver education and teen driver safety. '
             'Mobile and longer-term options, delivered and staffed from Tampa.' % official,
        crumbs='<a href="/">Home</a> / <a href="/school-districts/">School Districts</a> / ' + name,
        eyebrow='Serving ' + name,
        h1='Driving Simulator Programs for %s' % name,
        lede=pitch,
        cta1='Request Program Information',
        final_h='Start a conversation about %s' % name,
        final_p='Tell us the schools involved, rough student numbers and your timeframe. We will send '
                'program options and costs.',
        ld=ld('Service', 'Driving Simulator Programs For %s' % official,
              'Simulator-based driver education and teen driver safety programs available to %s.' % official,
              '/school-districts/%s/' % slug),
        body='\n\n'.join([
            prose('The District', 'What we know about %s' % name, '', facts),
            NO_INSTALLS,
            prose('The Fit', 'Where a simulator would actually help', '', situation),
            STATUTE,
            SLOSBERG,
            cards('Delivery', 'Three ways this could run', '', [
                ('Mobile program', 'We bring simulators to a campus, run sessions through the day and '
                 'remove everything afterwards. The simplest way for a district to trial the format.'),
                ('Short-term placement', 'Equipment on site for a defined period, such as a semester or a '
                 'safety initiative, supported by our staff.'),
                ('Longer-term solutions', 'Where a district wants a permanent capability, that is a '
                 'conversation rather than a catalog item. We are happy to have it.'),
            ]),
            linkgrid('Related', 'Programs and other districts', '', [
                ('/schools/', 'SCHOOL PROGRAMS', 'The four program formats in detail.'),
                ('/school-districts/', 'ALL DISTRICTS', 'Other Florida districts we can serve.'),
                ('/training/', 'SKILLS COVERED', 'The specific driving skills these programs address.'),
            ]),
            faq(faqs),
        ]),
    )


# ---------------------------------------------------------------- HUB -----
PAGES.append(dict(
    slug='school-districts', url='/school-districts/', ctype='district_hub',
    title='Driving Simulator Programs for Florida School Districts | Academy',
    desc='Driving simulator programs available to Florida school districts for driver education and teen driver safety. Mobile and longer-term options, delivered from Tampa.',
    crumbs='<a href="/">Home</a> / School Districts',
    eyebrow='Florida School Districts',
    h1='Driving Simulator Programs for Florida School Districts',
    lede='Academy offers simulator-based driver education and teen safety programs that Florida districts '
         'can evaluate, trial and deploy. We are based in Tampa and can serve districts statewide.',
    cta1='Request Program Information',
    final_h='Which district are you with?',
    final_p='Tell us the district, the schools involved and rough student numbers. We will come back with '
            'options and costs.',
    ld=ld('Service', 'Driving Simulator Programs For Florida School Districts',
          'Simulator-based driver education and teen driver safety programs available to Florida school districts.',
          '/school-districts/'),
    body='\n\n'.join([
        prose('Start Here', 'What districts are actually solving', '', [
            '<p>Every Florida district has the same structural constraint. Behind-the-wheel instruction '
            'needs a car, a certified instructor and a road, and those three things cap how many students '
            'can be trained no matter how much a district wants to train more.</p>',
            '<p>A simulator does not remove that constraint, and anyone claiming otherwise is overselling. '
            'What it does is add capacity for the parts of driver education that do not require a public '
            'road, and let students experience hazards that cannot be staged safely at all.</p>',
            '<h3>What we hear districts are working against</h3>',
            '<ul>'
            '<li><strong>Throughput.</strong> More students want the course than the vehicle fleet supports.</li>'
            '<li><strong>Instructor availability.</strong> Certified instructors are the binding constraint '
            'in most districts, not equipment.</li>'
            '<li><strong>Coverage.</strong> Programs that exist at some schools and not others.</li>'
            '<li><strong>Hazard exposure.</strong> The situations that cause crashes are the ones you cannot '
            'practice on a road with a permit holder.</li>'
            '</ul>',
        ]),
        NO_INSTALLS,
        STATUTE,
        linkgrid('Phase One', 'Districts with a dedicated page',
                 'These six are where we have written detail. We can serve any Florida district, with or '
                 'without a page here.', [
                     ('/school-districts/hillsborough-county/', 'HILLSBOROUGH COUNTY',
                      'Our home county, and the district with the most established program.'),
                     ('/school-districts/pasco-county/', 'PASCO COUNTY',
                      'Where the district course is delivered online.'),
                     ('/school-districts/pinellas-county/', 'PINELLAS COUNTY',
                      'Where driver education runs as after-school and summer camps.'),
                     ('/school-districts/polk-county/', 'POLK COUNTY',
                      'One of Florida’s largest districts by enrollment.'),
                     ('/school-districts/manatee-county/', 'MANATEE COUNTY',
                      'A mid-sized coastal district south of Tampa Bay.'),
                     ('/school-districts/sarasota-county/', 'SARASOTA COUNTY',
                      'A compact district with seven high schools.'),
                 ]),
        prose('Everywhere Else', 'We can serve any Florida district', '', [
            '<p>Orange, Osceola, Seminole, Lake, Marion, Brevard and every other Florida district can be '
            'served from Tampa. They do not have dedicated pages yet, which is deliberate. We would rather '
            'write something genuinely specific about a district than publish the same page with the name '
            'changed.</p>',
            '<p>If you are with a district not listed, get in touch. The answer is almost certainly yes.</p>',
        ]),
        SLOSBERG,
        prose('Context', 'Florida teen licensing, briefly', '', [
            '<p>Worth having straight when planning a program. Under Florida law a learner license is '
            'available from age 15, and a Class E license from 16 requires the learner license to have been '
            'held for at least 12 months and at least 50 hours of supervised driving, of which 10 must be '
            'at night. Sixteen year olds may not drive between 11pm and 6am, and seventeen year olds not '
            'between 1am and 5am, with exceptions for work or when accompanied by a licensed driver aged 21 '
            'or over.</p>',
            '<p>Source: <a href="https://www.flhsmv.gov/pdf/handbooks/englishdriverhandbook.pdf">Florida '
            'Driver License Handbook</a> and <a href="https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&amp;URL=0300-0399/0322/Sections/0322.05.html">s.322.05</a>. '
            'Confirm current requirements with FLHSMV rather than relying on this summary.</p>',
        ]),
        faq([
            ('Do you have simulators in Florida school districts already?',
             'No. Academy does not currently have simulators installed in any school district. Everything on '
             'this site describes programs we offer and can deploy, not existing installations.'),
            ('Can simulator time replace behind-the-wheel instruction?',
             'No. It supplements classroom and behind-the-wheel instruction. If your program is funded under '
             'the Dori Slosberg Act, note that at least 30 percent of student time must be behind the wheel, '
             'and simulator time does not count toward it.'),
            ('Which districts can you serve?',
             'Any Florida district. We are based in Tampa and travel statewide. The six with pages here are '
             'simply where we have written detail first.'),
            ('How does a district buy this?',
             'Tell us how your district procures and we will work to it. Quotes, W-9s, insurance '
             'certificates and vendor registration usually take longer than scheduling does, so raise it '
             'early.'),
            ('Can we trial it before committing?',
             'Yes, and we would suggest it. A single day on one campus tells a district more than a '
             'proposal does.'),
            ('What does it cost?',
             'It depends on student numbers, duration, number of simulators and travel. We quote per '
             'program rather than publishing a price.'),
        ]),
    ]),
))

# --------------------------------------------------------- HILLSBOROUGH ---
PAGES.append(district(
    'hillsborough-county', 'Hillsborough County', 'Hillsborough County Public Schools', 'Tampa',
    ['<p>Hillsborough County Public Schools is headquartered at 901 E. Kennedy Blvd in Tampa and reported '
     'approximately 171,553 non-charter students for 2025 to 2026. The county covers 1,266 square miles, '
     'which the district itself notes, and that spread matters for any program delivered across multiple '
     'campuses.</p>',
     '<p>Hillsborough runs one of the more established driver education programs in the region. The '
     'district describes school-based and summer instruction combining classroom and behind-the-wheel '
     'training through DELAP-certified educators, and states that each high school has a DMV-approved '
     'driving range. Its program page lists State Farm, the Kiefer Foundation and the Teen Safe Driving '
     'Coalition as partners.</p>',
     '<p>Source: <a href="https://www.hillsboroughschools.org/page/drivers-education/">district driver '
     'education program</a> and <a href="https://www.hillsboroughschools.org/o/hcps/page/about-hcps">'
     'district profile</a>.</p>'],
    ['<p>Hillsborough is the district where we would be least likely to talk about filling a gap, because '
     'the program is already there. A district with a driving range at every high school and certified '
     'instructors does not need someone explaining why driver education matters.</p>',
     '<p>What a simulator could add here is different. It is the hazard work that a driving range cannot '
     'safely stage: a car pulling out, a skid, a genuine emergency stop. A range teaches control in a '
     'controlled space. It cannot teach a student what an unexpected hazard feels like at speed.</p>',
     '<h3>Where it would fit</h3>',
     '<ul>'
     '<li><strong>Ahead of range time.</strong> Students arriving having already made the obvious mistakes '
     'somewhere with no consequences.</li>'
     '<li><strong>For the students in the queue.</strong> Behind-the-wheel and range time is rationed. A '
     'simulator gives the rest of a cohort something better than waiting.</li>'
     '<li><strong>Across 1,266 square miles.</strong> A mobile program can rotate between campuses in a way '
     'a fixed installation cannot.</li>'
     '<li><strong>Alongside existing partners.</strong> Safety-focused programming complements rather than '
     'competes with the initiatives already running.</li>'
     '</ul>',
     '<p>This is also our home county. Academy is based at 1421 Massaro Blvd in Tampa, which makes '
     'Hillsborough the easiest district in Florida for us to serve and the cheapest to trial.</p>'],
    'Hillsborough County Public Schools already runs an established driver education program with a '
    'DMV-approved range at each high school. A simulator is not a replacement for any of that. It covers '
    'the hazards a range cannot safely stage.',
    [('Does Hillsborough already have driver education?',
      'Yes, and a well established one. The district describes school-based and summer instruction with '
      'DELAP-certified educators and states that each high school has a DMV-approved driving range. Our '
      'programs would supplement that, not replace it.'),
     ('Do you have simulators in Hillsborough schools?',
      'No. Academy does not currently have simulators installed in any school district. This describes what '
      'we can provide.'),
     ('What would a simulator add to a program that already has a range?',
      'Hazard exposure. A range teaches vehicle control in a controlled space. It cannot safely stage a car '
      'pulling out, a skid or a genuine emergency stop, and those are what a simulator does well.'),
     ('Can you cover multiple campuses?',
      'Yes. A mobile program rotates between schools, which suits a district spread across 1,266 square '
      'miles better than a single fixed installation would.'),
     ('You are based in Hillsborough. Does that change anything?',
      'Practically, yes. We are at 1421 Massaro Blvd in Tampa, so this is the district with the shortest '
      'logistics and the lowest travel cost for a trial.'),
     ('How would we start?',
      'Usually a single day on one campus. It tells a district more than a proposal does, and it is the '
      'cheapest way to find out whether the format suits your students.')],
))

# ---------------------------------------------------------------- PASCO ---
PAGES.append(district(
    'pasco-county', 'Pasco County', 'Pasco County Schools', "Land O' Lakes",
    ['<p>Pasco County Schools is headquartered at 7227 Land O’ Lakes Blvd. The district’s driver '
     'education course is delivered online through Pasco eSchool, which lists Driver Education S among its '
     'current high school electives.</p>',
     '<p>We could not confirm a district-run behind-the-wheel program from public sources. That is a '
     'meaningful difference from neighboring districts and it shapes what would actually be useful here.</p>',
     '<p>Source: <a href="https://eschool.pasco.k12.fl.us/high-school-courses/">Pasco eSchool high school '
     'courses</a>.</p>'],
    ['<p>An online driver education course has an obvious structural limitation: there is no practical '
     'component at all. A student can complete it having never touched a steering wheel in any '
     'instructional setting.</p>',
     '<p>That makes Pasco a genuinely different conversation from Hillsborough. It is not about adding '
     'hazard work to an existing practical program. It is about whether there is any hands-on element '
     'available to students taking the course at all.</p>',
     '<h3>Where it would fit</h3>',
     '<ul>'
     '<li><strong>As the practical counterpart to an online course.</strong> A student who has completed '
     'the theory has somewhere to apply it.</li>'
     '<li><strong>Without needing a fleet.</strong> A simulator program does not require vehicles, '
     'certified behind-the-wheel instructors or a range, which is the whole reason those programs are hard '
     'to start.</li>'
     '<li><strong>Campus by campus.</strong> A mobile program can serve individual high schools without a '
     'district-wide commitment.</li>'
     '<li><strong>As an evaluation.</strong> A single day tells the district whether the format is worth '
     'pursuing further.</li>'
     '</ul>',
     '<p>To be clear about what this is not: a simulator does not make a student road-ready and does not '
     'satisfy licensing requirements. If the district wants a behind-the-wheel program, it needs vehicles '
     'and certified instructors, and we would say so.</p>'],
    'Pasco County Schools delivers driver education online through Pasco eSchool. That means the course has '
    'no practical component, which is a different problem from the one neighboring districts have.',
    [('Does Pasco County offer driver education?',
      'The district lists Driver Education S as an online course through Pasco eSchool. We could not '
      'confirm a district-run behind-the-wheel program from public sources.'),
     ('Do you have simulators in Pasco schools?',
      'No. Academy does not currently have simulators installed in any school district. This describes what '
      'we can provide.'),
     ('Could a simulator replace behind-the-wheel training?',
      'No. If the district wants a behind-the-wheel program it needs vehicles and certified instructors. A '
      'simulator adds a practical element to a course that currently has none, which is a different thing.'),
     ('Would this need a vehicle fleet?',
      'No, and that is much of the appeal here. A simulator program needs floor space and power rather than '
      'cars, instructors and a range.'),
     ('Can you serve a single high school rather than the whole district?',
      'Yes. A mobile program can run campus by campus without a district-wide commitment.'),
     ('How would a school start?',
      'A single day on one campus is the usual way. It costs little and answers the question.')],
))

# ------------------------------------------------------------- PINELLAS ---
PAGES.append(district(
    'pinellas-county', 'Pinellas County', 'Pinellas County Schools', 'Largo',
    ['<p>Pinellas County Schools is headquartered at 301 Fourth St. SW in Largo. The district runs driver '
     'education as after-school camps, normally about one per quarter and subject to instructor '
     'availability, and documented a 2025 summer program across ten high school sites with a $250 lab '
     'fee.</p>',
     '<p>District purchasing records show driver education vehicles leased at scale: approximately 27 '
     'vehicles for 13 high school sites, and approximately 57 for 2024 summer sessions across ten sites. '
     'That is a real, funded program with a real fleet.</p>',
     '<p>Source: <a href="https://www.pcsb.org/learning/high-school-education/driver-education">district '
     'driver education page</a> and <a href="https://www.pcsb.org/cms/lib/FL01903687/Centricity/Domain/187/NOIA%202%2027%202024.pdf">'
     'board purchasing documents</a>.</p>'],
    ['<p>Pinellas is the clearest throughput case of the six. The district has vehicles, sites and a funded '
     'program, and still delivers driver education as camps roughly once a quarter, explicitly subject to '
     'instructor availability.</p>',
     '<p>That phrase is the whole story. The constraint is not money or vehicles. It is certified '
     'instructors and calendar time, and neither of those is solved by leasing more cars.</p>',
     '<h3>Where it would fit</h3>',
     '<ul>'
     '<li><strong>Between camps.</strong> Students waiting for a quarterly slot have nothing in the '
     'meantime. A simulator program can run in that gap.</li>'
     '<li><strong>Increasing reach per instructor.</strong> One member of staff can oversee several '
     'simulators at once, which is not true of vehicles.</li>'
     '<li><strong>Across the sites already identified.</strong> The district has already mapped which high '
     'schools host driver education, so the rotation is defined.</li>'
     '<li><strong>Preparation before a camp.</strong> Students arriving at a camp having already covered '
     'basics get more from limited behind-the-wheel time.</li>'
     '</ul>'],
    'Pinellas County Schools runs driver education as after-school camps, about one a quarter, subject to '
    'instructor availability. That is a capacity problem, and it is the kind a simulator program can help '
    'with.',
    [('What does Pinellas currently offer?',
      'The district runs after-school driver education camps, normally about one per quarter and subject to '
      'instructor availability, and documented a 2025 summer program across ten high school sites with a '
      '$250 lab fee.'),
     ('Do you have simulators in Pinellas schools?',
      'No. Academy does not currently have simulators installed in any school district. This describes what '
      'we can provide.'),
     ('The district already leases vehicles. Why add simulators?',
      'Because the documented constraint is instructor availability rather than vehicles. One member of '
      'staff can oversee several simulators at once, which is not true of cars.'),
     ('Could this run between camps?',
      'That is the most obvious fit. Students waiting for a quarterly slot currently have nothing in the '
      'interim.'),
     ('Does simulator time count toward the behind-the-wheel component?',
      'No. If the program is funded under the Dori Slosberg Act, at least 30 percent of student time must '
      'be behind the wheel and simulator time does not count toward it.'),
     ('How would the district start?',
      'A single day at one of the sites already hosting driver education. The rotation is already mapped, '
      'which makes a trial straightforward.')],
))

# ----------------------------------------------------------------- POLK ---
PAGES.append(district(
    'polk-county', 'Polk County', 'Polk County Public Schools', 'Bartow',
    ['<p>Polk County Public Schools is headquartered at 1915 S. Floral Ave in Bartow and serves '
     'approximately 114,000 students, making it one of the largest districts in Florida.</p>',
     '<p>We could not confirm the current shape of the district’s driver education provision from '
     'public sources, so we are not going to characterize it. If you are with the district and can tell us '
     'what actually runs, that will make any conversation far more useful.</p>',
     '<p>Source: <a href="https://www.polkschoolsfl.com/about/thedistrict">district profile</a>.</p>'],
    ['<p>Polk is large, geographically spread and centered on Lakeland and Bartow rather than a single '
     'urban core. For any program delivered across campuses, that spread is the defining practical fact.</p>',
     '<p>A district of roughly 114,000 students has a scale problem before it has anything else. Whatever '
     'driver education provision exists, reaching a meaningful share of eligible students in a district '
     'that size is a throughput question.</p>',
     '<h3>Where it would fit</h3>',
     '<ul>'
     '<li><strong>Reach per instructor.</strong> One member of staff overseeing several simulators covers '
     'more students per session than vehicle-based instruction can.</li>'
     '<li><strong>A rotation rather than an installation.</strong> A mobile program can move between '
     'campuses across a spread-out district.</li>'
     '<li><strong>Weather independence.</strong> A simulator program runs in a gym regardless of what '
     'central Florida summer weather is doing.</li>'
     '<li><strong>Trial at one school first.</strong> In a district this size, a single campus is the '
     'sensible way to evaluate before scaling.</li>'
     '</ul>'],
    'Polk County Public Schools serves around 114,000 students across a large geographic area. At that '
    'scale, reaching a meaningful share of eligible students is a throughput question before it is '
    'anything else.',
    [('What driver education does Polk currently offer?',
      'We could not confirm that from public sources, so we are not going to characterize it. If you can '
      'tell us what actually runs, the conversation will be more useful.'),
     ('Do you have simulators in Polk schools?',
      'No. Academy does not currently have simulators installed in any school district. This describes what '
      'we can provide.'),
     ('Can you cover a district this spread out?',
      'Yes, through a rotating mobile program rather than a fixed installation. We are based in Tampa and '
      'travel across Florida.'),
     ('How many students could take part in a day?',
      'It depends on session length and how many simulators. Give us the cohort size and the window and we '
      'will give you a realistic number.'),
     ('Would we have to commit district-wide?',
      'No. In a district this size we would suggest one campus first, then decide.'),
     ('What does it cost?',
      'It depends on numbers, duration and travel. We quote per program rather than publishing a price.')],
))

# -------------------------------------------------------------- MANATEE ---
PAGES.append(district(
    'manatee-county', 'Manatee County', 'the School District of Manatee County', 'Bradenton',
    ['<p>The School District of Manatee County is headquartered at 215 Manatee Ave. W in Bradenton. The '
     'district’s published fast facts give a projected 2024 to 2025 enrollment of approximately 53,416 '
     'students across traditional, charter, home-school and PEP students, and approximately seven '
     'traditional high schools.</p>',
     '<p>We could not confirm the current shape of the district’s driver education provision from '
     'public sources.</p>',
     '<p>Source: <a href="https://www.manateeschools.net/page/fast-facts">district fast facts</a>.</p>'],
    ['<p>Seven high schools is a genuinely workable number. It is small enough that a rotating program can '
     'reach every campus in a manageable schedule, and large enough that the reach is meaningful.</p>',
     '<p>That is a different proposition from Hillsborough, where 1,266 square miles makes full coverage a '
     'logistics exercise, or Polk, where the scale itself is the constraint.</p>',
     '<h3>Where it would fit</h3>',
     '<ul>'
     '<li><strong>Full district coverage is realistic.</strong> Seven campuses can be reached in a defined '
     'rotation rather than as an ongoing program with no end.</li>'
     '<li><strong>Consistency across schools.</strong> Every student sees the same content rather than '
     'depending which campus they attend.</li>'
     '<li><strong>Close to Tampa.</strong> Travel from our Tampa base is short, which keeps the cost of a '
     'rotation down.</li>'
     '<li><strong>A defined initiative.</strong> A district-wide safety week across seven schools is an '
     'achievable piece of work rather than an aspiration.</li>'
     '</ul>'],
    'The School District of Manatee County has approximately seven traditional high schools, which makes '
    'full district coverage a realistic piece of work rather than an open-ended commitment.',
    [('How many high schools does Manatee have?',
      'The district’s published fast facts indicate approximately seven traditional high schools, with '
      'a projected 2024 to 2025 enrollment of about 53,416 students across all program types.'),
     ('Do you have simulators in Manatee schools?',
      'No. Academy does not currently have simulators installed in any school district. This describes what '
      'we can provide.'),
     ('Could you cover every high school in the district?',
      'With seven campuses, a full rotation is realistic in a defined schedule. That is not true of every '
      'district we could serve.'),
     ('What driver education does the district currently run?',
      'We could not confirm that from public sources. If you can tell us, the conversation will be more '
      'useful.'),
     ('How far is Manatee from your base?',
      'We are at 1421 Massaro Blvd in Tampa, so travel is short and a rotation across the district is '
      'practical.'),
     ('Could this be a district-wide safety initiative?',
      'Yes. Across seven campuses that is an achievable piece of work rather than an open-ended program.')],
))

# ------------------------------------------------------------- SARASOTA ---
PAGES.append(district(
    'sarasota-county', 'Sarasota County', 'Sarasota County Schools', 'Sarasota',
    ['<p>Sarasota County Schools is headquartered at 1960 Landings Blvd in Sarasota. The district profile '
     'gives more than 44,000 students and identifies seven high schools.</p>',
     '<p>We could not confirm the current shape of the district’s driver education provision from '
     'public sources.</p>',
     '<p>Source: <a href="https://www.sarasotacountyschools.net/o/scs/page/about-sarasota-county-schools">'
     'district profile</a>.</p>'],
    ['<p>Sarasota is compact and comparatively small, with seven high schools and more than 44,000 '
     'students. Both facts point the same way: a district-wide program here is a finite piece of work.</p>',
     '<p>Compactness matters more than it sounds. A rotation between seven schools in a geographically '
     'tight county is a fundamentally easier scheduling problem than the same rotation across a district '
     'spanning hundreds of square miles, and it costs less to run.</p>',
     '<h3>Where it would fit</h3>',
     '<ul>'
     '<li><strong>District-wide coverage is genuinely achievable.</strong> Seven campuses, close together.</li>'
     '<li><strong>Repeat visits are practical.</strong> Short travel makes a recurring program viable '
     'rather than a one-off.</li>'
     '<li><strong>Consistency.</strong> Every student in the district can see the same program.</li>'
     '<li><strong>Evaluation is cheap.</strong> One day at one campus, then decide.</li>'
     '</ul>'],
    'Sarasota County Schools has seven high schools and more than 44,000 students in a compact county. '
    'District-wide coverage is a finite piece of work here rather than an open-ended program.',
    [('How big is Sarasota County Schools?',
      'The district profile gives more than 44,000 students and identifies seven high schools.'),
     ('Do you have simulators in Sarasota schools?',
      'No. Academy does not currently have simulators installed in any school district. This describes what '
      'we can provide.'),
     ('Could you run a program across the whole district?',
      'With seven high schools in a compact county, yes. That is a finite rotation rather than an '
      'open-ended commitment.'),
     ('What driver education does the district currently run?',
      'We could not confirm that from public sources. Tell us what actually runs and the conversation will '
      'be more useful.'),
     ('Would repeat visits be practical?',
      'More so here than in most districts, because the travel is short and the campuses are close '
      'together.'),
     ('How would we evaluate it?',
      'One day at one campus. It costs little and tells you more than a proposal.')],
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-56s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
