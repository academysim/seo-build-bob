# -*- coding: utf-8 -*-
"""Stage the /tracks/ hub and /tracks/daytona/ into lounge_deploy."""
import io, os, shutil, re

B = 'lounge_build'
D = 'lounge_deploy'


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


CTA_SCRIPT = """
<script>
(function(){
  function track(label){
    if (typeof gtag === 'function') {
      gtag('event', 'track_page_cta', { page_track: '%s', cta_location: label });
    }
  }
  document.querySelectorAll('a[href*="booking.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){ track(a.textContent.trim().slice(0,40) || 'book'); });
  });
  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function(a){
    a.addEventListener('click', function(){
      if (typeof gtag === 'function') gtag('event','cross_domain_builds',{ page_track:'%s' });
    });
  });
})();
</script>
"""

# ---- 1. add the CTA tracking script the Sebring page already carries -------
for rel, slug in [('tracks/index.html', 'tracks-hub'),
                  ('tracks/daytona/index.html', 'daytona')]:
    p = os.path.join(B, *rel.split('/'))
    s = rd(p)
    if 'track_page_cta' not in s:
        anchor = '\n</body>\n</html>'
        assert s.count(anchor) == 1, 'body anchor in ' + rel
        s = s.replace(anchor, '\n' + (CTA_SCRIPT % (slug, slug)).strip() + anchor, 1)
        wr(p, s)
    print('  cta script  %-28s ok' % rel)

# ---- 2. copy into the deploy tree ------------------------------------------
for rel in ['tracks/index.html', 'tracks/daytona/index.html']:
    src = os.path.join(B, *rel.split('/'))
    dst = os.path.join(D, *rel.split('/'))
    d = os.path.dirname(dst)
    if not os.path.isdir(d):
        os.makedirs(d)
    shutil.copyfile(src, dst)
    print('  copied      %-28s %d bytes' % (rel, os.path.getsize(dst)))

# ---- 3. sitemap -------------------------------------------------------------
sp = os.path.join(D, 'sitemap.xml')
sm = rd(sp)
NEW = [('https://lounge.academysim.com/tracks/', '0.9'),
       ('https://lounge.academysim.com/tracks/daytona/', '0.9')]
anchor = '  <url>\n    <loc>https://lounge.academysim.com/tracks/sebring/</loc>'
assert sm.count(anchor) == 1, 'sitemap anchor'
add = ''
for loc, pri in NEW:
    if loc in sm:
        continue
    add += '  <url>\n    <loc>%s</loc>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>\n' % (loc, pri)
sm = sm.replace(anchor, add + anchor, 1)
wr(sp, sm)
print('  sitemap urls: %d' % sm.count('<loc>'))

# ---- 4. internal links so the hub is not orphaned ---------------------------
sb = os.path.join(D, 'tracks', 'sebring', 'index.html')
s = rd(sb)
link_p = '  <p>More circuits? See our <a href="/tracks/">track guides</a>, including the <a href="/tracks/daytona/">Daytona guide</a>.</p>\n\n'
note_anchor = '  <p class="note">Simulator practice is preparation, not a substitute'
if 'href="/tracks/"' not in s:
    assert s.count(note_anchor) == 1, 'sebring note anchor'
    s = s.replace(note_anchor, link_p + note_anchor, 1)
    wr(sb, s)
print('  sebring links to hub: %d' % s.count('href="/tracks/"'))

rh = os.path.join(D, 'racing', 'index.html')
s = rd(rh)
ev = '  <p>Need simulators brought to a corporate day, party or team event? See <a href="https://events.academysim.com">Academy Events</a>.</p>'
if 'href="/tracks/"' not in s:
    assert s.count(ev) == 1, 'racing hub events anchor'
    s = s.replace(ev, '  <p>Preparing for a real track weekend? See our <a href="/tracks/">track guides</a>.</p>\n' + ev, 1)
    wr(rh, s)
print('  racing hub links to hub: %d' % s.count('href="/tracks/"'))
