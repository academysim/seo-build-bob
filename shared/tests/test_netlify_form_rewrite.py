# -*- coding: utf-8 -*-
"""Tests for netlify_form_rewrite_only() in shared/tools/release_check.py.

Import strategy
---------------
release_check.py calls main() unconditionally at the module bottom (line 253).
main() calls sys.exit() unless exactly one valid key argument is present.
Importing the module via a normal ``import`` therefore kills the test runner.

To access only the pure function we need, we read the module source and exec()
just the definitions that netlify_form_rewrite_only depends on (re and the
function itself), leaving main() un-called.  No network calls are made.

We verified (by reading shared/tools/release_check.py lines 82-124) that
netlify_form_rewrite_only() uses only ``re`` and its two string arguments —
no I/O, no subprocess, no network.

Run:
    python -m unittest shared/tests/test_netlify_form_rewrite.py
    python -m unittest discover -s shared/tests
"""
import ast
import os
import re
import sys
import types
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
_RC_PATH = os.path.join(_ROOT, 'shared', 'tools', 'release_check.py')


def _load_form_rewrite_fn():
    """Return netlify_form_rewrite_only extracted from release_check.py source
    without executing the file (and thus without calling main())."""
    with open(_RC_PATH, encoding='utf-8') as f:
        src = f.read()
    tree = ast.parse(src, filename=_RC_PATH)

    # Collect top-level nodes that netlify_form_rewrite_only needs:
    #   - the FORM_OPEN assignment (re.compile used by the function)
    #   - the function definition itself
    needed = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == 'FORM_OPEN':
                    needed.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == 'netlify_form_rewrite_only':
            needed.append(node)

    # Build a tiny module that only contains those nodes.
    mini = ast.Module(body=needed, type_ignores=[])
    ast.fix_missing_locations(mini)

    ns = {'re': re}
    exec(compile(mini, _RC_PATH, 'exec'), ns)   # noqa: S102 (safe: our own source)
    return ns['netlify_form_rewrite_only']


netlify_form_rewrite_only = _load_form_rewrite_fn()


class TestNetlifyFormRewriteOnly(unittest.TestCase):

    # ------------------------------------------------------------------
    # Happy path: identical files
    # ------------------------------------------------------------------

    def test_identical_files_returns_true(self):
        text = '<html>\n<form data-netlify="true" name="contact">\n</html>\n'
        self.assertTrue(netlify_form_rewrite_only(text, text))

    # ------------------------------------------------------------------
    # Happy path: the Netlify rewrite and nothing else
    # ------------------------------------------------------------------

    def test_netlify_removes_data_netlify_attribute(self):
        """Netlify drops data-netlify from the live tag — must return True."""
        local = '<form data-netlify="true" name="contact" method="post">'
        live  = "<form name='contact' method='post'>"
        self.assertTrue(netlify_form_rewrite_only(local, live))

    def test_netlify_removes_honeypot_attribute(self):
        """Netlify also drops netlify-honeypot — must return True."""
        local = '<form data-netlify="true" netlify-honeypot="bot-field" name="bk">'
        live  = "<form name='bk'>"
        self.assertTrue(netlify_form_rewrite_only(local, live))

    def test_attribute_reorder_only_returns_true(self):
        """Same attributes (minus data-netlify), different order — still True."""
        local = '<form data-netlify="true" method="post" name="q">'
        live  = "<form name='q' method='post'>"
        self.assertTrue(netlify_form_rewrite_only(local, live))

    def test_multiline_file_form_rewrite_only(self):
        """Multiple identical lines plus one Netlify-rewritten form line."""
        local = (
            '<html>\n'
            '<head><title>T</title></head>\n'
            '<body>\n'
            '<form data-netlify="true" name="x" method="post">\n'
            '<input type="submit">\n'
            '</form>\n'
            '</body></html>\n'
        )
        live = (
            '<html>\n'
            '<head><title>T</title></head>\n'
            '<body>\n'
            "<form name='x' method='post'>\n"
            '<input type="submit">\n'
            '</form>\n'
            '</body></html>\n'
        )
        self.assertTrue(netlify_form_rewrite_only(local, live))

    # ------------------------------------------------------------------
    # Negative paths: must return False
    # ------------------------------------------------------------------

    def test_different_line_count_returns_false(self):
        local = 'line1\nline2\nline3\n'
        live  = 'line1\nline2\n'
        self.assertFalse(netlify_form_rewrite_only(local, live))

    def test_non_form_line_changed_returns_false(self):
        """A difference outside any <form> tag must return False."""
        local = '<p>Old text</p>\n<form data-netlify="true" name="x">\n'
        live  = "<p>New text</p>\n<form name='x'>\n"
        self.assertFalse(netlify_form_rewrite_only(local, live))

    def test_local_form_without_data_netlify_returns_false(self):
        """If the local form tag does not have data-netlify, it is not a
        Netlify rewrite — something else changed."""
        local = '<form name="x" method="post">'
        live  = "<form name='x' method='post'>"
        self.assertFalse(netlify_form_rewrite_only(local, live))

    def test_live_still_has_data_netlify_returns_false(self):
        """A diff where the live form tag also has data-netlify is not the
        expected Netlify rewrite."""
        local = '<form data-netlify="true" name="x">'
        live  = '<form data-netlify="true" name="x" class="extra">'
        self.assertFalse(netlify_form_rewrite_only(local, live))

    def test_content_outside_form_tag_changed_returns_false(self):
        """Characters before the opening <form are different — not a Netlify
        rewrite."""
        local = '  <form data-netlify="true" name="x">'
        live  = '  EXTRA<form name="x">'
        self.assertFalse(netlify_form_rewrite_only(local, live))

    def test_attribute_value_changed_returns_false(self):
        """Netlify does not change attribute values; a differing value fails."""
        local = '<form data-netlify="true" name="contact">'
        live  = "<form name='signup'>"
        self.assertFalse(netlify_form_rewrite_only(local, live))


if __name__ == '__main__':
    unittest.main()
