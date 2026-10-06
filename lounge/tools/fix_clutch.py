# -*- coding: utf-8 -*-
"""Malik confirmed the rigs have clutch pedals (2026-08-29), which unparks
/racing/manual-transmission-simulator-tampa/.

He said "all have clutch pedals" in answer to a question about the four
H-pattern rigs. That could mean all four or all eight. Everything below is
phrased so it is true under either reading: the pages only ever say the rigs
with the H-pattern shifter also have a clutch. Nothing claims all eight.
"""
import io, os, sys

b = sys.argv[1]


def edit(rel, pairs):
    p = os.path.join(b, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-46s SKIP' % rel)
        return
    s = io.open(p, encoding='utf-8', newline='').read()
    n = 0
    for o, x in pairs:
        if s.count(o) == 0:
            continue
        assert s.count(o) == 1, 'NOT ONCE in %s: %r' % (rel, o[:60])
        s = s.replace(o, x, 1)
        n += 1
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s %d edits' % (rel, n))


edit('racing/manual-transmission-simulator-tampa/index.html', [
    # hero
    ("Four of our rigs carry a real six-speed H-pattern shifter and a handbrake, which is what you need to practise the techniques that go with a gated gearbox.",
     "Four of our rigs carry a real six-speed H-pattern shifter, a clutch pedal and a handbrake, which is everything you need to practise the techniques that go with a gated gearbox."),

    # statline
    ("    <span><strong>Handbrake</strong> &nbsp;On the same rigs</span>",
     "    <span><strong>Clutch</strong> &nbsp;And handbrake fitted</span>"),

    # heel and toe now genuinely available rather than described in the abstract
    ("Braking and blipping the throttle at the same time with one foot, so you can rev match while still slowing for the corner. It is the technique people most often come to a simulator to work on, because doing it repeatedly in a road car is hard on the drivetrain.",
     "Braking and blipping the throttle at the same time with one foot, while the other works the clutch. It is the technique people most often come to a simulator to work on, because doing it repeatedly in a road car is hard on the drivetrain. It needs three pedals, which is why it is worth knowing that these rigs have them."),

    # hardware card
    ("Six-speed H-pattern shifter and handbrake, with load-cell or active pedals and direct drive steering.",
     "Six-speed H-pattern shifter, clutch pedal and handbrake, with load-cell or active pedals and direct drive steering."),

    # pedal spacing card, now able to say what the third pedal is
    ("Heel and toe depends on where the pedals sit relative to each other and to your foot.",
     "Heel and toe depends on where the brake and throttle sit relative to each other and to your foot, and on how the clutch is set up."),

    # builds cross-sell
    ("Academy also builds custom simulators and can specify a shifter and handbrake.",
     "Academy also builds custom simulators and can specify a shifter, clutch and handbrake."),
])

# The classic page was written around the question. It can now be direct.
edit('cars/classic-race-cars/index.html', [
    ("You choose the gears yourself on an H-pattern shifter, and you match engine speed on the way down the box so the car stays settled rather than being unsettled by the driveline.",
     "You choose the gears yourself on an H-pattern shifter, work a clutch, and match engine speed on the way down the box so the car stays settled rather than being unsettled by the driveline."),
    ("Four of our eight rigs have an H-pattern shifter fitted. Tell us when you book that you want to drive something with a manual gearbox and we will set you up on one of them and walk you through the pedal layout on that rig.",
     "Four of our eight rigs have an H-pattern shifter and a clutch pedal fitted. Tell us when you book that you want to drive something with a manual gearbox and we will set you up on one of them."),
])

# The /cars/ hub mentions the shifter rigs in two places.
edit('cars/index.html', [
    ("Drift or classic. Four of our eight rigs have an H-pattern shifter, so mention it when you book and we will put you on the right one.",
     "Drift or classic. Four of our eight rigs have an H-pattern shifter and a clutch pedal, so mention it when you book and we will put you on the right one."),
])

# The library tool's card copy for classic cars.
edit('cars-and-tracks/index.html', [
    ("Four of our eight rigs have an H-pattern shifter. Classic race cars and drift cars are the natural fit. Mention it when you book so we put you on the right rig.",
     "Four of our eight rigs have an H-pattern shifter and a clutch pedal. Classic race cars and drift cars are the natural fit. Mention it when you book so we put you on the right rig."),
])
