# -*- coding: utf-8 -*-
"""Rebuild deployable source for a drag-and-drop Netlify page from what it serves.

Netlify makes exactly two edits when SERVING an HTML file, and the served/stored
size delta on every Academy page is fully explained by them:

1. Pretty URLs (processing_settings.html.pretty_urls) rewrites internal links:
   `/about.html` is served `/about` (-5 each), `/index.html` served `/` (-10).
2. Form detection strips ` data-netlify="true" netlify-honeypot="bot-field"`
   from each <form> and re-serialises its attributes alphabetically in single
   quotes (-49 each).

Both are undone here. The link restoration is deliberately NOT reversed to
byte-exactness: whether a given link was authored with or without `.html` is
unknowable, and it does not matter, because pretty URLs re-strips it on the way
out either way. Writing `.html` is the safer of the two, since it still resolves
if pretty URLs is ever turned off.

So the reconstruction is not proven by SHA. It is proven by DRAFT DEPLOY: ship
it to a draft and diff what the draft serves against what production serves. A
clean diff means the file is equivalent to the stored one in every byte a
visitor receives. verify_draft() does that check.

Usage: python recover.py <key> <path> [<path> ...]
"""
import io, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from netlify_lib import SITES  # noqa

HOSTS = {k: 'https://%s.academysim.com' % k for k in SITES}

FORM = re.compile(r"<form([^>]*)>")
ATTR = re.compile(r"""([\w:-]+)(?:=(?:"([^"]*)"|'([^']*)'|([^\s"'>]+)))?""")
LINK = re.compile(r"""((?:href|action)=)(['"])(/[^'"]*)\2""")
INJECT = ' data-netlify="true" netlify-honeypot="bot-field"'


def url_for(key, path):
    u = HOSTS[key] + re.sub(r'index\.html$', '', path)
    return re.sub(r'\.html$', '', u)


def rebuild(key, path, text, paths):
    """served text -> deployable source"""
    def unpretty(m):
        pre, q, href = m.groups()
        if href + '.html' in paths:
            return '%s%s%s.html%s' % (pre, q, href, q)
        return m.group(0)

    out = LINK.sub(unpretty, text)

    def restore_form(m):
        attrs = {}
        order = []
        for a in ATTR.finditer(m.group(1)):
            v = next((g for g in a.groups()[1:] if g is not None), None)
            attrs[a.group(1)] = v
            order.append(a.group(1))
        if 'name' not in attrs:
            return m.group(0)
        parts = ['<form']
        for k in order:
            parts.append(k if attrs[k] is None else '%s="%s"' % (k, attrs[k]))
            if k == 'method':
                parts.append('data-netlify="true"')
                parts.append('netlify-honeypot="bot-field"')
        s = ' '.join(parts) + '>'
        if 'data-netlify' not in s:
            s = s[:-1] + INJECT + '>'
        return s

    return FORM.sub(restore_form, out)


def recover(key, path, outdir=None):
    man = json.load(io.open(os.path.join(HERE, '..', '..', key, 'tools',
                                         '%s_files.json' % key), encoding='utf-8'))
    paths = {f['path'] for f in man}
    if path not in paths:
        raise SystemExit('  %s not in the %s manifest' % (path, key))
    served = subprocess.run(['curl.exe', '-s', url_for(key, path)],
                            stdout=subprocess.PIPE).stdout
    src = rebuild(key, path, served.decode('utf-8'), paths)
    outdir = outdir or os.path.join(HERE, '..', '..', key, 'source')
    out = os.path.normpath(os.path.join(outdir, path.lstrip('/')))
    if not os.path.isdir(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))
    io.open(out, 'w', encoding='utf-8', newline='').write(src)
    print('  %-42s served %6d -> source %6d  (%s)'
          % (path, len(served), len(src.encode()), out))
    return out


def verify_draft(key, deploy_url, paths):
    """diff what a draft serves against what production serves, per path"""
    ok = True
    for p in paths:
        a = subprocess.run(['curl.exe', '-s', deploy_url + re.sub(r'\.html$', '', re.sub(r'index\.html$', '', p))],
                           stdout=subprocess.PIPE).stdout
        b = subprocess.run(['curl.exe', '-s', url_for(key, p)],
                           stdout=subprocess.PIPE).stdout
        same = a == b
        ok &= same
        print('  %-42s draft %6d  prod %6d  %s'
              % (p, len(a), len(b), 'IDENTICAL' if same else '*** DIFFERS ***'))
    return ok


if __name__ == '__main__':
    for p in sys.argv[2:]:
        recover(sys.argv[1], p)
