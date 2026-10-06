# -*- coding: utf-8 -*-
"""Verify every file in both baseline manifests is byte-identical to disk.

Two baselines are checked:
  BASELINE-site-hashes.txt   -- every versioned file under */site/
  BASELINE-upload-hashes.txt -- every shippable artefact under */upload/
                                (recorded from the build at commit 8e5768e)

Run after every refactor step to confirm no output changed.

  python shared/tools/verify_baseline.py            # check both
  python shared/tools/verify_baseline.py --quiet    # only print failures

Exit codes:
  0   all hashes match (both baselines)
  1   one or more files CHANGED or MISSING
  2   zero files checked (empty baseline or baseline not found)
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
BASELINE        = os.path.join(ROOT, 'BASELINE-site-hashes.txt')
BASELINE_UPLOAD = os.path.join(ROOT, 'BASELINE-upload-hashes.txt')

QUIET = '--quiet' in sys.argv


def check(baseline_path):
    """Check all entries in one baseline file. Returns (checked, failures).

    failures is a list of (status, path) where status is 'CHANGED' or 'MISSING'.
    """
    if not os.path.isfile(baseline_path):
        print('!! baseline file not found: %s' % baseline_path)
        raise SystemExit(2)

    entries = []
    with io.open(baseline_path, encoding='utf-8') as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            # format:  <sha256hex> *<path>
            space = line.find(' ')
            if space < 0 or not line[space:].startswith(' *'):
                print('!! line %d: unrecognised format: %r' % (lineno, line[:80]))
                continue
            sha_expected = line[:space]
            rel_path = line[space + 2:]   # strip ' *'
            entries.append((sha_expected, rel_path))

    if not entries:
        print('!! baseline is empty — checked zero files')
        raise SystemExit(2)

    failures = []
    for sha_expected, rel_path in entries:
        abs_path = os.path.normpath(os.path.join(ROOT, rel_path.replace('/', os.sep)))
        if not os.path.isfile(abs_path):
            failures.append(('MISSING', rel_path))
            if not QUIET:
                print('MISSING : %s' % rel_path)
            continue
        with io.open(abs_path, 'rb') as fh:
            sha_got = hashlib.sha256(fh.read()).hexdigest()
        if sha_got != sha_expected:
            failures.append(('CHANGED', rel_path))
            if not QUIET:
                print('CHANGED : %s' % rel_path)

    return len(entries), failures


def main():
    all_checked = 0
    all_failures = []

    # --- site baseline ---
    checked, failures = check(BASELINE)
    all_checked += checked
    all_failures.extend(failures)
    if not failures and not QUIET:
        print('OK  %d files match BASELINE-site-hashes.txt' % checked)

    # --- upload baseline ---
    checked2, failures2 = check(BASELINE_UPLOAD)
    all_checked += checked2
    all_failures.extend(failures2)
    if not failures2 and not QUIET:
        print('OK  %d files match BASELINE-upload-hashes.txt' % checked2)

    if all_failures:
        print('\n%d/%d files FAILED' % (len(all_failures), all_checked))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
