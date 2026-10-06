# -*- coding: utf-8 -*-
"""The rebuilt index.html is the right SIZE but the wrong SHA, which means the
attributes are correct and only their ORDER (or quoting) differs from what the
author wrote. Search the permutations until the SHA matches the live manifest.

Definitive: a SHA match means the reconstruction is byte-identical to the file
Netlify is actually storing.
"""
import hashlib, io, itertools, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITES = {
    'builds': ('https://builds.academysim.com/', 'builds_files.json', 'builds_new'),
    'health': ('https://health.academysim.com/', 'health_files.json', 'health_new'),
    'events': ('https://events.academysim.com/', 'ev_files.json', 'events_new'),
}

key = sys.argv[1]
url, manifest, outdir = SITES[key]

target = {f['path']: f['sha'] for f in
          json.load(io.open(os.path.join(HERE, manifest), encoding='utf-8'))}['/index.html']

served = subprocess.run(['curl.exe', '-s', url], stdout=subprocess.PIPE).stdout.decode('utf-8')

FORM = re.compile(r"<form([^>]*?)>")
ATTR = re.compile(r"""(\w[\w-]*)=['"]([^'"]*)['"]""")

forms = list(FORM.finditer(served))
print('  %d form(s) in the served page' % len(forms))
base = next(dict(ATTR.findall(f.group(1))) for f in forms
            if 'name' in dict(ATTR.findall(f.group(1))))
keys = list(base) + ['data-netlify', 'netlify-honeypot']
print('  attributes: %s' % ', '.join(keys))

vals = dict(base)
vals['data-netlify'] = 'true'
vals['netlify-honeypot'] = 'bot-field'

tried = 0
for quote in ('"', "'"):
    for order in itertools.permutations(keys):
        tried += 1
        def build(m):
            a = dict(ATTR.findall(m.group(1)))
            if 'name' not in a or 'method' not in a:
                return m.group(0)          # bare <form>, not a Netlify form
            v = dict(a)
            v['data-netlify'] = 'true'
            v['netlify-honeypot'] = 'bot-field'
            return '<form ' + ' '.join(
                '%s=%s%s%s' % (k, quote, v[k], quote) for k in order if k in v) + '>'
        cand = FORM.sub(build, served)
        if hashlib.sha1(cand.encode('utf-8')).hexdigest() == target:
            print('\n  SOLVED after %d attempts' % tried)
            print('  quote style : %s' % ('double' if quote == '"' else 'single'))
            print('  order       : %s' % ' '.join(order))
            p = os.path.join(HERE, outdir, 'index.html')
            io.open(p, 'w', encoding='utf-8', newline='').write(cand)
            print('  written     : %s' % p)
            print('  sha         : %s  BYTE-IDENTICAL' % target)
            for m in FORM.finditer(cand):
                print('    %s' % ' '.join(m.group(0).split())[:160])
            sys.exit(0)

print('\n  no permutation matched after %d attempts' % tried)
sys.exit(1)
