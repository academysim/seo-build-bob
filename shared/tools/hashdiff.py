# -*- coding: utf-8 -*-
"""Hash-diff <property>/upload/ against its live manifest (<property>/tools/<key>_files.json,
refreshed via netlify_lib.py). Prints files that differ/are new locally, and live files not
present locally (carried over untouched by deploy.py). This is the pre-deploy check.
Usage: python hashdiff.py <key>
"""
import hashlib, io, json, os, sys

key = sys.argv[1]
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', key))
UP = os.path.join(ROOT, 'upload')
MANIFEST = os.path.join(ROOT, 'tools', '%s_files.json' % key)

man = json.load(io.open(MANIFEST, encoding='utf-8'))
live = {f['path']: f['sha'] for f in man}

local_paths = set()
diffs = []
for root, _, fs in os.walk(UP):
    for f in fs:
        p = os.path.join(root, f)
        rel = '/' + os.path.relpath(p, UP).replace(os.sep, '/')
        local_paths.add(rel)
        sha = hashlib.sha1(io.open(p, 'rb').read()).hexdigest()
        if rel not in live:
            diffs.append((rel, 'NEW (not in live)'))
        elif live[rel] != sha:
            diffs.append((rel, 'DIFFERS'))

missing = sorted(set(live) - local_paths)

print('local upload files: %d   live files: %d' % (len(local_paths), len(live)))
print('--- differs / new locally (these are what a deploy would push) ---')
for rel, why in sorted(diffs):
    print('  %-55s %s' % (rel, why))
print('--- live but not touched locally (deploy.py carries these over unchanged) ---')
for rel in missing:
    print('  ' + rel)

replace = ','.join(sorted(rel for rel, _ in diffs))
print('\n--replace value for shared/tools/deploy.py:')
print(replace)
