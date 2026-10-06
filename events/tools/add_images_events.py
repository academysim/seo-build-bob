# -*- coding: utf-8 -*-
"""Give every inner events page a photo band under its page-hero (2026-09-03).
Uses the nine event photos already deployed at /images/ (all real event shots), absolute paths."""
import io, os, sys
D = sys.argv[1]
CSS = ('\n.lp .media-band{padding:28px 24px 0;}'
       '\n.lp .media-band figure{margin:0 auto;max-width:1100px;}'
       '\n.lp .media-band img{display:block;width:100%;height:auto;max-height:520px;object-fit:cover;border-radius:10px;box-shadow:0 14px 40px rgba(26,23,20,.14);}'
       '\n.lp .media-band figcaption{font-family:\'IBM Plex Mono\',monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#7a6f63;margin-top:10px;}')
P = {
 'event-types/index.html': ('rockway-hero.jpg', 'A branded Academy Sim Racing simulator activation at a trade show', 'A branded activation on the show floor'),
 'event-types/corporate-events/index.html': ('pwc-event.jpg', 'Employees racing on simulators at a corporate event', 'A corporate event on the simulators'),
 'event-types/brand-activations/index.html': ('rockway-hero.jpg', 'A fully branded simulator activation at an exhibit booth', 'A fully branded booth activation'),
 'event-types/car-dealership-events/index.html': ('porsche-holiday.jpg', 'A racing simulator at a Porsche dealership holiday event', 'Dealership event, Porsche'),
 'event-types/client-entertainment/index.html': ('ferrari-crowd.jpg', 'A crowd gathered around a simulator at a Ferrari event', 'A crowd at a Ferrari client event'),
 'event-types/conventions/index.html': ('rockway-gallery.jpg', 'Attendees around a simulator at a convention booth', 'On the convention floor'),
 'event-types/employee-appreciation/index.html': ('staff-coaching.jpg', 'An Academy staff member coaching a guest on a simulator', 'Staffed and coached, every seat'),
 'event-types/fundraisers/index.html': ('rooftop-rigs.jpg', 'Racing simulators set up at a rooftop event', 'Simulators at a rooftop event'),
 'event-types/private-parties/index.html': ('triple-screen.jpg', 'A guest on a triple-screen racing simulator', 'The triple-screen rig at a private party'),
 'event-types/trade-shows/index.html': ('leaderboard.jpg', 'A live leaderboard next to a simulator at a trade show', 'The live leaderboard draws the crowd'),
 'event-types/watch-parties/index.html': ('ferrari-crowd.jpg', 'A crowd watching and racing at a motorsport event', 'Race weekend crowd'),
 'experiences/index.html': ('triple-screen.jpg', 'A guest driving a triple-screen racing simulator', 'The triple-screen experience'),
 'experiences/drift-racing-simulator/index.html': ('triple-screen.jpg', 'A guest on a triple-screen racing simulator', 'Drift on the triple-screen rig'),
 'experiences/formula-racing-simulator/index.html': ('leaderboard.jpg', 'A live lap-time leaderboard at an event', 'Fastest lap wins'),
 'experiences/gt3-racing-simulator/index.html': ('pwc-event.jpg', 'Guests racing on simulators at a corporate event', 'GT3 racing at a corporate event'),
 'experiences/imsa-endurance-racing/index.html': ('rooftop-rigs.jpg', 'Racing simulators at an outdoor rooftop event', 'Endurance stints, rooftop event'),
 'experiences/nascar-racing-simulator/index.html': ('porsche-holiday.jpg', 'A racing simulator at a dealership event', 'Oval racing at a dealership event'),
 'experiences/rally-racing-simulator/index.html': ('staff-coaching.jpg', 'A staff member coaching a guest on a simulator', 'Coached rally stages'),
 'locations/index.html': ('rockway-gallery.jpg', 'Attendees around a simulator at a Florida convention', 'Delivered anywhere in Florida'),
 'locations/daytona-beach/index.html': ('rooftop-rigs.jpg', 'Racing simulators set up at an outdoor Florida event', 'Simulators at a Florida event'),
 'locations/orlando/index.html': ('ferrari-crowd.jpg', 'A crowd around a simulator at an Orlando-area event', 'Crowds at an Orlando event'),
 'locations/sarasota/index.html': ('porsche-holiday.jpg', 'A racing simulator at a dealership event', 'A dealership event on the Gulf coast'),
 'locations/tampa/index.html': ('pwc-event.jpg', 'Employees racing on simulators at a Tampa corporate event', 'A Tampa corporate event'),
}
def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='').write(s)
for rel, (fn, alt, cap) in sorted(P.items()):
    p = os.path.join(D, *rel.split('/'))
    if not os.path.isfile(p): print('  %-50s MISSING' % rel); continue
    s = rd(p)
    if 'class="section media-band"' in s: print('  %-50s already' % rel); continue
    if '.lp .media-band' not in s: s = s.replace('</style>', CSS + '\n</style>', 1)
    fig = ('\n<section class="section media-band">\n  <figure>\n    <img src="/images/%s" alt="%s" width="1100" height="520" loading="lazy" decoding="async">\n'
           '    <figcaption>%s</figcaption>\n  </figure>\n</section>\n' % (fn, alt, cap))
    i = s.find('<section class="page-hero">')
    if i < 0: print('  %-50s no page-hero, skipped' % rel); continue
    j = s.find('</section>', i) + len('</section>')
    s = s[:j] + fig + s[j:]
    wr(p, s); print('  %-50s + %s' % (rel, fn))
