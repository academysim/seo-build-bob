# -*- coding: utf-8 -*-
"""Stage /cars-and-tracks/ into lounge_deploy."""
import io, os, shutil

B = 'lounge_build'
D = 'lounge_deploy'
REL = 'cars-and-tracks/index.html'


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# ---- 1. CTA tracking script, matching the other pages ----------------------
p = os.path.join(B, *REL.split('/'))
s = rd(p)
if 'track_page_cta' not in s:
    anchor = '\n<script type="application/ld+json">'
    assert s.count(anchor) == 1, 'ld+json anchor'
    script = """<script>
(function(){
  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){
      if (typeof gtag === 'function') gtag('event','cross_domain_builds',{ page_track:'cars-and-tracks' });
    });
  });
  document.querySelectorAll('a[href*="booking.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){
      if (typeof gtag === 'function') {
        gtag('event','track_page_cta',{ page_track:'cars-and-tracks', cta_location: a.textContent.trim().slice(0,40) || 'book' });
      }
    });
  });
})();
</script>
"""
    s = s.replace(anchor, '\n' + script + anchor, 1)
    wr(p, s)
print('  cta script ok')

# ---- 2. copy ---------------------------------------------------------------
dst = os.path.join(D, *REL.split('/'))
if not os.path.isdir(os.path.dirname(dst)):
    os.makedirs(os.path.dirname(dst))
shutil.copyfile(p, dst)
print('  copied %d bytes' % os.path.getsize(dst))

# ---- 3. sitemap ------------------------------------------------------------
sp = os.path.join(D, 'sitemap.xml')
sm = rd(sp)
LOC = '<loc>https://lounge.academysim.com/cars-and-tracks/</loc>'
if LOC not in sm:
    anchor = '  <url>\n    <loc>https://lounge.academysim.com/tracks/</loc>'
    assert sm.count(anchor) == 1, 'sitemap anchor'
    sm = sm.replace(anchor, '  <url>\n    ' + LOC + '\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n' + anchor, 1)
    wr(sp, sm)
print('  sitemap urls: %d' % sm.count('<loc>'))

# ---- 4. internal links -----------------------------------------------------
LINK = 'href="/cars-and-tracks/"'

# tracks hub
th = os.path.join(D, 'tracks', 'index.html')
s = rd(th)
if LINK not in s:
    a = '  <p>More Florida and North American circuits are being added.'
    assert s.count(a) == 1, 'tracks hub anchor'
    s = s.replace(a, '  <p>Not sure what to drive? Our <a href="/cars-and-tracks/">what can I race</a> page lets you filter the library by car class, circuit and transmission.</p>\n' + a, 1)
    wr(th, s)
print('  tracks hub links: %d' % s.count(LINK))

# racing hub
rh = os.path.join(D, 'racing', 'index.html')
s = rd(rh)
if LINK not in s:
    a = '  <p>Preparing for a real track weekend? See our <a href="/tracks/">track guides</a>.</p>'
    assert s.count(a) == 1, 'racing hub anchor'
    s = s.replace(a, a + '\n  <p>Want to see what is in the library? Browse <a href="/cars-and-tracks/">cars and tracks</a>.</p>', 1)
    wr(rh, s)
print('  racing hub links: %d' % s.count(LINK))
