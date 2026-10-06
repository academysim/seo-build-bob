# -*- coding: utf-8 -*-
"""Tests for shared/tools/check_staged.py.

Covers:
  - Empty inventory → fails (a gate that passes nothing is worse than no gate)
  - Missing inventory file → fails
  - A path from inventory no longer staged → fails (the loss case)
  - A new path not in inventory → note, not fail (adding pages is routine)
  - Empty staging directory → fails

Uses check_staged.verify() and check_staged.record() directly with ROOT patched
to a temp directory, so no real upload/ directories are touched.

Run:
  python -m unittest shared/tests/test_check_staged.py
  python -m unittest discover -s shared/tests
"""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, '..', 'tools'))
sys.path.insert(0, _TOOLS)
import check_staged as CS  # noqa: E402


def _write_file(path, data=b'x'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, bytes):
        with open(path, 'wb') as fh:
            fh.write(data)
    else:
        with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(data)


def _write_inventory(path, entries):
    """Write a JSON inventory file (list of '/'-prefixed paths)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(entries, indent=1) + '\n')


class _Base(unittest.TestCase):
    """Set up a scratch tree and patch CS.ROOT for each test."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._orig_root = CS.ROOT

    def tearDown(self):
        CS.ROOT = self._orig_root
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _inv_path(self, key):
        """Path where check_staged expects the inventory for key."""
        CS.ROOT = self.tmpdir
        return CS.inventory_path(key)

    def _upload_dir(self, key):
        return os.path.join(self.tmpdir, key, 'upload')

    def _populate_upload(self, key, filenames):
        """Create real files in <tmpdir>/<key>/upload/."""
        up = self._upload_dir(key)
        for rel in filenames:
            _write_file(os.path.join(up, rel.lstrip('/')))

    def _verify(self, keys=None):
        """Call CS.verify() with ROOT patched to tmpdir."""
        CS.ROOT = self.tmpdir
        CS.verify(keys or ['lounge'])

    def _record(self, keys=None):
        """Call CS.record() with ROOT patched to tmpdir."""
        CS.ROOT = self.tmpdir
        CS.record(keys or ['lounge'])


class TestMissingInventory(unittest.TestCase):
    """A missing inventory file fails — you cannot verify what was never recorded."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._orig_root = CS.ROOT

    def tearDown(self):
        CS.ROOT = self._orig_root
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_no_inventory_file_fails(self):
        """verify() with no inventory JSON → SystemExit (non-zero)."""
        up = os.path.join(self.tmpdir, 'lounge', 'upload')
        os.makedirs(up)
        _write_file(os.path.join(up, 'index.html'))

        CS.ROOT = self.tmpdir
        with self.assertRaises(SystemExit) as ctx:
            CS.verify(['lounge'])
        self.assertNotEqual(ctx.exception.code, 0)


class TestEmptyInventory(_Base):
    """An empty inventory file fails — it can never catch a missing file."""

    def test_empty_inventory_fails(self):
        """An inventory JSON with zero entries → SystemExit (non-zero)."""
        self._populate_upload('lounge', ['/index.html'])
        inv = self._inv_path('lounge')
        _write_inventory(inv, [])   # empty list

        with self.assertRaises(SystemExit) as ctx:
            self._verify()
        self.assertNotEqual(ctx.exception.code, 0)


class TestMissingPath(_Base):
    """A path recorded in the inventory that is no longer staged → fails."""

    def test_missing_path_fails(self):
        """inventory has /index.html and /about.html; upload/ only has /index.html."""
        self._populate_upload('lounge', ['/index.html'])
        inv = self._inv_path('lounge')
        _write_inventory(inv, ['/index.html', '/about.html'])

        with self.assertRaises(SystemExit) as ctx:
            self._verify()
        self.assertNotEqual(ctx.exception.code, 0,
            'verify() must fail when a recorded path is missing from upload/')


class TestNewPath(_Base):
    """A new path not in the inventory is a note, not a failure."""

    def test_new_path_is_note_not_failure(self):
        """upload/ has /index.html and /new-page.html; inventory only has /index.html."""
        self._populate_upload('lounge', ['/index.html', '/new-page.html'])
        inv = self._inv_path('lounge')
        _write_inventory(inv, ['/index.html'])

        # Must NOT raise
        try:
            self._verify()
        except SystemExit as exc:
            self.fail('verify() raised SystemExit for a new (additive) path: %s' % exc)


class TestEmptyStagingDir(_Base):
    """An empty upload/ directory fails — no staged files at all."""

    def test_empty_upload_fails(self):
        """upload/ exists but is empty → SystemExit (non-zero)."""
        up = self._upload_dir('lounge')
        os.makedirs(up)
        inv = self._inv_path('lounge')
        _write_inventory(inv, ['/index.html'])

        with self.assertRaises(SystemExit) as ctx:
            self._verify()
        self.assertNotEqual(ctx.exception.code, 0)


class TestGoldenPath(_Base):
    """All inventory paths present → passes cleanly."""

    def test_all_present_passes(self):
        """upload/ matches inventory exactly → no SystemExit."""
        paths = ['/index.html', '/sitemap.xml', '/netlify.toml']
        self._populate_upload('lounge', paths)
        inv = self._inv_path('lounge')
        _write_inventory(inv, paths)

        # Must NOT raise
        try:
            self._verify()
        except SystemExit as exc:
            self.fail('verify() raised unexpectedly: %s' % exc)


class TestRecord(_Base):
    """record() writes an inventory from what is currently in upload/."""

    def test_record_writes_inventory(self):
        """record() creates a JSON inventory from the current upload/ tree."""
        paths = ['/index.html', '/about.html']
        self._populate_upload('lounge', paths)
        # record() writes to <key>/tools/<key>_staged.json; create the dir
        os.makedirs(os.path.join(self.tmpdir, 'lounge', 'tools'), exist_ok=True)
        CS.ROOT = self.tmpdir
        CS.record(['lounge'])

        inv_path = CS.inventory_path('lounge')
        self.assertTrue(os.path.isfile(inv_path), 'inventory file should exist after record()')
        recorded = json.loads(io.open(inv_path, encoding='utf-8').read())
        self.assertEqual(sorted(recorded), sorted(paths))

    def test_record_refuses_empty_upload(self):
        """record() with empty upload/ → SystemExit (refuses to record nothing)."""
        up = self._upload_dir('lounge')
        os.makedirs(up)
        CS.ROOT = self.tmpdir
        with self.assertRaises(SystemExit):
            CS.record(['lounge'])


if __name__ == '__main__':
    unittest.main()
