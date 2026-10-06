# -*- coding: utf-8 -*-
"""Unpark /racing/manual-transmission-simulator-tampa/.

It was written before several site-wide fixes landed, so it needs the prose
link rule, the nav eyebrow and the tracking snippet applied to it as well as
being copied in and added to the sitemap.
"""
import io, os, shutil

B, D = 'lounge_build', 'lounge_deploy'
REL = 'racing/manual-transmission-simulator-tampa/index.html'
URL = 'https://lounge.academysim.com/racing/manual-transmission-simulator-tampa/'

rd = lambda p: io.open(p, encoding='utf-8', newline='').read()
wr = lambda p, s: io.open(p, 'w', encoding='utf-8', newline='').write(s)

src = os.path.join(B, *REL.split('/'))
s = rd(src)

# ---- CTA tracking, matching the sibling racing pages ----------------------
if 'track_page_cta' not in s:
    a = '\n<script type="application/ld+json">'
    assert s.count(a) == 1, 'ld anchor'
    sc = """<script>
(function(){
  function ev(n,e){ if (typeof gtag === 'function') gtag('event', n, e); }
  document.querySelectorAll('a[href*="booking.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){ ev('track_page_cta', { page_track: 'manual-transmission', cta_location: a.textContent.trim().slice(0,40) || 'book' }); });
  });
  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){ ev('cross_domain_builds', { page_track: 'manual-transmission' }); });
  });
})();
</script>
"""
    s = s.replace(a, '\n' + sc + a, 1)
    wr(src, s)
    print('  cta script added')

dst = os.path.join(D, *REL.split('/'))
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copyfile(src, dst)
print('  copied %d bytes' % os.path.getsize(dst))

# ---- sitemap ---------------------------------------------------------------
sp = os.path.join(D, 'sitemap.xml')
sm = rd(sp)
loc = '<loc>%s</loc>' % URL
if loc not in sm:
    anchor = '  <url>\n    <loc>https://lounge.academysim.com/racing/rally-simulator-tampa/</loc>'
    assert sm.count(anchor) == 1, 'sitemap anchor'
    block = ('  <url>\n    %s\n    <changefreq>monthly</changefreq>\n'
             '    <priority>0.8</priority>\n  </url>\n' % loc)
    sm = sm.replace(anchor, anchor.replace('  <url>\n    ', '') and (anchor + ''), 1)
    # insert AFTER the rally block, so find its closing tag
    i = sm.find(anchor)
    j = sm.find('  </url>\n', i) + len('  </url>\n')
    sm = sm[:j] + block + sm[j:]
    wr(sp, sm)
print('  sitemap urls: %d' % sm.count('<loc>'))

# ---- inbound links ---------------------------------------------------------
L = 'href="/racing/manual-transmission-simulator-tampa/"'

# racing hub: it lists the experience pages
rh = os.path.join(D, 'racing', 'index.html')
s = rd(rh)
if L not in s:
    a = '  <p>Not sure which class suits you? Compare the <a href="/cars/">car classes</a>.</p>'
    assert s.count(a) == 1, 'racing hub anchor'
    s = s.replace(a, '  <p>Want to use a real gearbox? See <a href="/racing/manual-transmission-simulator-tampa/">manual transmission sessions</a>.</p>\n' + a, 1)
    wr(rh, s)
print('  racing hub inbound: %d' % s.count(L))

# classic race cars page: the natural sibling
cc = os.path.join(D, 'cars', 'classic-race-cars', 'index.html')
s = rd(cc)
if L not in s:
    a = '  <p>Not sure this is the one? Compare it against the other <a href="/cars/">car classes</a>, or see all our <a href="/racing/">racing experiences</a>.</p>'
    assert s.count(a) == 1, 'classic anchor'
    s = s.replace(a, '  <p>Want to work specifically on gearbox technique? See <a href="/racing/manual-transmission-simulator-tampa/">manual transmission sessions</a>.</p>\n' + a, 1)
    wr(cc, s)
print('  classic page inbound: %d' % s.count(L))
