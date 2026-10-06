# -*- coding: utf-8 -*-
"""F1: fold the 2026-09-07 hand-authored homepage work into the maintained source.

The 09-07 production deploy was a Netlify drag-and-drop of an OLD local lounge
folder (homepage + Sebring + assets only). It deleted 16 live pages, reverted
Sebring to its pre-2026-08-29 state (scroll bug and all), reverted netlify.toml,
and dropped llms.txt. So the live homepage is NOT simply newer: it is an old
base carrying a handful of genuinely new sections.

Every candidate difference was classified against git history (605f815..2631cfb).
Only differences absent from EVERY repo revision are treated as new work and
ported here. Everything else on the live page is an old leftover the repo had
already fixed, and is deliberately not carried back.

Ported (new on 09-07):  the hours block in the hero, the HOURS section and its
  CSS, "8 racing simulators plus 2 driving simulators", "8 Racing / 2 Driving",
  two driver-ed rigs, the buyout card moving from a published price to a quote,
  the restyled ABS easter-egg toggle, the Sebring track-guide feature card.
Not ported (old leftovers): 65-review counts, em dashes, `.lp .pad-mobile`,
  missing postalCode/@id/priceRange/sameAs, missing alt text, missing GA4
  content_view tracking, missing internal links to the other 16 pages.
"""
import io, os

ROOT = 'D:/AcademySimRacing/03-SEO-Build/lounge'
BLK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blocks_0907')

EMDASH = u'\u2014'
ARROW = u'\u2192'
MIDDOT = u'\u00b7'


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def nodash(s):
    """The ported blocks were authored outside the repo and carry em dashes,
    which every page here is gated against. Replaced explicitly rather than by a
    blanket regex, so each one still reads as written English."""
    for a, b in [
        (u'first-come during these hours ' + EMDASH + u' booking ahead still guarantees',
         u'first-come during these hours, though booking ahead still guarantees'),
        (u'usually pick an hour ' + EMDASH + u' long enough to settle in',
         u'usually pick an hour, long enough to settle in'),
        (u'drives at the same time ' + EMDASH + u' add a sim for each racer',
         u'drives at the same time. Add a sim for each racer'),
        (u'the circuits our drivers run ' + EMDASH + u' plus how to prepare',
         u'the circuits our drivers run, plus how to prepare'),
        (u'Lock out the entire lounge ' + EMDASH + u' all 8 racing simulators',
         u'Lock out the entire lounge, all 8 racing simulators'),
        (u'private events ' + EMDASH + u' you get every rig',
         u'private events. You get every rig'),
    ]:
        s = s.replace(a, b)
    if EMDASH in s:
        i = s.find(EMDASH)
        raise SystemExit('unhandled em dash in ported block: %r'
                         % s[max(0, i - 70):i + 70])
    return s


CSS_HOURS = nodash(rd(os.path.join(BLK, 'css_hours.txt')))
HERO_HOURS = nodash(rd(os.path.join(BLK, 'hero_hours.txt')))
HOURS_SECT = nodash(rd(os.path.join(BLK, 'hours_section.txt')))
TRACK_GUIDE = nodash(rd(os.path.join(BLK, 'track_guides.txt')))
ABS_CSS = nodash(rd(os.path.join(BLK, 'abs_css.txt')))

# ABS_CSS was lifted out of a media query and carries its closing brace.
assert ABS_CSS.rstrip().endswith(u'} }'), repr(ABS_CSS[-20:])
ABS_CSS = ABS_CSS.rstrip()[:-1].rstrip() + u'\n'

BUYOUT_DESC_NEW = nodash(
    u'Lock out the entire lounge ' + EMDASH + u' all 8 racing simulators reserved '
    u'for your group. Perfect for parties, corporate team-building, and private '
    u'events. Driving simulators not included.<br><br>'
    u'<strong>This is private simulator time, not a hosted event.</strong> '
    u"We'll get everyone set up and running, but there's no race director, "
    u'tournament format, or catering. Want us to run the whole thing? '
    u'<a class="amber" href="https://academysim.com/pages/lounge-events">'
    u'See hosted race events ' + ARROW + u'</a></div>')

FAQ_GROUP_NEW = (
    u'From a solo session up to a full lounge of racers rotating through all 8 '
    u'racing rigs. Friend groups, birthday parties, and corporate teams are all '
    u'welcome. For larger groups, request a full lounge buyout quote.')

FAQ_BUYOUT_NEW = nodash(
    u'Yes. Full lounge buyouts are available for birthday parties, corporate '
    u'team-building, and private events ' + EMDASH + u' you get every rig and the '
    u'run of the space for your group. Pricing depends on day, time, and group '
    u'size, so buyouts are quoted individually.')


def edits(h):
    """(old, new) pairs. Every one must match exactly once."""
    E = []

    # --- facts: two driving simulators, not one -----------------------------
    E.append((
        u'<meta property="og:description" content="8 professional racing simulators. ',
        u'<meta property="og:description" content="8 racing simulators plus 2 driving '
        u'simulators. '))
    E.append((
        u'<p class="hero-sub">8 professional racing simulators. ',
        u'<p class="hero-sub">8 racing simulators plus 2 driving simulators. '))
    E.append((u'8 Pro Rigs</div></div>',
              u'8 Racing ' + MIDDOT + u' 2 Driving</div></div>'))
    E.append((
        u'Dedicated driver-ed rig running City Car Driving Enterprise, real-world '
        u'traffic, weather, and road conditions. Built for new drivers, teen '
        u'programs, and schools.',
        u'Two dedicated driver-ed rigs running City Car Driving Enterprise, '
        u'real-world traffic, weather, and road conditions. Built for new drivers, '
        u'teen programs, and schools.'))

    # --- the hours work -----------------------------------------------------
    i = h.find(u'<div class="hero-price">')
    j = h.find(u'</div>', i) + len(u'</div>')
    E.append((h[i:j], HERO_HOURS.rstrip()))
    E.append((u'.lp .hero-credit {', CSS_HOURS + u'.lp .hero-credit {'))
    E.append((u'<section class="section reviews-section">',
              HOURS_SECT + u'\n\n<section class="section reviews-section">'))

    # --- buyout: published price -> quote (owner change, 2026-09-07) ---------
    i = h.find(u'Lock out the entire lounge')
    j = h.find(u'</div>', i) + len(u'</div>')
    E.append((h[i:j], BUYOUT_DESC_NEW))
    i = h.find(u'<span class="badge">Nobody Else In The Room</span>')
    j = h.find(u'</div>', i)
    E.append((h[i:j],
              u'<span class="badge">Private Event</span>'
              u'<span class="badge">Parties</span>'
              u'<span class="badge">Corporate</span>'))
    E.append((
        u'<div class="sim-price">FROM $249<span class="sim-unit"> / HR</span></div>'
        u'<a class="mono amber sim-book" style="font-size:10px;" '
        u'href="https://booking.academysim.com/?category=racing">BOOK LOCKOUT '
        + ARROW + u'</a>',
        u'<div class="mono dim" style="font-size:10px;">CUSTOM QUOTE</div>'
        u'<a class="mono amber sim-book" style="font-size:10px;" '
        u'href="https://inquiry.academysim.com/">GET A QUOTE ' + ARROW + u'</a>'))

    # Each answer appears twice, once in the FAQ JSON-LD and once in the visible
    # accordion, and the two copies are NOT identical: the accordion wraps the
    # prices in <strong>. Each occurrence is spanned and replaced on its own.
    for old_start, new in [
        (u'From a solo session up to a full lounge of racers rotating through all 8 rigs.',
         FAQ_GROUP_NEW),
        (u'Yes. A full lounge buyout is', FAQ_BUYOUT_NEW),
    ]:
        seen = set()
        pos = 0
        while True:
            i = h.find(old_start, pos)
            if i < 0:
                break
            ends = [x for x in (h.find(u'"}', i), h.find(u'</div>', i)) if x > 0]
            j = min(ends)
            span = h[i:j]
            if span not in seen:
                seen.add(span)
                E.append((span, new, h.count(span)))
            pos = j
        if len(seen) not in (1, 2):
            raise SystemExit('  !! %d distinct copies of %r' % (len(seen), old_start))

    # --- restyled ABS easter egg -------------------------------------------
    # Replaces the blinking green/red toggle with the flat amber/grey one, and
    # takes the now-stale comment and the two @keyframes with it.
    i = h.find(u'/* Toggle ' + EMDASH + u' lives in the sticky nav')
    j = h.find(u'@keyframes absBoxOff', i)
    j = h.find(u'\n', j) + 1
    E.append((h[i:j],
              u'/* Toggle: lives in the sticky nav, top right, next to BOOK NOW.\n'
              u'   Flat amber when ABS is on, flat grey when off. */\n' + ABS_CSS))
    E.append((u'title="Toggle ABS, changes the skid marks when you stop scrolling"',
              u'title="Easter egg: stop scrolling to lay down skid marks. ABS on = '
              u'short dashed marks. ABS off = long locked-wheel slides."'))
    E.append((u'skid-layer { position:fixed; inset:0; pointer-events:none; '
              u'z-index:45; overflow:hidden; }',
              u'skid-layer { position:fixed; inset:0; pointer-events:none; '
              u'z-index:45; opacity:0.62; overflow:hidden; }'))
    E.append((u'.lp .abs-toggle { font-size:8px; padding:6px 8px; '
              u'letter-spacing:0.15em; }',
              u'.lp .abs-toggle { display:none; }'))

    # --- Sebring feature card ----------------------------------------------
    E.append((u'<section class="faq">', TRACK_GUIDE + u'\n\n<section class="faq">'))
    return E


def main():
    results = {}
    fail = False
    for rel in ('upload/index.html', 'site/index.html'):
        p = os.path.join(ROOT, rel)
        h = rd(p)
        before = len(h)
        dashes_before = h.count(EMDASH)
        bad = False
        for edit in edits(h):
            old, new = edit[0], edit[1]
            want = edit[2] if len(edit) > 2 else 1
            n = h.count(old)
            if n != want:
                print('  !! %s: %d matches (wanted %d) for %r'
                      % (rel, n, want, old[:70]))
                bad = True
                continue
            h = h.replace(old, new)
        for must in (u'hero-hours', u'hours-card', u'8 Racing', u'CUSTOM QUOTE',
                     u'Two dedicated driver-ed rigs', u'Easter egg',
                     u'READ THE GUIDE', u'plus 2 driving simulators',
                     u'content_view', u'postalCode', u'.lp.pad-mobile'):
            if must not in h:
                print('  !! %s: %r missing after merge' % (rel, must))
                bad = True
        for banned in (u'FROM $249', u'BOOK LOCKOUT'):
            if banned in h:
                print('  !! %s: %r survived the merge' % (rel, banned))
                bad = True
        # The four em dashes this file already had are all in code comments.
        # The ported blocks must not add a fifth, and one comment loses its own.
        if h.count(EMDASH) > dashes_before - 1:
            print('  !! %s: em dashes %d -> %d, expected %d'
                  % (rel, dashes_before, h.count(EMDASH), dashes_before - 1))
            bad = True
        if bad:
            fail = True
            continue
        results[p] = h
        print('  %-18s %d -> %d bytes' % (rel, before, len(h)))
    if fail:
        raise SystemExit('  MERGE FAILED, nothing written')
    for p, h in results.items():
        wr(p, h)
    print('  merged')


main()
