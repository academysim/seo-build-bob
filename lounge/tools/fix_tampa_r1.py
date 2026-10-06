# -*- coding: utf-8 -*-
"""Codex round 1 on /things-to-do-in-tampa/.

REJECTED both "consistency" findings. Codex claimed the homepage says Sunday
3-9 PM and that its buyout pricing lacked a weekend split. Checked directly:
the homepage JSON-LD says Sunday 12:00-18:00 and the visible copy says Sun
12-6 PM, and both the visible copy and the FAQ JSON-LD carry the full
day-of-week buyout split. Codex read the "FROM $249 / HR" floor label as a
contradiction. This page already matched the homepage.

Also rejected most of the "unverifiable claim" list, which would have replaced
ordinary descriptive prose with corporate boilerplate on the one page written
for people who have never heard of sim racing. Kept the items that are real
factual assertions about the business rather than description.
"""
import io, os, sys

b = sys.argv[1]
p = os.path.join(b, 'things-to-do-in-tampa', 'index.html')
s = io.open(p, encoding='utf-8', newline='').read()

EDITS = [
    # 3. professional-training claim, not supported anywhere on the site
    ("running the same software professional drivers train on.",
     "running iRacing and Assetto Corsa."),

    # 22. "fixed" contradicts the motion rig, and 21. define the jargon
    ("This is not an arcade and it is not VR. Each rig is a fixed racing seat with a direct drive steering wheel, a proper pedal set and screens filling your vision, running iRacing and Assetto Corsa.",
     "This is not an arcade and it is not VR. Each rig, meaning the seat, wheel, pedals and screens together, has a direct drive steering wheel, a proper pedal set and screens filling your vision, running iRacing and Assetto Corsa. Most have a fixed cockpit. One, the Motion GT, sits on a platform that moves."),

    # 21. kerbs without explanation
    ("You feel the front tyres start to slide before the car actually goes, you feel the kerbs, and on the motion rig you feel the braking and cornering forces through the seat. It is close enough to driving that people come out of a first session genuinely tired.",
     "The wheel loads up as the front tyres start to slide, you feel the kerbs at the edge of the track, and on the motion rig the braking and cornering come through the seat as well. It is closer to driving than to playing a game."),

    # 6. do not promise a specific setup procedure
    ("Staff set the car up with driver aids on, put you on a circuit that suits you, and turn things off as you get comfortable. Most people are setting competitive laps inside their first session.",
     "Staff get first-timers set up and comfortable, with a car and a circuit chosen to suit you. Most people are setting competitive laps inside their first session."),

    # 10. overpromising
    ("If you watch F1, IMSA or NASCAR, this is the closest you will get to the cars without a licence. Drive the real circuits you watch on Sundays.",
     "If you watch F1, IMSA or NASCAR, you can drive the same real-world circuits you watch on Sundays, in cars of the same type."),

    # 12. invented footwear guidance
    ("Seat position, wheel, pedals, and a car and circuit chosen to suit you. Wear whatever you like. Flat shoes are slightly better than flip flops for the pedals.",
     "Seat position, wheel, pedals, and a car and circuit chosen to suit you. There is nothing to bring and nothing to wear specially."),

    # 21. telemetry jargon
    ("Advanced ($60) adds telemetry review.",
     "Advanced ($60) adds telemetry review, meaning the recorded braking, steering and lap data."),

    # 16. soften the travel framing, keep the place names the brief asks for
    ("We are on Massaro Boulevard in east Tampa, which puts us within an easy drive of most of the bay area.",
     "We are on Massaro Boulevard in east Tampa."),
    ("Brandon, Riverview and Valrico are close by, and we are a straightforward drive from St. Petersburg, Clearwater and Wesley Chapel. If you are making the trip rather than passing by,",
     "Brandon, Riverview and Valrico are the nearest neighbourhoods, and people also come over from St. Petersburg, Clearwater and Wesley Chapel. If you are making a trip of it rather than passing by,"),

    # 23. do not mint a second entity for the same business under a different type
    ("""  "isPartOf": { "@type": "WebSite", "name": "Academy Sim Racing Lounge", "url": "https://lounge.academysim.com/" },
  "about": {
    "@type": "EntertainmentBusiness",
    "name": "Academy Sim Racing",
    "telephone": "+1-813-355-9071",
    "url": "https://lounge.academysim.com/",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1421 Massaro Blvd",
      "addressLocality": "Tampa",
      "addressRegion": "FL",
      "postalCode": "33619",
      "addressCountry": "US"
    }
  }""",
     """  "isPartOf": { "@type": "WebSite", "name": "Academy Sim Racing Lounge", "url": "https://lounge.academysim.com/" },
  "about": { "@id": "https://lounge.academysim.com/#business" },
  "primaryImageOfPage": "https://lounge.academysim.com/og-image.jpg\""""),

    # 24. schema description
    ('"description": "What a racing simulator lounge in Tampa is like to visit, who it suits, and current hours and prices.",',
     '"description": "What a racing simulator lounge in Tampa is like to visit, who it suits, and visitor information including hours and pricing.",'),
]

n = 0
for o, x in EDITS:
    assert s.count(o) == 1, 'NOT ONCE: %r' % o[:70]
    s = s.replace(o, x, 1)
    n += 1

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('  %d edits' % n)
