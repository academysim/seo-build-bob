# -*- coding: utf-8 -*-
"""Buyout card: published price with instant booking, quote kept as secondary.

The 2026-09-07 homepage took the day-of-week buyout prices off the page and made
the only action a quote request. Malik asked which converts better. At $249-$549
this is a low-consideration local purchase, and a quote form inserts a human
round-trip into a decision people make in one sitting. The deciding factor is
capacity rather than theory: the CRM already carries eleven overdue tasks and
five unassigned leads, so routing buyouts there converts a booking into a lead
that may not get answered.

So the price and BOOK LOCKOUT come back as the primary action, and the inquiry
form stays reachable for the asks it is actually good at: larger groups, dates
that are not bookable online, and hosted events.
"""
import io
import os

ROOT = 'D:/AcademySimRacing/03-SEO-Build/lounge'
ARROW = u'\u2192'

DESC_PRICED = (
    u'Lock out the entire lounge, all 8 racing simulators reserved for your '
    u'group, with nobody else in the room. $249 for an hour, $449 for two, '
    u'Sunday, Monday, Wednesday and Thursday. Friday and Saturday are $300 and $549. Cheaper '
    u'than booking six rigs separately, and you get all eight. Great for '
    u'birthdays, bachelor parties, car clubs, and small team outings. '
    u'(Student driving sim not included.)<br><br>'
    u'<strong>This is private simulator time, not a hosted event.</strong> '
    u"We'll get everyone set up and running, but there's no race director, "
    u'tournament format, or catering. Want us to run the whole thing? '
    u'<a class="amber" href="https://academysim.com/pages/lounge-events">'
    u'See hosted race events ' + ARROW + u'</a><br><br>'
    u'Bigger group, or a date that will not book online? '
    u'<a class="amber" href="https://inquiry.academysim.com/">'
    u'Ask for a quote ' + ARROW + u'</a></div>')

PRICE_BLOCK = (
    u'<div class="sim-price">FROM $249<span class="sim-unit"> / HR</span></div>'
    u'<a class="mono amber sim-book" style="font-size:10px;" '
    u'href="https://booking.academysim.com/?category=racing">BOOK LOCKOUT '
    + ARROW + u'</a>')

FAQ_GROUP_PRICED = (
    u'From a solo session up to a full lounge of racers rotating through all 8 '
    u'racing rigs. Friend groups, birthday parties, and corporate teams are all '
    u'welcome. For larger groups, a full lounge buyout is $249 for an hour or '
    u'$449 for two Sunday, Monday, Wednesday and Thursday, and $300 or $549 on Friday and '
    u'Saturday, with all 8 rigs and nobody else in the room.')

FAQ_BUYOUT_JSONLD = (
    u'Yes. A full lounge buyout is $249 for one hour or $449 for two hours '
    u'Sunday, Monday, Wednesday and Thursday. Friday and Saturday are $300 for one hour or '
    u'$549 for two. You get all 8 racing simulators and the run of the space '
    u'for your group, with nobody else in the room.')

FAQ_BUYOUT_ACCORDION = (
    u'Yes. A full lounge buyout is <strong>$249 for one hour or $449 for two'
    u'</strong> Sunday, Monday, Wednesday and Thursday, and <strong>$300 or $549</strong> on '
    u'Friday and Saturday, all 8 racing simulators and the run of the space for '
    u'your group, with nobody else in the room.')

# What the 09-07 merge put there, and what replaces it.
CUR_DESC_START = u'Lock out the entire lounge ' if False else u'Lock out the entire lounge,'
CUR_PRICE = (
    u'<div class="mono dim" style="font-size:10px;">CUSTOM QUOTE</div>'
    u'<a class="mono amber sim-book" style="font-size:10px;" '
    u'href="https://inquiry.academysim.com/">GET A QUOTE ' + ARROW + u'</a>')
CUR_FAQ_GROUP = (
    u'From a solo session up to a full lounge of racers rotating through all 8 '
    u'racing rigs. Friend groups, birthday parties, and corporate teams are all '
    u'welcome. For larger groups, request a full lounge buyout quote.')
CUR_FAQ_BUYOUT = (
    u'Yes. Full lounge buyouts are available for birthday parties, corporate '
    u'team-building, and private events. You get every rig and the run of the '
    u'space for your group. Pricing depends on day, time, and group size, so '
    u'buyouts are quoted individually.')


def main():
    out = {}
    fail = False
    for rel in ('upload/index.html', 'site/index.html'):
        p = os.path.join(ROOT, rel)
        h = io.open(p, encoding='utf-8', newline='').read()
        dashes_before = h.count(u'—')
        bad = False

        i = h.find(CUR_DESC_START)
        j = h.find(u'</div>', i) + len(u'</div>')
        edits = [
            (h[i:j], DESC_PRICED, 1),
            (CUR_PRICE, PRICE_BLOCK, 1),
            (CUR_FAQ_GROUP, FAQ_GROUP_PRICED, 2),
        ]
        # the buyout answer is one string in the JSON-LD and another in the
        # accordion after the merge; both currently read the same, so they are
        # split apart again here by which one is reached first.
        n = h.count(CUR_FAQ_BUYOUT)
        if n != 2:
            print('  !! %s: %d copies of the quote-worded buyout answer' % (rel, n))
            bad = True
        else:
            a = h.find(CUR_FAQ_BUYOUT)
            b = h.find(CUR_FAQ_BUYOUT, a + 1)
            # the JSON-LD block sits in <head>, so the first hit is the schema
            h = h[:a] + FAQ_BUYOUT_JSONLD + h[a + len(CUR_FAQ_BUYOUT):]
            b = h.find(CUR_FAQ_BUYOUT)
            h = h[:b] + FAQ_BUYOUT_ACCORDION + h[b + len(CUR_FAQ_BUYOUT):]

        for old, new, want in edits:
            c = h.count(old)
            if c != want:
                print('  !! %s: %d matches (wanted %d) for %r' % (rel, c, want, old[:60]))
                bad = True
                continue
            h = h.replace(old, new)

        for must in (u'BOOK LOCKOUT', u'FROM $249', u'Ask for a quote',
                     u'inquiry.academysim.com', u'$300 or $549'):
            if must not in h:
                print('  !! %s: %r missing' % (rel, must))
                bad = True
        if u'CUSTOM QUOTE' in h or u'GET A QUOTE' in h:
            print('  !! %s: the quote-only CTA survived' % rel)
            bad = True
        # the three that remain are in code comments; this must not add a fourth
        if h.count(u'\u2014') != dashes_before:
            print('  !! %s: em dashes %d -> %d' % (rel, dashes_before, h.count(u'\u2014')))
            bad = True
        if bad:
            fail = True
            continue
        out[p] = h
        print('  %-18s ok, %d chars' % (rel, len(h)))
    if fail:
        raise SystemExit('  FAILED, nothing written')
    for p, h in out.items():
        io.open(p, 'w', encoding='utf-8', newline='').write(h)
    print('  buyout card: price + BOOK LOCKOUT primary, quote secondary')


main()
