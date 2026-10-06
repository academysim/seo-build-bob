# -*- coding: utf-8 -*-
"""Tests for trail() in shared/tools/add_breadcrumbs.py.

Covers linked crumbs (anchor elements), unlinked crumbs (plain text nodes),
and mixed trails containing both.

Run:
    python -m unittest shared/tests/test_add_breadcrumbs.py
    python -m unittest discover -s shared/tests
"""
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _ROOT)

from shared.tools.add_breadcrumbs import trail

BASE  = 'https://example.academy.com'
CANON = 'https://example.academy.com/section/page/'


class TestTrailLinkedCrumbs(unittest.TestCase):
    """Crumbs that are anchor elements — trail() must read href and link text."""

    def test_single_linked_crumb(self):
        block = '<a href="/">Home</a>'
        result = trail(block, BASE, CANON)
        self.assertEqual(result, [('Home', BASE + '/')])

    def test_two_linked_crumbs(self):
        block = '<a href="/">Home</a> / <a href="/section/">Section</a>'
        result = trail(block, BASE, CANON)
        self.assertEqual(result, [
            ('Home', BASE + '/'),
            ('Section', BASE + '/section/'),
        ])

    def test_absolute_href_kept_as_is(self):
        """An href that already starts with http must not be prefixed with base."""
        block = '<a href="https://other.com/page/">Away</a>'
        result = trail(block, BASE, CANON)
        self.assertEqual(result, [('Away', 'https://other.com/page/')])

    def test_html_in_link_text_stripped(self):
        """Nested HTML inside link text is stripped; only text is kept."""
        block = '<a href="/section/"><span>Deep<em> Link</em></span></a>'
        result = trail(block, BASE, CANON)
        self.assertEqual(len(result), 1)
        self.assertNotIn('<', result[0][0])
        self.assertIn('Deep', result[0][0])


class TestTrailUnlinkedCrumbs(unittest.TestCase):
    """Crumbs that are plain text (the current page, no anchor)."""

    def test_single_unlinked_crumb_uses_canon(self):
        block = 'Current Page'
        result = trail(block, BASE, CANON)
        self.assertEqual(result, [('Current Page', CANON)])

    def test_unlinked_crumb_with_slashes_stripped(self):
        """Separator slashes between crumbs must not become crumb names."""
        # A raw ' / ' node matches the PART regex as plain text.
        # strip(' / ') removes surrounding separators.
        block = ' / Current Page / '
        result = trail(block, BASE, CANON)
        # Only non-empty names after stripping ' / '
        names = [n for n, _ in result]
        self.assertNotIn('', names)
        self.assertNotIn('/', names)


class TestTrailMixedCrumbs(unittest.TestCase):
    """Real-world pattern: linked parent crumbs + unlinked current-page crumb."""

    def test_home_then_unlinked(self):
        block = '<a href="/">Home</a> / Page Title'
        result = trail(block, BASE, CANON)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ('Home', BASE + '/'))
        self.assertEqual(result[1][0], 'Page Title')
        self.assertEqual(result[1][1], CANON)

    def test_three_level_trail(self):
        block = ('<a href="/">Home</a> / '
                 '<a href="/section/">Section</a> / '
                 'Leaf Page')
        result = trail(block, BASE, CANON)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], ('Home', BASE + '/'))
        self.assertEqual(result[1], ('Section', BASE + '/section/'))
        self.assertEqual(result[2][0], 'Leaf Page')
        self.assertEqual(result[2][1], CANON)

    def test_empty_block_returns_empty_list(self):
        result = trail('', BASE, CANON)
        self.assertEqual(result, [])

    def test_all_empty_names_filtered(self):
        """Whitespace-only segments must produce no crumb entries."""
        block = '   '
        result = trail(block, BASE, CANON)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
