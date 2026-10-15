# -*- coding: utf-8 -*-
"""Tests for shared/tools/verify_baseline.py.

Covers:
  - Golden path: all hashes match → check() returns no failures
  - Mutation: a site file is altered → check() reports CHANGED
  - Missing file: a site file is deleted → check() reports MISSING
  - Empty baseline: zero entries → SystemExit(2)
  - Malformed/blank lines are skipped, valid entries still checked
  - upload/ baseline: main() checks BOTH baselines; a mutation in upload/
    that passes the site baseline still exits 1 (regression gate for F8 class)
  - Extra file in upload/: a file not listed in the baseline → EXTRA failure
    and main() exits 1

Run:
  python -m unittest shared/tests/test_verify_baseline.py
  python -m unittest discover -s shared/tests
"""
import hashlib
import io
import os
import sys
import tempfile
import unittest

# Make shared/tools importable regardless of cwd
_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, '..', 'tools'))
sys.path.insert(0, _TOOLS)
import verify_baseline as VB  # noqa: E402


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as fh:
        fh.write(data)


class TestVerifyBaseline(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_baseline(self, entries, name='BASELINE.txt'):
        """Write a baseline file from {rel_path: bytes} and return its path."""
        baseline = os.path.join(self.tmpdir, name)
        lines = []
        for rel, data in entries.items():
            sha = _sha256(data)
            lines.append('%s *%s' % (sha, rel))
        with io.open(baseline, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(lines) + '\n')
        return baseline

    def _make_files(self, entries):
        """Write actual files under tmpdir from {rel_path: bytes}."""
        for rel, data in entries.items():
            abs_path = os.path.join(self.tmpdir, rel.replace('/', os.sep))
            _write(abs_path, data)

    def _check(self, baseline_path):
        """Call VB.check() with ROOT patched to self.tmpdir."""
        original_root = VB.ROOT
        try:
            VB.ROOT = self.tmpdir
            return VB.check(baseline_path)
        finally:
            VB.ROOT = original_root

    # ------------------------------------------------------------------
    # Golden path
    # ------------------------------------------------------------------

    def test_all_match(self):
        """All hashes correct → 0 failures."""
        content = {
            'a/index.html': b'<html>hello</html>',
            'b/index.html': b'<html>world</html>',
        }
        self._make_files(content)
        baseline = self._make_baseline(content)
        checked, failures = self._check(baseline)
        self.assertEqual(checked, 2)
        self.assertEqual(failures, [])

    # ------------------------------------------------------------------
    # Mutation test (the important one per the F8 protocol)
    # ------------------------------------------------------------------

    def test_changed_file_reported(self):
        """A file whose bytes differ from the baseline → CHANGED in failures."""
        content = {'site/index.html': b'original content'}
        self._make_files(content)
        baseline = self._make_baseline(content)

        # Now silently alter the file on disk
        altered_path = os.path.join(self.tmpdir, 'site', 'index.html')
        with open(altered_path, 'wb') as fh:
            fh.write(b'ALTERED content')

        checked, failures = self._check(baseline)
        self.assertEqual(checked, 1)
        self.assertEqual(len(failures), 1)
        status, path = failures[0]
        self.assertEqual(status, 'CHANGED')
        self.assertIn('index.html', path)

    def test_changed_file_exits_1(self):
        """main() exits 1 when there is a mismatch."""
        content = {'site/page.html': b'<p>original</p>'}
        self._make_files(content)
        baseline = self._make_baseline(content)
        # Alter the file on disk (mutation test)
        p = os.path.join(self.tmpdir, 'site', 'page.html')
        with open(p, 'wb') as fh:
            fh.write(b'<p>TAMPERED</p>')

        original_root, original_baseline, original_upload = (
            VB.ROOT, VB.BASELINE, VB.BASELINE_UPLOAD)
        try:
            VB.ROOT = self.tmpdir
            VB.BASELINE = baseline
            # upload baseline: a small valid second baseline so main() doesn't
            # exit(2) before reaching the site failure; use a distinct name
            # to avoid overwriting the site baseline file on disk.
            upload_content = {'lounge/upload/f.html': b'<html/>'}
            self._make_files(upload_content)
            VB.BASELINE_UPLOAD = self._make_baseline(upload_content,
                                                     name='BASELINE-upload.txt')
            with self.assertRaises(SystemExit) as ctx:
                VB.main()
            self.assertEqual(ctx.exception.code, 1)
        finally:
            VB.ROOT = original_root
            VB.BASELINE = original_baseline
            VB.BASELINE_UPLOAD = original_upload

    # ------------------------------------------------------------------
    # Missing file
    # ------------------------------------------------------------------

    def test_missing_file_reported(self):
        """A file recorded in the baseline but absent on disk → MISSING."""
        content = {'site/exists.html': b'here'}
        self._make_files(content)
        # Add a second entry to the baseline that has no file on disk
        baseline = os.path.join(self.tmpdir, 'BASELINE.txt')
        sha_exists = _sha256(b'here')
        sha_ghost = _sha256(b'ghost')
        with io.open(baseline, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('%s *site/exists.html\n' % sha_exists)
            fh.write('%s *site/ghost.html\n' % sha_ghost)

        checked, failures = self._check(baseline)
        self.assertEqual(checked, 2)
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0][0], 'MISSING')

    # ------------------------------------------------------------------
    # Empty baseline → exit 2
    # ------------------------------------------------------------------

    def test_empty_baseline_exits_2(self):
        """An empty baseline file → SystemExit(2). A gate checking nothing must not pass."""
        baseline = os.path.join(self.tmpdir, 'empty.txt')
        with open(baseline, 'w') as fh:
            fh.write('\n')  # only blank lines

        original_root = VB.ROOT
        try:
            VB.ROOT = self.tmpdir
            with self.assertRaises(SystemExit) as ctx:
                VB.check(baseline)
            self.assertEqual(ctx.exception.code, 2)
        finally:
            VB.ROOT = original_root

    def test_missing_baseline_exits_2(self):
        """A non-existent baseline file → SystemExit(2)."""
        original_root = VB.ROOT
        try:
            VB.ROOT = self.tmpdir
            with self.assertRaises(SystemExit) as ctx:
                VB.check(os.path.join(self.tmpdir, 'no-such-file.txt'))
            self.assertEqual(ctx.exception.code, 2)
        finally:
            VB.ROOT = original_root

    # ------------------------------------------------------------------
    # Skips blank / malformed lines, counts only valid entries
    # ------------------------------------------------------------------

    def test_blank_lines_skipped(self):
        """Blank lines do not contribute to the checked count."""
        content = {'x/a.html': b'aaa'}
        self._make_files(content)
        baseline = os.path.join(self.tmpdir, 'BASELINE.txt')
        sha = _sha256(b'aaa')
        with io.open(baseline, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n')
            fh.write('%s *x/a.html\n' % sha)
            fh.write('\n')

        checked, failures = self._check(baseline)
        self.assertEqual(checked, 1)
        self.assertEqual(failures, [])

    def test_multiple_failures_all_reported(self):
        """Every failing file is reported, not just the first."""
        content = {
            'p1/index.html': b'p1',
            'p2/index.html': b'p2',
            'p3/index.html': b'p3',
        }
        self._make_files(content)
        baseline = self._make_baseline(content)
        # Alter two of three files
        for rel in ('p1/index.html', 'p3/index.html'):
            p = os.path.join(self.tmpdir, rel.replace('/', os.sep))
            with open(p, 'wb') as fh:
                fh.write(b'altered')

        checked, failures = self._check(baseline)
        self.assertEqual(checked, 3)
        self.assertEqual(len(failures), 2)
        statuses = {s for s, _ in failures}
        self.assertEqual(statuses, {'CHANGED'})

    # ------------------------------------------------------------------
    # Upload baseline: main() must catch mutations in upload/ even when
    # site/ is clean  (the gap that motivated BASELINE-upload-hashes.txt)
    # ------------------------------------------------------------------

    def test_upload_mutation_caught_by_main(self):
        """A mutation in upload/ that passes the site baseline still exits 1.

        This is the regression test for the gap: verify_baseline.py used to
        check only */site/, so add_hub_links/fix_* patches to upload/ could
        regress without the gate catching it.
        """
        site_content = {'lounge/site/index.html': b'<html>site</html>'}
        upload_content = {'lounge/upload/index.html': b'<html>upload</html>'}
        self._make_files(site_content)
        self._make_files(upload_content)
        site_baseline = self._make_baseline(site_content)
        upload_baseline = self._make_baseline(upload_content)

        # Tamper with the upload file only — site is still clean
        p = os.path.join(self.tmpdir, 'lounge', 'upload', 'index.html')
        with open(p, 'wb') as fh:
            fh.write(b'<html>TAMPERED upload</html>')

        original_root, original_baseline, original_upload = (
            VB.ROOT, VB.BASELINE, VB.BASELINE_UPLOAD)
        try:
            VB.ROOT = self.tmpdir
            VB.BASELINE = site_baseline
            VB.BASELINE_UPLOAD = upload_baseline
            with self.assertRaises(SystemExit) as ctx:
                VB.main()
            self.assertEqual(ctx.exception.code, 1)
        finally:
            VB.ROOT = original_root
            VB.BASELINE = original_baseline
            VB.BASELINE_UPLOAD = original_upload

    def test_upload_mutation_not_caught_without_upload_baseline(self):
        """Confirm the gap: check() on site baseline alone misses upload/ mutations.

        This test documents WHY BASELINE-upload-hashes.txt was added. If only
        the site baseline is checked, an upload/ mutation goes undetected.
        """
        site_content = {'lounge/site/index.html': b'<html>site</html>'}
        upload_content = {'lounge/upload/index.html': b'<html>upload</html>'}
        self._make_files(site_content)
        self._make_files(upload_content)
        site_baseline = self._make_baseline(site_content)

        # Tamper with upload only
        p = os.path.join(self.tmpdir, 'lounge', 'upload', 'index.html')
        with open(p, 'wb') as fh:
            fh.write(b'<html>TAMPERED upload</html>')

        # check() against site baseline alone sees no failures — the gap
        checked, failures = self._check(site_baseline)
        self.assertEqual(failures, [], 'site-only check missed the upload mutation (expected)')

    # ------------------------------------------------------------------
    # Extra file in upload/ → EXTRA failure and main() exits 1
    # ------------------------------------------------------------------

    def test_extra_file_in_upload_reported(self):
        """A file present in upload/ but absent from the baseline → EXTRA failure."""
        upload_content = {'lounge/upload/index.html': b'<html/>'}
        self._make_files(upload_content)
        baseline = self._make_baseline(upload_content)

        # Drop an extra file into upload/ that is NOT in the baseline
        extra_path = os.path.join(self.tmpdir, 'lounge', 'upload', 'stowaway.html')
        with open(extra_path, 'wb') as fh:
            fh.write(b'<html>extra</html>')

        original_root = VB.ROOT
        try:
            VB.ROOT = self.tmpdir
            checked, failures = VB.check(baseline, check_extra=True)
        finally:
            VB.ROOT = original_root

        self.assertEqual(checked, 1)
        self.assertEqual(len(failures), 1)
        status, path = failures[0]
        self.assertEqual(status, 'EXTRA')
        self.assertIn('stowaway.html', path)

    def test_extra_file_in_upload_exits_1(self):
        """main() exits 1 when upload/ contains a file not listed in the baseline."""
        site_content = {'lounge/site/index.html': b'<html>site</html>'}
        upload_content = {'lounge/upload/index.html': b'<html>upload</html>'}
        self._make_files(site_content)
        self._make_files(upload_content)
        site_baseline = self._make_baseline(site_content)
        upload_baseline = self._make_baseline(upload_content, name='BASELINE-upload.txt')

        # Add an extra file to upload/ that is NOT recorded in upload_baseline
        extra_path = os.path.join(self.tmpdir, 'lounge', 'upload', 'intruder.html')
        with open(extra_path, 'wb') as fh:
            fh.write(b'<html>intruder</html>')

        original_root, original_baseline, original_upload = (
            VB.ROOT, VB.BASELINE, VB.BASELINE_UPLOAD)
        try:
            VB.ROOT = self.tmpdir
            VB.BASELINE = site_baseline
            VB.BASELINE_UPLOAD = upload_baseline
            with self.assertRaises(SystemExit) as ctx:
                VB.main()
            self.assertEqual(ctx.exception.code, 1)
        finally:
            VB.ROOT = original_root
            VB.BASELINE = original_baseline
            VB.BASELINE_UPLOAD = original_upload


if __name__ == '__main__':
    unittest.main()
