# -*- coding: utf-8 -*-
"""Round 4.

1. Malik: "only the 4 with the h pattern have clutches, and the motion one has
   a shifter and clutch". Since only four rigs have clutches and the motion rig
   has one, the motion rig is one of the four. The homepage rig cards agree
   independently: MOTION GT lists "6-Speed", and the MANUAL COCKPIT card is
   labelled "SHIFTER + CLUTCH". So the count of four stays correct, and we can
   now add the genuinely strong line that the flagship motion rig is one of them.

2. Homepage gets an Academy Builds link. Placed at the end of the rig-spec
   section, because someone reading direct-drive and pedal specs is the highest
   intent Builds prospect on the page, and it does not interrupt any booking CTA.
"""
import io, os, sys

b = sys.argv[1]


def edit(rel, pairs, required=True):
    p = os.path.join(b, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-46s SKIP' % rel)
        return
    s = io.open(p, encoding='utf-8', newline='').read()
    n = 0
    for o, x in pairs:
        c = s.count(o)
        if c == 0:
            continue
        assert c == 1, 'NOT ONCE in %s (%d): %r' % (rel, c, o[:60])
        s = s.replace(o, x, 1)
        n += 1
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s %d edits' % (rel, n))


# ---------------- 1. the motion rig is one of the four ----------------------
edit('racing/manual-transmission-simulator-tampa/index.html', [
    ("Four of our rigs carry a real six-speed H-pattern shifter, a clutch pedal and a handbrake, which is everything you need to practise the techniques that go with a gated gearbox.",
     "Four of our rigs carry a real six-speed H-pattern shifter, a clutch pedal and a handbrake, which is everything you need to practise the techniques that go with a gated gearbox. One of the four is the Motion GT, so you can run a manual gearbox on the motion platform."),

    ("Six-speed H-pattern shifter, clutch pedal and handbrake, with load-cell or active pedals and direct drive steering.",
     "Six-speed H-pattern shifter, clutch pedal and handbrake, with load-cell or active pedals and direct drive steering. The flagship Motion GT is one of them."),
])

edit('cars/classic-race-cars/index.html', [
    ("Four of our eight rigs have an H-pattern shifter and a clutch pedal fitted. Tell us when you book that you want to drive something with a manual gearbox and we will set you up on one of them.",
     "Four of our eight rigs have an H-pattern shifter and a clutch pedal fitted, including the Motion GT. Tell us when you book that you want to drive something with a manual gearbox and we will set you up on one of them."),
])

edit('cars/index.html', [
    ("Drift or classic. Four of our eight rigs have an H-pattern shifter and a clutch pedal, so mention it when you book and we will put you on the right one.",
     "Drift or classic. Four of our eight rigs have an H-pattern shifter and a clutch pedal, including the flagship Motion GT, so mention it when you book and we will put you on the right one."),
])

edit('cars-and-tracks/index.html', [
    ("Four of our eight rigs have an H-pattern shifter and a clutch pedal. Classic race cars and drift cars are the natural fit.",
     "Four of our eight rigs have an H-pattern shifter and a clutch pedal, including the Motion GT. Classic race cars and drift cars are the natural fit."),
])

# ---------------- 2. homepage Academy Builds link ---------------------------
p = os.path.join(b, 'index.html')
s = io.open(p, encoding='utf-8', newline='').read()

anchor = '</section>\n\n<section class="faq">'
assert s.count(anchor) == 1, 'homepage section anchor x%d' % s.count(anchor)

if 'builds.academysim.com' not in s:
    line = ('      <p style="text-align:center;margin-top:26px;font-size:13px;color:#a1a1aa;">'
            'Like the hardware? Academy builds custom simulators, from a single screen to full motion. '
            '<a class="amber" href="https://builds.academysim.com">See sim builds &rarr;</a></p>\n')
    s = s.replace(anchor, line + anchor, 1)
    print('  index.html                                     builds link added')
else:
    print('  index.html                                     builds link already present')

# the homepage tracking snippet only wired Events; wire Builds too
if 'cross_domain_builds' not in s:
    a = "  gtag('event', 'content_view', { content_type: type, content_id: id });\n"
    assert s.count(a) == 1, 'tracking anchor'
    add = a + """  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'cross_domain_builds', { content_type: type, content_id: id });
    });
  });
"""
    s = s.replace(a, add, 1)
    print('  index.html                                     builds tracking added')

io.open(p, 'w', encoding='utf-8', newline='').write(s)
