# -*- coding: utf-8 -*-
"""Section 10 of the brief wants track/car-class/experience views tracked, plus
cross-domain Events clicks. One identical snippet on every page, deriving the
content type from the path so there is nothing per-page to keep in sync.
Only adds the Events listener where one is not already present, so pages that
already have bespoke tracking do not double-fire.
"""
import io, os, sys

D = sys.argv[1]

SNIPPET_OPEN = '<!-- content + cross-domain tracking -->'

BASE = """<!-- content + cross-domain tracking -->
<script>
(function () {
  if (typeof gtag !== 'function') return;
  var p = location.pathname.replace(/\\/+$/, '/') || '/';
  var seg = p.split('/').filter(Boolean);
  var type = 'page', id = seg[seg.length - 1] || 'home';
  if (p === '/') { type = 'home'; id = 'home'; }
  else if (seg[0] === 'racing') { type = seg.length > 1 ? 'experience' : 'experience_hub'; }
  else if (seg[0] === 'tracks') { type = seg.length > 1 ? 'track' : 'track_hub'; }
  else if (seg[0] === 'cars') { type = seg.length > 1 ? 'car_class' : 'car_class_hub'; }
  else if (seg[0] === 'cars-and-tracks') { type = 'library'; }
  else if (seg[0] === 'things-to-do-in-tampa') { type = 'local'; }
  gtag('event', 'content_view', { content_type: type, content_id: id });
__EVENTS__})();
</script>
"""

EVENTS = """  document.querySelectorAll('a[href*="events.academysim.com"]').forEach(function (a) {
    a.addEventListener('click', function () {
      gtag('event', 'cross_domain_events', { content_type: type, content_id: id });
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
    if SNIPPET_OPEN in s:
        print('  %-46s already' % rel)
        continue
    anchor = '\n</body>'
    if s.count(anchor) != 1:
        print('  %-46s SKIP (body anchor x%d)' % (rel, s.count(anchor)))
        continue
    block = BASE.replace('__EVENTS__', '' if 'cross_domain_events' in s else EVENTS)
    s = s.replace(anchor, '\n' + block + anchor, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s added%s' % (rel, '' if 'cross_domain_events' in block else ' (events already tracked)'))
