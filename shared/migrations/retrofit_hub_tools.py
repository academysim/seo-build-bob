# Retrofit --tree site|source|upload + newline-aware patterns + honest idempotence
# reporting onto the three per-property add_hub_links.py tools. Files are LF; keep LF.
import io, os, re

os.chdir('D:/AcademySimRacing/03-SEO-Build')

HEADER_OLD = ("import io, os\n\n"
              "ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))\n"
              "UP = os.path.join(ROOT, 'upload')\n"
              "TEMPLATE = os.path.join(ROOT, 'template')\n")
HEADER_NEW = """import io, os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TREE = 'upload'
if '--tree' in sys.argv:
    TREE = sys.argv[sys.argv.index('--tree') + 1]
if TREE not in ('site', 'source', 'upload'):
    raise SystemExit('--tree must be site, source or upload')
UP = os.path.join(ROOT, TREE)
if not os.path.isdir(UP):
    raise SystemExit('!! %s does not exist, nothing to patch' % UP)
print('  tree: %s' % UP)
TEMPLATE = os.path.join(ROOT, 'template')
"""
RDWR_OLD = "def wr(p, s):\n    io.open(p, 'w', encoding='utf-8', newline='').write(s)\n"
RDWR_NEW = RDWR_OLD + '''

def adapt(pattern, s):
    """The patterns below are written with LF. A file that is CRLF throughout
    (builds/source/index.html) needs the same pattern with CRLF, and the
    replacement written back with the file's own endings, so the source tree
    never gains mixed line endings from this tool."""
    return pattern.replace('\\n', '\\r\\n') if '\\r\\n' in s else pattern
'''

DOC = {
 'events': ('hours in the footer (address + phone already present).\n"""',
            '''hours in the footer (address + phone already present).

2026-09-09, F8. This wrote only into upload/ and was not a build step, so a
full rebuild dropped the whole section and the hours block (56 lines). It now
takes `--tree site|source|upload` (default upload) and runs from build_all.py
on source/ (where fix_events_p0.py stages the homepage from) and again on
upload/ after staging. Every pass is idempotent and says so.

Usage: python add_hub_links.py [--tree site|source|upload]
"""'''),
 'builds': ('(builds currently has neither).\n"""',
            '''(builds currently has neither).

2026-09-09, F8. This wrote only into upload/ and was not a build step, so a
full rebuild dropped the catalogue section and every footer address+hours
block (182 lines over 20 pages). It now takes `--tree site|source|upload`
(default upload) and runs from build_all.py on source/ (fix_review_counts.py
stages the homepage from there), on site/ (the 19 leaf pages), and again on
upload/ after staging. Every pass is idempotent and says so.

Usage: python add_hub_links.py [--tree site|source|upload]
"""'''),
 'health': ('homepage footer has no hours either).\n"""',
            '''homepage footer has no hours either).

2026-09-09, F8. This wrote only into upload/ and was not a build step, so a
full rebuild dropped the Explore section and every footer hours block (124
lines over 13 pages). It now takes `--tree site|source|upload` (default
upload) and runs from build_all.py on source/ (fix_health_claims.py stages the
homepage from there), on site/ (the 12 leaf pages), and again on upload/ after
staging. Every pass is idempotent and says so.

Usage: python add_hub_links.py [--tree site|source|upload]
"""'''),
}

FOOTER_LOOP_OLD_RE = re.compile(
    r"touched = \[\]\nfor root, _, fs in os\.walk\(UP\):\n    for f in fs:\n        if f != 'index\.html':\n            continue\n"
    r"        p = os\.path\.join\(root, f\)\n        rel = os\.path\.relpath\(p, UP\)\.replace\(os\.sep, '/'\)\n        s = rd\(p\)\n"
    r"        if OLD_CONTACT in s:\n            s = s\.replace\(OLD_CONTACT, NEW_CONTACT, 1\)\n            wr\(p, s\)\n            touched\.append\(rel\)\n\n"
    r"print\('pages patched with (address\+hours|hours line): %d' % len\(touched\)\)\nfor rel in touched:\n    print\('  ' \+ rel\)\n")
FOOTER_LOOP_NEW = """touched, present, unmatched = [], [], []
for root, _, fs in os.walk(UP):
    for f in fs:
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, UP).replace(os.sep, '/')
        s = rd(p)
        old, new = adapt(OLD_CONTACT, s), adapt(NEW_CONTACT, s)
        if old in s:
            s = s.replace(old, new, 1)
            wr(p, s)
            touched.append(rel)
        elif new in s:
            present.append(rel)
        else:
            unmatched.append(rel)

print('pages patched with %s: %d' % ('LABEL', len(touched)))
for rel in touched:
    print('  ' + rel)
if present:
    print('pages where the footer block is already present, skipped: %d' % len(present))
if unmatched:
    print('pages whose footer matched neither form (left alone): %d' % len(unmatched))
    for rel in unmatched:
        print('  ' + rel)
"""

ANCHORS = {
    'events': "anchor = '<section class=\"faq\">'\n",
    'builds': "anchor = '<section class=\"faq\" id=\"faq\">'\n",
    'health': "anchor = '<!-- FAQ -->\\n<section class=\"faq\">'\n",
}

for key in ('events', 'builds', 'health'):
    p = '%s/tools/add_hub_links.py' % key
    raw = io.open(p, encoding='utf-8', newline='').read()
    # The tool files themselves are a mix of LF and CRLF in the working tree
    # (git autocrlf re-materialises some of them). Patch in LF space and write
    # back with the file's own endings, so this retrofit adds no ending churn.
    eol = '\r\n' if '\r\n' in raw else '\n'
    s = raw.replace('\r\n', '\n')
    assert s.count(HEADER_OLD) == 1, key
    s = s.replace(HEADER_OLD, HEADER_NEW, 1)
    assert s.count(RDWR_OLD) == 1, key
    s = s.replace(RDWR_OLD, RDWR_NEW, 1)
    old, new = DOC[key]
    assert s.count(old) == 1, (key, 'doc')
    s = s.replace(old, new, 1)
    m = FOOTER_LOOP_OLD_RE.search(s)
    assert m, (key, 'footer loop')
    s = s[:m.start()] + FOOTER_LOOP_NEW.replace('LABEL', m.group(1)) + s[m.end():]
    a = ANCHORS[key]
    assert s.count(a) == 1, (key, 'anchor')
    s = s.replace(a, a.replace("anchor = '", "anchor = adapt('").replace("'\n", "', s)\n"), 1)
    s2 = s.replace("    s = s.replace(anchor, EXPLORE + anchor, 1)\n    wr(p, s)\n",
                   "    s = s.replace(anchor, adapt(EXPLORE, s) + anchor, 1)\n    wr(p, s)\n")
    assert s2 != s, (key, 'explore')
    s = s2
    s2 = s.replace("ts = rd(tpath)\nif OLD_CONTACT in ts:\n    wr(tpath, ts.replace(OLD_CONTACT, NEW_CONTACT, 1))",
                   "ts = rd(tpath)\nif adapt(OLD_CONTACT, ts) in ts:\n    wr(tpath, ts.replace(adapt(OLD_CONTACT, ts), adapt(NEW_CONTACT, ts), 1))")
    s2 = s2.replace("elif NEW_CONTACT in ts:", "elif adapt(NEW_CONTACT, ts) in ts:")
    assert s2 != s, (key, 'template')
    s = s2
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', eol))
    print('patched %s (%s)' % (p, 'CRLF' if eol == '\r\n' else 'LF'))
