# -*- coding: utf-8 -*-
"""Regenerate replace_<key>.txt from the LIVE manifest, never by hand.

deploy.py refuses to overwrite a path that already exists live unless --replace
names it, and it aborts on the FIRST unnamed one. So the list has to be exactly
"every staged path that is already live", and it goes stale the moment the
staged file set changes. On 2026-09-09 replace_lounge.txt held 29 paths against
38 staged, and four properties had no list at all; a deploy would have aborted.

Written from the live manifest rather than from HTTP on purpose: netlify.toml
404s over HTTP but is present in the manifest, so an HTTP-derived list silently
omits it.

A property that stages nothing, or whose list comes out empty while files are
staged, is a FAILURE. A list that cannot be wrong is not a check.

Usage: python gen_replace.py [key ...]      (default: all five)
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from netlify_lib import live_manifest, SITES  # noqa: E402


def staged_paths(key):
    up = os.path.join(ROOT, key, 'upload')
    out = []
    for root, _, fs in os.walk(up):
        for f in fs:
            out.append('/' + os.path.relpath(os.path.join(root, f), up).replace(os.sep, '/'))
    return sorted(out)


def main(keys):
    bad = 0
    for key in keys:
        staged = staged_paths(key)
        if not staged:
            print('%-7s !! nothing staged in %s/upload' % (key, key))
            bad += 1
            continue
        dep, man = live_manifest(key)
        live = set(f['path'] for f in man)
        overlap = [p for p in staged if p in live]
        new = [p for p in staged if p not in live]
        if not overlap:
            print('%-7s !! %d staged, none matched live deploy %s -- manifest looks wrong'
                  % (key, len(staged), dep))
            bad += 1
            continue
        dst = os.path.join(ROOT, 'replace_%s.txt' % key)
        io.open(dst, 'w', encoding='utf-8', newline='\n').write(','.join(overlap))
        print('%-7s %3d staged, %3d already live -> replace_%s.txt (deploy %s)'
              % (key, len(staged), len(overlap), key, dep))
        for p in new:
            print('        new path, not in --replace: %s' % p)
    if bad:
        raise SystemExit('  %d problem(s)' % bad)
    print('\n  replace lists regenerated')


if __name__ == '__main__':
    main(sys.argv[1:] or ['lounge', 'events', 'builds', 'driver', 'health'])
