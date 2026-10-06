# -*- coding: utf-8 -*-
"""Add real photography to the new lounge pages.

Every image below was opened and looked at before being placed; alt text
describes what is actually in the frame, not what the filename claims. All are
served from the Shopify CDN the homepage already uses, so nothing is uploaded.

Deliberately NOT used: florida-blue-lounge-event-group.jpg (real, but shot
against a Hot Wheels mural with no simulator in frame - third-party branding
risks implying an affiliation, README rule 2), and every ChatGPT_Image_* /
Gemini_Generated_* file, which are AI renders and must never be presented as
photographs of the lounge.
"""
import io, os, sys

D = sys.argv[1]
CDN = 'https://cdn.shopify.com/s/files/1/0644/3447/1128/files'

CSS_MARKER = '.lp a:focus-visible,.lp button:focus-visible{outline:2px solid #fbbf24;outline-offset:3px;}'
CSS = (
    '\n.lp .media-band{padding-top:34px;padding-bottom:0;border-bottom:none;}'
    '\n.lp figure{margin:0;}'
    '\n.lp figure img{display:block;width:100%;height:auto;border:1px solid rgba(255,255,255,.1);background:#111113;}'
    '\n.lp figcaption{font-family:\'IBM Plex Mono\',monospace;font-size:10px;letter-spacing:.16em;'
    'text-transform:uppercase;color:#71717a;margin-top:9px;}'
)

# page -> (file, version query, natural w, natural h, alt, caption)
IMAGES = {
    'tracks/daytona/index.html': (
        'asr-hpde-daytona.jpg', '', 960, 1200,
        'A TT3 class race car at speed on the banking at Daytona International Speedway',
        'Daytona International Speedway'),
    'tracks/index.html': (
        'asr-driver-coach-back.jpg', '', 1792, 1198,
        'An Academy driver coach in HPDE progression kit at a circuit',
        'Circuit familiarity is the part that transfers'),
    'racing/manual-transmission-simulator-tampa/index.html': (
        'LQRA7465.jpg', '&v=1778973338', 4032, 3024,
        'The Manual Cockpit simulator, showing its H-pattern shifter, handbrake and three-pedal set including the clutch',
        'The Manual Cockpit, shifter, handbrake and three pedals'),
    'cars/classic-race-cars/index.html': (
        'LQRA7465.jpg', '&v=1778973338', 4032, 3024,
        'The Manual Cockpit simulator with its H-pattern shifter, handbrake and three pedals',
        'H-pattern shifter, handbrake and a clutch'),
    'cars/index.html': (
        'VJKZ8462.jpg', '&v=1778970448', 4032, 3024,
        'The Motion GT simulator on its motion platform, with triple curved screens and a direct drive wheel',
        'The Motion GT'),
    'cars-and-tracks/index.html': (
        'IMG_5363.jpg', '&v=1780945875', 5712, 4284,
        'Inside the Academy Sim Racing lounge in Tampa, with racing simulators along both walls',
        'The lounge, 1421 Massaro Blvd'),
    'things-to-do-in-tampa/index.html': (
        'florida-blue-lounge-event-racing.jpg', '', 1178, 1557,
        'A corporate group racing on triple-screen simulators at the Tampa lounge',
        'A corporate group at the lounge'),
}


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


for rel, (fn, ver, w, h, alt, cap) in sorted(IMAGES.items()):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p):
        print('  %-46s MISSING' % rel)
        continue
    s = rd(p)

    if 'class="media-band"' in s:
        print('  %-46s already has image' % rel)
        continue

    # 1. stylesheet
    if '.lp .media-band' not in s:
        assert s.count(CSS_MARKER) == 1, 'css marker in ' + rel
        s = s.replace(CSS_MARKER, CSS_MARKER + CSS, 1)

    # 2. the figure, right after the hero
    base = '%s/%s?%s' % (CDN, fn, ver.lstrip('&'))
    sep = '&' if ver else ''

    def src(width):
        return '%s/%s?width=%d%s' % (CDN, fn, width, ver)

    ratio_h = int(round(1200 * h / float(w)))
    fig = (
        '\n<section class="section media-band">\n'
        '  <figure>\n'
        '    <img src="%s" alt="%s"\n'
        '         srcset="%s 800w, %s 1200w, %s 1600w"\n'
        '         sizes="(max-width: 1100px) 100vw, 1100px"\n'
        '         width="1200" height="%d" loading="lazy" decoding="async">\n'
        '    <figcaption>%s</figcaption>\n'
        '  </figure>\n'
        '</section>\n' % (src(1200), alt, src(800), src(1200), src(1600), ratio_h, cap)
    )

    anchor = '</header>\n'
    assert s.count(anchor) == 1, '%s: header anchor x%d' % (rel, s.count(anchor))
    s = s.replace(anchor, anchor + fig, 1)

    wr(p, s)
    print('  %-46s + %s' % (rel, fn))
