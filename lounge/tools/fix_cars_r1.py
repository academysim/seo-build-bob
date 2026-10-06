# -*- coding: utf-8 -*-
"""Codex round 1 on the /cars/ pages.

Accepted nearly everything. The recurring defect in my own writing is
over-generalising a whole class from its best-known subset: "classic" is not
all pre-war, "stock car" is not all H-pattern, and Formula cars do not lack
grip below speed. Difficulty labels are kept but made relative rather than
absolute, because a comparison table that hedges every cell is useless.
"""
import io, os, sys

b = sys.argv[1]


def edit(rel, pairs):
    p = os.path.join(b, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-38s SKIP' % rel)
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
    print('  %-38s %d edits' % (rel, n))


# ------------------------------ /cars/ hub ----------------------------------
edit('cars/index.html', [
    # 3. unsupported promotional claim
    ("Almost everyone who tries something harder first ends up wishing they had started here.",
     "That combination is what makes it the sensible first session."),

    # 4/5. stock car row
    ("        <td><strong>Stock car</strong></td>\n        <td>Manual</td>\n        <td>Little to none</td>\n        <td>Low</td>\n        <td>Physical and loose</td>",
     "        <td><strong>Stock car</strong></td>\n        <td>Sequential in current Cup cars, H-pattern in many older ones</td>\n        <td>Little to none</td>\n        <td>Low to moderate, varies by package</td>\n        <td>Physical and loose</td>"),

    # 6. classic row
    ("        <td><strong>Classic</strong></td>\n        <td>Manual</td>\n        <td>None</td>\n        <td>Almost none</td>\n        <td>Slow and demanding</td>",
     "        <td><strong>Classic</strong></td>\n        <td>Usually manual, varies by era</td>\n        <td>Few or none</td>\n        <td>None to high, depending on era</td>\n        <td>Often demanding</td>"),

    # 7. prototype difficulty
    ("        <td>High</td>\n        <td>Fast, but stable</td>", "        <td>High</td>\n        <td>Very fast and demanding</td>"),

    # 8. formula difficulty
    ("        <td>Hardest here</td>", "        <td>Least forgiving</td>"),

    # 15. drift difficulty
    ("        <td>Hard, but failure is fun</td>", "        <td>A different technique entirely</td>"),

    # 9. prototype multi-class
    ("The distinctive skill is not raw speed but multi-class awareness: knowing what is behind you, what class it is, and how to pass or be passed without ruining anyone&rsquo;s race.",
     "In endurance racing the distinctive skill is multi-class awareness: knowing what is behind you, what class it is, and how to pass or be passed without ruining anyone&rsquo;s race."),

    # 10. drift gearbox
    ("It needs an H-pattern shifter to do properly.",
     "Drift cars use manual or sequential gearboxes depending on the car."),

    # 11. handbrake absolute
    ("The car spends far more of the time slightly out of shape than it ever does on a circuit, and a handbrake matters here in a way it does not anywhere else.",
     "The car spends far more of the time slightly out of shape than it ever does on a circuit, and a handbrake is useful for the tighter corners, though technique varies with the car and the surface."),

    # 12. classic over-generalised
    ("Skinny tyres, no downforce worth the name, no electronics, and an H-pattern gearbox that has to be used properly. Classic race cars are considerably slower than a modern GT3 car and considerably harder to drive well, which is exactly why people who have driven everything else keep coming back to them.",
     "Earlier historic cars tend to combine narrow tyres, little aerodynamic downforce and an H-pattern gearbox that has to be used properly. Later classics vary a great deal. What they share is that the driver is given very little help, which is exactly why people who have driven everything else keep coming back to them."),

    # 13/14. formula grip
    ("No traction control, very little weight, and grip that only arrives with speed, which means you have to commit before the car has given you a reason to.",
     "No traction control, very little weight, and aerodynamic load that rises sharply with speed, so the car has most grip exactly where it is least comfortable to trust it."),
])

# -------------------------- /cars/classic-race-cars/ -------------------------
edit('cars/classic-race-cars/index.html', [
    # 16. title, pull it toward the informational cluster
    ("<title>Classic Race Car Simulator Tampa | Academy Sim Racing</title>",
     "<title>Classic Race Cars Explained | Academy Sim Racing Tampa</title>"),
    ('<meta property="og:title" content="Classic Race Car Simulator Tampa | Academy Sim Racing">',
     '<meta property="og:title" content="Classic Race Cars Explained | Academy Sim Racing Tampa">'),
    ('<meta name="twitter:title" content="Classic Race Car Simulator Tampa | Academy Sim Racing">',
     '<meta name="twitter:title" content="Classic Race Cars Explained | Academy Sim Racing Tampa">'),

    # 17/18. hero over-generalisation and the outright wrong speed claim
    ("No traction control, no anti-lock brakes, no downforce worth the name, and a gearbox you have to operate properly. Older racing cars are slower than anything modern in our library and considerably harder to drive well. That is the appeal.",
     "Few or no electronic aids, little aerodynamic downforce and a gearbox you have to operate properly. Many earlier historic cars are slower than a modern GT3 car, though later classics can be extremely quick. What they have in common is that nothing helps you. That is the appeal."),

    # 19. downforce and stability
    ("Traction control manages wheelspin, anti-lock brakes stop you locking a wheel, and downforce grows as you go faster so quick corners feel more stable than slow ones. Take all of that away and what is left asks considerably more of the driver.",
     "Traction control manages wheelspin, anti-lock brakes stop you locking a wheel, and aerodynamic downforce increases with speed, loading the tyres more in fast corners. Take all of that away and what is left asks considerably more of the driver."),

    # 20/21/22. tyres, grip and the fast-corner claim
    ("Older racing cars run narrow tyres by modern standards, so there is simply less grip available in every direction. They generate little aerodynamic downforce, and in the earlier eras effectively none, which means the car does not gain grip as speed rises. A fast corner in a classic car is harder than a slow one, which is the opposite of how a modern aerodynamic car behaves.",
     "Many earlier cars run narrower period-style tyres whose construction and compounds generally give less grip than a modern racing tyre. They also generate little aerodynamic downforce, and in the earliest eras effectively none, so aerodynamics adds little or nothing to the load on the tyres. A fast corner therefore gives you none of the extra assistance a modern high-downforce car would provide."),

    # 23. paddle generalisation
    ("Modern racing cars shift with paddles, which removes the gearbox as a thing to think about. Classic cars do not.",
     "Many modern racing cars use paddle-operated sequential gearboxes, which cut the workload of each shift down to almost nothing. Classic cars do not."),

    # 24. downshift mechanism
    ("Get a downshift wrong under braking and the rear axle is suddenly being asked to slow the car more than the tyres can manage, which upsets it exactly where you least want that.",
     "Get a downshift wrong under braking and an abrupt braking torque goes through the driven wheels, which can unsettle the rear of the car or lock a wheel, exactly where you least want that."),

    # 25. breakaway behaviour
    ("Lower speeds give you more time to feel what is happening at the limit. The car slides for longer before it goes, rather than snapping away in an instant.",
     "Lower speeds can give you more time to recognise and correct a slide as it develops, though how abruptly a car lets go varies a great deal between them."),

    # 26. circuit design claim
    ("Older cars suit older circuits. The layouts that were built before big run-off areas and heavy aerodynamic grip are the ones these cars were designed around.",
     "Older cars suit older circuits, and a historic layout gives period machinery the context it actually raced in."),
])

# ------------- the same formula-grip phrasing already shipped ---------------
edit('cars-and-tracks/index.html', [
    ("No traction control in most classes, very little weight, and a lot of aerodynamic grip that only arrives with speed. It is the steepest learning curve we offer.",
     "No traction control in most classes, very little weight, and aerodynamic load that rises sharply with speed. It is the steepest learning curve we offer."),
])
