# -*- coding: utf-8 -*-
"""Verify no page under upload/ links the extensionless form of the 7
duplicate-URL pages anymore."""
import io, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
UP = os.path.join(ROOT, 'upload')
PATHS = ['about', 'contact', 'public-safety', 'resources',
         'schools-programs', 'simulator-rentals', 'teen-training']
BAD = re.compile(r'''href=(['"])/(%s)((?!\.html)[#'"])''' % '|'.join(PATHS))

bad_found = 0
checked = 0
for root, _, fs in os.walk(UP):
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        checked += 1
        s = io.open(p, encoding='utf-8').read()
        ms = BAD.findall(s)
        if ms:
            bad_found += len(ms)
            print('  !! %s : %d remaining non-canonical href(s)' % (os.path.relpath(p, UP), len(ms)))
        if 'Hours' not in s and ('<nav class="nav">' in s or '<footer class="ftr">' in s):
            print('  ?? %s : has nav/footer but no Hours block' % os.path.relpath(p, UP))

print('checked %d pages, %d remaining bad hrefs' % (checked, bad_found))
