import io, os, sys

b = sys.argv[1]


def edit(rel, pairs):
    p = os.path.join(b, *rel.split('/'))
    s = io.open(p, encoding='utf-8', newline='').read()
    for o, n in pairs:
        assert s.count(o) == 1, "NOT ONCE in %s: %s" % (rel, o[:70])
        s = s.replace(o, n, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print("  %-42s %d edits" % (rel, len(pairs)))


# ---------------- STOCK CAR --------------------------------------------------
edit('racing/nascar-simulator-tampa/index.html', [
    ('<p class="lead">Stock cars are heavy, powerful, and comparatively low on aerodynamic downforce. Those three facts together explain almost everything about how they behave.</p>',
     '<p class="lead">Stock cars are heavy and powerful, and they generate less aerodynamic downforce relative to their mass than a prototype or a formula car does. Those facts together shape most of how they behave.</p>'),

    ("<p>Weight resists changes of direction and loads the tyres hard through a long corner. Power means the rear axle can overwhelm its tyres on exit. Limited downforce means the car depends far more on mechanical grip from the tyres and suspension than on air pressing it down. Put together, you get a car that slides &mdash; not occasionally, but as a normal part of going quickly.</p>",
     "<p>Weight resists changes of direction and loads the tyres hard through a long corner. Power means the rear axle can overwhelm its tyres on exit. Leaning less on downforce means the car depends more on mechanical grip from the tyres and suspension. Aerodynamics still matter a great deal in stock car racing, with splitter behaviour and the effects of running in another car&rsquo;s air being central to how these races unfold, but the car moves around under the driver in a way a high-downforce car does not.</p>"),

    ("      <h3>The banking changes the grip</h3>\n      <p>Banked corners push the car into the track surface, so the grip available depends on where on the banking you are. That gives multiple viable lines, and choosing between them is part of the craft.</p>",
     "      <h3>Banking changes what the corner asks for</h3>\n      <p>On a banked corner part of the cornering force is carried by the angle of the track rather than by the tyres alone, which is why banked ovals are taken so much faster than flat ones. Banking usually varies across the width of the track, so different lines trade radius against angle, and choosing between them is part of the craft.</p>"),

    ("      <h3>Air matters when other cars are near</h3>\n      <p>Running close to another car changes the airflow over both. In real oval racing that produces the effects known as drafting and aerodynamic loss, and simulators model this closely enough that it is a real part of racing them.</p>",
     "      <h3>Air matters when other cars are near</h3>\n      <p>Running close to another car changes the airflow over both. In real oval racing that produces the effects known as drafting and side drafting, and it is a large part of why oval racing looks the way it does.</p>"),

    ("      <p>Sustained lateral load through a banked corner is one of the things a motion platform communicates most clearly. Our flagship pairs motion with triple screens, direct drive steering, active pedals and a real cockpit.</p>",
     "      <p>Our flagship is a Trak Racer TR160 V5 on four D-BOX Gen 5 actuators, giving pitch, roll and heave, with triple screens, direct drive steering, active pedals and a real cockpit. A motion platform supplies transient cues as loads change rather than reproducing sustained cornering force, and on an oval those transitions are where the information is.</p>"),

    ("  <p>Single-screen rigs are also available and run the same software. Our library covers more than 170 cars across more than 140 tracks through iRacing and Assetto Corsa, including a range of ovals.</p>",
     "  <p>Single-screen rigs are also available. Our library covers more than 170 cars across more than 140 tracks through iRacing and Assetto Corsa.</p>"),

    ("  <p>Coaching is available as an optional add-on: Basic Coaching ($40) puts an instructor beside you for the whole session, and Advanced Coaching ($60) adds telemetry review. Oval running is one of the areas where comparing your throttle and steering traces against a reference is especially informative.</p>",
     "  <p>Coaching is available as an optional add-on: Basic Coaching ($40) puts an instructor beside you for the whole session, and Advanced Coaching ($60) adds telemetry review, which compares your inputs against a reference lap.</p>"),
])

# ---------------- DRIFT ------------------------------------------------------
edit('racing/drift-simulator-tampa/index.html', [
    ('<p class="lead">A drift is a sustained, controlled oversteer. The rear tyres are sliding, the front wheels are usually pointed away from the direction of the turn, and the car is being balanced there deliberately rather than recovered from.</p>',
     '<p class="lead">A drift is a sustained, controlled oversteer. The rear tyres are sliding, the front wheels are steered opposite to the direction the car is rotating, and the car is being balanced there deliberately rather than recovered from.</p>'),

    ("<p>In competition, drifting is scored by judges on criteria such as angle, line and commitment, sometimes with two cars running in close proximity. That is a useful thing to know because it explains why drifting looks the way it does: the goal is not to get round the corner efficiently, it is to get round it in a particular manner.</p>",
     "<p>In competition, drifting is scored by judges on criteria such as line, angle and style, often with two cars running in close proximity. That is worth knowing because it explains why drifting looks the way it does: the goal is not to get round the corner efficiently, it is to get round it in a particular manner.</p>"),

    ("      <p>Four rigs carry a six-speed H-pattern shifter and a handbrake, with load-cell or active pedals. Mention drifting when you book and we will put you on one of them.</p>",
     "      <p>Four rigs carry a six-speed H-pattern shifter and a handbrake, with load-cell or active pedals. Mention drifting when you book so one can be set aside where possible.</p>"),

    ("      <p>Our flagship pairs motion with triple screens and a real cockpit. Feeling the rear step out through the seat, slightly before the wheel tells you, is genuinely useful when learning to catch a slide.</p>",
     "      <p>Our flagship is a Trak Racer TR160 V5 on four D-BOX Gen 5 actuators, giving pitch, roll and heave, with triple screens and a real cockpit. The platform adds a physical cue as the car rotates, alongside what the wheel is doing.</p>"),

    ("  <p>Sessions start at $40 an hour and no experience is required. Setup and a few orientation laps come with every booking. Say that you want to drift when you book, so we can put you on a rig with a handbrake.</p>",
     "  <p>Sessions start at $40 an hour and no experience is required. Setup and a few orientation laps come with every booking. Say that you want to drift when you book, so a rig with a handbrake can be set aside where possible.</p>"),

    ("  <p>Coaching is available as an optional add-on: Basic Coaching ($40) puts an instructor beside you for the whole session, and Advanced Coaching ($60) adds telemetry review. Drifting is one of the areas where having someone talk you through the timing of the inputs tends to shorten the frustrating early stage.</p>",
     "  <p>Coaching is available as an optional add-on: Basic Coaching ($40) puts an instructor beside you for the whole session, and Advanced Coaching ($60) adds telemetry review.</p>"),

    ("      <p>Academy builds custom simulators and can specify a handbrake and H-pattern shifter. Try the rigs in Tampa first.</p>",
     "      <p>Academy also builds custom simulators. Try the rigs in Tampa first.</p>"),
])
