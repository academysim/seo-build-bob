# -*- coding: utf-8 -*-
"""Tests for shared/tools/release_check.py — HTTP logic, offline.

Import strategy
---------------
release_check.py calls main() unconditionally at the module bottom (line 253).
main() calls sys.exit() unless a valid key argument is present and the Netlify
token file exists.  Importing the module via a normal ``import`` would kill the
test runner.

We use the same AST-extraction approach as test_netlify_form_rewrite.py: read
the source, compile only the nodes that fetch() depends on, and exec() those
into a throwaway namespace.  No network calls, no subprocess, no Netlify token.

The four scenarios covered:
  1. Healthy (200)  — fetch returns (200, body).
  2. 404 page       — fetch returns (404, body).
  3. Redirect (301) — curl follows redirects; the status embedded in the
                      __STATUS__ trailer is the final code.  We simulate a
                      redirect that lands on a 301 (i.e. curl did NOT follow).
  4. Timeout        — curl returns an empty stdout; fetch returns (0, '').

Run:
    python -m unittest shared/tests/test_release_check.py
    python -m unittest discover -s shared/tests
"""
import ast
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
_RC_PATH = os.path.join(_ROOT, 'shared', 'tools', 'release_check.py')


def _load_fetch_fn():
    """Return the fetch() function from release_check.py without executing main()."""
    with open(_RC_PATH, encoding='utf-8') as f:
        src = f.read()
    tree = ast.parse(src, filename=_RC_PATH)

    # Collect just the fetch() function definition.
    needed = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'fetch':
            needed.append(node)

    mini = ast.Module(body=needed, type_ignores=[])
    ast.fix_missing_locations(mini)

    import subprocess as _subprocess
    ns = {'subprocess': _subprocess}
    exec(compile(mini, _RC_PATH, 'exec'), ns)   # noqa: S102 (our own source)
    return ns['fetch']


_fetch = _load_fetch_fn()


def _make_proc_result(stdout_bytes):
    """Return a mock CompletedProcess whose .stdout is stdout_bytes."""
    result = MagicMock()
    result.stdout = stdout_bytes
    return result


class TestReleaseCheckFetch(unittest.TestCase):
    """Unit tests for the fetch() function in release_check.py.

    fetch() shells out to curl.exe and parses the __STATUS__ trailer it
    appends via -w '\\n__STATUS__%{http_code}'.  We mock subprocess.run so
    no real network call is made.
    """

    def _run(self, raw_stdout_str):
        """Call _fetch with subprocess.run mocked to return raw_stdout_str."""
        encoded = raw_stdout_str.encode('utf-8')
        mock_result = _make_proc_result(encoded)
        with patch('subprocess.run', return_value=mock_result) as mock_run:
            status, body = _fetch('http://example.invalid/page')
        mock_run.assert_called_once()
        return status, body

    # ------------------------------------------------------------------
    # 1. Healthy 200
    # ------------------------------------------------------------------

    def test_healthy_200(self):
        """A 200 response with a real body is parsed correctly."""
        raw = '<html><h1>Hello</h1></html>\n__STATUS__200'
        status, body = self._run(raw)
        self.assertEqual(200, status)
        self.assertIn('<h1>Hello</h1>', body)

    # ------------------------------------------------------------------
    # 2. 404 page
    # ------------------------------------------------------------------

    def test_404_page(self):
        """A 404 response returns status 404 and the body text."""
        raw = 'Page not found\n__STATUS__404'
        status, body = self._run(raw)
        self.assertEqual(404, status)
        self.assertIn('Page not found', body)

    # ------------------------------------------------------------------
    # 3. Redirect (301)
    # ------------------------------------------------------------------

    def test_redirect_301(self):
        """A 301 redirect (curl not following it) returns status 301."""
        raw = '\n__STATUS__301'
        status, body = self._run(raw)
        self.assertEqual(301, status)

    # ------------------------------------------------------------------
    # 4. Timeout / empty response
    # ------------------------------------------------------------------

    def test_timeout_returns_zero_status(self):
        """When curl times out it returns empty stdout; fetch returns (0, '')."""
        encoded = b''
        mock_result = _make_proc_result(encoded)
        with patch('subprocess.run', return_value=mock_result):
            status, body = _fetch('http://example.invalid/slow')
        self.assertEqual(0, status)
        self.assertEqual('', body)

    # ------------------------------------------------------------------
    # Edge: missing __STATUS__ trailer
    # ------------------------------------------------------------------

    def test_missing_status_trailer_returns_zero(self):
        """If curl produces output without the trailer, status is 0."""
        raw = 'some partial output with no status marker'
        status, body = self._run(raw)
        self.assertEqual(0, status)


if __name__ == '__main__':
    unittest.main()
