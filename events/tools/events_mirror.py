# -*- coding: utf-8 -*-
"""Mirror events.academysim.com locally and prove the mirror is byte-identical
to what Netlify is serving, by comparing SHA1 against the deploy manifest.

_redirects and netlify.toml are not fetchable over HTTP. They are NOT
reconstructed. The digest deploy declares them by their existing SHA1, so
Netlify reuses its stored copies and their content is never needed.
"""
import hashlib, io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'events_deploy')
MANIFEST = os.path.join(HERE, 'ev_files.json')
BASE = 'https://events.academysim.com'

files = json.load(io.open(MANIFEST, encoding='utf-8'))
manifest = {f['path']: (f['sha'], f.get('size')) for f in files}

# Netlify strips these from the CDN; they exist in the deploy only.
UNFETCHABLE = {'/_redirects', '/netlify.toml'}


def sha1(b):
    return hashlib.sha1(b).hexdigest()


ok = bad = skipped = 0
for path, (sha, size) in sorted(manifest.items()):
    if path in UNFETCHABLE:
        print('  %-42s reused by sha (not fetchable)' % path)
        skipped += 1
        continue
    dst = os.path.join(OUT, *path.lstrip('/').split('/'))
    d = os.path.dirname(dst)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    url = BASE + path
    subprocess.run(['curl.exe', '-s', '-o', dst, url], check=True)
    got = sha1(io.open(dst, 'rb').read())
    if got == sha:
        print('  %-42s OK   %d bytes' % (path, os.path.getsize(dst)))
        ok += 1
    else:
        print('  %-42s SHA MISMATCH  manifest=%s local=%s (%d vs %d bytes)'
              % (path, sha[:10], got[:10], size or -1, os.path.getsize(dst)))
        bad += 1

print('\n  identical: %d   mismatched: %d   reused-by-sha: %d   total: %d'
      % (ok, bad, skipped, len(manifest)))
sys.exit(1 if bad else 0)
