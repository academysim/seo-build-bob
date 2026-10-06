# -*- coding: utf-8 -*-
"""Health: /programs/ hub + 5 programs, /locations/ hub + 5 service areas.

These pages describe format, staffing, setup, accessibility and logistics.
They deliberately do NOT describe health, cognitive or rehabilitation benefits,
because Academy is not a medical provider and the brief forbids outcome claims.

Location pages here target activity directors at senior communities, which is a
different intent from the Events location pages (corporate rentals). Titles are
explicit about that so the two properties do not compete.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from health_pages import (write, sec, prose, cards, faq, linkgrid,
                          SCOPE, ACCESS, CROSS, ld)

PAGES = []

LOGISTICS = prose('Logistics', 'WHAT WE NEED FROM YOU', '', [
    '<h3>The room</h3>'
    '<p>An activity room, dining room, common area or multipurpose space all work. We need floor space, '
    'mains power at the setup point, and a route in from a vehicle. Tell us about elevators, door widths '
    'and thresholds before the day rather than on it.</p>',
    '<h3>Numbers and time</h3>'
    '<p>How many residents you expect and how long you have. Those two numbers decide how many simulators '
    'make sense and how long each person gets in the seat.</p>',
    '<h3>Your staff</h3>'
    '<p>Our team runs the simulators. Your staff know your residents and handle anything involving personal '
    'care, transfers or supervision. That division works better than either of us trying to do both.</p>',
    '<h3>Scheduling</h3>'
    '<p>Mid-morning and early afternoon tend to work best in most communities, but you know your residents '
    'and your calendar better than we do.</p>',
])


def program(slug, eyebrow, title, desc, h1, lede, what, format_cards, extras, faqs, ldname):
    return dict(
        slug=slug, url='/programs/%s/' % slug, ctype='health_program',
        title=title, desc=desc,
        crumbs='<a href="/">Home</a> / <a href="/programs/">Programs</a> / ' + eyebrow,
        eyebrow=eyebrow, h1=h1, lede=lede,
        cta1='Plan a Program',
        final_h='TALK TO US ABOUT<br><span class="amber">YOUR COMMUNITY.</span>',
        final_p='Tell us the community, roughly how many residents and what you are trying to arrange. '
                'We will come back with formats and costs.',
        ld=ld('Service', ldname, desc, '/programs/%s/' % slug),
        body='\n\n'.join([
            prose('The Program', 'WHAT IT ACTUALLY IS', '', what),
            SCOPE,
            cards('Format', 'HOW IT RUNS', '', format_cards),
            prose('Accessibility', 'WHO CAN TAKE PART', '', ACCESS),
            LOGISTICS,
        ] + list(extras) + [
            linkgrid('Related', 'OTHER PROGRAMS', '', [
                ('/programs/', 'ALL PROGRAMS', 'The full range of formats we run.'),
                ('/locations/', 'WHERE WE SERVE', 'Florida communities we can travel to.'),
            ]),
            CROSS,
            faq(faqs),
        ]),
    )


# --------------------------------------------------------- PROGRAM HUB ----
PAGES.append(dict(
    slug='programs', url='/programs/', ctype='health_program_hub',
    title='Racing Simulator Programs for Senior Living Communities | Academy',
    desc='Simulator programs for senior living, 55+ and retirement communities in Florida. Staffed, seated, wheelchair-friendly setups. Event and recurring formats available.',
    crumbs='<a href="/">Home</a> / Programs',
    eyebrow='Programs',
    h1='RACING SIMULATOR PROGRAMS<br>FOR SENIOR COMMUNITIES',
    lede='We bring simulators to senior living, 55+ and retirement communities across Florida, set them up '
         'and run the session. Residents drive sitting down, at whatever pace suits them.',
    cta1='Plan a Program',
    final_h='WHAT ARE YOU<br><span class="amber">PLANNING?</span>',
    final_p='Tell us the community, resident numbers and the kind of occasion. We will suggest a format.',
    ld=ld('CollectionPage', 'Racing Simulator Programs For Senior Living Communities',
          'Simulator programs for senior living, 55+ and retirement communities across Florida.',
          '/programs/'),
    body='\n\n'.join([
        prose('Start Here', 'WHY THIS WORKS IN A COMMUNITY', '', [
            '<p>Activity directors have a hard problem. Most programming splits the room into people who '
            'can take part and people who watch, and the watching group knows exactly which one they are '
            'in.</p>',
            '<p>A racing simulator is unusual because it is seated, it needs no physical strength, and it '
            'does not require anyone to have done it before. A resident who cannot stand for long, cannot '
            'grip firmly or has not driven for a decade can still take a turn.</p>',
            '<h3>What actually happens in the room</h3>',
            '<ul>'
            '<li>Residents take turns in the seat while others watch the screen</li>'
            '<li>Our staff set each person up individually and stay with them</li>'
            '<li>Difficulty is adjusted per person, so nobody is out of their depth</li>'
            '<li>Conversation happens around it, which is usually the real value</li>'
            '<li>Anybody can stop at any point, with no fuss</li>'
            '</ul>',
            '<p>A lot of residents drove for fifty years and gave it up. Being back behind a wheel, even a '
            'simulated one, means something to people. That is the honest reason this lands, and we are not '
            'going to dress it up as anything more clinical than that.</p>',
        ]),
        SCOPE,
        linkgrid('Programs', 'BROWSE BY FORMAT', 'Five formats, described in detail.', [
            ('/programs/senior-living-racing-simulator/', 'SENIOR LIVING PROGRAMS',
             'The core offering for senior living and independent living communities.'),
            ('/programs/55-plus-community-activities/', '55+ COMMUNITY ACTIVITIES',
             'Active adult communities, where the audience is younger and more competitive.'),
            ('/programs/senior-community-race-night/', 'RACE NIGHT',
             'A competitive evening with a leaderboard, for communities that want an event.'),
            ('/programs/retirement-community-events/', 'RETIREMENT COMMUNITY EVENTS',
             'Open houses, family days, holidays and marketing events.'),
            ('/programs/senior-wellness-activities/', 'WELLNESS PROGRAMMING',
             'Recurring sessions as part of an ongoing activity calendar.'),
        ]),
        prose('Accessibility', 'WHO CAN TAKE PART', '', ACCESS),
        LOGISTICS,
        CROSS,
        faq([
            ('Can you bring simulators to our community?',
             'Yes. We are based in Tampa and travel across Florida. Tell us where you are and we will '
             'confirm what a visit involves.'),
            ('How much space do we need?',
             'An activity room, dining room or common area is normally enough. We need floor space, mains '
             'power and a route in from a vehicle. Send photos or dimensions and we will confirm.'),
            ('Is staff provided?',
             'Yes. Our team sets up, runs the session and packs down. Your staff handle anything involving '
             'residents personally, including transfers and supervision.'),
            ('Is this suitable for beginners?',
             'Yes, and most participants are. Nobody needs to have driven recently or used a simulator '
             'before. Settings are adjusted per person.'),
            ('Can residents in wheelchairs take part?',
             'Tell us in advance and we will talk it through properly. Some setups work without '
             'transferring and some do not, and it is much better to plan that beforehand.'),
            ('Can the program be recurring?',
             'Yes. Some communities book a one-off event, others a recurring slot in the activity calendar. '
             'Both work.'),
            ('How does pricing work?',
             'It depends on the number of simulators, the length of the visit, travel and whether it is a '
             'one-off or recurring. We quote per program rather than publishing a price.'),
        ]),
    ]),
))

PAGES.append(program(
    'senior-living-racing-simulator', 'Senior Living',
    'Racing Simulator Programs for Senior Living Communities | Academy',
    'Staffed racing simulator programs for senior living and independent living communities in Florida. Seated, adjustable and suitable for beginners.',
    'SIMULATOR PROGRAMS FOR<br>SENIOR LIVING COMMUNITIES',
    'The core program. We bring simulators into your community, set up in a room you already use, and run '
    'sessions for residents at whatever pace suits them.',
    ['<p>This is the format most senior living and independent living communities book. It is not an event '
     'with a theme, it is simply an afternoon where residents get to drive.</p>',
     '<p>What makes it work in this setting is that it asks very little physically. Residents sit down, the '
     'wheel force can be reduced to almost nothing, and there is no time pressure or competition unless a '
     'community wants one.</p>',
     '<h3>The shape of a typical visit</h3>',
     '<ul>'
     '<li>We arrive ahead of the session and set up in your activity or common room</li>'
     '<li>Residents come and go rather than being scheduled into slots</li>'
     '<li>Each person gets set up individually, with settings adjusted to them</li>'
     '<li>Others watch the screen, which is a large part of the appeal</li>'
     '<li>We pack down afterwards and the room goes back to normal</li>'
     '</ul>'],
    [('Afternoon session', 'The most common booking. A few hours in an activity room with residents '
      'dropping in.'),
     ('Half day or full day', 'For larger communities where more residents want a turn than one afternoon '
      'allows.'),
     ('Recurring visits', 'A regular slot in the activity calendar, which residents start to look forward '
      'to.'),
     ('Alongside another activity', 'Running in the corner of an existing event rather than as the main '
      'attraction.')],
    [],
    [('How long does each resident get?',
      'As long as suits them. Some want two minutes, some want twenty. We adjust rather than running a '
      'strict rotation, unless numbers make that necessary.'),
     ('What if a resident has not driven in years?',
      'That is most participants. Settings are adjusted so the car is easy to control, and our staff stay '
      'with each person.'),
     ('Do residents need to remember anything?',
      'No. There is nothing to learn beforehand and nothing to memorize. Our staff handle everything except '
      'steering.'),
     ('Can residents with dementia take part?',
      'Often yes, with your staff present and guiding. You know your residents and we do not, so we would '
      'follow your lead entirely on who takes part and how.'),
     ('Is there any risk of falls?',
      'Participants are seated throughout. Getting into and out of the seat is where care is needed, and '
      'that is where your staff should assist.'),
     ('Can families join in?',
      'Yes, and it works well on family days. Grandchildren and grandparents competing tends to be the '
      'moment people remember.')],
    'Racing Simulator Programs For Senior Living Communities',
))

PAGES.append(program(
    '55-plus-community-activities', '55+ Communities',
    'Racing Simulator Activities for 55+ Communities | Academy',
    'Racing simulator activities for active adult and 55+ communities in Florida. Competitive formats, leaderboards and clubs, staffed and delivered.',
    'ACTIVITIES FOR<br>55+ COMMUNITIES',
    'Active adult communities are a different audience from senior living, and pretending otherwise '
    'produces a bland program. Here the appetite for competition is real.',
    ['<p>Residents of a 55+ community are typically independent, active and frequently competitive. Many '
     'still drive daily. Programming that treats them as frail lands badly, and they will tell you so.</p>',
     '<p>So this format leans into competition. Leaderboards, timed events, clubs and rivalries. The '
     'simulators are the same and the accessibility adjustments are still available, but the framing is '
     'completely different.</p>',
     '<h3>What works with this audience</h3>',
     '<ul>'
     '<li><strong>A leaderboard that persists.</strong> Residents come back specifically to move up it.</li>'
     '<li><strong>Recurring sessions.</strong> One-offs are enjoyed. Regular slots build a following.</li>'
     '<li><strong>Real competition.</strong> Brackets, head-to-head, and a season if the community wants '
     'one.</li>'
     '<li><strong>Difficulty available.</strong> Some residents want it genuinely hard, and turning the '
     'assistance off is trivial.</li>'
     '</ul>'],
    [('Competitive race night', 'A leaderboard, an evening, and a winner. The most requested format in '
      'active adult communities.'),
     ('Recurring club', 'A regular slot with a running leaderboard across weeks or months.'),
     ('Community tournament', 'A bracket across several sessions building to a final.'),
     ('Clubhouse open day', 'Simulators as the draw at an open house or amenity showcase.')],
    [],
    [('Is this different from your senior living program?',
      'In framing, yes. The equipment and the accessibility options are the same, but this audience usually '
      'wants competition rather than a gentle activity, and the program is built that way.'),
     ('Can we run an ongoing league?',
      'Yes. A persistent leaderboard across recurring visits is the format that builds the most '
      'participation in active adult communities.'),
     ('Can residents make it genuinely difficult?',
      'Yes. Driver assistance can be turned off entirely for anyone who wants that, and plenty do.'),
     ('Would this suit a clubhouse or amenity event?',
      'Very well. It draws people in and gives them something to do rather than stand around.'),
     ('How many simulators for a large community?',
      'It depends on how many residents you expect and over how long. Tell us both and we will size it.'),
     ('Can we do this annually rather than regularly?',
      'Yes, though communities that run it regularly get noticeably more out of it than those who book '
      'once a year.')],
    'Racing Simulator Activities For 55+ And Active Adult Communities',
))

PAGES.append(program(
    'senior-community-race-night', 'Race Night',
    'Senior Community Race Night | Racing Simulator Events | Academy',
    'A race night for your senior or 55+ community. Leaderboard, competition and a winner, delivered and staffed by Academy across Florida.',
    'RACE NIGHT<br>AT YOUR COMMUNITY',
    'A defined event with a beginning, a middle and a winner. Easier to promote than an open activity, and '
    'residents turn up for it because there is something at stake.',
    ['<p>An open activity session is easy to run and easy to ignore. A race night has a start time, a '
     'format and an outcome, which is why attendance is usually much higher.</p>',
     '<p>It also gives your community something to talk about afterwards, and something to photograph for '
     'a newsletter or a marketing page, which matters to more communities than will admit it.</p>',
     '<h3>How an evening usually runs</h3>',
     '<ul>'
     '<li>Everyone drives the same course under the same settings, so times are comparable</li>'
     '<li>A live leaderboard updates as people drive, which draws a crowd</li>'
     '<li>Residents can drive more than once to improve their time</li>'
     '<li>A final and a winner, with whatever prize the community wants to put up</li>'
     '<li>Accessibility settings remain available without affecting anyone&rsquo;s standing</li>'
     '</ul>'],
    [('Standard race night', 'Two to three hours, a leaderboard, a winner. The usual format.'),
     ('Head to head', 'Two simulators running the same session so residents race each other directly.'),
     ('Themed evening', 'Built around a holiday, an anniversary or a community occasion.'),
     ('Family race night', 'Residents and visiting family competing together, which is consistently the '
      'most popular version.')],
    [],
    [('How long does a race night take?',
      'Two to three hours suits most communities. Tell us resident numbers and we will confirm whether that '
      'is realistic for everyone to get a turn.'),
     ('Do we need to provide prizes?',
      'Entirely up to you. Most communities put up something small, and it matters far less than the '
      'leaderboard does.'),
     ('Can residents with limited mobility still compete fairly?',
      'Yes. Assistance settings do not change the leaderboard, so adjusting for a resident does not put '
      'them at a disadvantage.'),
     ('Is it noisy?',
      'It can get lively, which is usually the point. Volume is adjustable and headphones are an option if '
      'the space is shared.'),
     ('Can families attend?',
      'Yes, and family race nights are consistently the version residents enjoy most.'),
     ('Can you run this in the evening?',
      'Yes. Tell us the timing that suits your community and we will work to it.')],
    'Senior Community Race Night Simulator Events',
))

PAGES.append(program(
    'retirement-community-events', 'Community Events',
    'Racing Simulators for Retirement Community Events | Academy',
    'Racing simulators for retirement community open houses, family days, holidays and marketing events across Florida. Delivered and staffed.',
    'SIMULATORS FOR<br>COMMUNITY EVENTS',
    'For open houses, family days and holidays, where the job is drawing people in and giving them '
    'something to do once they arrive.',
    ['<p>Community events have a different objective from regular activity programming. An open house needs '
     'prospective residents and their adult children to stay long enough to have a conversation. A family '
     'day needs something that spans three generations.</p>',
     '<p>A simulator does both, because it is genuinely unexpected in this setting. People stop to watch, '
     'and a grandchild racing a grandparent is the kind of thing that gets photographed.</p>',
     '<h3>Where it helps most</h3>',
     '<ul>'
     '<li><strong>Open houses.</strong> Something for visitors to do while your team talks to the '
     'decision maker.</li>'
     '<li><strong>Family days.</strong> Works across ages, which very little programming does.</li>'
     '<li><strong>Holiday events.</strong> An alternative to another party with the same format as last '
     'year.</li>'
     '<li><strong>Marketing and press.</strong> It photographs well and it is genuinely differentiating.</li>'
     '</ul>'],
    [('Open house', 'Simulators running through a marketing event, drawing visitors in and holding them.'),
     ('Family day', 'Multi-generational, with residents and visiting family both taking part.'),
     ('Holiday event', 'Built into a seasonal celebration rather than run as a standalone.'),
     ('Grand opening', 'For a new community or a renovated amenity space.')],
    [],
    [('Will visitors and family want to take part, not just residents?',
      'Usually more so. Adult children and grandchildren tend to be the most competitive people in the '
      'room.'),
     ('Can this run alongside our existing event?',
      'Yes, and that is how most communities use it. It runs in a corner of a larger event rather than '
      'being the whole thing.'),
     ('Is it good for marketing photography?',
      'It is one of the more photogenic activities you can run, particularly when generations are '
      'competing against each other.'),
     ('How long do you stay?',
      'As long as your event runs, within reason. Tell us the hours and we will quote to them.'),
     ('Can you set up outdoors?',
      'Under cover and with power, yes. Direct sun on the screens is a problem and the equipment needs '
      'weather protection.'),
     ('How far ahead should we book?',
      'Earlier for holiday dates, which cluster. Otherwise a few weeks is usually enough.')],
    'Racing Simulators For Retirement Community Events',
))

PAGES.append(program(
    'senior-wellness-activities', 'Wellness Programming',
    'Racing Simulators in Senior Wellness Programming | Academy',
    'Adding simulator sessions to a senior community wellness and activity calendar. Recurring, seated and adjustable, delivered and staffed across Florida.',
    'SIMULATORS IN YOUR<br>ACTIVITY CALENDAR',
    'For communities that want this as a recurring part of programming rather than a one-off event. The '
    'main change is that residents build familiarity, and familiarity changes participation.',
    ['<p>A single visit is enjoyable and largely forgotten. A recurring slot behaves differently: '
     'residents who watched the first time take a turn the third time, and people who tried it once come '
     'back to beat their own time.</p>',
     '<p>That is the honest argument for recurring programming. It is about participation building over '
     'time, not about outcomes we are not qualified to claim.</p>',
     '<h3>What changes when it recurs</h3>',
     '<ul>'
     '<li>Residents who were hesitant the first time often join later</li>'
     '<li>A persistent leaderboard gives people a reason to return</li>'
     '<li>Our staff get to know your residents and what settings suit them</li>'
     '<li>It becomes a fixture on the calendar rather than a novelty</li>'
     '</ul>'],
    [('Monthly slot', 'The most common recurring arrangement, and enough for residents to remember it '
      'between visits.'),
     ('Fortnightly or weekly', 'For larger communities or where the activity calendar has room.'),
     ('Seasonal block', 'A defined run of visits, such as through the winter months.'),
     ('Rotating between buildings', 'For operators with several communities in one region.')],
    [SCOPE],
    [('Is this a therapy or wellness treatment?',
      'No. Academy is not a medical provider and we do not offer therapy, treatment or assessment. This is '
      'recreational activity programming, and we make no health or cognitive claims.'),
     ('Why book recurring rather than one-off?',
      'Participation builds. Residents who watch the first session often take part later, and a persistent '
      'leaderboard gives people a reason to come back.'),
     ('Can you serve several communities in one group?',
      'Yes. Operators with multiple communities in a region often rotate visits, which is usually more '
      'efficient for everyone.'),
     ('Does it fit into an existing activity calendar?',
      'Yes, and that works better than treating it as separate. Tell us your calendar and we will fit '
      'around it.'),
     ('Do the same staff come each time?',
      'Where we can, yes, and it helps. Staff who know your residents set them up faster and better.'),
     ('How does pricing work for recurring visits?',
      'Recurring arrangements are quoted differently from one-off events. Tell us the frequency you have in '
      'mind and we will price it properly.')],
    'Racing Simulators In Senior Wellness And Activity Programming',
))


if __name__ == '__main__':
    for p in PAGES:
        path, n = write(p)
        print('  %-52s %6d bytes' % (p['url'], n))
    print('  --- %d pages ---' % len(PAGES))
