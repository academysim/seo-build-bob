"""Expand __GA__/__STYLE__/__NAV__/__FOOTER__ placeholders and validate the result."""
import io, os, sys, re, json
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from shared.tools.constants import GA4_TAG

b = sys.argv[1]
pages = sys.argv[2:]


def rd(name):
    return io.open(os.path.join(b, name), encoding='utf-8', newline='').read().strip()


ga = rd('_ga.html')
style = rd('_style.css')
nav = rd('_nav.html')
footer = rd('_footer.html')

AI_TELLS = ["delve", "testament to", "seamless", "elevate your", "unlock",
            "cutting-edge", "state-of-the-art", "game-changer", "In today's",
            "It is worth noting", "Ultimately,", "robust", "leverage",
            "navigate the world", "when it comes to", "look no further"]

fail = 0
for rel in pages:
    p = os.path.join(b, *rel.split('/'))
    s = io.open(p, encoding='utf-8', newline='').read()

    if '__GA__' in s:
        s = s.replace('__GA__', ga)
    s = s.replace('__STYLE__', style).replace('__NAV__', nav).replace('__FOOTER__', footer)

    # The shared nav carries a per-section brand eyebrow. It was originally
    # hardcoded to "TRACK GUIDE", which shipped onto every racing page.
    if rel.startswith('racing/'):
        eyebrow = 'RACING'
    elif rel == 'tracks/index.html':
        eyebrow = 'TRACK GUIDES'
    elif rel.startswith('tracks/'):
        eyebrow = 'TRACK GUIDE'
    elif rel.startswith('cars-and-tracks/'):
        eyebrow = 'CARS &amp; TRACKS'
    elif rel.startswith('cars/'):
        eyebrow = 'CAR CLASSES'
    else:
        eyebrow = 'LOUNGE'
    s = s.replace('__EYEBROW__', eyebrow)

    io.open(p, 'w', encoding='utf-8', newline='').write(s)

    # ---------------------------- validate ----------------------------------
    probs = []
    if '__' in re.sub(r'[A-Za-z0-9]__|__[A-Za-z0-9]', '', ''):
        pass
    for ph in ('__GA__', '__STYLE__', '__NAV__', '__FOOTER__', '__EYEBROW__'):
        if ph in s:
            probs.append('unexpanded ' + ph)

    body = s.partition('<main>')[2].partition('</main>')[0]

    if re.search(r'&mdash;|—', body):
        probs.append('em dash in body')
    for t in AI_TELLS:
        if t.lower() in body.lower():
            probs.append('AI tell: ' + t)
    if s.count(GA4_TAG) < 1:
        probs.append('no GA4 id')
    if s.count('googletagmanager') != 1:
        probs.append('gtm count %d' % s.count('googletagmanager'))
    if s.count('<p') != s.count('</p>'):
        probs.append('p tags %d/%d' % (s.count('<p'), s.count('</p>')))
    if s.count('<div') != s.count('</div>'):
        probs.append('div tags %d/%d' % (s.count('<div'), s.count('</div>')))
    if s.count('<section') != s.count('</section>'):
        probs.append('section tags')
    if s.count('<h1') != 1:
        probs.append('h1 count %d' % s.count('<h1'))
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(blk)
        except Exception as e:
            probs.append('bad JSON-LD: %s' % e)
    for tag in ('canonical', 'og:title', 'og:description', 'twitter:card', 'viewport'):
        if tag not in s:
            probs.append('missing ' + tag)

    ok = 'OK' if not probs else '*** ' + '; '.join(probs)
    print("  %-34s %7d bytes  %s" % (rel, len(s.encode()), ok))
    if probs:
        fail += 1

sys.exit(1 if fail else 0)
