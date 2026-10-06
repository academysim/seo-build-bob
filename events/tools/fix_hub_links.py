# -*- coding: utf-8 -*-
"""All ten event types now have pages, so the hub's "Also Available" card block
(which existed to describe the ones without pages) is replaced by real links.
"""
import io

P = 'events_content.py'
s = io.open(P, encoding='utf-8', newline='').read()

# extend the linkgrid to all ten
old_tail = """                     ('/event-types/watch-parties/', 'WATCH PARTIES',
                      'Race-day viewing with simulators running the circuit on the broadcast.'),
                 ]),"""
new_tail = """                     ('/event-types/watch-parties/', 'WATCH PARTIES',
                      'Race-day viewing with simulators running the circuit on the broadcast.'),
                     ('/event-types/employee-appreciation/', 'EMPLOYEE APPRECIATION',
                      'Recognition days built for inclusiveness rather than competition.'),
                     ('/event-types/client-entertainment/', 'CLIENT ENTERTAINMENT',
                      'Small-group hospitality where the racing supports the conversation.'),
                     ('/event-types/private-parties/', 'PRIVATE PARTIES',
                      'Birthdays and celebrations, delivered to your home or venue.'),
                     ('/event-types/fundraisers/', 'FUNDRAISERS',
                      'Charity events where the simulator is the fundraising mechanism.'),
                 ]),"""
assert s.count(old_tail) == 1, 'linkgrid tail anchor'
s = s.replace(old_tail, new_tail, 1)

# drop the now-redundant cards block
start = s.index("        cards('Also Available', 'OTHER FORMATS WE RUN',")
end = s.index("        prose('What Is Included'", start)
s = s[:start] + s[end:]

# and the sentence that pointed at it
s = s.replace(
    "'of event, and what to tell us when you ask for a quote.</p>',",
    "'of event, and what to tell us when you ask for a quote.</p>',", 1)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('  hub updated: %d bytes' % len(s.encode()))
print('  cards block removed, linkgrid now has 10 entries')
