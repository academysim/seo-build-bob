# -*- coding: utf-8 -*-
"""Codex found the tracking uneven: cross_domain_builds and booking-CTA events
were missing on several templates. Each listener is added only where that event
name is not already bound on the page, so nothing double-fires.
"""
import io, os, sys

D = sys.argv[1]
ANCHOR = "  gtag('event', 'content_view', { content_type: type, content_id: id });\n"

BUILDS = """  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'cross_domain_builds', { content_type: type, content_id: id });
    });
  });
"""

BOOKING = """  document.querySelectorAll('a[href*="booking.academysim.com"]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'booking_cta', { content_type: type, content_id: id,
        cta_location: (a.textContent || '').trim().slice(0, 40) || 'book' });
    });
  });
"""

pages = []
for root, _, files in os.walk(D):
    for f in files:
        if f == 'index.html':
            pages.append(os.path.join(root, f))
pages.sort()

for p in pages:
    rel = os.path.relpath(p, D).replace('\\', '/')
    s = io.open(p, encoding='utf-8', newline='').read()
    if ANCHOR not in s:
        print('  %-46s no tracking block' % rel)
        continue
    add = ''
    what = []
    if 'cross_domain_builds' not in s:
        add += BUILDS
        what.append('builds')
    if 'booking_cta' not in s:
        add += BOOKING
        what.append('booking_cta')
    if not add:
        print('  %-46s complete' % rel)
        continue
    s = s.replace(ANCHOR, ANCHOR + add, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s + %s' % (rel, ', '.join(what)))
