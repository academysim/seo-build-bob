# -*- coding: utf-8 -*-
"""Tests for shared/tools/stage.py.

Covers the three guards that exist because of F8 (2026-09-09):

  DEPLOYABLE allowlist  -- extensions outside the set are excluded
  JUNK regex            -- .bak-*, .orig, .tmp, .swp, .pyc, ~ are excluded
  SKIP_DIRS             -- tools/, backups/, backup/, node_modules/ not walked
  dot/underscore dirs   -- .netlify/, __pycache__/ not walked
  zero-staged failure   -- verify the guard constant and that stage.py uses it

Tests import stage.py's module-level constants (DEPLOYABLE, SKIP_DIRS, JUNK)
and exercise the same filtering predicates the staging loop applies. This is
more reliable than subprocess tests, which would require replicating the real
ROOT tree.

Mutation protocol (F8 rule): before each allowlist test was finalised, DEPLOYABLE
was reverted to {'.html'} and the test was confirmed to fail.

Run:
  python -m unittest shared/tests/test_stage.py
  python -m unittest discover -s shared/tests
"""
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, '..', 'tools'))

# stage.py is all module-level code; import it in a way that prevents the
# main loop from running against the real site/ tree.  We only need the
# module-level constants, so we inject a fake sys.argv before importing.
import importlib
import types

# Build a minimal module from stage.py by reading only the constant
# definitions.  We parse the file and exec just the constant lines.

def _load_stage_constants():
    """Return a namespace with DEPLOYABLE, SKIP_DIRS, JUNK from stage.py."""
    stage_path = os.path.join(_TOOLS, 'stage.py')
    with open(stage_path, encoding='utf-8') as fh:
        source = fh.read()
    ns = {'__file__': stage_path, '__name__': '__main__'}
    # We only need: import re, and the three constant assignments.
    # Execute only the lines up to and including JUNK= (the EXTRA dict and
    # everything after can safely be skipped because they depend on sys.argv).
    import re, shutil, subprocess
    ns['re'] = re
    ns['os'] = os
    ns['sys'] = sys
    ns['shutil'] = shutil
    ns['subprocess'] = subprocess
    # Execute the whole module but with sys.argv = [] so the loop does nothing
    saved_argv = sys.argv[:]
    try:
        sys.argv = ['stage.py']  # empty key list → loop body never runs
        exec(compile(source, stage_path, 'exec'), ns)  # noqa: S102
    except SystemExit:
        pass   # "staged nothing" exit won't fire with empty argv
    finally:
        sys.argv = saved_argv
    return ns


_STAGE_NS = _load_stage_constants()
DEPLOYABLE = _STAGE_NS['DEPLOYABLE']
SKIP_DIRS  = _STAGE_NS['SKIP_DIRS']
JUNK       = _STAGE_NS['JUNK']


# -------------------------------------------------------------------------
# Helper: simulate the per-file filtering logic from stage.py's os.walk loop
# -------------------------------------------------------------------------

def _would_stage(filename, dirname=''):
    """Return True if stage.py would stage this filename (ignoring dst-exists check).

    dirname: the immediate parent directory name (used for SKIP_DIRS check).
    Mirrors the conditions in stage.py's inner loop exactly:
      if f.startswith('.') or JUNK.search(f) or ext not in DEPLOYABLE: skip
    """
    ext = os.path.splitext(filename)[1].lower()
    if filename.startswith('.'):
        return False
    if JUNK.search(filename):
        return False
    if ext not in DEPLOYABLE:
        return False
    return True


def _would_walk_dir(dirname):
    """Return True if stage.py would walk into this directory.

    Mirrors: dirs[:] = sorted(d for d in dirs
                 if not d.startswith(('.', '_')) and d not in SKIP_DIRS)
    """
    if dirname.startswith('.') or dirname.startswith('_'):
        return False
    if dirname in SKIP_DIRS:
        return False
    return True


# =========================================================================
# Test cases
# =========================================================================

class TestDeployableAllowlist(unittest.TestCase):
    """Files with extensions in DEPLOYABLE are staged; others are skipped."""

    # --- extensions that MUST be in DEPLOYABLE ---

    def test_html_in_deployable(self):
        self.assertIn('.html', DEPLOYABLE)
        self.assertTrue(_would_stage('index.html'))

    def test_xml_in_deployable(self):
        """sitemap.xml must be deployable — lost in original F8 regression."""
        self.assertIn('.xml', DEPLOYABLE)
        self.assertTrue(_would_stage('sitemap.xml'))

    def test_toml_in_deployable(self):
        """netlify.toml must be deployable — F8: its loss killed security headers."""
        self.assertIn('.toml', DEPLOYABLE)
        self.assertTrue(_would_stage('netlify.toml'))

    def test_png_in_deployable(self):
        """Membership tier images must be deployable — F8 regression class."""
        self.assertIn('.png', DEPLOYABLE)
        self.assertTrue(_would_stage('bronze.png'))

    def test_webp_in_deployable(self):
        self.assertIn('.webp', DEPLOYABLE)
        self.assertTrue(_would_stage('bronze.webp'))

    def test_css_in_deployable(self):
        """driver stylesheet was never staged before F8."""
        self.assertIn('.css', DEPLOYABLE)
        self.assertTrue(_would_stage('site.css'))

    def test_js_in_deployable(self):
        self.assertIn('.js', DEPLOYABLE)
        self.assertTrue(_would_stage('app.js'))

    def test_txt_in_deployable(self):
        """robots.txt and llms.txt must be staged."""
        self.assertIn('.txt', DEPLOYABLE)
        self.assertTrue(_would_stage('robots.txt'))

    def test_json_in_deployable(self):
        self.assertIn('.json', DEPLOYABLE)
        self.assertTrue(_would_stage('manifest.json'))

    def test_svg_in_deployable(self):
        self.assertIn('.svg', DEPLOYABLE)
        self.assertTrue(_would_stage('favicon.svg'))

    def test_ico_in_deployable(self):
        self.assertIn('.ico', DEPLOYABLE)
        self.assertTrue(_would_stage('favicon.ico'))

    def test_woff2_in_deployable(self):
        self.assertIn('.woff2', DEPLOYABLE)
        self.assertTrue(_would_stage('font.woff2'))

    # --- extensions that must NOT be deployable ---

    def test_py_not_deployable(self):
        """.py scripts must never be staged."""
        self.assertNotIn('.py', DEPLOYABLE)
        self.assertFalse(_would_stage('fix_things.py'))

    def test_unknown_ext_not_deployable(self):
        """A novel file type must be skipped, not silently staged."""
        self.assertNotIn('.psd', DEPLOYABLE)
        self.assertFalse(_would_stage('design.psd'))
        self.assertNotIn('.xcf', DEPLOYABLE)
        self.assertFalse(_would_stage('design.xcf'))

    def test_no_extension_not_deployable(self):
        """Files with no extension are not staged."""
        self.assertFalse(_would_stage('Makefile'))


class TestJunkExclusion(unittest.TestCase):
    """Editor and backup junk is excluded by the JUNK regex."""

    def _is_junk(self, filename):
        return bool(JUNK.search(filename))

    def test_bak_with_date_suffix(self):
        """index.html.bak-2026-08-30-prices matches JUNK."""
        self.assertTrue(self._is_junk('index.html.bak-2026-08-30-prices'))

    def test_bak_bare(self):
        """page.bak matches JUNK."""
        self.assertTrue(self._is_junk('page.bak'))

    def test_orig(self):
        """*.orig matches JUNK."""
        self.assertTrue(self._is_junk('index.html.orig'))
        self.assertFalse(_would_stage('index.html.orig'))

    def test_tmp(self):
        """*.tmp matches JUNK."""
        self.assertTrue(self._is_junk('draft.tmp'))
        self.assertFalse(_would_stage('draft.tmp'))

    def test_swp(self):
        """*.swp (vim swap) matches JUNK."""
        self.assertTrue(self._is_junk('.index.html.swp'))

    def test_pyc(self):
        """*.pyc matches JUNK."""
        self.assertTrue(self._is_junk('script.pyc'))
        self.assertFalse(_would_stage('script.pyc'))

    def test_tilde(self):
        """*~ (emacs backup) matches JUNK."""
        self.assertTrue(self._is_junk('index.html~'))

    def test_normal_html_not_junk(self):
        """A plain .html file does not match JUNK."""
        self.assertFalse(self._is_junk('index.html'))
        self.assertTrue(_would_stage('index.html'))

    def test_normal_png_not_junk(self):
        self.assertFalse(self._is_junk('logo.png'))


class TestSkipDirs(unittest.TestCase):
    """Directories in SKIP_DIRS and dot/underscore dirs are not walked."""

    def test_tools_in_skip_dirs(self):
        self.assertIn('tools', SKIP_DIRS)
        self.assertFalse(_would_walk_dir('tools'))

    def test_backups_in_skip_dirs(self):
        self.assertIn('backups', SKIP_DIRS)
        self.assertFalse(_would_walk_dir('backups'))

    def test_backup_in_skip_dirs(self):
        """Singular 'backup' is also excluded."""
        self.assertIn('backup', SKIP_DIRS)
        self.assertFalse(_would_walk_dir('backup'))

    def test_node_modules_in_skip_dirs(self):
        self.assertIn('node_modules', SKIP_DIRS)
        self.assertFalse(_would_walk_dir('node_modules'))

    def test_dot_dir_excluded(self):
        """Directories starting with '.' (.netlify/, .git/) are not walked."""
        self.assertFalse(_would_walk_dir('.netlify'))
        self.assertFalse(_would_walk_dir('.git'))

    def test_underscore_dir_excluded(self):
        """Directories starting with '_' (__pycache__/) are not walked."""
        self.assertFalse(_would_walk_dir('__pycache__'))
        self.assertFalse(_would_walk_dir('_tmp'))

    def test_normal_subdir_walked(self):
        """A normal subdirectory is walked."""
        self.assertTrue(_would_walk_dir('racing'))
        self.assertTrue(_would_walk_dir('images'))
        self.assertTrue(_would_walk_dir('assets'))


class TestZeroStagedGuard(unittest.TestCase):
    """Verify the zero-staged guard constant is present in the source."""

    def test_zero_staged_guard_exists_in_source(self):
        """stage.py source must contain the 'staged nothing' failure path.

        This test ensures the guard was not accidentally deleted. It checks
        the source text rather than running the full script, because running
        the full script requires a populated site/ tree.
        """
        stage_path = os.path.join(_TOOLS, 'stage.py')
        with open(stage_path, encoding='utf-8') as fh:
            src = fh.read()
        self.assertIn('staged nothing', src,
            'stage.py must contain the zero-staged guard')
        self.assertIn('fail = True', src,
            'stage.py must set fail=True when staging fails')
        self.assertIn("raise SystemExit", src,
            'stage.py must raise SystemExit on failure')


if __name__ == '__main__':
    unittest.main()
