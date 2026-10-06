# -*- coding: utf-8 -*-
"""Tests for shared/tools/hub_links_lib.py.

Covers:
  adapt()           -- LF input unchanged; CRLF input gets CRLF-converted pattern
  patch_homepage()  -- idempotency (second call is a no-op)
  patch_footer()    -- idempotency (second call skips already-patched pages)

Run:
  python -m unittest shared/tests/test_hub_links_lib.py
  python -m unittest discover -s shared/tests
"""
import io
import os
import sys
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, '..', 'tools'))
sys.path.insert(0, _TOOLS)
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, '..', '..')))

from shared.tools.hub_links_lib import adapt, rd, wr, patch_homepage, patch_footer


class TestAdapt(unittest.TestCase):
    """adapt() must return the pattern unchanged for LF files, and with CRLF
    substituted for LF when the file content uses CRLF line endings."""

    PATTERN = 'line one\nline two\nline three\n'

    def test_lf_input_unchanged(self):
        s = 'some\ncontent\nhere\n'
        result = adapt(self.PATTERN, s)
        self.assertEqual(result, self.PATTERN)
        self.assertNotIn('\r\n', result)

    def test_crlf_input_converts_pattern(self):
        s = 'some\r\ncontent\r\nhere\r\n'
        result = adapt(self.PATTERN, s)
        self.assertIn('\r\n', result)
        self.assertNotIn('\r\n', self.PATTERN,
                         msg='PATTERN must be authored with LF for this test to be meaningful')
        expected = self.PATTERN.replace('\n', '\r\n')
        self.assertEqual(result, expected)

    def test_mixed_crlf_triggers_conversion(self):
        # A file with at least one CRLF anywhere in it triggers conversion.
        s = 'first\r\nsecond\nthird\n'
        result = adapt('a\nb\n', s)
        self.assertEqual(result, 'a\r\nb\r\n')

    def test_pure_lf_no_conversion(self):
        s = 'a\nb\nc\n'
        self.assertEqual(adapt('x\ny\n', s), 'x\ny\n')


class TestPatchHomepage(unittest.TestCase):
    """patch_homepage() must insert the section on the first call and be a
    no-op on every subsequent call (idempotency)."""

    def _make_tree(self, content):
        """Write content to index.html in a temp dir, return the dir path."""
        d = tempfile.mkdtemp()
        io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(content)
        return d

    def test_first_call_inserts_section(self):
        page = '<body>\n<section class="faq">FAQ</section>\n</body>\n'
        section = '<section class="explore">LINKS</section>\n\n'
        d = self._make_tree(page)
        patch_homepage(d, anchor='<section class="faq">', section_html=section,
                       sentinel='LINKS')
        result = rd(os.path.join(d, 'index.html'))
        self.assertIn(section, result)
        self.assertIn('<section class="faq">', result)
        # Section must come before the anchor
        self.assertLess(result.index(section), result.index('<section class="faq">'))

    def test_second_call_is_noop(self):
        page = '<body>\n<section class="faq">FAQ</section>\n</body>\n'
        section = '<section class="explore">LINKS</section>\n\n'
        d = self._make_tree(page)
        patch_homepage(d, anchor='<section class="faq">', section_html=section,
                       sentinel='LINKS')
        content_after_first = rd(os.path.join(d, 'index.html'))
        patch_homepage(d, anchor='<section class="faq">', section_html=section,
                       sentinel='LINKS')
        content_after_second = rd(os.path.join(d, 'index.html'))
        self.assertEqual(content_after_first, content_after_second)

    def test_sentinel_already_present_skips(self):
        # If the sentinel is already in the page, nothing is written.
        page = ('<body>\n<section class="explore">LINKS</section>\n'
                '<section class="faq">FAQ</section>\n</body>\n')
        section = '<section class="explore">LINKS</section>\n\n'
        d = self._make_tree(page)
        patch_homepage(d, anchor='<section class="faq">', section_html=section,
                       sentinel='LINKS')
        result = rd(os.path.join(d, 'index.html'))
        # Must not double-insert
        self.assertEqual(result.count('LINKS'), 1)


class TestPatchFooter(unittest.TestCase):
    """patch_footer() must replace old_block with new_block in every non-
    homepage index.html it finds, and be idempotent on second call."""

    OLD = '<footer>OLD</footer>\n'
    NEW = '<footer>NEW</footer>\n'

    def _make_subpage(self, tree_dir, rel_dir, content):
        d = os.path.join(tree_dir, *rel_dir.split('/'))
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(content)

    def test_subpage_is_patched(self):
        d = tempfile.mkdtemp()
        # Write a homepage (must be skipped) and a subpage (must be patched)
        io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='').write(
            '<body>' + self.OLD + '</body>')
        self._make_subpage(d, 'sub', '<body>' + self.OLD + '</body>')
        touched, present, unmatched = patch_footer(d, self.OLD, self.NEW)
        self.assertIn('sub/index.html', touched)
        # homepage must NOT appear in touched
        self.assertNotIn('index.html', touched)

    def test_already_patched_goes_to_present(self):
        d = tempfile.mkdtemp()
        self._make_subpage(d, 'sub', '<body>' + self.NEW + '</body>')
        touched, present, unmatched = patch_footer(d, self.OLD, self.NEW)
        self.assertEqual(touched, [])
        self.assertIn('sub/index.html', present)

    def test_second_call_is_noop(self):
        d = tempfile.mkdtemp()
        self._make_subpage(d, 'sub', '<body>' + self.OLD + '</body>')
        patch_footer(d, self.OLD, self.NEW)
        content_first = rd(os.path.join(d, 'sub', 'index.html'))
        patch_footer(d, self.OLD, self.NEW)
        content_second = rd(os.path.join(d, 'sub', 'index.html'))
        self.assertEqual(content_first, content_second)

    def test_crlf_file_patched_correctly(self):
        """A CRLF subpage must be patched with CRLF blocks and stay CRLF."""
        old_lf = '<footer>OLD</footer>\n'
        new_lf = '<footer>NEW</footer>\n'
        crlf_page = ('<body>\r\n'
                     + old_lf.replace('\n', '\r\n')
                     + '</body>\r\n')
        d = tempfile.mkdtemp()
        self._make_subpage(d, 'sub', crlf_page)
        io.open(os.path.join(d, 'sub', 'index.html'),
                'w', encoding='utf-8', newline='').write(crlf_page)
        patch_footer(d, old_lf, new_lf)
        result = rd(os.path.join(d, 'sub', 'index.html'))
        self.assertIn(new_lf.replace('\n', '\r\n'), result)
        self.assertNotIn('\r\r\n', result,
                         msg='double-CRLF would indicate adapt() was applied twice')


if __name__ == '__main__':
    unittest.main()
