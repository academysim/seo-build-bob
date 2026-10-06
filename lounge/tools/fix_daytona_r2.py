# -*- coding: utf-8 -*-
"""Round 2 on the track pages.

Rejected from the Codex review: every correction that renumbered the turns.
They cite NASCAR's 14-turn / 3.570 mi road course, which is a different
circuit from the 12-turn / 3.560 mi sports car course this page describes.
Since the two layouts number the corners differently and I could not confirm
the sports car numbering from a primary source, the page now names corners
and gives their position instead of numbering them.
"""
import io, os, sys

b = sys.argv[1]


def edit(rel, pairs):
    p = os.path.join(b, *rel.split('/'))
    s = io.open(p, encoding='utf-8', newline='').read()
    for o, n in pairs:
        assert s.count(o) == 1, "NOT ONCE in %s: %r" % (rel, o[:70])
        s = s.replace(o, n, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print("  %-30s %d edits" % (rel, len(pairs)))


D = 'tracks/daytona/index.html'

edit(D, [
    # ---- 1. drop the unverifiable rejoin/numbering claim, and "half a lap" --
    ("The road course runs the tri-oval, then turns off into a flat infield section rather than taking the banked oval Turns 1 and 2. It rejoins the oval at the exit of Turn 2, runs the backstretch, takes the chicane partway along it, and then goes through the banked oval Turns 3 and 4, which are numbered 11 and 12 on the road course. So you get roughly half a lap of flat, technical driving and half a lap of banking.",
     "The road course leaves the tri-oval for a flat infield section, rejoins the oval, runs the backstretch with a chicane partway along it, and finishes the lap through the banked corners at the far end of the speedway. So a lap combines slow, technical infield driving with long high-speed running on the banking."),

    # ---- 3. repave wording ------------------------------------------------
    ("The oval, apron and pit road were last fully repaved in 2010, only the second full repave in the track history after 1978.",
     "The oval was completely reconstructed in 2010. The previous resurfacing, in 1978, was an asphalt overlay."),

    # ---- 22. plainer -------------------------------------------------------
    ("That split is what makes Daytona unusual to learn. Most circuits ask you to build one consistent set of habits. Daytona asks you to switch between two, and the transitions between flat pavement and steep banking are where the car changes most.",
     "That split is what makes Daytona unusual to learn. You have to adjust between the flat infield and the banked oval sections, and the transitions between the two are where the car changes most."),

    # ---- corner 1 ----------------------------------------------------------
    ('    <div class="cnum">Turns 1 &amp; 2 &middot; Infield Entry</div>\n    <h3>Where the banking stops</h3>',
     '    <div class="cnum">Infield Entry</div>\n    <h3>Where the banking stops</h3>'),
    ("The road course leaves the banking and drops into the flat infield. Turn 1 is the entry, and Turn 2 is a right then left complex that sets up the rest of the infield. The car arrives here carrying speed from the tri-oval onto a surface with far less support than the banking gave it, so this is a corner where arriving too fast costs you the whole sequence that follows.",
     "The road course leaves the tri-oval and drops into the flat infield through a right then left complex. The car arrives carrying speed from the banked tri-oval onto flat pavement, so arriving too fast here compromises the whole sequence that follows."),

    # ---- corner 2 ----------------------------------------------------------
    ('    <div class="cnum">Turn 3 &middot; International Horseshoe</div>\n    <h3>The slowest corner on the circuit</h3>',
     '    <div class="cnum">International Horseshoe</div>\n    <h3>One of the slowest corners on the circuit</h3>'),
    ("A long right-hand hairpin and the slowest part of the circuit. Corners like this reward patience more than bravery. It is long enough that a driver who turns in early runs out of road on exit, and because it is followed by more infield rather than a straight, the temptation to force it is worth resisting.",
     "A long right-hand hairpin and one of the slowest parts of the circuit. It is long enough that an early turn-in leaves you short of road at the exit. It is followed by more infield rather than a straight, so the exit matters less here than it does at the corners that feed the oval."),

    # ---- corner 3 ----------------------------------------------------------
    ('    <div class="cnum">Turns 4 &amp; 5 &middot; The Kink and West Horseshoe</div>\n    <h3>The pair that sets up the backstretch</h3>',
     '    <div class="cnum">The Kink and West Horseshoe</div>\n    <h3>The run back toward the oval</h3>'),
    ("The Kink is a quicker left that leads into the West Horseshoe, another right-hander. This pair is where a lap in the infield is won or lost, because the West Horseshoe determines your speed for the run back out onto the oval.",
     "The Kink is a quicker left that leads into the West Horseshoe, another right-hander. These corners set up the approach to the left that takes you back onto the banking, so they affect how much speed you carry into the oval section."),

    # ---- corner 4 ----------------------------------------------------------
    ('    <div class="cnum">Turn 6 &middot; Rejoin</div>\n    <h3>The biggest transition on the lap</h3>',
     '    <div class="cnum">Rejoining The Banking</div>\n    <h3>The biggest transition on the lap</h3>'),
    ("A left that puts you back onto the oval at the exit of Turn 2 and onto the backstretch. This is the biggest transition on the circuit. The infield is flat, the oval is banked, and the camber change through this rejoin is one of the things drivers notice first at Daytona. Get the exit right and you carry it the length of the backstretch.",
     "A left-hander that feeds the car off the flat infield and back onto the banking. This is the biggest transition on the circuit. The infield is flat and the oval is banked, and the camber change through the rejoin is one of the things drivers notice first at Daytona. The exit sets your speed for the run down the backstretch."),

    # ---- corner 5 ----------------------------------------------------------
    ('    <div class="cnum">Turns 7 to 10 &middot; Le Mans Chicane</div>\n    <h3>The one that used to be the Bus Stop</h3>',
     '    <div class="cnum">Le Mans Chicane</div>\n    <h3>The one that used to be the Bus Stop</h3>'),
    ("The chicane partway along the backstretch, known for years as the Bus Stop. It is four numbered turns, and the sequence is left, right, right, left, so the first input on approach is a left. It interrupts the fastest part of the lap, which makes it both the main overtaking opportunity and the easiest place to throw away a lap by overdriving the entry.",
     "The chicane partway along the backstretch, known for years as the Bus Stop and renamed the Le Mans Chicane in 2022. Its four changes of direction run left, right, right, left, so the first input on approach is a left. It interrupts the fastest part of the lap, so its braking zone can offer an overtaking opportunity, and an overcommitted entry compromises the rest of the sequence."),

    # ---- corner 6 ----------------------------------------------------------
    ('    <div class="cnum">Turns 11 &amp; 12 &middot; Oval Turns 3 and 4</div>\n    <h3>Thirty-one degrees of banking</h3>',
     '    <div class="cnum">The Banked Oval Corners</div>\n    <h3>Thirty-one degrees of banking</h3>'),
    ("Oval Turns 3 and 4 at 31 degrees. Banking works by pointing part of the road surface into the corner for you, so a banked corner takes less steering input and supports more speed than the same radius would if it were flat. For a driver used only to flat circuits it is a genuinely different sensation, and it is one of the things a simulator conveys reasonably well because the visual and the steering load both change.",
     "The lap finishes through the banked corners at the far end of the speedway, at 31 degrees. Banking tilts the road so that part of the force supporting the car also pushes it into the corner, which means more speed is available at a given radius than on a flat corner. For a driver used only to flat circuits it is a genuinely different sensation. A simulator shows the visual change clearly, though how the steering feels depends on the software, the car and the hardware."),

    # ---- numbering note ----------------------------------------------------
    ("  </div>\n</section>\n\n<section class=\"section\">\n  <h2>Who Runs Events At Daytona</h2>",
     "  </div>\n\n  <p class=\"note\">Corner numbering at Daytona depends on which layout you are running. The sports car road course is 3.560 miles with 12 turns, while the road course NASCAR uses is 3.570 miles with 14 turns, so the same corner can carry different numbers. We have used corner names here for that reason. Check the numbering on the map your organiser supplies.</p>\n</section>\n\n<section class=\"section\">\n  <h2>Who Runs Events At Daytona</h2>"),

    # ---- 10. statline distance --------------------------------------------
    ("    <span><strong>2 hr 15</strong> &nbsp;From Our Tampa Lounge</span>",
     "    <span><strong>135 mi</strong> &nbsp;From Our Tampa Lounge</span>"),

    # ---- 21. CTA brand risk ------------------------------------------------
    ('>DRIVE DAYTONA IN TAMPA &rarr;</a>', '>PRACTISE THE LAYOUT IN TAMPA &rarr;</a>'),

    # ---- 17. prep step -----------------------------------------------------
    ("The parts of Daytona that surprise people are the changes between flat and banked surfaces rather than any single corner. Knowing where those transitions are is worth more than knowing a fast line.",
     "The parts of Daytona that surprise people are the changes between flat and banked surfaces rather than any single corner. Learn where those transitions are, then work on the line with your instructor once you are there."),

    # ---- 18/19. car prep ---------------------------------------------------
    ("Fresh brake fluid, decent pads, good tyres, correct pressures, and nothing loose in the cabin. Bring more water than you think you need. Florida heat does most of the damage to drivers at summer events.",
     "Have the car inspected and follow the organiser&rsquo;s requirements for brakes, tyres, fluids and cold tyre pressures, and clear anything loose out of the cabin. Summer events in Florida get hot and humid, so follow the organiser&rsquo;s guidance on hydration and heat."),

    # ---- 20. closing step --------------------------------------------------
    ("Leave margin, especially on the banking, where speeds are highest and the consequences of a mistake are largest. Nobody has ever regretted a cautious first session.",
     "Leave margin, especially on the banking, where speeds are highest and the consequences of a mistake are largest. Build pace as conditions and your instructor allow."),

    # ---- 11. CTA card ------------------------------------------------------
    ("Daytona is in our track library on eight professional simulators at 1421 Massaro Blvd, Tampa. Sessions from $40 an hour, coaching optional, no experience needed. About two and a quarter hours closer than the circuit itself.",
     "Daytona is in our track library on eight professional simulators at 1421 Massaro Blvd, Tampa. Sessions from $40 an hour, coaching optional, no experience needed. The speedway itself is roughly a two and a half hour drive from Tampa depending on traffic."),

    # ---- 25. Article schema completeness ------------------------------------
    ('  "headline": "Daytona Track Guide: Learn the Road Course Before Your Track Weekend",',
     '  "headline": "Daytona Track Guide: Learn the Road Course Before Your Track Weekend",\n  "url": "https://lounge.academysim.com/tracks/daytona/",\n  "mainEntityOfPage": "https://lounge.academysim.com/tracks/daytona/",\n  "image": "https://lounge.academysim.com/og-image.jpg",\n  "datePublished": "2026-08-29",\n  "dateModified": "2026-08-29",'),
])

# ------------------------------- TRACKS HUB ---------------------------------
edit('tracks/index.html', [
    # ---- 12. tri-oval "flat out" -------------------------------------------
    ("Daytona International Speedway. Steep banking, a tri-oval that is flat out for most of a lap, and an infield road course used for sports car racing. Two very different circuits sharing the same site.",
     "Daytona International Speedway. A high-speed banked oval and a flat infield road course used for sports car racing. Two very different kinds of road on the same site."),

    # ---- 24. promotional filler --------------------------------------------
    ("The first session of a track day is largely spent working out where the circuit goes. That is a poor use of paid track time, and it is the part a simulator can genuinely take off your hands.",
     "The first session of a track day is largely spent working out where the circuit goes. Simulator practice can cut down the time it takes to learn the corner sequence."),
])
