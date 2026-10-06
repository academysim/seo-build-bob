import io, os, sys, re, json

b = sys.argv[1]
ga = io.open(os.path.join(b, '_ga.html'), encoding='utf-8', newline='').read().strip()

PAGES = [
    'racing/index.html',
    'racing/gt3-simulator-tampa/index.html',
    'racing/formula-simulator-tampa/index.html',
    'racing/nascar-simulator-tampa/index.html',
    'racing/drift-simulator-tampa/index.html',
]

# ---- 1. the two remaining Codex blockers -----------------------------------
BLOCKERS = {
 'racing/formula-simulator-tampa/index.html': [(
   "Very little weight, a great deal of aerodynamic grip, and in most classes nothing electronic between your foot and the tyres.",
   "Very little weight, a great deal of aerodynamic grip, and in most classes no traction control to catch a mistake with the throttle.")],
 'racing/nascar-simulator-tampa/index.html': [(
   "Banking usually varies across the width of the track, so different lines trade radius against angle, and choosing between them is part of the craft.",
   "Some ovals hold a constant banking angle across the racing surface while others vary it by lane, and where a track does vary, different lines trade radius against angle.")],
}

# ---- 2. em dashes and AI-tell phrasing -------------------------------------
# Straight swaps that keep the sentence readable without a dash.
DASH_FIXES = [
    ("racing simulators at 1421 Massaro Blvd, Tampa. Sessions from $40 an hour, coaching optional, no experience needed.",
     "racing simulators at 1421 Massaro Blvd, Tampa. Sessions from $40 an hour, coaching optional, no experience needed."),
]

AI_TELLS = [
    ("Whether you want to", "If you want to"),
    ("It is worth noting that ", ""),
    ("Ultimately, ", ""),
    ("In today's world, ", ""),
    ("delve into", "get into"),
    ("a testament to", "a sign of"),
    ("seamless", "smooth"),
    ("elevate your", "improve your"),
    ("unlock", "open up"),
    ("robust", "solid"),
    ("leverage", "use"),
    ("cutting-edge", "modern"),
    ("state-of-the-art", "modern"),
    ("game-changer", "big difference"),
    ("dive in", "get started"),
]


def strip_dashes(s):
    """Replace em dashes with punctuation that reads naturally."""
    # ' &mdash; ' or ' — ' between clauses -> comma, or full stop where it ends a clause pair
    s = re.sub(r'\s*&mdash;\s*', ', ', s)
    s = re.sub(r'\s*—\s*', ', ', s)
    # tidy the artefacts that creates
    s = s.replace(', ,', ',').replace(' ,', ',').replace(',,', ',')
    s = re.sub(r',\s*and\s+', ' and ', s) if False else s
    return s


report = []
for rel in PAGES:
    p = os.path.join(b, *rel.split('/'))
    s = io.open(p, encoding='utf-8', newline='').read()
    before_dashes = len(re.findall(r'&mdash;|—', s))

    for old, new in BLOCKERS.get(rel, []):
        assert s.count(old) == 1, "blocker text not found once in %s" % rel
        s = s.replace(old, new, 1)

    # only touch the body, never the <style>/<script>/head
    head, sep, rest = s.partition('<main>')
    body, sep2, tail = rest.partition('</main>')
    body = strip_dashes(body)
    for old, new in AI_TELLS:
        body = body.replace(old, new)
    s = head + sep + body + sep2 + tail

    # ---- 3. Google Analytics, matching the existing pages ------------------
    if 'googletagmanager' not in s:
        anchor = '<link rel="preconnect" href="https://fonts.googleapis.com">'
        assert s.count(anchor) == 1, "font anchor missing in %s" % rel
        s = s.replace(anchor, ga + "\n" + anchor, 1)

    io.open(p, 'w', encoding='utf-8', newline='').write(s)

    after_dashes = len(re.findall(r'&mdash;|—', s))
    for x in re.findall(r'<script type="application/ld[+]json">(.*?)</script>', s, re.S):
        json.loads(x)
    report.append((rel.split('/')[1] if rel != 'racing/index.html' else 'racing-hub',
                   len(s.encode()), before_dashes, after_dashes,
                   s.count('googletagmanager'), s.count('G-SQL40ZS59K'),
                   s.count('<p'), s.count('</p>')))

print("  %-24s %8s %7s %7s %5s %5s %8s" % ("page", "bytes", "dash>", "dash<", "gtm", "Gtag", "p-tags"))
for r in report:
    print("  %-24s %8d %7d %7d %5d %5d %5d/%d %s" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7],
          "OK" if r[3] == 0 and r[4] == 1 and r[6] == r[7] else "*** CHECK"))
