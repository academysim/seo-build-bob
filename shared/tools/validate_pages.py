# -*- coding: utf-8 -*-
"""Quick sanity check for a directory of HTML pages: h1 count, tag balance,
em dash in body, target string presence. Usage:
  python validate_pages.py <dir> [required_substring]
"""
import io, os, re, sys

target = os.path.normpath(sys.argv[1])
needle = sys.argv[2] if len(sys.argv) > 2 else None

probs_all = {}
count = 0
for root, _, fs in os.walk(target):
    for f in fs:
        if f != 'index.html':
            continue
        p = os.path.join(root, f)
        count += 1
        s = io.open(p, encoding='utf-8').read()
        body = s.partition('<main>')[2].partition('</main>')[0] or s
        body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
        body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
        probs = []
        if re.search(r'&mdash;|—', body):
            probs.append('em dash in main/body')
        h1 = s.count('<h1')
        if h1 != 1:
            probs.append('h1=%d' % h1)
        for tag in ['div', 'section', 'p']:
            o = len(re.findall(r'<' + tag + r'[ >]', s))
            c = s.count('</' + tag + '>')
            if o != c:
                probs.append('%s %d/%d' % (tag, o, c))
        if needle and needle not in s:
            probs.append('missing needle: %s' % needle)
        if probs:
            probs_all[os.path.relpath(p, target)] = probs

print('checked %d pages under %s' % (count, target))
if probs_all:
    for rel, probs in sorted(probs_all.items()):
        print('  !! %s : %s' % (rel, '; '.join(probs)))
    sys.exit(1)
print('ALL OK')
