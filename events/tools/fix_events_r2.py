# -*- coding: utf-8 -*-
"""Codex round 2 on the four newest event-type pages, plus a few site-wide items.

Kept "a lift of the throttle" on the drift page: that is motorsport usage, not
the British word for elevator. The other three were the elevator sense.
"""
import io, os, sys

D = sys.argv[1]


def edit(rel, pairs):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p):
        return 0
    s = io.open(p, encoding='utf-8', newline='').read()
    n = 0
    for o, x in pairs:
        c = s.count(o)
        if c:
            s = s.replace(o, x)
            n += c
    if n:
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s %d' % (rel, n))
    return n


ALL = []
for root, _, fs in os.walk(D):
    for f in fs:
        if f == 'index.html':
            ALL.append(os.path.relpath(os.path.join(root, f), D).replace(os.sep, '/'))
ALL.sort()

# ---------------- site-wide: British "lift" meaning elevator ----------------
# and the doorway claim, which the frame width alone does not establish
GLOBAL = [
    ('steps, gates, lifts, narrow hallways', 'steps, gates, elevators, narrow hallways'),
    ('door widths, steps, lifts, gate access', 'door widths, steps, elevators, gate access'),
    ('door and lift access', 'door and elevator access'),
    ('The frame is 26 inches wide, so a standard doorway is fine, but',
     'The frame is 26 inches wide, which usually clears a standard doorway, but that alone does not settle it:'),
    ('The frame is 26 inches wide, so a standard doorway is fine.',
     'The frame is 26 inches wide, which usually clears a standard doorway, though corners, thresholds and '
     'handling clearance still matter.'),
    # contractual hedging
    ('Delivery, setup, calibration, staffing and teardown are included as standard, and your quote '
     'sets out exactly what is covered for your event.',
     'Delivery, setup, calibration, staffing and teardown are typically included, and your quote sets out '
     'exactly what is covered and for how many hours.'),
    ('Delivery, setup, calibration, staffing and teardown are included as standard, and your quote confirms the detail.',
     'Delivery, setup, calibration, staffing and teardown are typically included, and your quote confirms '
     'the detail and the hours.'),
    ('Delivery, setup, staffing and teardown are included as standard, and your quote confirms the detail.',
     'Delivery, setup, staffing and teardown are typically included, and your quote confirms the detail '
     'and the hours.'),
    ('Bookings include delivery, setup, staffing and teardown as standard, with the detail confirmed in '
     'your quote.',
     'Bookings typically include delivery, setup, staffing and teardown, with the detail and the booked '
     'hours confirmed in your quote.'),
    ('Yes. Staffing is included as standard. Our team sets drivers up, resets sessions and keeps the queue '
     'moving, and your quote confirms the hours covered.',
     'Staffing is normally included. Our team sets drivers up, resets sessions and keeps the queue moving, '
     'and your quote confirms the hours covered.'),
]
for rel in ALL:
    edit(rel, GLOBAL)

# ---------------------------------------------------------- FUNDRAISERS ----
edit('event-types/fundraisers/index.html', [
    # manufactured performance history -> options
    ('<p>It also produces something a raffle cannot: a leaderboard that keeps updating all evening, which '
     'gives people a reason to enter more than once. The second and third entries are usually where the '
     'money actually comes from.</p>',
     '<p>It also produces something a raffle cannot: a leaderboard that keeps updating all evening, which '
     'gives people a reason to enter more than once. Repeat entries are the mechanic most fundraising '
     'formats are built around.</p>'),
    ('<h3>Find a sponsor for the activation</h3>'
     '<p>The most effective fundraising setups we see have a local business covering the cost of the rig in '
     'exchange for branding. It removes the activation from your budget entirely, which means everything '
     'taken on the night goes to the cause.</p>',
     '<h3>Consider a sponsor for the activation</h3>'
     '<p>One approach is to have a local business cover the cost of the rig in exchange for branding on the '
     'wrap and the leaderboard, so that less of what you raise goes back out on costs. We do not source or '
     'guarantee sponsors, and any sponsorship is an arrangement between you and them.</p>'),
    ('<h3>Keep the entry price low and the queue moving</h3>'
     '<p>Each simulator handles roughly 15 to 40 drivers an hour depending on session length. For a '
     'fundraiser, short runs at a low price usually raise more than long sessions at a high one, because '
     'people enter repeatedly.</p>',
     '<h3>Think about entry price against throughput</h3>'
     '<p>Each simulator handles roughly 15 to 40 drivers an hour depending on session length. Short runs at '
     'a lower price and long sessions at a higher one are both workable, and which suits you depends on your '
     'audience and how long the event runs.</p>'),
    ('Usually by selling entries. A small amount per run, with a live leaderboard giving people a reason to '
     'come back and try again. Repeat entries are normally where most of the money comes from.',
     'Most commonly by selling entries: a set amount per run, with a live leaderboard giving people a reason '
     'to come back and try again. How you price and structure it is your call.'),
    ('Yes, and it is the arrangement we would suggest. A local business covers the activation in exchange for '
     'branding on the rig and the leaderboard, so more of what you take on the night goes to the cause.',
     'That is a common arrangement: a local business covers the activation in exchange for branding on the '
     'rig and the leaderboard. To be clear, we do not source or guarantee sponsors, and the agreement is '
     'between you and them.'),
    ('In our experience short paid runs with a live leaderboard, because people enter more than once. Team '
     'entries work well when you are selling to businesses rather than individuals.',
     'Short paid runs with a live leaderboard suit events selling to individuals, and team entries suit '
     'events selling to businesses. We can run either, and we would rather talk through your audience than '
     'promise a figure.'),
    # fund handling
    ('We are a commercial supplier, not a charity partner, and we '
     'do not administer donations or handle funds raised at your event.',
     'We are a commercial supplier, not a charity partner. Collecting entries, handling funds, refunds, '
     'prizes, receipts and any tax, charity registration or local rules that apply to your event are the '
     'organizer&rsquo;s responsibility, not ours.'),
    ('No. We supply and run the simulators. Collecting entries and administering funds is for your team, and '
     'we are a commercial supplier rather than a charity partner.',
     'No. We supply and run the simulators. Collecting entries, handling funds, refunds, prizes, receipts '
     'and any tax or charity compliance are for your team. We are a commercial supplier rather than a '
     'charity partner.'),
    ('the ask, because '
     'entering a race is a transaction people understand and enjoy rather than a donation they feel obliged '
     'to make.',
     'the ask, because entering a race is a transaction people understand and enjoy rather than a '
     'straight request for money.'),
    ('<li><strong>Challenge the guest.</strong> Someone credible sets a time and people pay to try to beat it.</li>',
     '<li><strong>Challenge a guest driver.</strong> An invited driver sets a time and people pay to try to '
     'beat it.</li>'),
    # child suitability
    ('Yes. Driver aids make the cars manageable for children and first-time adults, and our staff set every '
     'driver up.',
     'Usually yes. Driver aids make the cars manageable for children and first-time adults and our staff set '
     'every driver up, though suitability depends on the child fitting the rig safely and on supervision and '
     'venue rules. Tell us the age range and we will advise.'),
])

# ------------------------------------------------- CLIENT ENTERTAINMENT ----
edit('event-types/client-entertainment/index.html', [
    ('<li><strong>Our staff run it entirely.</strong> Your team should be talking to clients, not resetting '
     'sessions or explaining the pedals.</li>',
     '<li><strong>Our staff run it.</strong> Your team should be talking to clients, not resetting sessions '
     'or explaining the pedals.</li>'),
    ('There is no fixed minimum. Small hospitality events are quoted differently from large activations, so '
     'tell us the group size and we will give you a sensible number.',
     'We do not publish a minimum. Small hospitality events are quoted differently from large activations, '
     'so tell us the group size and we will give you a sensible number.'),
    ('No. Our staff run the activation for the duration so your people can concentrate on your clients.',
     'No. Our staff run the activation for the booked hours so your people can concentrate on your clients.'),
    ('(\'04 / Pitches\', \'PITCH AND PROPOSAL EVENTS\', \'Something memorable attached to a business conversation.\')',
     '(\'04 / Pitches\', \'PITCH AND PROPOSAL EVENTS\', \'Something memorable attached to a business conversation.\')'),
    ('<div class="type-desc">Something memorable attached to a business conversation.</div>',
     '<div class="type-desc">Something memorable attached to a business conversation, subject to your '
     'client&rsquo;s own gift and hospitality policy.</div>'),
    ('<li><strong>Volume matters.</strong> Headphones or lower audio, so the room stays conversational.</li>',
     '<li><strong>Volume matters.</strong> Headphones or lower audio, so the room stays conversational.</li>'
     '\n     <li><strong>Check their policy first.</strong> Regulated industries, government clients and many '
     'large firms have gift and hospitality rules. Worth confirming before you invite.</li>'),
    ('for clients who do not play golf and have had enough dinners.',
     'for clients who do not play golf and have been to enough dinners.'),
    ('For clients who do not play golf and have had enough dinners.',
     'For clients who do not play golf and have been to enough dinners.'),
])

# ------------------------------------------------ EMPLOYEE APPRECIATION ----
edit('event-types/employee-appreciation/index.html', [
    ('<li><strong>Driver aids on, and left on.</strong> Nobody should be embarrassed in front of colleagues. '
     'We turn them down only for people who ask.</li>',
     '<li><strong>Driver aids on by default.</strong> Nobody should be embarrassed in front of colleagues. '
     'We turn them down only for people who ask.</li>'),
    ('<li><strong>Team formats over individual ones.</strong> A relay gets people mixing across departments. '
     'A fastest lap board gets the same three people at the top.</li>',
     '<li><strong>Team formats over individual ones.</strong> A relay gets people mixing across departments, '
     'where a fastest lap board tends to be settled by the same few drivers.</li>'),
    ('Not at all, and for appreciation events we often suggest not having one. Open racing where people come '
     'and go tends to produce a better afternoon than a bracket nobody asked for.',
     'Not at all, and for appreciation events we often suggest not having one. Open racing where people come '
     'and go usually suits the occasion better than a structured competition.'),
    ('Yes. Driver aids make the cars manageable for children and our staff set each driver up individually.',
     'Usually yes. Driver aids make the cars manageable and our staff set each driver up, though suitability '
     'for younger children depends on them fitting the rig safely and on supervision. Tell us the age range.'),
    # differentiate from private parties: make this about workforce logistics
    ('<h3>Onsite is often easier than a venue</h3>',
     '<h3>Accessibility and workforce scale</h3>'
     '<p>An appreciation event has to work for the whole workforce, which is a different problem from a party. '
     'Tell us if you have colleagues who use a wheelchair or who cannot transfer into a fixed racing seat, '
     'and we will talk through what is and is not workable rather than leaving anyone to find out on the day.</p>'
     '<h3>Onsite is often easier than a venue</h3>'),
])

# ---------------------------------------------------- PRIVATE PARTIES ------
edit('event-types/private-parties/index.html', [
    ('Birthdays, milestone celebrations and anything where the guest list is people you actually know. ',
     'Birthdays, milestone celebrations and anything where the guest list is personal rather than professional. '),
    ('Yes. Driver aids make the cars manageable and our staff set each driver up. Mixed-age parties are one '
     'of the things it does best.',
     'Usually yes. Driver aids make the cars manageable and our staff set each driver up, though suitability '
     'for younger children depends on them fitting the rig safely and on supervision. Tell us the ages and '
     'we will advise.'),
    ('No. Our staff run the whole thing so the host can enjoy their own party.',
     'No. Our staff run the activation for the booked hours so the host can enjoy their own party.'),
    # dedupe the Related grid
    ('    <a class="linkcard" href="/locations/">\n'
     '      <div class="lc-name">WHERE WE DELIVER</div>\n'
     '      <div class="lc-desc">Mobile simulator events across Florida, delivered from Tampa.</div>\n'
     '    </a>\n',
     '    <a class="linkcard" href="/event-types/fundraisers/">\n'
     '      <div class="lc-name">FUNDRAISERS</div>\n'
     '      <div class="lc-desc">Charity events where the simulator is the fundraising mechanism.</div>\n'
     '    </a>\n'),
])
