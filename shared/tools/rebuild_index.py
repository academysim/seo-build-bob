# -*- coding: utf-8 -*-
"""Reconstruct a deployable index.html from what Netlify serves.

Proven transformation (derived by diffing events deploy 6a72bc47's stored file
against what that deploy's permalink serves today):

  stored:  <form name="X" class="Y" method="POST" data-netlify="true"
                 netlify-honeypot="bot-field" action="/Z">
  served:  <form action='/Z' class='Y' method='POST' name='X'>

Netlify strips ` data-netlify="true" netlify-honeypot="bot-field"` (49 bytes)
and normalises attribute order and quoting. So restoring those two attributes
to each form turns a fetched copy back into a deployable source.

The reconstruction is then PROVEN on a draft deploy: if the draft serves bytes
identical to what production serves today, the source is correct.

Usage: python rebuild_index.py <site-key>
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

SITES = {
    'events': ('https://events.academysim.com/', 'events_deploy', 'events_new'),
    'builds': ('https://builds.academysim.com/', 'builds_deploy', 'builds_new'),
    'health': ('https://health.academysim.com/', 'health_deploy', 'health_new'),
}

key = sys.argv[1]
url, _, outdir = SITES[key]

served = subprocess.run(['curl.exe', '-s', url], stdout=subprocess.PIPE).stdout
text = served.decode('utf-8')
print('  served %s: %d bytes' % (url, len(served)))

FORM = re.compile(r"<form([^>]*?)>")
ATTR = re.compile(r"""(\w[\w-]*)=['"]([^'"]*)['"]""")

n = 0


def restore(m):
    global n
    attrs = dict(ATTR.findall(m.group(1)))
    if 'name' not in attrs or 'method' not in attrs:
        return m.group(0)          # not a Netlify form
    n += 1
    # rebuild in the authored order, with the stripped attributes restored
    parts = ['<form']
    parts.append('name="%s"' % attrs['name'])
    if 'class' in attrs:
        parts.append('class="%s"' % attrs['class'])
    if 'id' in attrs:
        parts.append('id="%s"' % attrs['id'])
    parts.append('method="%s"' % attrs['method'])
    parts.append('data-netlify="true"')
    parts.append('netlify-honeypot="bot-field"')
    if 'action' in attrs:
        parts.append('action="%s"' % attrs['action'])
    return ' '.join(parts) + '>'


rebuilt = FORM.sub(restore, text)
print('  restored netlify attributes on %d form(s)' % n)
print('  rebuilt: %d bytes  (served + %d)' % (len(rebuilt.encode()), len(rebuilt.encode()) - len(served)))

dst = os.path.join(HERE, outdir, 'index.html')
io.open(dst, 'w', encoding='utf-8', newline='').write(rebuilt)
print('  written to %s' % dst)
print('\n  forms in the rebuilt file:')
for m in FORM.finditer(rebuilt):
    print('    %s' % ' '.join(m.group(0).split())[:150])
