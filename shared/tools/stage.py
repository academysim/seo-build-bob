# -*- coding: utf-8 -*-
"""Copy a property's site/ tree into upload/, without clobbering staged edits.

upload/ is what deploy.py ships. Files already there came from a fix_*.py and
are newer than site/, so they win. Everything else is copied across, and the
--replace list deploy.py needs is printed at the end.

What gets copied (F8, 2026-09-09). This used to copy *.html and nothing else,
which is why a full rebuild silently dropped lounge's netlify.toml, both
sitemap.xml files and the eight membership tier images -- all present,
byte-identical, in site/ -- and why driver's stylesheet was never staged at
all. The rule is now general: every file under site/ whose extension is in
DEPLOYABLE is staged, except

  * directories whose name starts with '.' or '_' (.netlify/, __pycache__/),
    or is in SKIP_DIRS (tools/, backups/);
  * editor and backup junk, matched by JUNK (index.html.bak-2026-08-30-prices,
    *.orig, *.tmp, *.swp, *~);
  * anything with an extension NOT in DEPLOYABLE, which is printed as skipped so
    a new kind of asset cannot vanish quietly.

EXTRA lists files a property needs in upload/ that do not live under its
site/. driver keeps its stylesheet at template/site.css (one copy, the one
driver_pages.py links to as /assets/css/site.css) and nothing else ever put it
in upload/, so commit 2631cfb's mobile fix could not reach live from a rebuild.

A property that stages zero files is a failure, not a quiet success.

Usage: python stage.py <key> [more keys ...]
"""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

DEPLOYABLE = {
    '.html', '.htm', '.xml', '.txt', '.toml', '.json', '.webmanifest',
    '.css', '.js',
    '.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.ico', '.avif',
    '.woff', '.woff2', '.ttf',
    '.pdf', '.mp4', '.webm',
}
SKIP_DIRS = {'tools', 'backups', 'backup', 'node_modules'}
JUNK = re.compile(r'(\.bak(\b|-|$)|\.orig$|\.tmp$|\.swp$|\.pyc$|~$)', re.I)

# (source path relative to <key>/, destination relative to <key>/upload/)
EXTRA = {
    'driver': [('template/site.css', 'assets/css/site.css')],
}


def copy_into(src, dst):
    d = os.path.dirname(dst)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    shutil.copyfile(src, dst)


fail = False
for key in sys.argv[1:]:
    site = os.path.join(ROOT, key, 'site')
    up = os.path.join(ROOT, key, 'upload')
    if not os.path.isdir(site):
        print('!! %s: %s does not exist' % (key, site))
        fail = True
        continue
    copied = kept = 0
    skipped = []
    for root, dirs, fs in os.walk(site):
        dirs[:] = sorted(d for d in dirs
                         if not d.startswith(('.', '_')) and d not in SKIP_DIRS)
        for f in sorted(fs):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, site).replace(os.sep, '/')
            ext = os.path.splitext(f)[1].lower()
            if f.startswith('.') or JUNK.search(f) or ext not in DEPLOYABLE:
                skipped.append(rel)
                continue
            dst = os.path.join(up, rel)
            if os.path.exists(dst):
                kept += 1
                continue
            copy_into(p, dst)
            copied += 1
    for src_rel, dst_rel in EXTRA.get(key, []):
        src = os.path.join(ROOT, key, *src_rel.split('/'))
        if not os.path.isfile(src):
            print('!! %s: EXTRA source %s is missing' % (key, src_rel))
            fail = True
            continue
        dst = os.path.join(up, *dst_rel.split('/'))
        if os.path.exists(dst):
            kept += 1
        else:
            copy_into(src, dst)
            copied += 1
    paths = []
    for root, _, fs in os.walk(up):
        for f in fs:
            paths.append('/' + os.path.relpath(os.path.join(root, f), up).replace(os.sep, '/'))
    print('%-7s %d copied, %d already staged, %d total' % (key, copied, kept, len(paths)))
    for rel in skipped:
        print('  skipped (not deployable): %s' % rel)
    if copied + kept == 0:
        print('!! %s: staged nothing from %s' % (key, site))
        fail = True
    print('  --replace ' + ','.join(sorted(paths)))

if fail:
    raise SystemExit('  stage.py FAILED')
