import io, os, sys

p = os.path.join(sys.argv[1], 'tracks', 'daytona', 'index.html')
s = io.open(p, encoding='utf-8', newline='').read()

# old h3 text  ->  (cnum label, new descriptive h3)
MAP = [
    ("Turns 1 and 2, off the tri-oval and into the infield",
     "Turns 1 &amp; 2 &middot; Infield Entry", "Where the banking stops"),
    ("Turn 3, the International Horseshoe",
     "Turn 3 &middot; International Horseshoe", "The slowest corner on the circuit"),
    ("Turns 4 and 5, the Kink and the West Horseshoe",
     "Turns 4 &amp; 5 &middot; The Kink and West Horseshoe", "The pair that sets up the backstretch"),
    ("Turn 6, back onto the banking",
     "Turn 6 &middot; Rejoin", "The biggest transition on the lap"),
    ("Turns 7 to 10, the Le Mans Chicane",
     "Turns 7 to 10 &middot; Le Mans Chicane", "The one that used to be the Bus Stop"),
    ("Turns 11 and 12, the banked oval corners",
     "Turns 11 &amp; 12 &middot; Oval Turns 3 and 4", "Thirty-one degrees of banking"),
]

for old_h3, cnum, new_h3 in MAP:
    src = "    <h3>%s</h3>\n" % old_h3
    assert s.count(src) == 1, "not once: %s" % old_h3
    dst = '    <div class="cnum">%s</div>\n    <h3>%s</h3>\n' % (cnum, new_h3)
    s = s.replace(src, dst, 1)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print("corners restructured: %d" % len(MAP))
print("cnum blocks: %d   corner blocks: %d" % (s.count('class="cnum"'), s.count('class="corner"')))
print("div balance: %d/%d   p balance: %d/%d" % (s.count('<div'), s.count('</div>'), s.count('<p'), s.count('</p>')))
