# -*- coding: utf-8 -*-
"""Check whether the zips in Downloads contain the exact files currently
deployed, verified by SHA1 against each site's live deploy manifest.

The three files that cannot be fetched over HTTP are _redirects, netlify.toml
and (on some sites) __forms.html. If their SHA1 matches the live manifest, the
zip copy IS the deployed copy and the source is recovered.
"""
import hashlib, io, json, os, zipfile

DL = 'C:/Users/malik/Downloads'
HERE = os.path.dirname(os.path.abspath(__file__))

JOBS = [
    ('EVENTS', 'ev_files.json', ['deploy-6a72bc4716ddbdc9a46078da.zip',
                                 'academy-events-ROCKWAY-CASE.zip']),
    ('BUILDS', 'builds_files.json', ['academy-builds-SPEC-CORRECTIONS.zip']),
]


def sha1(b):
    return hashlib.sha1(b).hexdigest()


for label, manifest_name, zips in JOBS:
    print('=== %s ===' % label)
    manifest = {f['path']: f['sha'] for f in
                json.load(io.open(os.path.join(HERE, manifest_name), encoding='utf-8'))}
    for zname in zips:
        p = os.path.join(DL, zname)
        if not os.path.isfile(p):
            print('  %s: missing' % zname)
            continue
        print('  %s' % zname)
        z = zipfile.ZipFile(p)
        hits = misses = 0
        matched_paths = []
        for n in z.namelist():
            if n.endswith('/'):
                continue
            data = z.read(n)
            h = sha1(data)
            # try matching by basename-derived deploy path
            cand = '/' + n.split('/', 1)[1] if n.startswith('academy-events-netlify/') else '/' + n
            for path, sha in manifest.items():
                if sha == h and (path == cand or path.split('/')[-1] == n.split('/')[-1]):
                    matched_paths.append((path, n))
                    hits += 1
                    break
        print('    files matching the LIVE deploy by sha1: %d' % hits)
        for path, n in sorted(matched_paths):
            star = '  <-- unfetchable over HTTP' if path.split('/')[-1] in (
                '_redirects', 'netlify.toml', '__forms.html') else ''
            print('      %-34s  from %s%s' % (path, n, star))
    print()
