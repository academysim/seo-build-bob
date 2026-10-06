# -*- coding: utf-8 -*-
"""Task 03-hub-links item 4: driver's canonical is the .html form (already
indexed, already what the sitemap lists) but nav/body links point at the
extensionless form, so the canonical URLs get zero internal links. Rewrite
every internal href pointing at one of the 7 duplicate-form pages to the
.html form, sitewide (nav, body CTAs, JS analytics-binding selectors).

Also adds an hours line to the footer's Visit column (driver currently
publishes none).

Covers all HTML pages in the live manifest. 11 already sit in upload/ from
earlier patches; the other 17 (school-districts/schools/training leaves +
thanks.html) are fetched live -- verified first to carry no <form>, since a
fetched copy of a Netlify Forms page has its data-netlify attributes
stripped by Netlify's serving layer and is not safe to redeploy.
"""
import io, json, os, re, sys, urllib.request

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
UP = os.path.join(ROOT, 'upload')
TEMPLATE = os.path.join(ROOT, 'template')
MANIFEST = os.path.join(ROOT, 'tools', 'driver_files.json')
SITE = 'https://driver.academysim.com'

PATHS = ['about', 'contact', 'public-safety', 'resources',
         'schools-programs', 'simulator-rentals', 'teen-training']
HREF_RE = re.compile(
    r'''(?<![\w-])href=(['"])/(%s)(#[^'"]*)?\1''' % '|'.join(PATHS)
)


def fix_hrefs(s):
    n = [0]

    def repl(m):
        n[0] += 1
        return 'href=%s/%s.html%s%s' % (m.group(1), m.group(2), m.group(3) or '', m.group(1))

    return HREF_RE.sub(repl, s), n[0]


OLD_VISIT = (
    '    <div>\n'
    '      <h4>Visit</h4>\n'
    '      <ul>\n'
    '        <li>1421 Massaro Blvd</li><li>Tampa, FL 33619</li>\n'
    '        <li><a href="tel:+18133559071">(813) 355-9071</a></li>\n'
    '        <li><a href="mailto:info@academysim.com">info@academysim.com</a></li>\n'
    '      </ul>\n'
    '    </div>\n'
)
NEW_VISIT = (
    '    <div>\n'
    '      <h4>Visit</h4>\n'
    '      <ul>\n'
    '        <li>1421 Massaro Blvd</li><li>Tampa, FL 33619</li>\n'
    '        <li><a href="tel:+18133559071">(813) 355-9071</a></li>\n'
    '        <li><a href="mailto:info@academysim.com">info@academysim.com</a></li>\n'
    '      </ul>\n'
    '      <h4 style="margin-top:16px">Hours</h4>\n'
    '      <ul>\n'
    '        <li>Fri &amp; Sat 2–10 PM</li>\n'
    '        <li>Mon, Wed, Thu 12–9 PM</li>\n'
    '        <li>Sun 12–6 PM · Tue Closed</li>\n'
    '      </ul>\n'
    '    </div>\n'
)


def patch(s):
    s, n_href = fix_hrefs(s)
    n_visit = 0
    if OLD_VISIT in s:
        s = s.replace(OLD_VISIT, NEW_VISIT, 1)
        n_visit = 1
    return s, n_href, n_visit


# ---------------------------------------------------- already-local files --
local_rels = []
for root, _, fs in os.walk(UP):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            local_rels.append(os.path.relpath(p, UP).replace(os.sep, '/'))

print('=== already local (%d) ===' % len(local_rels))
for rel in sorted(local_rels):
    p = os.path.join(UP, *rel.split('/'))
    s = io.open(p, encoding='utf-8', newline='').read()
    s2, n_href, n_visit = patch(s)
    if s2 != s:
        io.open(p, 'w', encoding='utf-8', newline='').write(s2)
    print('  %-45s href-fixes=%d  hours-added=%d' % (rel, n_href, n_visit))

# ------------------------------------------------------- fetch the rest --
man = json.load(io.open(MANIFEST, encoding='utf-8'))
all_html = [f['path'].lstrip('/') for f in man if f['path'].endswith('.html')
            and not f['path'].startswith('/__')]
remote_rels = [p for p in all_html if p not in local_rels]

print('\n=== fetching (%d) ===' % len(remote_rels))
for rel in sorted(remote_rels):
    url = SITE + '/' + rel
    with urllib.request.urlopen(url) as r:
        s = r.read().decode('utf-8')
    if '<form' in s.lower():
        print('  !! %-45s HAS A <form>, refusing to fetch-and-redeploy (Netlify strips form attrs on serve). Skipped.' % rel)
        continue
    s2, n_href, n_visit = patch(s)
    out_p = os.path.join(UP, *rel.split('/'))
    os.makedirs(os.path.dirname(out_p), exist_ok=True)
    io.open(out_p, 'w', encoding='utf-8', newline='').write(s2)
    print('  %-45s href-fixes=%d  hours-added=%d' % (rel, n_href, n_visit))

# ------------------------------------------------------------- templates --
hpath = os.path.join(TEMPLATE, '_header.html')
hs = io.open(hpath, encoding='utf-8', newline='').read()
hs2, n = fix_hrefs(hs)
if hs2 != hs:
    io.open(hpath, 'w', encoding='utf-8', newline='').write(hs2)
print('\ntemplate/_header.html: href-fixes=%d' % n)

fpath = os.path.join(TEMPLATE, '_footer.html')
fs_ = io.open(fpath, encoding='utf-8', newline='').read()
fs2, n_href = fix_hrefs(fs_)
n_visit = 0
if OLD_VISIT in fs2:
    fs2 = fs2.replace(OLD_VISIT, NEW_VISIT, 1)
    n_visit = 1
if fs2 != fs_:
    io.open(fpath, 'w', encoding='utf-8', newline='').write(fs2)
print('template/_footer.html: href-fixes=%d  hours-added=%d' % (n_href, n_visit))
