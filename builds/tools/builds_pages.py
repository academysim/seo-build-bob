# -*- coding: utf-8 -*-
"""Page template for new builds.academysim.com pages.

Constraints:
  * The brief: these are configuration and use-case pages, NOT new products.
    Route people into the five real builds. Do not invent equipment.
  * The site's nav uses on-page anchors (#tiers, #start). Those do not exist on
    a subpage, so they are rewritten to absolute homepage anchors carrying ?ref.
  * The quote form is a single Netlify form (build-request) on the homepage.
    Netlify serves index.html 49 bytes smaller than it stores it, so that file
    must never be redeployed from a fetched copy. New pages link to /#start.
  * American spelling throughout, matching the rest of the site.
"""
import io, os

import builds_prices as P

HERE = os.path.dirname(os.path.abspath(__file__))
# The shared partials. These used to be read from a 'builds_build' scratch
# copy that was never committed, so a fresh checkout could not run the
# generator at all - it died on a missing _style.css. Read the tracked
# template directly instead.
B = os.path.normpath(os.path.join(HERE, '..', 'template'))
OUT = os.path.join(HERE, 'builds_new')

SITE = 'https://builds.academysim.com'
LOUNGE = 'https://lounge.academysim.com'
EVENTS = 'https://events.academysim.com'


def part(n):
    return io.open(os.path.join(B, n), encoding='utf-8', newline='').read().strip()


STYLE = part('_style.css')
NAV = part('_nav.html')
FOOTER = part('_footer.html')
GA = part('_ga.html')

# ---- the five real builds, exactly as published on the homepage -----------
# Prices are NOT typed here. They come from builds_prices, which is the single
# source for every published number; specs stay here because they are not
# price data. See builds_prices.py for why this split exists.
SPECS = {
    'rookie':        ('34" curved WQHD 165Hz', '8Nm direct drive', 'Load cell', 'None'),
    'base':          ('49" curved 144Hz', '15Nm direct drive', 'Load cell', 'Buttkicker'),
    'club-oled':     ('49" QD-OLED 240Hz', '25Nm, DD2 or Simucube 3', 'Simucube Active', 'Buttkicker'),
    'club-triple':   ('3 x 32" curved 165Hz', '25Nm, DD2 or Simucube 3', 'Simucube Active', 'Buttkicker'),
    'pole-position': ('Triple OLED', '25Nm, DD2 or Simucube 3', 'Simucube Active', 'Buttkicker and D-BOX motion'),
}

BUILDS = dict(
    (slug, (P.NAME[slug], P.tier_price(slug)) + SPECS[slug])
    for slug, _, _ in P.TIERS
)


def nav_for(slug):
    n = NAV
    for anchor in ('#tiers', '#test-drive', '#reviews', '#personalize', '#install', '#faq', '#start'):
        n = n.replace('href="%s"' % anchor, 'href="%s/?ref=%s%s"' % (SITE, slug, anchor))
    return n


def build_table(keys, note=''):
    """Comparison table of the real builds relevant to a page."""
    rows = []
    for k in keys:
        name, price, disp, wb, ped, hap = BUILDS[k]
        rows.append(
            '        <tr>\n'
            '          <td class="c-name">%s</td>\n'
            '          <td class="c-price">%s</td>\n'
            '          <td>%s</td>\n'
            '          <td>%s</td>\n'
            '          <td>%s</td>\n'
            '          <td>%s</td>\n'
            '        </tr>' % (name, price, disp, wb, ped, hap))
    return (
        '  <div class="compare-wrap">\n'
        '    <table class="compare">\n'
        '      <thead>\n'
        '        <tr><th>Build</th><th>Price</th><th>Display</th><th>Wheelbase</th>'
        '<th>Pedals</th><th>Haptics &amp; Motion</th></tr>\n'
        '      </thead>\n'
        '      <tbody>\n' + '\n'.join(rows) + '\n'
        '      </tbody>\n'
        '    </table>\n'
        '  </div>\n'
        + ('  <p class="form-note">%s</p>\n' % note if note else ''))


EXTRA_CSS = """
/* additions for the new pages, built from the existing token set */
.crumbs { font-family:'IBM Plex Mono',monospace; font-size:0.7rem; letter-spacing:0.16em;
  text-transform:uppercase; color:var(--muted); padding:1.25rem 0 0; }
.crumbs a { color:var(--muted); text-decoration:none; }
.crumbs a:hover { color:var(--gold); }
.prose { max-width:720px; }
.prose p { margin:0 0 1rem; line-height:1.7; }
.prose h3 { font-family:'Bebas Neue',sans-serif; letter-spacing:0.02em; font-size:1.4rem;
  margin:2rem 0 0.6rem; }
.prose ul { margin:0 0 1.1rem; padding-left:1.25rem; line-height:1.75; }
.prose a:link, .prose a:visited { color:var(--gold); text-decoration:underline; text-underline-offset:2px; }
.prose a:hover { color:var(--ink); }
.callout { border:1px solid var(--border); border-radius:12px; padding:1.15rem 1.25rem;
  margin:1.5rem 0; max-width:720px; }
.callout p { margin:0; font-size:0.92rem; color:var(--muted); }
.linkgrid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:1rem; margin-top:1.5rem; }
.linkcard { display:block; border:1px solid var(--border); border-radius:12px; padding:1.15rem;
  text-decoration:none; transition:transform .15s, border-color .15s; }
.linkcard:hover { transform:translateY(-2px); border-color:var(--gold); }
.lc-name { font-family:'Bebas Neue',sans-serif; font-size:1.15rem; letter-spacing:0.02em; margin-bottom:.3rem; }
.lc-desc { font-size:0.86rem; color:var(--muted); line-height:1.5; }
.pagefig { margin:0 0 1.5rem; }
.pagefig img { display:block; max-width:100%; max-height:560px; width:auto; height:auto; margin:0 auto; border-radius:12px; border:1px solid var(--border); }
.pagefig { text-align:center; }
.pagefig figcaption { font-family:'IBM Plex Mono',monospace; font-size:0.68rem; letter-spacing:0.14em;
  text-transform:uppercase; color:var(--muted); margin-top:.55rem; }
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{GA}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{site}{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/images/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/images/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Rajdhani:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
{style}
{extra}
</style>
</head>
<body>

{nav}

<div class="container"><div class="crumbs">{crumbs}</div></div>

<header class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">
      <span class="dot"></span>
      <span class="eyebrow">{eyebrow}</span>
    </div>
    <h1>{h1}</h1>
    <p class="hero-lead">{lede}</p>
    <div class="hero-meta">
      <span>From {entry}</span>
      <span class="hero-meta-divider"></span>
      <span>2&ndash;4 Week Build Time</span>
      <span class="hero-meta-divider"></span>
      <span>Nationwide Shipping</span>
    </div>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="{site}/?ref={slug}#start">Start Your Build</a>
      <a class="btn btn-secondary" href="{lounge}">Drive One First</a>
    </div>
  </div>
</header>

{body}

<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Next Step</span>
      <h2>{final_h}</h2>
      <p>{final_p}</p>
    </div>
    <div class="hero-ctas" style="justify-content:center;">
      <a class="btn btn-primary" href="{site}/?ref={slug}#start">Start Your Build</a>
      <a class="btn btn-secondary" href="{lounge}">Book a Lounge Session</a>
    </div>
  </div>
</section>

{footer}

<script>
(function () {{
  if (typeof gtag !== 'function') return;
  gtag('event', 'content_view', {{ content_type: '{ctype}', content_id: '{slug}' }});
  function bind(sel, name) {{
    document.querySelectorAll(sel).forEach(function (a) {{
      a.addEventListener('click', function () {{
        gtag('event', name, {{ content_type: '{ctype}', content_id: '{slug}',
          cta_location: (a.textContent || '').trim().slice(0, 40) }});
      }});
    }});
  }}
  bind('a[href*="#start"]', 'build_cta');
  bind('a[href*="lounge.academysim.com"]', 'cross_domain_lounge');
  bind('a[href*="events.academysim.com"]', 'cross_domain_events');
  bind('a[href^="tel:"]', 'phone_click');
}})();
</script>

<script type="application/ld+json">
{ld}
</script>

</body>
</html>
"""


def render(p):
    d = dict(p)
    return PAGE.format(GA=GA, site=SITE, lounge=LOUNGE, style=STYLE, extra=EXTRA_CSS,
                       entry=P.ENTRY,
                       nav=nav_for(d['slug']), footer=FOOTER, **d)


def write(p):
    html = render(p)
    rel = p['url'].strip('/')
    d = os.path.join(OUT, *rel.split('/')) if rel else OUT
    if not os.path.isdir(d):
        os.makedirs(d)
    path = os.path.join(d, 'index.html')
    io.open(path, 'w', encoding='utf-8', newline='').write(html)
    return path, len(html.encode())


def section(eyebrow, h2, intro, inner):
    out = ['<section class="section">', '  <div class="container">', '    <div class="section-header">',
           '      <span class="eyebrow">%s</span>' % eyebrow, '      <h2>%s</h2>' % h2]
    if intro:
        out.append('      <p>%s</p>' % intro)
    out.append('    </div>')
    out.append(inner)
    out += ['  </div>', '</section>']
    return '\n'.join(out)


def prose(eyebrow, h2, intro, blocks):
    return section(eyebrow, h2, intro,
                   '    <div class="prose">\n' + '\n'.join('      ' + b for b in blocks) + '\n    </div>')


def faq(items, eyebrow='Frequently Asked', h2='Real <span class="accent">answers.</span>', intro=''):
    inner = ['    <div class="faq-list">']
    for q, a in items:
        inner.append('      <div class="faq-item">')
        inner.append('        <div class="faq-q">%s</div>' % q)
        inner.append('        <div class="faq-a">%s</div>' % a)
        inner.append('      </div>')
    inner.append('    </div>')
    return section(eyebrow, h2, intro, '\n'.join(inner))


def linkgrid(eyebrow, h2, intro, links):
    inner = ['    <div class="linkgrid">']
    for href, name, desc in links:
        inner.append('      <a class="linkcard" href="%s">' % href)
        inner.append('        <div class="lc-name">%s</div>' % name)
        inner.append('        <div class="lc-desc">%s</div>' % desc)
        inner.append('      </a>')
    inner.append('    </div>')
    return section(eyebrow, h2, intro, '\n'.join(inner))


def figure(img, alt, cap):
    return ('  <figure class="pagefig">\n'
            '    <img src="/images/%s" alt="%s" loading="lazy" decoding="async">\n'
            '    <figcaption>%s</figcaption>\n'
            '  </figure>' % (img, alt, cap))


CROSS = linkgrid('Elsewhere at Academy', 'Try before <span class="accent">you buy.</span>',
                 'Every build on this site is a rig we run daily in the Tampa lounge.', [
                     (LOUNGE, 'DRIVE ONE IN TAMPA',
                      'Book a session and drive the components before you commit to them.'),
                     (EVENTS, 'NEED ONE FOR AN EVENT?',
                      'Academy Events delivers staffed simulator rentals across Florida.'),
                 ])


def ld(kind, name, desc, url):
    return """{
  "@context": "https://schema.org",
  "@type": "%s",
  "name": "%s",
  "description": "%s",
  "url": "%s%s",
  "isPartOf": { "@type": "WebSite", "name": "Academy Sim Racing Builds", "url": "%s/" },
  "provider": {
    "@type": "Organization",
    "name": "Academy Sim Racing",
    "telephone": "+1-813-355-9071",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1421 Massaro Blvd",
      "addressLocality": "Tampa",
      "addressRegion": "FL",
      "postalCode": "33619",
      "addressCountry": "US"
    }
  }
}""" % (kind, name, desc, SITE, url, SITE)
