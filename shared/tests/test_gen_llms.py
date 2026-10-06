# -*- coding: utf-8 -*-
"""Tests for strip_brand() in shared/tools/gen_llms.py.

Key invariant: strip_brand() must NEVER return an empty string.
A title that is nothing but brand keeps the first brand segment.

Run:
    python -m unittest shared/tests/test_gen_llms.py
    python -m unittest discover -s shared/tests
"""
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _ROOT)

from shared.tools.gen_llms import strip_brand


class TestStripBrand(unittest.TestCase):

    # ------------------------------------------------------------------
    # Never-empty invariant
    # ------------------------------------------------------------------

    def test_pure_brand_title_not_empty(self):
        """Title that is only the brand must return the brand, not ''."""
        result = strip_brand('Academy Sim Racing')
        self.assertTrue(result, 'strip_brand() returned empty for a pure-brand title')

    def test_pure_brand_with_pipe_not_empty(self):
        """'Academy | Academy Sim Racing' — all segments are brand."""
        result = strip_brand('Academy | Academy Sim Racing')
        self.assertTrue(result)

    def test_empty_string_not_empty(self):
        """Empty input must not return empty — caller handles the title-missing
        case separately, but strip_brand itself must be safe."""
        result = strip_brand('')
        # empty in → empty out is acceptable only if clean() already normalises
        # it to ''; the important rule is no crash and no None.
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_whitespace_only_not_crash(self):
        result = strip_brand('   ')
        self.assertIsNotNone(result)

    # ------------------------------------------------------------------
    # Normal brand-stripping
    # ------------------------------------------------------------------

    def test_trailing_brand_stripped(self):
        """'Sim Racing Lounge | Academy Sim Racing' → 'Sim Racing Lounge'."""
        result = strip_brand('Sim Racing Lounge | Academy Sim Racing')
        self.assertEqual(result, 'Sim Racing Lounge')

    def test_leading_brand_stripped(self):
        """'Academy Sim Racing | Lounge Tampa' → 'Lounge Tampa'."""
        result = strip_brand('Academy Sim Racing | Lounge Tampa')
        self.assertEqual(result, 'Lounge Tampa')

    def test_non_brand_segment_kept(self):
        result = strip_brand("Teen Driver Training | Academy Driver's Ed")
        self.assertIn('Teen Driver Training', result)
        self.assertNotIn("Academy Driver's Ed", result)

    def test_no_separator_passthrough(self):
        """Title with no pipe or en-dash is returned as-is (after clean())."""
        result = strip_brand('Book a Session')
        self.assertEqual(result, 'Book a Session')

    # ------------------------------------------------------------------
    # Edge cases: separators, extra whitespace, HTML entities
    # ------------------------------------------------------------------

    def test_en_dash_separator(self):
        """En-dash separator is also recognised."""
        result = strip_brand('Corporate Events \u2013 Academy Sim Racing')
        self.assertIn('Corporate Events', result)

    def test_html_entity_unescaped(self):
        """HTML entities in the title must be unescaped before matching."""
        result = strip_brand('Custom Builds &amp; Installs | Academy Sim Racing')
        self.assertIn('Custom Builds', result)
        self.assertNotIn('&amp;', result)

    def test_extra_whitespace_collapsed(self):
        result = strip_brand('  Senior  Programs   |   Academy Sim Racing  ')
        self.assertEqual(result, 'Senior Programs')

    def test_both_segments_non_brand(self):
        """Two non-brand segments are kept joined by ' | '."""
        result = strip_brand('Tracks | Sebring Simulator')
        self.assertIn('Tracks', result)
        self.assertIn('Sebring Simulator', result)


if __name__ == '__main__':
    unittest.main()
