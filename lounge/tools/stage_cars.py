# -*- coding: utf-8 -*-
"""Stage /cars/ and /cars/classic-race-cars/ into lounge_deploy."""
import io, os, shutil

B = 'lounge_build'
D = 'lounge_deploy'
PAGES = ['cars/index.html', 'cars/classic-race-cars/index.html']


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


CTA = """<script>
(function(){
  function ev(name, extra){
    if (typeof gtag === 'function') gtag('event', name, extra);
  }
  document.querySelectorAll('a[href*="booking.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){
      ev('track_page_cta', { page_track: '%s', cta_location: a.textContent.trim().slice(0,40) || 'book' });
    });
  });
  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){ ev('cross_domain_builds', { page_track: '%s' }); });
  });
  document.querySelectorAll('a[href*="events.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){ ev('cross_domain_events', { page_track: '%s' }); });
  });
})();
</script>
"""

SLUG = {'cars/index.html': 'cars-hub', 'cars/classic-race-cars/index.html': 'classic-race-cars'}

for rel in PAGES:
    p = os.path.join(B, *rel.split('/'))
    s = rd(p)
    if 'track_page_cta' not in s:
        a = '\n<script type="application/ld+json">'
        assert s.count(a) == 1, 'ld anchor ' + rel
        sl = SLUG[rel]
        s = s.replace(a, '\n' + (CTA % (sl, sl, sl)) + a, 1)
        wr(p, s)
    dst = os.path.join(D, *rel.split('/'))
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copyfile(p, dst)
    print('  staged %-36s %d bytes' % (rel, os.path.getsize(dst)))

# ---- sitemap ---------------------------------------------------------------
sp = os.path.join(D, 'sitemap.xml')
sm = rd(sp)
NEW = [('https://lounge.academysim.com/cars/', '0.9'),
       ('https://lounge.academysim.com/cars/classic-race-cars/', '0.8')]
anchor = '  <url>\n    <loc>https://lounge.academysim.com/cars-and-tracks/</loc>'
assert sm.count(anchor) == 1, 'sitemap anchor'
add = ''
for loc, pri in NEW:
    if ('<loc>' + loc + '</loc>') in sm:
        continue
    add += '  <url>\n    <loc>%s</loc>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>\n' % (loc, pri)
if add:
    sm = sm.replace(anchor, add + anchor, 1)
    wr(sp, sm)
print('  sitemap urls: %d' % sm.count('<loc>'))

# ---- inbound internal links ------------------------------------------------
LINK = 'href="/cars/"'

rh = os.path.join(D, 'racing', 'index.html')
s = rd(rh)
if LINK not in s:
    a = '  <p>Want to see what is in the library? Browse <a href="/cars-and-tracks/">cars and tracks</a>.</p>'
    assert s.count(a) == 1, 'racing hub anchor'
    s = s.replace(a, '  <p>Not sure which class suits you? Compare the <a href="/cars/">car classes</a>.</p>\n' + a, 1)
    wr(rh, s)
print('  racing hub -> /cars/ : %d' % s.count(LINK))

ct = os.path.join(D, 'cars-and-tracks', 'index.html')
s = rd(ct)
if LINK not in s:
    a = '  <p class="lead">The list below is a curated selection, not the full library.'
    assert s.count(a) == 1, 'cars-and-tracks anchor'
    s = s.replace(a, '  <p>New to this? The <a href="/cars/">car class comparison</a> explains what separates them before you filter.</p>\n' + a, 1)
    wr(ct, s)
print('  cars-and-tracks -> /cars/ : %d' % s.count(LINK))
