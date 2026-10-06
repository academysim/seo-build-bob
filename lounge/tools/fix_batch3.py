import io, os, sys

b = sys.argv[1]


def edit(rel, pairs):
    p = os.path.join(b, *rel.split('/'))
    s = io.open(p, encoding='utf-8', newline='').read()
    for o, n in pairs:
        assert s.count(o) == 1, "NOT ONCE in %s: %s" % (rel, o[:70])
        s = s.replace(o, n, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print("  %-44s %d edits" % (rel.split('/')[1], len(pairs)))


# ------------------------------- ENDURANCE ----------------------------------
edit('racing/imsa-endurance-simulator-tampa/index.html', [
    ("Races run for hours, grids mix cars of very different speeds, and the driver who wins is usually the one who made the fewest mistakes rather than the one who set the quickest time. This page explains what that actually asks of you.",
     "Races run for hours and grids mix cars of very different speeds, so avoiding mistakes across a long stint matters alongside outright pace. This page explains what that asks of a driver."),

    ('<p class="lead">A prototype is a closed-cockpit racing car built from scratch to a set of rules, rather than developed from a road-going model. Nothing about it has to relate to a car you could buy.</p>',
     '<p class="lead">A prototype is a racing car built from scratch to a set of rules, rather than developed from a road-going model. Nothing about it has to relate to a car you could buy. Current top-flight prototypes are usually closed-cockpit, though open-cockpit prototypes have raced for much of the category history.</p>'),

    ("<p>That freedom shows up mainly in aerodynamics. Prototypes generate considerably more downforce for their weight than GT cars do, and much of it comes from the underfloor, which is shaped to accelerate air beneath the car and reduce the pressure there. The practical effect is grip that arrives with speed, so the car feels progressively more planted the harder it is driven through a quick corner.</p>",
     "<p>That freedom shows up mainly in aerodynamics. Prototypes typically generate more downforce for their weight than GT cars, and a large share of it comes from the underfloor, which is shaped to accelerate air beneath the car and reduce the pressure there. Aerodynamic grip rises with speed, though how it builds depends on ride height, aero balance and the specific car, so it is not a simple linear relationship.</p>"),

    ("<p>That produces the skill endurance drivers talk about most. A prototype driver has to plan a pass on a slower car several corners ahead, in a way that does not compromise their own line or the GT driver&rsquo;s race. A GT driver has to be predictable, hold their line, and not surprise the faster car arriving behind them.</p>",
     "<p>That produces a skill particular to the category. A prototype driver plans a pass on a slower car ahead of time, ideally without compromising their own line or the GT driver&rsquo;s race. A GT driver is expected to be predictable and not to surprise the faster car arriving behind them.</p>"),

    ("<p>It is a genuinely different mental exercise from a single-class sprint, and it is the reason experienced sim racers often find endurance the most absorbing category once the novelty of raw speed has worn off.</p>",
     "<p>It is a different mental exercise from a single-class sprint, and it is a large part of what draws people to the category.</p>"),

    ("      <p>Running within a small window of your own best time, for stint after stint, matters more than a single quick effort. A driver who is half a second slower but never varies is usually worth more to a team than one who is fast and erratic.</p>",
     "      <p>Running within a small window of your own best time, stint after stint, is what teams tend to value. Consistency is discussed in endurance circles at least as much as outright pace.</p>"),

    ("      <p>Tyres degrade, fuel load changes the handling as it burns off, and brakes have to survive to the end. Driving to preserve the car is a skill in its own right, and it is often the difference between finishing and not.</p>",
     "      <p>Tyres degrade, fuel load changes the handling as it burns off, and brakes have to last. Driving to preserve the car is a skill in its own right, and one that barely features in a short sprint.</p>"),

    ("      <p>Mirrors and spatial awareness matter far more when a car ten seconds a lap quicker is closing on you. Knowing where you are on the circuit, who is behind, and what class they are in becomes constant background work.</p>",
     "      <p>Mirrors and spatial awareness matter more when a much quicker car is closing on you. Knowing where you are on the circuit, who is behind, and what class they are in becomes constant background work.</p>"),

    ("      <p>Long stints are physically and mentally tiring, and the mistakes that decide endurance races usually happen when concentration slips rather than when a driver is on the limit.</p>",
     "      <p>Long stints are physically and mentally tiring, and holding concentration when the novelty has worn off is part of what the discipline asks for.</p>"),

    ("      <p>Our flagship is a Trak Racer TR160 V5 on four D-BOX Gen 5 actuators, giving pitch, roll and heave, with triple screens, direct drive steering, active pedals and a real cockpit. Over a long run the motion cues help you register small changes in the car as tyres go off.</p>",
     "      <p>Our flagship is a Trak Racer TR160 V5 on four D-BOX Gen 5 actuators, giving pitch, roll and heave, with triple screens, direct drive steering, active pedals and a real cockpit. The platform adds physical cues alongside what the wheel and screens are telling you."),

    ("      <p>Peripheral vision matters more in multi-class racing than anywhere else, because a large part of the job is knowing what is beside you. Triple screens make that natural rather than a mirror-checking exercise.</p>",
     "      <p>Peripheral vision matters a great deal in multi-class racing, because a large part of the job is knowing what is beside you. Triple screens widen the field of view considerably.</p>"),

    ("<p>Sessions start at $40 an hour and no experience is required. Setup and a few orientation laps come with every booking. Endurance is one category where booking two hours rather than one changes the character of the session, because stint length is part of the point.</p>",
     "<p>Sessions start at $40 an hour and no experience is required. Setup and a few orientation laps come with every booking. Stint length is part of what defines endurance racing, so a two hour booking suits the category better than one.</p>"),
])

# --------------------------------- RALLY ------------------------------------
edit('racing/rally-simulator-tampa/index.html', [
    ("<p class=\"hero-sub\">Rally is the only major discipline where you are not racing anyone directly. One car at a time, against the clock, on a road you have usually never driven, with a surface that changes under you from corner to corner. It teaches car control faster than circuit racing because you spend so much of the time slightly out of shape.</p>",
     "<p class=\"hero-sub\">Rally is run against the clock rather than wheel to wheel. One car at a time, on closed public roads, with a surface that changes under you from corner to corner. It asks for a different kind of car control from circuit racing, because the car spends far more of the time slightly out of shape.</p>"),

    ('<p class="lead">On a circuit you learn a fixed piece of road and then refine it over many laps. On a stage you get one run, and most of the road is new to you as you arrive at it.</p>',
     '<p class="lead">On a circuit you learn a fixed piece of road and refine it over many laps. On a stage you usually get one run, and even after a reconnaissance pass you are working from notes rather than from repetition.</p>'),

    ("<p>That inverts how you drive. Circuit racing rewards building a precise mental model of a known corner. Rally rewards reading the road as it appears, leaving margin for what you cannot see, and being able to correct a car that is already sliding rather than avoiding the slide in the first place.</p>",
     "<p>That changes how you drive. Circuit racing rewards building a precise mental model of a known corner. Rally leans more on reading the road as it appears, leaving margin for what you cannot see, and correcting a car that is already sliding rather than avoiding the slide in the first place.</p>"),

    ('<p class="lead">In real rallying the driver does not memorise the stage. A co-driver reads a running description of the road aloud, a corner or two ahead, throughout the run.</p>',
     '<p class="lead">In rallying a co-driver reads a running description of the road aloud, ahead of the car, throughout the run. Drivers may recall parts of a stage they have run before, but the notes are what they drive to.</p>'),

    ("<p>Those notes are written by the crew themselves during a reconnaissance pass and use a numbered severity system for corners, along with shorthand for crests, jumps, surface changes and hazards. The driver commits to a corner they cannot yet see on the strength of what they have just been told, which is why the trust between driver and co-driver is talked about the way it is.</p>",
     "<p>Notes are typically written by the crew during a reconnaissance pass, using a shorthand for corner severity along with markers for crests, jumps, surface changes and hazards. Systems vary between crews, and some grade corners by number while others describe them in words. Either way the driver commits to a corner they cannot yet see on the strength of what they have just been told, which is why the trust between driver and co-driver is talked about the way it is.</p>"),

    ("<p>Simulators reproduce this: stage rally titles include co-driver calls, and learning to act on a call rather than on what your eyes have confirmed is one of the genuinely novel things about trying rally for the first time.</p>",
     "<p>Learning to act on a call rather than on what your eyes have already confirmed is one of the more unusual things about trying rally, and it is the part people tend to remember.</p>"),

    ("      <p>On a stage your eyes have to be much further down the road than on a circuit, because you are reacting rather than repeating. It is the single habit that changes most between the two.</p>",
     "      <p>On a stage your eyes need to be a long way down the road, because you are reading rather than repeating. It is one of the habits that differs most from circuit driving.</p>"),

    ('<p class="lead">Rally is one of the two categories where the hardware genuinely changes what you can practise, because of the handbrake.</p>',
     '<p class="lead">Rally is one of the categories where the hardware changes what you can practise, because of the handbrake.</p>'),
])
