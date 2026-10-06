# -*- coding: utf-8 -*-
"""Page template for new health.academysim.com pages.

Governing rules from the brief:
  * No medical claims. Academy is not a medical provider.
  * Do not guarantee cognitive, neurological, rehabilitation or health outcomes.
  * Where rehabilitation is mentioned, position Academy as complementary to
    professional care, never a replacement.
  * No fake case studies, testimonials, medical results or facility partnerships.

So these pages describe format, setup, staffing, accessibility and logistics.
They do not describe benefits to health. `health_audit.py` fails the build on
outcome verbs applied to health nouns.
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'health_build')
OUT = os.path.join(HERE, 'health_new')

SITE = 'https://health.academysim.com'
LOUNGE = 'https://lounge.academysim.com'
EVENTS = 'https://events.academysim.com'


def part(n):
    return io.open(os.path.join(B, n), encoding='utf-8', newline='').read().strip()


STYLE = part('_style.css')
NAV = part('_nav.html')
FOOTER = part('_footer.html')
GA = part('_ga.html')

# The site's own scope note, reused verbatim so the message stays consistent.
SCOPE = (
    '  <div class="disclaimer"><p>A note on scope: Academy Sim Racing provides simulator experiences and '
    'structured programs. <strong>We are not a medical provider and we do not offer therapy, treatment or '
    'clinical assessment.</strong> Where a program runs alongside rehabilitation or clinical care, it is '
    'complementary to that care and designed with your facility&rsquo;s qualified staff, never a substitute '
    'for it. We make no claims about health, cognitive or physical outcomes.</p></div>')

EXTRA_CSS = """
.crumbs{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:#8a8a8a;padding:16px 0 0;}
.crumbs a{color:#8a8a8a;text-decoration:none;}
.crumbs a:hover{color:#fbbf24;}
.prose{max-width:720px;}
.prose p{margin:0 0 14px;line-height:1.7;}
.prose h3{font-family:'Bebas Neue',sans-serif;letter-spacing:.02em;font-size:22px;margin:26px 0 8px;}
.prose ul{margin:0 0 16px;padding-left:20px;line-height:1.75;}
.prose a:link,.prose a:visited{color:#fbbf24;text-decoration:underline;text-underline-offset:2px;}
.linkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:20px;}
.linkcard{display:block;border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:18px;
  text-decoration:none;transition:transform .15s,border-color .15s;}
.linkcard:hover{transform:translateY(-2px);border-color:#fbbf24;}
.lc-name{font-family:'Bebas Neue',sans-serif;font-size:19px;letter-spacing:.02em;margin-bottom:5px;}
.lc-desc{font-size:13px;color:#a9a9a9;line-height:1.55;}
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
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{style}
{extra}
</style>
</head>
<body>
<div class="lp">

{nav}

<div class="section" style="padding-top:0;padding-bottom:0;"><div class="crumbs">{crumbs}</div></div>

<header class="hero" style="min-height:auto;">
  <div class="hero-glow"></div>
  <div class="eyebrow">{eyebrow}</div>
  <h1 class="h1">{h1}</h1>
  <p class="hero-sub">{lede}</p>
  <div class="hero-ctas">
    <a class="btn-amber" href="{site}/?ref={slug}#contact">{cta1}</a>
    <a class="btn-ghost" href="tel:+18133559071">Call (813) 355-9071</a>
  </div>
</header>

{body}

<section class="final">
  <h2>{final_h}</h2>
  <p>{final_p}</p>
  <div class="final-ctas">
    <a class="btn-amber" href="{site}/?ref={slug}#contact">{cta1}</a>
    <a class="btn-ghost" href="tel:+18133559071">Call (813) 355-9071</a>
  </div>
</section>

{footer}
</div>

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
  bind('a[href*="#contact"]', 'program_inquiry');
  bind('a[href^="tel:"]', 'phone_click');
  bind('a[href*="events.academysim.com"]', 'cross_domain_events');
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
    d.setdefault('cta1', 'Plan a Program')
    return PAGE.format(GA=GA, site=SITE, style=STYLE, extra=EXTRA_CSS,
                       nav=NAV.replace('href="#contact"', 'href="%s/?ref=%s#contact"' % (SITE, d['slug'])),
                       footer=FOOTER, **d)


def write(p):
    html = render(p)
    rel = p['url'].strip('/')
    d = os.path.join(OUT, *rel.split('/')) if rel else OUT
    if not os.path.isdir(d):
        os.makedirs(d)
    path = os.path.join(d, 'index.html')
    io.open(path, 'w', encoding='utf-8', newline='').write(html)
    return path, len(html.encode())


def sec(eyebrow, h2, intro, inner):
    out = ['<section class="section">', '  <div class="section-head">',
           '    <div class="eyebrow">%s</div>' % eyebrow, '    <h2 class="h2">%s</h2>' % h2]
    if intro:
        out.append('    <p class="section-intro">%s</p>' % intro)
    out.append('  </div>')
    out.append(inner)
    out.append('</section>')
    return '\n'.join(out)


def prose(eyebrow, h2, intro, blocks):
    return sec(eyebrow, h2, intro, '  <div class="prose">\n' + '\n'.join('    ' + b for b in blocks) + '\n  </div>')


def cards(eyebrow, h2, intro, items):
    inner = ['  <div class="types-grid">']
    for i, (name, desc) in enumerate(items, 1):
        inner.append('    <div class="type-card">')
        inner.append('      <div class="type-num">%02d</div>' % i)
        inner.append('      <div class="type-name">%s</div>' % name)
        inner.append('      <div class="type-desc">%s</div>' % desc)
        inner.append('    </div>')
    inner.append('  </div>')
    return sec(eyebrow, h2, intro, '\n'.join(inner))


def faq(items, eyebrow='Questions', h2='WHAT ACTIVITY DIRECTORS ASK'):
    inner = ['  <div class="faq-list">']
    for q, a in items:
        inner.append('    <div class="faq-item">')
        inner.append('      <div class="faq-q">%s</div>' % q)
        inner.append('      <div class="faq-a"><div class="faq-a-inner">%s</div></div>' % a)
        inner.append('    </div>')
    inner.append('  </div>')
    return sec(eyebrow, h2, '', '\n'.join(inner))


def linkgrid(eyebrow, h2, intro, links):
    inner = ['  <div class="linkgrid">']
    for href, name, desc in links:
        inner.append('    <a class="linkcard" href="%s">' % href)
        inner.append('      <div class="lc-name">%s</div>' % name)
        inner.append('      <div class="lc-desc">%s</div>' % desc)
        inner.append('    </a>')
    inner.append('  </div>')
    return sec(eyebrow, h2, intro, '\n'.join(inner))


ACCESS = [
    '<h3>Accessibility is the first conversation, not the last</h3>',
    '<p>The single most useful thing you can tell us in advance is who is taking part. A simulator seat is '
    'a fixed racing seat, and getting into one is not possible or comfortable for every resident.</p>',
    '<ul>'
    '<li><strong>Wheelchair users.</strong> Tell us in advance. There are setups that work without '
    'transferring out of a chair, and setups that do not, and we would rather solve that before we arrive.</li>'
    '<li><strong>Limited mobility or transfers.</strong> If a resident needs assistance to transfer, your '
    'staff should handle that. Our team runs the simulators and does not provide personal care.</li>'
    '<li><strong>Hand and grip strength.</strong> Wheel force can be reduced substantially, and for some '
    'participants turned down to almost nothing.</li>'
    '<li><strong>Vision and hearing.</strong> Screen distance, text size and volume are all adjustable.</li>'
    '<li><strong>Motion sensitivity.</strong> Some people find any moving screen uncomfortable. Sessions '
    'can be kept short and stationary, and nobody should feel obliged to continue.</li>'
    '</ul>',
    '<p>Tell us the range of needs in the room and we will tell you honestly what will work and what will '
    'not, rather than discovering it in front of your residents.</p>',
]

CROSS = linkgrid('Elsewhere at Academy', 'OTHER ACADEMY SERVICES', '', [
    (EVENTS, 'CORPORATE AND PUBLIC EVENTS',
     'Academy Events runs staffed simulator rentals for corporate and public events across Florida.'),
    (LOUNGE, 'THE TAMPA LOUNGE',
     'Eight simulators at 1421 Massaro Blvd, for families and visitors who want to drive.'),
])


def ld(kind, name, desc, url):
    return """{
  "@context": "https://schema.org",
  "@type": "%s",
  "name": "%s",
  "description": "%s",
  "url": "%s%s",
  "isPartOf": { "@type": "WebSite", "name": "Academy Sim Racing for Seniors", "url": "%s/" },
  "provider": {
    "@type": "Organization",
    "name": "Academy Sim Racing",
    "telephone": "+1-813-355-9071",
    "areaServed": { "@type": "State", "name": "Florida" },
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
