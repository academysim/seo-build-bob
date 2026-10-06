# -*- coding: utf-8 -*-
"""Page template for new driver.academysim.com pages.

The overriding rule on this property, from the brief and from memory:
ACADEMY HAS NO SIMULATORS INSTALLED IN ANY SCHOOL. Nothing here may imply
otherwise. Allowed phrasing is future-facing: "Academy offers", "can provide",
"can deploy", "districts can evaluate", "available for qualifying programs".
`driver_audit.py` fails the build on the forbidden phrasings.

This site uses external CSS at /assets/css/site.css, so pages link it rather
than inlining, and inherit design changes automatically.
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'driver_build')
OUT = os.path.join(HERE, 'driver_new')

SITE = 'https://driver.academysim.com'
BOOK = 'https://booking.academysim.com/?category=lessons_de'


def part(n):
    return io.open(os.path.join(B, n), encoding='utf-8', newline='').read().strip()


HEADER = part('_header.html')
FOOTER = part('_footer.html')
MCTA = part('_mcta.html')
GA = part('_ga.html')

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
<meta property="og:image" content="{site}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/og-image.jpg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body class="has-mcta">
<div class="wrap">

{header}

<div class="crumb"><div class="crumb-in">{crumbs}</div></div>

<section class="hero">
  <div class="hero-in">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lead">{lede}</p>
    <div class="hero-ctas">
      <a class="btn btn-y" href="/contact">{cta1}</a>
      <a class="btn btn-n" href="tel:+18133559071">Call (813) 355-9071</a>
    </div>
  </div>
</section>

{body}

<section class="final">
  <div class="sec-in">
    <h2>{final_h}</h2>
    <p>{final_p}</p>
    <div class="final-ctas">
      <a class="btn btn-y" href="/contact">{cta1}</a>
      <a class="btn btn-n" href="tel:+18133559071">Call (813) 355-9071</a>
    </div>
  </div>
</section>

{footer}
</div>
{mcta}
<script src="/assets/js/site.js"></script>

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
  bind('a[href="/contact"]', 'district_inquiry');
  bind('a[href^="tel:"]', 'phone_click');
  bind('a[href*="booking.academysim.com"]', 'booking_cta');
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
    d.setdefault('cta1', 'Request Program Information')
    return PAGE.format(GA=GA, site=SITE, header=HEADER, footer=FOOTER, mcta=MCTA, **d)


def write(p):
    html = render(p)
    rel = p['url'].strip('/')
    d = os.path.join(OUT, *rel.split('/')) if rel else OUT
    if not os.path.isdir(d):
        os.makedirs(d)
    path = os.path.join(d, 'index.html')
    io.open(path, 'w', encoding='utf-8', newline='').write(html)
    return path, len(html.encode())


def sec(eyebrow, h2, intro, inner, cls='sec'):
    out = ['<section class="%s">' % cls, '  <div class="sec-in">', '    <div class="sec-head">',
           '      <div class="eyebrow">%s</div>' % eyebrow, '      <h2>%s</h2>' % h2]
    if intro:
        out.append('      <p class="lead">%s</p>' % intro)
    out.append('    </div>')
    out.append(inner)
    out += ['  </div>', '</section>']
    return '\n'.join(out)


def prose(eyebrow, h2, intro, blocks):
    return sec(eyebrow, h2, intro, '\n'.join('    ' + b for b in blocks))


def cards(eyebrow, h2, intro, items, grid='g3'):
    inner = ['    <div class="%s">' % grid]
    for i, (name, desc) in enumerate(items, 1):
        inner.append('      <div class="card">')
        inner.append('        <div class="card-num">%02d</div>' % i)
        inner.append('        <h3>%s</h3>' % name)
        inner.append('        <p>%s</p>' % desc)
        inner.append('      </div>')
    inner.append('    </div>')
    return sec(eyebrow, h2, intro, '\n'.join(inner))


def faq(items, eyebrow='Questions', h2='What districts ask'):
    inner = ['    <div class="faq">']
    for q, a in items:
        inner.append('      <div class="faq-i">')
        inner.append('        <div class="faq-q">%s</div>' % q)
        inner.append('        <div class="faq-a"><div class="faq-a-in">%s</div></div>' % a)
        inner.append('      </div>')
    inner.append('    </div>')
    return sec(eyebrow, h2, '', '\n'.join(inner))


def linkgrid(eyebrow, h2, intro, links, grid='g3'):
    inner = ['    <div class="%s">' % grid]
    for href, name, desc in links:
        inner.append('      <a class="card" href="%s">' % href)
        inner.append('        <h3>%s</h3>' % name)
        inner.append('        <p>%s</p>' % desc)
        inner.append('      </a>')
    inner.append('    </div>')
    return sec(eyebrow, h2, intro, '\n'.join(inner))


# The disclosure that must appear on every institutional page.
NO_INSTALLS = (
    '  <div class="note"><p><strong>Please note:</strong> Academy Sim Racing does not currently have '
    'simulators installed in Florida school districts. The programs described here are services Academy '
    'offers and can deploy. Any reference to a district on this site describes an area we can serve, not '
    'an existing installation or partnership.</p></div>')


def ld(kind, name, desc, url):
    return """{
  "@context": "https://schema.org",
  "@type": "%s",
  "name": "%s",
  "description": "%s",
  "url": "%s%s",
  "isPartOf": { "@type": "WebSite", "name": "Academy Driver's Ed", "url": "%s/" },
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
