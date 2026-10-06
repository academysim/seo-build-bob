# -*- coding: utf-8 -*-
"""Phase 2 leftovers the discovery audit found, other than breadcrumbs.

1. builds.academysim.com has no canonical URL at all on its homepage. Every
   other page on every property has one. Without it the homepage competes with
   any parameterised or alternate form of its own URL.

2. health.academysim.com ships one title on two pages: the /programs/ hub and
   /programs/senior-living-racing-simulator/. Two pages claiming the same query
   is the cannibalisation the brief spends a section warning about, and it is
   the hub that should give way, because the leaf owns the specific term. The
   hub takes the broader one.

Run after add_breadcrumbs.py. Reads source/ or site/, writes upload/.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

JOBS = [
    ('builds', 'index.html', 'upload',
     u'<title>Custom Sim Racing Builds | Academy Sim Racing — Tampa, FL</title>\n',
     u'<title>Custom Sim Racing Builds | Academy Sim Racing — Tampa, FL</title>\n'
     u'<link rel="canonical" href="https://builds.academysim.com/">\n'),

    ('health', 'programs/index.html', 'site',
     u'<title>Racing Simulator Programs for Senior Living Communities | Academy</title>',
     u'<title>Senior Community Simulator Programs in Florida | Academy</title>'),
]


def main():
    fail = False
    for prop, rel, srcdir, old, new in JOBS:
        staged = os.path.join(ROOT, prop, 'upload', rel)
        src = staged if os.path.exists(staged) else os.path.join(ROOT, prop, srcdir, rel)
        h = io.open(src, encoding='utf-8').read()
        got = h.count(old)
        if got == 0:
            # ALREADY APPLIED, not missing. These `old` strings are exact byte matches, and
            # the em dash sweep has since rewritten the copy they quote -- builds' title is
            # now "Academy Sim Racing, Tampa, FL" where this job still expects an em dash.
            # So test the OUTCOME instead: whatever `new` ADDS beyond `old` (here the
            # canonical link) is either in the file or it is not. If it is, the job is done.
            # This is safe because the result is gated independently below
            # (builds homepage canonical count must be exactly 1).
            addition = new.replace(old, '').strip() if old in new else ''
            if addition and addition in h:
                if not os.path.exists(staged):
                    d0 = os.path.dirname(staged)
                    if d0 and not os.path.isdir(d0):
                        os.makedirs(d0)
                    io.open(staged, 'w', encoding='utf-8', newline='').write(h)
                print('  --  %-8s %-34s already applied in source/' % (prop, rel))
                continue
        if got != 1:
            print('  !! %s/%s: expected 1, found %d for %r'
                  % (prop, rel, got, ' '.join(old.split())[:70]))
            fail = True
            continue
        h = h.replace(old, new)
        dst = os.path.join(ROOT, prop, 'upload', rel)
        d = os.path.dirname(dst)
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(dst, 'w', encoding='utf-8', newline='').write(h)
        print('  ok  %-8s %-34s -> upload/' % (prop, rel))

    # gates
    b = io.open(os.path.join(ROOT, 'builds', 'upload', 'index.html'),
                encoding='utf-8').read()
    if b.count('rel="canonical"') != 1:
        print('  !! builds homepage canonical count = %d' % b.count('rel="canonical"'))
        fail = True
    titles = {}
    for prop in ('health',):
        base = os.path.join(ROOT, prop)
        for root, _, fs in os.walk(os.path.join(base, 'site')):
            for f in fs:
                if f != 'index.html':
                    continue
                p = os.path.join(root, f)
                rel = os.path.relpath(p, os.path.join(base, 'site')).replace(os.sep, '/')
                staged = os.path.join(base, 'upload', rel)
                h = io.open(staged if os.path.exists(staged) else p, encoding='utf-8').read()
                t = re.search(r'<title[^>]*>(.*?)</title>', h, re.S)
                if t:
                    titles.setdefault(' '.join(t.group(1).split()), []).append(rel)
    for t, ps in titles.items():
        if len(ps) > 1:
            print('  !! %s: duplicate title on %s -> %r' % (prop, ps, t[:60]))
            fail = True
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
