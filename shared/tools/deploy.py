# -*- coding: utf-8 -*-
"""Generic digest deploy for any of the five Netlify properties.

Declares every file in the live published deploy by its CURRENT sha, overlays
the files in <property>/upload/, and asks Netlify for a deploy. Netlify replies
with only the hashes it lacks, so untouched files are reused byte-for-byte and
their content is never needed. Overwriting an existing path requires --replace.

Usage: python deploy.py <key> [--prod] [--replace path,path]
"""
import hashlib, io, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from netlify_lib import SITES, API, token, curl, live_manifest  # noqa

key = sys.argv[1]
PROD = '--prod' in sys.argv
replace = set()
if '--replace' in sys.argv:
    replace = set(sys.argv[sys.argv.index('--replace') + 1].split(','))

ROOT = os.path.normpath(os.path.join(HERE, '..', '..', key))
UP = os.path.join(ROOT, 'upload')
TOK = token()

_, man = live_manifest(key)
digest = {f['path']: f['sha'] for f in man}
print('  carrying over %d live files by sha' % len(digest))

local = {}
for root, _, fs in os.walk(UP):
    for f in fs:
        p = os.path.join(root, f)
        rel = '/' + os.path.relpath(p, UP).replace(os.sep, '/')
        sha = hashlib.sha1(io.open(p, 'rb').read()).hexdigest()
        if rel in digest and rel not in replace:
            raise SystemExit('  !! %s exists live; pass --replace to overwrite' % rel)
        print('  %-9s %-52s %s' % ('REPLACE' if rel in digest else 'add', rel, sha[:10]))
        digest[rel] = sha
        local[rel] = p

if not local:
    raise SystemExit('  nothing in %s' % UP)
print('  total files: %d' % len(digest))

res = curl(['-X', 'POST', '%s/sites/%s/deploys' % (API, SITES[key])],
           data=json.dumps({'files': digest, 'draft': not PROD}), tok=TOK)
dep = json.loads(res)
if 'id' not in dep:
    raise SystemExit(json.dumps(dep, indent=1)[:900])
dep_id = dep['id']
print('\n  deploy %s (%s), %d file(s) required'
      % (dep_id, 'PROD' if PROD else 'DRAFT', len(dep.get('required', []))))

by_sha = {}
for rel, p in local.items():
    by_sha.setdefault(hashlib.sha1(io.open(p, 'rb').read()).hexdigest(), []).append(rel)
for sha in dep.get('required', []):
    for rel in by_sha.get(sha, []):
        out = curl(['-X', 'PUT', '%s/deploys/%s/files%s' % (API, dep_id, rel)],
                   binary=local[rel], tok=TOK)
        print('  uploaded %-52s %s' % (rel, 'ok' if ('"id"' in out or '"sha"' in out) else out[:120]))

for _ in range(60):
    d = json.loads(curl(['%s/deploys/%s' % (API, dep_id)], tok=TOK))
    if d.get('state') in ('ready', 'error'):
        break
    time.sleep(3)
print('\n  state : %s' % d.get('state'))
print('  url   : %s' % d.get('deploy_ssl_url'))
sys.exit(0 if d.get('state') == 'ready' else 1)
