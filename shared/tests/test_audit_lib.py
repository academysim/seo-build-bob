# -*- coding: utf-8 -*-
"""Unit tests for shared/tools/audit_lib.py helpers.

Run:
    python -m unittest shared/tests/test_audit_lib.py
    python -m unittest discover -s shared/tests
"""
import io
import json
import os
import sys
import tempfile
import shutil
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _ROOT)

from shared.tools import audit_lib


# ---------------------------------------------------------------------------
# walk_pages
# ---------------------------------------------------------------------------

class TestWalkPages(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_audit_lib_walk_')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _make(self, rel):
        """Create an empty file at *rel* under self.tmp."""
        full = os.path.join(self.tmp, *rel.split('/'))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w') as fh:
            fh.write('<html></html>')
        return full

    def test_returns_empty_for_empty_directory(self):
        self.assertEqual([], audit_lib.walk_pages(self.tmp))

    def test_returns_empty_for_missing_directory(self):
        self.assertEqual([], audit_lib.walk_pages(os.path.join(self.tmp, 'nonexistent')))

    def test_finds_html_files(self):
        self._make('index.html')
        self._make('sub/index.html')
        pages = audit_lib.walk_pages(self.tmp)
        rels = [r for r, _ in pages]
        self.assertIn('index.html', rels)
        self.assertIn('sub/index.html', rels)

    def test_ignores_non_html_by_default(self):
        self._make('style.css')
        self._make('script.js')
        pages = audit_lib.walk_pages(self.tmp)
        self.assertEqual([], pages)

    def test_custom_extension(self):
        self._make('data.xml')
        self._make('page.html')
        pages = audit_lib.walk_pages(self.tmp, extensions=('.xml',))
        rels = [r for r, _ in pages]
        self.assertIn('data.xml', rels)
        self.assertNotIn('page.html', rels)

    def test_sorted(self):
        self._make('b.html')
        self._make('a.html')
        pages = audit_lib.walk_pages(self.tmp)
        rels = [r for r, _ in pages]
        self.assertEqual(sorted(rels), rels)

    def test_uses_forward_slashes(self):
        self._make('sub/deep/page.html')
        pages = audit_lib.walk_pages(self.tmp)
        for rel, _ in pages:
            self.assertNotIn('\\', rel)


# ---------------------------------------------------------------------------
# check_ai_phrases
# ---------------------------------------------------------------------------

class TestCheckAiPhrases(unittest.TestCase):

    AI = ['delve', 'seamless', 'leverage']

    def test_no_match(self):
        self.assertEqual([], audit_lib.check_ai_phrases('hello world', self.AI))

    def test_single_match(self):
        self.assertEqual(['ai:delve'], audit_lib.check_ai_phrases('let us delve here', self.AI))

    def test_multiple_matches(self):
        result = audit_lib.check_ai_phrases('seamless delve leverage', self.AI)
        self.assertIn('ai:delve', result)
        self.assertIn('ai:seamless', result)
        self.assertIn('ai:leverage', result)

    def test_case_sensitive_input_already_lowered(self):
        # The callers pass pre-lowered text; uppercase should not match
        self.assertEqual([], audit_lib.check_ai_phrases('DELVE', self.AI))

    def test_substring_match(self):
        # 'seamless' inside a word should still match (per original audit logic)
        self.assertEqual(['ai:seamless'], audit_lib.check_ai_phrases('xseamlessy', self.AI))


# ---------------------------------------------------------------------------
# check_british
# ---------------------------------------------------------------------------

class TestCheckBritish(unittest.TestCase):

    BRITISH = ['tyre', 'colour', 'realise']

    def test_no_match(self):
        self.assertEqual([], audit_lib.check_british('the red tire', self.BRITISH))

    def test_single_match_whole_word(self):
        self.assertEqual(['british:tyre'], audit_lib.check_british('check the tyre', self.BRITISH))

    def test_word_boundary_prevents_partial(self):
        # 'colour' should not fire on 'discoloured' — wait, original uses \b prefix only
        # so 'discoloured' starts a new word boundary before 'colour'? No, \bcolour
        # means 'colour' must start at a word boundary.
        # 'discoloured' contains 'colour' but after a non-word boundary from 'dis'.
        # Actually \b matches before 'c' in 'discoloured' only if preceded by non-word.
        # 'discoloured' = d-i-s-c... so 'c' is preceded by 's' (word char), no \b before c.
        self.assertEqual([], audit_lib.check_british('discoloured', self.BRITISH))

    def test_matches_colour_standalone(self):
        self.assertEqual(['british:colour'], audit_lib.check_british('choose colour wisely', self.BRITISH))


# ---------------------------------------------------------------------------
# check_tag_balance
# ---------------------------------------------------------------------------

class TestCheckTagBalance(unittest.TestCase):

    def test_balanced_returns_empty(self):
        html = '<div><p>hello</p></div>'
        self.assertEqual([], audit_lib.check_tag_balance(html))

    def test_unbalanced_div(self):
        html = '<div><div></div>'  # 2 open, 1 close
        probs = audit_lib.check_tag_balance(html, tags=('<div',))
        self.assertEqual(['<div 2/1'], probs)

    def test_unbalanced_p(self):
        html = '<p>one</p><p>two</p></p>'  # 2 open, 3 close
        probs = audit_lib.check_tag_balance(html, tags=('<p',))
        self.assertEqual(['<p 2/3'], probs)

    def test_pre_not_counted_as_p(self):
        # <pre> must not count as <p>
        html = '<pre>code</pre><p>text</p>'
        probs = audit_lib.check_tag_balance(html, tags=('<p',))
        self.assertEqual([], probs)

    def test_picture_not_counted_as_p(self):
        html = '<picture><source/></picture><p>text</p>'
        probs = audit_lib.check_tag_balance(html, tags=('<p',))
        self.assertEqual([], probs)

    def test_balanced_all_tags(self):
        html = '<div><section><p>x</p></section></div>'
        self.assertEqual([], audit_lib.check_tag_balance(html))


# ---------------------------------------------------------------------------
# check_json_ld
# ---------------------------------------------------------------------------

class TestCheckJsonLd(unittest.TestCase):

    def test_no_block_returns_empty(self):
        self.assertEqual([], audit_lib.check_json_ld('<html></html>'))

    def test_valid_block_returns_empty(self):
        html = '<script type="application/ld+json">{"@type":"Thing"}</script>'
        self.assertEqual([], audit_lib.check_json_ld(html))

    def test_invalid_block_returns_error(self):
        html = '<script type="application/ld+json">{ INVALID }</script>'
        self.assertEqual(['BAD-JSON-LD'], audit_lib.check_json_ld(html))

    def test_multiple_blocks_one_bad(self):
        html = ('<script type="application/ld+json">{"ok":1}</script>'
                '<script type="application/ld+json">{ BAD }</script>')
        self.assertEqual(['BAD-JSON-LD'], audit_lib.check_json_ld(html))

    def test_multiple_blocks_both_bad(self):
        html = ('<script type="application/ld+json">{ A }</script>'
                '<script type="application/ld+json">{ B }</script>')
        # Returns one entry per bad block
        self.assertEqual(['BAD-JSON-LD', 'BAD-JSON-LD'], audit_lib.check_json_ld(html))


# ---------------------------------------------------------------------------
# check_ga4
# ---------------------------------------------------------------------------

class TestCheckGa4(unittest.TestCase):

    TAG = 'G-SQL40ZS59K'

    def test_present_returns_empty(self):
        html = '<script>%s</script>' % self.TAG
        self.assertEqual([], audit_lib.check_ga4(html, self.TAG))

    def test_absent_returns_error(self):
        self.assertEqual(['NO-GA4'], audit_lib.check_ga4('<html></html>', self.TAG))

    def test_default_tag(self):
        self.assertEqual(['NO-GA4'], audit_lib.check_ga4('<html></html>'))

    def test_default_tag_present(self):
        html = 'G-SQL40ZS59K'
        self.assertEqual([], audit_lib.check_ga4(html))


# ---------------------------------------------------------------------------
# check_internal_links
# ---------------------------------------------------------------------------

class TestCheckInternalLinks(unittest.TestCase):

    def test_known_path_ok(self):
        html = '<a href="/about/">link</a>'
        self.assertEqual([], audit_lib.check_internal_links(html, {'/about/'}))

    def test_unknown_path_broken(self):
        html = '<a href="/missing/">link</a>'
        probs = audit_lib.check_internal_links(html, {'/about/'})
        self.assertEqual(['BROKEN /missing/'], probs)

    def test_asset_skipped(self):
        html = '<a href="/file.pdf">pdf</a><img src="/img.png">'
        # pdf not in skip list but png is; pdf is not internal (no href)
        # Actually pdf has href but it is not in the SKIP list... let's check
        # the SKIP list in audit_lib: .xml .txt .png .svg .ico .webmanifest .jpg .css .js
        # pdf is NOT in SKIP so it should report broken
        probs = audit_lib.check_internal_links('<a href="/img.png">x</a>', set())
        self.assertEqual([], probs)

    def test_external_link_ignored(self):
        # external links don't start with /
        html = '<a href="https://example.com">link</a>'
        self.assertEqual([], audit_lib.check_internal_links(html, set()))

    def test_single_quoted_href(self):
        html = "<a href='/about/'>link</a>"
        self.assertEqual([], audit_lib.check_internal_links(html, {'/about/'}))

    def test_fragment_stripped(self):
        # The base check strips fragments (#...) so /about/#section is checked as /about/
        # Actually check_internal_links uses [^"\'#?]* so fragment is excluded from match
        html = '<a href="/about/#section">link</a>'
        self.assertEqual([], audit_lib.check_internal_links(html, {'/about/'}))

    def test_deduplicates_hrefs(self):
        # Same broken href appearing 5 times should only report once
        html = '<a href="/x/">1</a><a href="/x/">2</a><a href="/x/">3</a>'
        probs = audit_lib.check_internal_links(html, set())
        self.assertEqual(['BROKEN /x/'], probs)


# ---------------------------------------------------------------------------
# check_sitemap_coverage
# ---------------------------------------------------------------------------

class TestCheckSitemapCoverage(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_audit_lib_sitemap_')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write_sitemap(self, urls):
        content = '<?xml version="1.0"?><urlset>'
        for u in urls:
            content += '<url><loc>%s</loc></url>' % u
        content += '</urlset>'
        path = os.path.join(self.tmp, 'sitemap.xml')
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        return path

    def test_missing_sitemap_increments_fail(self):
        path = os.path.join(self.tmp, 'no_such_sitemap.xml')
        result = audit_lib.check_sitemap_coverage([], path, fail_count=0)
        self.assertEqual(1, result)

    def test_fully_covered_returns_unchanged_fail(self):
        path = self._write_sitemap(['https://example.com/'])
        pages = [('index.html', '/dummy')]
        result = audit_lib.check_sitemap_coverage(pages, path, fail_count=0)
        self.assertEqual(0, result)

    def test_uncovered_url_increments_fail(self):
        path = self._write_sitemap([
            'https://example.com/',
            'https://example.com/about/',
        ])
        # Only index.html → covers /
        pages = [('index.html', '/dummy')]
        result = audit_lib.check_sitemap_coverage(pages, path, fail_count=0)
        self.assertEqual(1, result)

    def test_non_index_html_covered(self):
        path = self._write_sitemap(['https://example.com/about.html'])
        pages = [('about.html', '/dummy')]
        result = audit_lib.check_sitemap_coverage(pages, path, fail_count=0)
        self.assertEqual(0, result)

    def test_accumulates_existing_fail_count(self):
        path = self._write_sitemap(['https://example.com/missing/'])
        result = audit_lib.check_sitemap_coverage([], path, fail_count=3)
        self.assertEqual(4, result)


# ---------------------------------------------------------------------------
# parse_sitemap
# ---------------------------------------------------------------------------

class TestParseSitemap(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='test_audit_lib_parse_')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_missing_file_returns_empty(self):
        self.assertEqual([], audit_lib.parse_sitemap('/no/such/file.xml'))

    def test_parses_locs(self):
        path = os.path.join(self.tmp, 'sitemap.xml')
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write('<urlset><url><loc>https://x.com/</loc></url>'
                     '<url><loc>https://x.com/about/</loc></url></urlset>')
        result = audit_lib.parse_sitemap(path)
        self.assertIn('https://x.com/', result)
        self.assertIn('https://x.com/about/', result)
        self.assertEqual(2, len(result))


if __name__ == '__main__':
    unittest.main()
