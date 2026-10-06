# -*- coding: utf-8 -*-
"""Second image pass (2026-09-03): the six racing discipline pages, the league page and Sebring.
Same insertion pattern as add_images.py (a media-band figure right after the hero). Real photos
and the league's own round-one art only; no AI renders."""
import io, os, sys
D = sys.argv[1]
CDN = 'https://cdn.shopify.com/s/files/1/0644/3447/1128/files'
CSS_MARKER = '.lp a:focus-visible,.lp button:focus-visible{outline:2px solid #fbbf24;outline-offset:3px;}'
CSS = ('\n.lp .media-band{padding-top:34px;padding-bottom:0;border-bottom:none;}'
       '\n.lp figure{margin:0;}'
       '\n.lp figure img{display:block;width:100%;height:auto;border:1px solid rgba(255,255,255,.1);background:#111113;}'
       '\n.lp figcaption{font-family:\'IBM Plex Mono\',monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#71717a;margin-top:9px;}')
IMAGES = {
    'racing/gt3-simulator-tampa/index.html': ('IMG_3161.jpg', '&v=1753063123', 1920, 1280, 'A driver racing a GT car on a triple-screen simulator at the Tampa lounge', 'GT racing on the triple-screen rig'),
    'racing/formula-simulator-tampa/index.html': ('asr-hero-sim.jpg', '&v=1785985871', 2400, 1200, 'A racing simulator cockpit with a formula-style wheel and triple screens', 'Open-wheel on the triple-screen cockpit'),
    'racing/nascar-simulator-tampa/index.html': ('VJKZ8462.jpg', '&v=1778970448', 4032, 3024, 'The Motion GT simulator on its motion platform with triple curved screens', 'The Motion GT, built for oval speed'),
    'racing/drift-simulator-tampa/index.html': ('LQRA7465.jpg', '&v=1778973338', 4032, 3024, 'The Manual Cockpit with its H-pattern shifter, handbrake and three pedals', 'Handbrake and clutch, the drift essentials'),
    'racing/imsa-endurance-simulator-tampa/index.html': ('asr-hpde-daytona.jpg', '', 960, 1200, 'A race car at speed on the banking at Daytona International Speedway', 'Daytona, home of the 24'),
    'racing/rally-simulator-tampa/index.html': ('asr-driver-coach-back.jpg', '&v=1785985116', 1792, 1198, 'A coach standing behind a driver on a simulator, watching the screens', 'Coaching from behind the seat'),
    'league/index.html': ('Week1_ROAD_ATLANTA.jpg', '&v=1786459444', 1620, 1080, 'Thursday Night Lights round 1 of 6, Road Atlanta, Porsche 911 GT3 Cup', 'Round 1: Road Atlanta, September 3'),
    'tracks/sebring/index.html': ('florida-blue-lounge-event-racing.jpg', '&v=1785900364', 1178, 1557, 'A group racing on triple-screen simulators at the Tampa lounge', 'Sebring on the triple-screen rigs'),
}
def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='').write(s)
for rel, (fn, ver, w, h, alt, cap) in sorted(IMAGES.items()):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p): print('  %-46s MISSING' % rel); continue
    s = rd(p)
    if 'class="media-band"' in s: print('  %-46s already has image' % rel); continue
    if '.lp .media-band' not in s:
        if s.count(CSS_MARKER) == 1: s = s.replace(CSS_MARKER, CSS_MARKER + CSS, 1)
        else: s = s.replace('</style>', CSS + '\n</style>', 1)
    def src(width): return '%s/%s?width=%d%s' % (CDN, fn, width, ver)
    ratio_h = int(round(1200 * h / float(w)))
    fig = ('\n<section class="section media-band">\n  <figure>\n    <img src="%s" alt="%s"\n         srcset="%s 800w, %s 1200w, %s 1600w"\n         sizes="(max-width: 1100px) 100vw, 1100px"\n'
           '         width="1200" height="%d" loading="lazy" decoding="async">\n    <figcaption>%s</figcaption>\n  </figure>\n</section>\n' % (src(1200), alt, src(800), src(1200), src(1600), ratio_h, cap))
    anchor = '</header>\n'
    if s.count(anchor) != 1: print('  %-46s header anchor x%d, skipped' % (rel, s.count(anchor))); continue
    s = s.replace(anchor, anchor + fig, 1); wr(p, s); print('  %-46s + %s' % (rel, fn))
