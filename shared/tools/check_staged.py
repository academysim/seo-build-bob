# -*- coding: utf-8 -*-
"""Fail the build when a file that belongs in the deploy stops being staged.

Why this exists. F8 generalized stage.py from "*.html only" to an extension
allowlist, because the old rule silently dropped netlify.toml, both sitemap.xml
files, the membership images and driver's stylesheet from every rebuild. The
commit claimed a mutation test proved the new rule. An audit on 2026-09-09
reverted DEPLOYABLE to {'.html'} -- the exact pre-F8 regression -- and found
build_all.py exited 0 and all five property audits exited 0. Nothing caught it.
The property audits only read the HTML they find, so losing every non-HTML file
makes them pass FASTER. netlify.toml is the file whose loss on 2026-09-07 took
the security headers and a 301 with it.

So the guard cannot be "the audits pass". It has to be an explicit inventory,
recorded from a staging tree that was verified against live, and compared path
by path on every build.

  python check_staged.py                 verify all five (build_all runs this)
  python check_staged.py --record        rewrite the inventories from upload/

A missing path FAILS. A new path is reported and does not fail, because adding
a page is routine and this gate is about loss. An empty inventory, a missing
inventory file, or a property staging nothing FAILS -- a gate that passes when
handed nothing to check is worse than no gate at all.
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
KEYS = ['lounge', 'events', 'builds', 'driver', 'health']


def inventory_path(key):
    return os.path.join(ROOT, key, 'tools', '%s_staged.json' % key)


def staged(key):
    up = os.path.join(ROOT, key, 'upload')
    out = []
    for root, _, fs in os.walk(up):
        for f in fs:
            out.append('/' + os.path.relpath(os.path.join(root, f), up).replace(os.sep, '/'))
    return sorted(out)


def record(keys):
    for key in keys:
        paths = staged(key)
        if not paths:
            raise SystemExit('  !! %s: refusing to record an empty inventory' % key)
        io.open(inventory_path(key), 'w', encoding='utf-8', newline='\n').write(
            json.dumps(paths, indent=1) + '\n')
        print('%-7s recorded %d paths' % (key, len(paths)))


def verify(keys):
    bad = 0
    for key in keys:
        p = inventory_path(key)
        if not os.path.isfile(p):
            print('%-7s !! no inventory at %s; run --record' % (key, p))
            bad += 1
            continue
        expected = json.loads(io.open(p, encoding='utf-8').read())
        if not expected:
            print('%-7s !! inventory is empty, so it can never fail' % key)
            bad += 1
            continue
        now = staged(key)
        if not now:
            print('%-7s !! staged nothing' % key)
            bad += 1
            continue
        missing = [x for x in expected if x not in now]
        added = [x for x in now if x not in expected]
        for x in missing:
            print('%-7s !! NO LONGER STAGED: %s' % (key, x))
        for x in added:
            print('%-7s    new since the inventory: %s' % (key, x))
        if missing:
            bad += 1
        else:
            print('%-7s %3d/%d staged, nothing lost' % (key, len(now), len(expected)))
    if bad:
        raise SystemExit('  %d property(ies) LOST staged files' % bad)
    print('\n  nothing dropped from staging')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    keys = args or KEYS
    if '--record' in sys.argv:
        record(keys)
    else:
        verify(keys)
