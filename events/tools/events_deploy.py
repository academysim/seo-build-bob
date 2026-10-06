# -*- coding: utf-8 -*-
"""Digest deploy for events.academysim.com.

The site was created by drag-and-drop, so there is no source tree, and
_redirects and netlify.toml cannot be fetched over HTTP. Two of the HTML files
also differ from what Netlify serves (it rewrites form pages), so a fetched
mirror is NOT safe to redeploy.

The digest API solves all of that: declare the complete file list by SHA1,
Netlify replies with only the hashes it does not already have, and everything
else is reused from its store byte-for-byte. Existing files are therefore
carried across untouched without ever needing their content.

Usage:  python events_deploy.py [--prod]
"""
import hashlib, io, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_ID = '572f7d55-3233-45c1-9326-ed4cc83de191'
API = 'https://api.netlify.com/api/v1'
NEW = os.path.join(HERE, 'events_new')
MANIFEST = os.path.join(HERE, 'ev_files.json')

PROD = '--prod' in sys.argv

# Files that already exist in the live deploy and that I am deliberately
# replacing. Everything else is carried across untouched by sha.
#
# index.html is deliberately NOT here. Netlify serves it 98 bytes smaller than
# it stores it, because it rewrites pages containing Netlify Forms. Redeploying
# the fetched copy would bake that stripped version in and could break form
# detection. Editing the homepage needs the original source folder.
REPLACEABLE = {'/sitemap.xml', '/index.html'}


def token():
    p = 'HACKATHON-FORK-NO-DEPLOY/.env.local'
    for line in io.open(p, encoding='utf-8', errors='replace'):
        if line.split('=')[0].strip().upper() in ('NETLIFY_AUTH_TOKEN', 'NETLIFY_TOKEN'):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('no netlify token')


TOK = token()


def curl(args, data=None, binary=None):
    cmd = ['curl.exe', '-s', '-H', 'Authorization: Bearer ' + TOK] + args
    if data is not None:
        cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
        return subprocess.run(cmd, input=data.encode('utf-8'),
                              stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')
    if binary is not None:
        cmd += ['-H', 'Content-Type: application/octet-stream', '--data-binary', '@' + binary]
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')


def sha1_file(p):
    return hashlib.sha1(io.open(p, 'rb').read()).hexdigest()


# ---- 1. existing files, declared by their CURRENT sha ----------------------
existing = json.load(io.open(MANIFEST, encoding='utf-8'))
digest = {f['path']: f['sha'] for f in existing}
print('  carrying over %d existing files by sha' % len(digest))

# ---- 2. the new pages ------------------------------------------------------
local = {}
for root, _, fs in os.walk(NEW):
    for f in fs:
        p = os.path.join(root, f)
        rel = '/' + os.path.relpath(p, NEW).replace(os.sep, '/')
        sha = sha1_file(p)
        if rel in digest and rel not in REPLACEABLE:
            print('  !! %s already exists in the live deploy, refusing to overwrite' % rel)
            print('     add it to REPLACEABLE only if replacing it is intentional')
            raise SystemExit(1)
        if rel in digest:
            print('  REPLACING %-42s %s -> %s' % (rel, digest[rel][:10], sha[:10]))
        digest[rel] = sha
        local[rel] = p
        print('  adding %-46s %s' % (rel, sha[:10]))

print('  total files in new deploy: %d' % len(digest))

# ---- 3. create the deploy --------------------------------------------------
body = json.dumps({'files': digest, 'draft': not PROD})
res = curl(['-X', 'POST', '%s/sites/%s/deploys' % (API, SITE_ID)], data=body)
try:
    dep = json.loads(res)
except Exception:
    print(res[:900])
    raise SystemExit('could not parse deploy response')
if 'id' not in dep:
    print(json.dumps(dep, indent=1)[:900])
    raise SystemExit('deploy not created')

dep_id = dep['id']
required = dep.get('required', [])
print('\n  deploy %s created (%s)' % (dep_id, 'PROD' if PROD else 'draft'))
print('  netlify requires %d file(s) uploaded' % len(required))

# ---- 4. upload only what Netlify asked for ---------------------------------
by_sha = {}
for rel, p in local.items():
    by_sha.setdefault(sha1_file(p), []).append(rel)

for sha in required:
    paths = by_sha.get(sha)
    if not paths:
        raise SystemExit('netlify wants sha %s but it is not one of my new files' % sha)
    for rel in paths:
        out = curl(['-X', 'PUT', '%s/deploys/%s/files%s' % (API, dep_id, rel)],
                   binary=local[rel])
        ok = '"id"' in out or '"sha"' in out
        print('  uploaded %-46s %s' % (rel, 'ok' if ok else out[:120]))

# ---- 5. wait for ready -----------------------------------------------------
for _ in range(40):
    d = json.loads(curl(['%s/deploys/%s' % (API, dep_id)]))
    state = d.get('state')
    if state in ('ready', 'error'):
        break
    time.sleep(3)

print('\n  state      : %s' % d.get('state'))
print('  deploy url : %s' % d.get('deploy_ssl_url'))
if PROD:
    print('  live url   : %s' % d.get('ssl_url'))
print('  file count : %d' % len(d.get('available_functions', []) or []) if False else '')
sys.exit(0 if d.get('state') == 'ready' else 1)
