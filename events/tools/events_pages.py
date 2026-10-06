# -*- coding: utf-8 -*-
"""Build new pages for events.academysim.com in the existing site's own template.

Constraints that shaped this:
  * The site uses <body> + <div class="lp">. `.lp` sets overflow:hidden, which
    is fine on a div but would kill viewport scrolling if put on <body>.
    Do not move that class. (Learned the hard way on the lounge.)
  * The quote flow is two Netlify Forms on the homepage. Codex was clear: link
    to /#quote rather than duplicating a tested form across ~30 pages. Context
    rides along as ?ref=<slug> so GA4 can attribute the lead.
  * No em dashes, no AI-tell phrasing, no invented clients, venues, prices or
    travel times. Only claims already public on the events homepage are reused.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'events_build')
OUT = os.path.join(HERE, 'events_new')

SITE = 'https://events.academysim.com'


def part(name):
    return io.open(os.path.join(B, name), encoding='utf-8', newline='').read().strip()


STYLE = part('_style.css')
NAV = part('_nav.html')
FOOTER = part('_footer.html')
GA = part('_ga.html')

# Subpage nav: the homepage CTA is an on-page #quote anchor, which does not
# exist here. Point it at the homepage anchor and carry the source.
def nav_for(slug):
    return NAV.replace('href="#quote"', 'href="%s/?ref=%s#quote"' % (SITE, slug))


HEAD_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=3">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#FAF7F2">"""

EXTRA_CSS = """
/* new-page helpers, built from the existing token set */
.lp .page-hero{background:linear-gradient(160deg,#FFF9F0 0%,#FAF1E4 45%,#F3EEE6 100%);padding:72px 24px 56px;border-bottom:1px solid var(--line-soft);}
.lp .page-hero .eyebrow{margin-bottom:10px;}
.lp .page-hero h1{margin:0 0 14px;}
.lp .page-hero p{color:var(--ink-soft);max-width:660px;margin:0 0 22px;font-size:15px;}
.lp .crumbs{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-faint);padding:16px 24px 0;}
.lp .crumbs a{color:var(--ink-faint);text-decoration:none;}
.lp .crumbs a:hover{color:var(--gold);}
.lp .prose{max-width:720px;}
.lp .prose p{color:var(--ink-soft);margin:0 0 14px;font-size:14.5px;line-height:1.65;}
.lp .prose h3{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.02em;margin:26px 0 8px;color:var(--ink);}
.lp .prose ul{margin:0 0 16px;padding-left:20px;color:var(--ink-soft);font-size:14.5px;line-height:1.7;}
.lp .prose a:link,.lp .prose a:visited{color:var(--gold);text-decoration:underline;text-underline-offset:2px;}
.lp .prose a:hover{color:var(--ink);}
.lp .note-band{background:var(--bg-tint);border:1px solid var(--line-soft);border-radius:12px;padding:18px 20px;margin:24px 0;max-width:720px;}
.lp .note-band p{margin:0;font-size:13px;color:var(--ink-soft);}
.lp .linkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:20px;}
.lp .linkcard{background:var(--surface);border:1px solid var(--line-soft);border-radius:12px;padding:18px;box-shadow:var(--shadow);text-decoration:none;display:block;transition:transform .15s,box-shadow .15s;}
.lp .linkcard:hover{transform:translateY(-2px);box-shadow:var(--shadow-lift);}
.lp .linkcard .lc-name{font-family:'Bebas Neue',sans-serif;font-size:19px;letter-spacing:.02em;color:var(--ink);margin-bottom:5px;}
.lp .linkcard .lc-desc{font-size:13px;color:var(--ink-soft);line-height:1.55;}
@media (max-width:760px){.lp .page-hero{padding:52px 20px 40px;}}
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
<meta property="og:image" content="{site}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/og-image.jpg">
{headlinks}
<style>
{style}
{extra}
</style>
</head>
<body>
<div class="lp">

{nav}

<div class="crumbs">{crumbs}</div>

<section class="page-hero">
  <div class="eyebrow">{eyebrow}</div>
  <h1 class="h1">{h1}</h1>
  <p>{lede}</p>
  <div class="hero-ctas">
    <a class="btn-amber" href="{site}/?ref={slug}#quote">{cta1}</a>
    <a class="btn-ghost" href="{cta2_href}">{cta2}</a>
  </div>
</section>

{body}

<section class="final">
  <h2>{final_h}</h2>
  <p>{final_p}</p>
  <div class="final-ctas">
    <a class="btn-amber" style="font-size:13px; padding:14px 24px;" href="{site}/?ref={slug}#quote">REQUEST A QUOTE &rarr;</a>
    <a class="btn-ghost" style="font-size:13px; padding:14px 24px;" href="tel:+18133559071">CALL (813) 355-9071</a>
  </div>
</section>

{footer}
</div>

<script>
(function () {{
  if (typeof gtag !== 'function') return;
  gtag('event', 'content_view', {{ content_type: '{ctype}', content_id: '{slug}' }});
  document.querySelectorAll('a[href*="#quote"]').forEach(function (a) {{
    a.addEventListener('click', function () {{
      gtag('event', 'quote_cta', {{ content_type: '{ctype}', content_id: '{slug}',
        cta_location: (a.textContent || '').trim().slice(0, 40) || 'quote' }});
    }});
  }});
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {{
    a.addEventListener('click', function () {{
      gtag('event', 'phone_click', {{ content_type: '{ctype}', content_id: '{slug}' }});
    }});
  }});
  document.querySelectorAll('a[href*="lounge.academysim.com"]').forEach(function (a) {{
    a.addEventListener('click', function () {{
      gtag('event', 'cross_domain_lounge', {{ content_type: '{ctype}', content_id: '{slug}' }});
    }});
  }});
  document.querySelectorAll('a[href*="builds.academysim.com"]').forEach(function (a) {{
    a.addEventListener('click', function () {{
      gtag('event', 'cross_domain_builds', {{ content_type: '{ctype}', content_id: '{slug}' }});
    }});
  }});
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
    d.setdefault('cta1', 'REQUEST A QUOTE &rarr;')
    d.setdefault('cta2', 'CALL (813) 355-9071')
    d.setdefault('cta2_href', 'tel:+18133559071')
    return PAGE.format(
        GA=GA, site=SITE, headlinks=HEAD_LINKS, style=STYLE, extra=EXTRA_CSS,
        nav=nav_for(p['slug']), footer=FOOTER, **d)


def write(p):
    html = render(p)
    rel = p['url'].strip('/')
    d = os.path.join(OUT, *rel.split('/')) if rel else OUT
    if not os.path.isdir(d):
        os.makedirs(d)
    path = os.path.join(d, 'index.html')
    io.open(path, 'w', encoding='utf-8', newline='').write(html)
    return path, len(html.encode())
