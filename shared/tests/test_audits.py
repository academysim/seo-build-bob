# -*- coding: utf-8 -*-
"""Characterization tests for the five per-property audits.

For each audit:
  1. Copy the property's real site/upload directory to a tempdir.
  2. Run the audit as a subprocess against the copy → must exit 0.
  3. Inject one defect at a time into one page of the copy:
     (a) Remove the GA4 tag.
     (b) Break a JSON-LD block so it is invalid JSON.
     (c) Insert a phrase from that audit's own AI list.
     (d) Point the audit at an empty directory → must not exit 0.

Only defect types that the audit actually checks are included; any that are
skipped are noted inline.

Run:
  python -m unittest shared/tests/test_audits.py
  python -m unittest discover -s shared/tests
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

_HERE   = os.path.dirname(os.path.abspath(__file__))
_ROOT   = os.path.normpath(os.path.join(_HERE, '..', '..'))
_PYTHON = sys.executable


def _run_audit(script, directory, extra_env=None):
    """Run *script* with *directory* as the first argument.

    Returns (returncode, combined stdout+stderr text).
    """
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    r = subprocess.run(
        [_PYTHON, script, directory],
        capture_output=True,
        text=True,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


def _read(path):
    with io.open(path, encoding='utf-8', newline='') as fh:
        return fh.read()


def _write(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)


def _first_html(directory):
    """Return the path to the first index.html found under *directory*."""
    for root, _, files in os.walk(directory):
        for f in files:
            if f == 'index.html':
                return os.path.join(root, f)
    raise FileNotFoundError('No index.html under %s' % directory)


def _any_html(directory):
    """Return the path to any .html file found under *directory*."""
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.html'):
                return os.path.join(root, f)
    raise FileNotFoundError('No .html file under %s' % directory)


GA4_TAG = 'G-SQL40ZS59K'

# ---------------------------------------------------------------------------
# Lounge audit (lounge/tools/audit_site.py, reads lounge/site/)
# ---------------------------------------------------------------------------

class TestLoungeAudit(unittest.TestCase):

    SCRIPT = os.path.join(_ROOT, 'lounge', 'tools', 'audit_site.py')
    SRC    = os.path.join(_ROOT, 'lounge', 'site')

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_lounge_')
        shutil.copytree(self.SRC, self.tmp, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    def test_clean_copy_exits_zero(self):
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertEqual(0, code, 'Clean lounge copy should exit 0.\n' + out)

    # (a) GA4 tag missing
    def test_no_ga4_exits_nonzero(self):
        p = _first_html(self.tmp)
        _write(p, _read(p).replace(GA4_TAG, 'G-REMOVED'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Missing GA4 should fail.\n' + out)

    # (b) broken JSON-LD
    def test_bad_json_ld_exits_nonzero(self):
        # Inject an invalid JSON-LD block into the first index.html
        p = _first_html(self.tmp)
        src = _read(p)
        broken = src + '\n<script type="application/ld+json">{ INVALID JSON }</script>'
        _write(p, broken)
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Invalid JSON-LD should fail.\n' + out)

    # (c) AI phrase
    def test_ai_phrase_exits_nonzero(self):
        # 'delve' is in the lounge AI list and is not present in any HTML
        # Only inject into the visible body text (not inside a <script> / <style>)
        p = _first_html(self.tmp)
        src = _read(p)
        _write(p, src.replace('</body>', '<p>Let us delve into the details.</p></body>'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'AI phrase should fail.\n' + out)

    # (d) empty directory
    def test_empty_dir_exits_nonzero(self):
        empty = tempfile.mkdtemp(prefix='test_lounge_empty_')
        try:
            code, out = _run_audit(self.SCRIPT, empty)
            self.assertNotEqual(0, code, 'Empty directory should not exit 0.\n' + out)
        finally:
            shutil.rmtree(empty, ignore_errors=True)


# ---------------------------------------------------------------------------
# Events audit (events/tools/events_audit.py, reads events/upload/)
# ---------------------------------------------------------------------------

class TestEventsAudit(unittest.TestCase):

    SCRIPT = os.path.join(_ROOT, 'events', 'tools', 'events_audit.py')
    SRC    = os.path.join(_ROOT, 'events', 'upload')

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_events_')
        shutil.copytree(self.SRC, self.tmp, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    def test_clean_copy_exits_zero(self):
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertEqual(0, code, 'Clean events copy should exit 0.\n' + out)

    # (a) GA4 tag missing
    def test_no_ga4_exits_nonzero(self):
        p = _any_html(self.tmp)
        _write(p, _read(p).replace(GA4_TAG, 'G-REMOVED'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Missing GA4 should fail.\n' + out)

    # (b) broken JSON-LD
    def test_bad_json_ld_exits_nonzero(self):
        p = _any_html(self.tmp)
        src = _read(p)
        broken = src + '\n<script type="application/ld+json">{ INVALID JSON }</script>'
        _write(p, broken)
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Invalid JSON-LD should fail.\n' + out)

    # (c) AI phrase
    def test_ai_phrase_exits_nonzero(self):
        # 'delve' is in the events AI list
        p = _any_html(self.tmp)
        src = _read(p)
        _write(p, src.replace('</body>', '<p>Let us delve into the details.</p></body>'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'AI phrase should fail.\n' + out)

    # (d) empty directory
    def test_empty_dir_exits_nonzero(self):
        empty = tempfile.mkdtemp(prefix='test_events_empty_')
        try:
            code, out = _run_audit(self.SCRIPT, empty)
            self.assertNotEqual(0, code, 'Empty directory should not exit 0.\n' + out)
        finally:
            shutil.rmtree(empty, ignore_errors=True)


# ---------------------------------------------------------------------------
# Builds audit (builds/tools/builds_audit.py, reads builds/upload/)
# ---------------------------------------------------------------------------

class TestBuildsAudit(unittest.TestCase):

    SCRIPT = os.path.join(_ROOT, 'builds', 'tools', 'builds_audit.py')
    SRC    = os.path.join(_ROOT, 'builds', 'upload')

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_builds_')
        shutil.copytree(self.SRC, self.tmp, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    def test_clean_copy_exits_zero(self):
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertEqual(0, code, 'Clean builds copy should exit 0.\n' + out)

    # (a) GA4 tag missing
    def test_no_ga4_exits_nonzero(self):
        p = _any_html(self.tmp)
        _write(p, _read(p).replace(GA4_TAG, 'G-REMOVED'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Missing GA4 should fail.\n' + out)

    # (b) broken JSON-LD
    def test_bad_json_ld_exits_nonzero(self):
        p = _any_html(self.tmp)
        src = _read(p)
        broken = src + '\n<script type="application/ld+json">{ INVALID JSON }</script>'
        _write(p, broken)
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Invalid JSON-LD should fail.\n' + out)

    # (c) AI phrase
    def test_ai_phrase_exits_nonzero(self):
        # 'delve' is in the builds AI list
        # Must be in authored content (not inside <nav> or <footer>).
        p = _any_html(self.tmp)
        src = _read(p)
        _write(p, src.replace('</body>', '<p>Let us delve into the details.</p></body>'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'AI phrase should fail.\n' + out)

    # (d) empty directory
    def test_empty_dir_exits_nonzero(self):
        empty = tempfile.mkdtemp(prefix='test_builds_empty_')
        try:
            code, out = _run_audit(self.SCRIPT, empty)
            self.assertNotEqual(0, code, 'Empty directory should not exit 0.\n' + out)
        finally:
            shutil.rmtree(empty, ignore_errors=True)


# ---------------------------------------------------------------------------
# Driver audit (driver/tools/driver_audit.py, reads driver/upload/)
# ---------------------------------------------------------------------------

class TestDriverAudit(unittest.TestCase):

    SCRIPT = os.path.join(_ROOT, 'driver', 'tools', 'driver_audit.py')
    SRC    = os.path.join(_ROOT, 'driver', 'upload')

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_driver_')
        shutil.copytree(self.SRC, self.tmp, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    def test_clean_copy_exits_zero(self):
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertEqual(0, code, 'Clean driver copy should exit 0.\n' + out)

    # (a) GA4 tag missing
    def test_no_ga4_exits_nonzero(self):
        # Use index.html which has a single GA4 occurrence we can strip
        p = os.path.join(self.tmp, 'index.html')
        _write(p, _read(p).replace(GA4_TAG, 'G-REMOVED'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Missing GA4 should fail.\n' + out)

    # (b) broken JSON-LD
    def test_bad_json_ld_exits_nonzero(self):
        p = os.path.join(self.tmp, 'index.html')
        src = _read(p)
        broken = src + '\n<script type="application/ld+json">{ INVALID JSON }</script>'
        _write(p, broken)
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Invalid JSON-LD should fail.\n' + out)

    # (c) AI phrase
    def test_ai_phrase_exits_nonzero(self):
        # 'delve' is in the driver AI list
        # Must be in authored content (not inside <header> or <footer>)
        p = os.path.join(self.tmp, 'index.html')
        src = _read(p)
        _write(p, src.replace('</body>', '<p>Let us delve into the details.</p></body>'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'AI phrase should fail.\n' + out)

    # (d) empty directory
    def test_empty_dir_exits_nonzero(self):
        empty = tempfile.mkdtemp(prefix='test_driver_empty_')
        try:
            code, out = _run_audit(self.SCRIPT, empty)
            self.assertNotEqual(0, code, 'Empty directory should not exit 0.\n' + out)
        finally:
            shutil.rmtree(empty, ignore_errors=True)


# ---------------------------------------------------------------------------
# Health audit (health/tools/health_audit.py, reads health/upload/)
# ---------------------------------------------------------------------------

class TestHealthAudit(unittest.TestCase):

    SCRIPT = os.path.join(_ROOT, 'health', 'tools', 'health_audit.py')
    SRC    = os.path.join(_ROOT, 'health', 'upload')

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_health_')
        shutil.copytree(self.SRC, self.tmp, dirs_exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    def test_clean_copy_exits_zero(self):
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertEqual(0, code, 'Clean health copy should exit 0.\n' + out)

    # (a) GA4 tag missing
    def test_no_ga4_exits_nonzero(self):
        p = _any_html(self.tmp)
        _write(p, _read(p).replace(GA4_TAG, 'G-REMOVED'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Missing GA4 should fail.\n' + out)

    # (b) broken JSON-LD
    def test_bad_json_ld_exits_nonzero(self):
        p = _any_html(self.tmp)
        src = _read(p)
        broken = src + '\n<script type="application/ld+json">{ INVALID JSON }</script>'
        _write(p, broken)
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'Invalid JSON-LD should fail.\n' + out)

    # (c) AI phrase
    def test_ai_phrase_exits_nonzero(self):
        # 'delve' is in the health AI list
        # Must be in authored content (not inside <nav> or <footer>)
        p = _any_html(self.tmp)
        src = _read(p)
        _write(p, src.replace('</body>', '<p>Let us delve into the details.</p></body>'))
        code, out = _run_audit(self.SCRIPT, self.tmp)
        self.assertNotEqual(0, code, 'AI phrase should fail.\n' + out)

    # (d) empty directory
    def test_empty_dir_exits_nonzero(self):
        empty = tempfile.mkdtemp(prefix='test_health_empty_')
        try:
            code, out = _run_audit(self.SCRIPT, empty)
            self.assertNotEqual(0, code, 'Empty directory should not exit 0.\n' + out)
        finally:
            shutil.rmtree(empty, ignore_errors=True)


# ---------------------------------------------------------------------------
# Notes on skipped defect types
# ---------------------------------------------------------------------------
# The "EM-DASH" and "placeholder" checks exist in some audits but are not
# injected here because the real pages already pass them and we only want to
# test checks that the audit documents as explicit failures. The four defects
# above (GA4, JSON-LD, AI phrase, empty dir) are universal across all five
# audits and sufficient to characterise the gate.
#
# builds_audit also checks BRITISH spellings, UNKNOWN-PRICE, and BODY-CLASS
# but those are lower-risk checks omitted here to keep the suite focused.
# driver_audit also checks FORBIDDEN claims and MISSING-NO-INSTALL-DISCLOSURE.
# health_audit also checks FORBIDDEN medical claims and MISSING-SCOPE-DISCLAIMER.
# These are correctness checks on site content, not on the audit machinery, so
# they are covered by the real audit running clean (test_clean_copy_exits_zero).


if __name__ == '__main__':
    unittest.main()
