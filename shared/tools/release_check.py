# -*- coding: utf-8 -*-
"""Release inventory and live smoke check for any of the five properties.

Why this exists: on 2026-09-07 two Netlify drag-and-drop deploys replaced the
lounge's 38-file release with a 13-file one. Sixteen live pages became 404s,
/tracks/sebring/ was reverted to a pre-2026-08-29 copy carrying the body-scroll
bug, netlify.toml lost its security headers and its apex 301, and llms.txt
disappeared. Nothing noticed for two days, because every local audit still
passed: they audit the local tree, and the local tree was fine.

So this checks the two things a local audit structurally cannot:

  1. INVENTORY  - every path in <property>/upload/ is present in the published
                  Netlify deploy at the same sha, and the published deploy has
                  not lost paths it used to serve.
  2. SMOKE      - every URL in the intended sitemap answers 200 over HTTP with
                  its own page: a unique title, a self-referential canonical,
                  one h1, and none of Netlify's "Page not found" body.

Zero URLs checked is a hard failure, not a pass. That is the same trap the four
property audits fell into: os.walk over a missing directory yields nothing
silently, so the gate printed "ALL OK" having audited nothing.

Usage: python release_check.py <key> [--url https://host] [--deploy <id>] [--no-live]
Exit:  0 all clear, 1 findings, 2 the check had nothing to check.

`--url` + `--deploy` point the whole check at a draft deploy before it is
published. Sitemap paths are then fetched from the draft host, but canonicals are
still required to name the production URL, which is what they must say on a draft.
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from netlify_lib import SITES, live_manifest  # noqa: E402
from constants import HOSTS  # noqa: E402

ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

NETLIFY_404 = 'Page not found'


def fetch(url):
    """(status, body). curl.exe rather than urllib: the same binary the deploy
    path already depends on, and it follows the same TLS stack as a visitor."""
    r = subprocess.run(
        ['curl.exe', '-s', '-m', '25', '-w', '\n__STATUS__%{http_code}', url],
        stdout=subprocess.PIPE)
    out = r.stdout.decode('utf-8', 'replace')
    i = out.rfind('\n__STATUS__')
    if i < 0:
        return 0, out
    return int(out[i + len('\n__STATUS__'):].strip() or 0), out[:i]


def sitemap_urls(key):
    for d in ('upload', 'site'):
        p = os.path.join(ROOT, key, d, 'sitemap.xml')
        if os.path.exists(p):
            xml = io.open(p, encoding='utf-8').read()
            return p, re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', xml)
    return None, []


def local_paths(key):
    up = os.path.join(ROOT, key, 'upload')
    out = {}
    for root, _, fs in os.walk(up):
        for f in fs:
            p = os.path.join(root, f)
            rel = '/' + os.path.relpath(p, up).replace(os.sep, '/')
            out[rel] = hashlib.sha1(io.open(p, 'rb').read()).hexdigest()
    return out


FORM_OPEN = re.compile(r'<form\s[^>]*>', re.I)


def netlify_form_rewrite_only(local_text, live_text):
    """True when the ONLY thing separating the local file from the live one is
    Netlify's own form post-processing.

    Netlify parses `data-netlify="true"` at deploy time, registers the form and
    serves the tag back with its own attribute set: it drops `data-netlify` and
    `netlify-honeypot`, requotes with single quotes and reorders. That is a
    deterministic 49-byte-per-form rewrite, established 2026-09-09 by diffing
    builds/ and health/ live against upload/ (one line changed in each, exactly
    49 bytes, nothing else).

    Reported as a note rather than a finding, because a gate that flags a
    known-benign difference on every run teaches people to ignore it. Anything
    outside a <form> open tag, or a form tag the local side did not mark with
    data-netlify, still fails.
    """
    a = local_text.splitlines()
    b = live_text.splitlines()
    if len(a) != len(b):
        return False
    for la, lb in zip(a, b):
        if la == lb:
            continue
        fa, fb = FORM_OPEN.search(la), FORM_OPEN.search(lb)
        if not fa or not fb:
            return False
        # everything outside the form tag must be untouched
        if la[:fa.start()] != lb[:fb.start()] or la[fa.end():] != lb[fb.end():]:
            return False
        if 'data-netlify' not in fa.group(0) or 'data-netlify' in fb.group(0):
            return False
        # same attributes once Netlify's two are removed
        def attrs(tag):
            return sorted(
                (k.lower(), v)
                for k, v in re.findall(r'([\w:-]+)\s*=\s*["\']([^"\']*)["\']', tag)
                if k.lower() not in ('data-netlify', 'netlify-honeypot'))
        if attrs(fa.group(0)) != attrs(fb.group(0)):
            return False
    return True


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SITES:
        raise SystemExit('usage: release_check.py <%s>' % '|'.join(SITES))
    key = sys.argv[1]
    canon = HOSTS[key]
    host = canon
    if '--url' in sys.argv:
        host = sys.argv[sys.argv.index('--url') + 1]
    live = '--no-live' not in sys.argv
    host = host.rstrip('/')
    only = None
    if '--deploy' in sys.argv:
        only = sys.argv[sys.argv.index('--deploy') + 1]
    draft = host != canon

    findings = []
    notes = []
    checked = 0

    # ---------------------------------------------------------- inventory --
    if only:
        from netlify_lib import API, curl  # noqa
        man = json.loads(curl(['%s/deploys/%s/files' % (API, only)]))
        dep_id = only
    else:
        dep_id, man = live_manifest(key)
    published = {f['path']: f['sha'] for f in man}
    local = local_paths(key)
    print('  published deploy %s : %d files' % (dep_id, len(published)))
    print('  local upload/            : %d files' % len(local))
    if not published:
        findings.append('published deploy has no files at all')
    for rel, sha in sorted(local.items()):
        checked += 1
        if rel not in published:
            findings.append('MISSING from the published deploy: %s' % rel)
        elif published[rel] != sha:
            benign = False
            if live and not draft and rel.endswith('.html'):
                url = host + (rel[:-len('index.html')] if rel.endswith('/index.html')
                              else rel)
                code, body = fetch(url)
                if code == 200:
                    lp = os.path.join(ROOT, key, 'upload', rel.lstrip('/'))
                    benign = netlify_form_rewrite_only(
                        io.open(lp, encoding='utf-8').read(), body)
            if benign:
                notes.append("sha differs from upload/ but only by Netlify's own "
                             'form rewrite, which is expected: %s' % rel)
            else:
                findings.append('sha differs from upload/: %s (live %s, local %s)'
                                % (rel, published[rel][:10], sha[:10]))

    # A path the deploy used to serve and no longer does is the exact shape of
    # the 09-07 regression, so it is reported even when upload/ never had it.
    inv = os.path.join(ROOT, key, 'tools', '%s_release.json' % key)
    prev = {}
    if os.path.exists(inv):
        prev = json.loads(io.open(inv, encoding='utf-8').read()).get('files', {})
    for rel in sorted(prev):
        if rel not in published:
            findings.append('DROPPED since the last recorded release: %s' % rel)

    # ------------------------------------------------------------- smoke --
    sm_path, urls = sitemap_urls(key)
    print('  sitemap                  : %s (%d urls)' % (sm_path, len(urls)))
    if not urls:
        print('\n  !! no sitemap URLs found: this check verified nothing')
        raise SystemExit(2)

    if live:
        titles = {}
        for u in urls:
            checked += 1
            path = u[len(canon):] if u.startswith(canon) else u
            code, body = fetch(host + path if draft else u)
            if code != 200:
                findings.append('HTTP %s  %s' % (code, path))
                continue
            if NETLIFY_404 in body:
                findings.append('200 but serving the Netlify 404 body: %s' % path)
                continue
            t = re.search(r'<title>(.*?)</title>', body, re.S)
            t = t.group(1).strip() if t else ''
            if not t:
                findings.append('no title: %s' % path)
            elif t in titles:
                findings.append('title duplicated with %s: %s' % (titles[t], path))
            else:
                titles[t] = path
            can = re.search(r'<link rel="canonical" href="([^"]+)"', body)
            if not can:
                findings.append('no canonical: %s' % path)
            elif can.group(1).rstrip('/') != u.rstrip('/'):
                findings.append('canonical points elsewhere (%s): %s'
                                % (can.group(1), path))
            n = len(re.findall(r'<h1[\s>]', body))
            if n != 1:
                findings.append('%d h1 elements: %s' % (n, path))
            print('    %s  %-58s %s' % (code, path, t[:52]))
    else:
        print('  (live smoke skipped)')

    # ------------------------------------------------------------ record --
    if not findings and live and not draft:
        io.open(inv, 'w', encoding='utf-8').write(json.dumps(
            {'deploy': dep_id, 'host': host, 'files': published}, indent=1))
        print('\n  release inventory recorded -> %s' % inv)

    print('\n  checks run: %d' % checked)
    if notes:
        print('  %d note(s), classified as expected rather than failed:' % len(notes))
        for n in notes:
            print('     - %s' % n)
    if checked == 0:
        print('  !! this check verified nothing, which is not a pass')
        raise SystemExit(2)
    if findings:
        print('\n  %d FINDING(S):' % len(findings))
        for f in findings:
            print('    !! %s' % f)
        raise SystemExit(1)
    print('  ALL CLEAR')
    return 0


main()
