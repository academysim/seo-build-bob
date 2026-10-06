# -*- coding: utf-8 -*-
"""Work out exactly what Netlify does to an HTML file containing Netlify Forms.

The zip in Downloads is the source for events deploy 6a72bc4716ddbdc9a46078da,
which is still live on its permalink. So:

    stored  = the index.html inside that zip  (verified by sha against that
              deploy's own manifest)
    served  = what the permalink returns today

Diffing the two gives the exact transformation. Inverting it turns today's
served index.html back into today's stored index.html, which makes the file
safely editable.
"""
import difflib, hashlib, io, json, os, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DL = 'C:/Users/malik/Downloads'
ZIP = os.path.join(DL, 'deploy-6a72bc4716ddbdc9a46078da.zip')
DEPLOY = '6a72bc4716ddbdc9a46078da'
PERMALINK = 'https://%s--simevents.netlify.app/' % DEPLOY


def sha1(b):
    return hashlib.sha1(b).hexdigest()


def token():
    for line in io.open('HACKATHON-FORK-NO-DEPLOY/.env.local', encoding='utf-8', errors='replace'):
        if line.split('=')[0].strip().upper() in ('NETLIFY_AUTH_TOKEN', 'NETLIFY_TOKEN'):
            return line.split('=', 1)[1].strip().strip('"').strip("'")


TOK = token()

# ---- 1. what did THAT deploy actually store for /index.html? --------------
out = subprocess.run(['curl.exe', '-s', '-H', 'Authorization: Bearer ' + TOK,
                      'https://api.netlify.com/api/v1/deploys/%s/files' % DEPLOY],
                     stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')
files = json.loads(out)
want = {f['path']: f['sha'] for f in files}
print('  deploy %s has %d files' % (DEPLOY, len(files)))
target_sha = want.get('/index.html')
print('  stored /index.html sha: %s' % target_sha)

# ---- 2. find the matching file in the zip ---------------------------------
z = zipfile.ZipFile(ZIP)
stored = None
for n in z.namelist():
    if n.endswith('index.html'):
        d = z.read(n)
        print('    zip %-44s sha %s %s' % (n, sha1(d)[:12],
                                           '<-- MATCH' if sha1(d) == target_sha else ''))
        if sha1(d) == target_sha:
            stored = d
if stored is None:
    print('\n  no zip file matches that deploy sha; cannot derive the transform this way')
    sys.exit(1)

# ---- 3. what does that same deploy SERVE today? ---------------------------
served = subprocess.run(['curl.exe', '-s', PERMALINK], stdout=subprocess.PIPE).stdout
print('\n  stored %d bytes   served %d bytes   delta %d'
      % (len(stored), len(served), len(stored) - len(served)))

s_txt = stored.decode('utf-8', 'replace').split('\n')
v_txt = served.decode('utf-8', 'replace').split('\n')

print('\n  --- the exact difference ---')
n = 0
for line in difflib.unified_diff(s_txt, v_txt, 'STORED', 'SERVED', lineterm='', n=0):
    if line.startswith(('---', '+++', '@@')):
        continue
    print('   ', line[:200])
    n += 1
    if n > 30:
        print('    ... truncated')
        break
if n == 0:
    print('    (identical)')
