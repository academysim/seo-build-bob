# -*- coding: utf-8 -*-
"""P0: one Google review figure across every Academy property.

The audit found three properties publishing three different numbers: builds and
health said 67 Google reviews, lounge said 65, in eight places between them.
Builds also carried an AggregateRating in its JSON-LD asserting reviewCount 67.

The live count could not be read from here (the Google share link 302s to a
search page that returns nothing usable), so hardcoding any number would just be
picking one of the two and hoping. The main site, academysim.com, already solved
this its own way: it shows real review quotations and then links out with "READ
ALL REVIEWS ON GOOGLE", carrying no count at all. Nothing to drift, nothing to
verify.

That is the default here. Set COUNT to a number and every property gets that
number instead, in one pass, from one constant.

The AggregateRating block is removed regardless. A business marking up its own
Google rating on its own site is self-serving review markup, which Google's
structured data policy does not allow, and it was the only place a stale number
would have been machine-readable.

Reads  <property>/source/ or <property>/site/, writes <property>/upload/.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

# Set to e.g. '71' to publish a count everywhere. None = link out, no number.
COUNT = None

# (property, path relative to that property, source dir, [(old, new_with_count,
#  new_without_count), ...])
JOBS = [
    ('builds', 'index.html', 'source', [
        # the comma belongs to the property BEFORE this block; dropping the
        # block alone leaves a trailing comma and the whole LocalBusiness
        # graph stops parsing, which a substring check for the removed key
        # cannot see. Hence the JSON-LD gate below.
        (u',\n  "aggregateRating": {\n'
         u'    "@type": "AggregateRating",\n'
         u'    "ratingValue": "5.0",\n'
         u'    "reviewCount": "67"\n'
         u'  }\n',
         None, None),                     # always removed
        (u'<span class="rating-text">5.0 \xb7 67 Google reviews</span>',
         u'<span class="rating-text">5.0 \xb7 {n} Google reviews</span>',
         u'<span class="rating-text">5.0 on Google</span>'),
        (u'Read all 67 reviews on Google →',
         u'Read all {n} reviews on Google →',
         u'Read our reviews on Google →'),
    ]),
    ('health', 'index.html', 'upload', [
        (u'<div class="trust-val">★ 5.0 \xb7 67 Reviews</div>',
         u'<div class="trust-val">★ 5.0 \xb7 {n} Reviews</div>',
         u'<div class="trust-val">★ 5.0 on Google</div>'),
        (u'<span class="stars">★★★★★</span> 5.0 on Google \xb7 67 Reviews',
         u'<span class="stars">★★★★★</span> 5.0 on Google \xb7 {n} Reviews',
         u'<span class="stars">★★★★★</span> 5.0 on Google'),
        (u'Read All 67 Reviews on Google →',
         u'Read All {n} Reviews on Google →',
         u'Read Our Reviews on Google →'),
    ]),
    ('lounge', 'index.html', 'site', [
        (u'<div class="trust-val amber">5.0 ★ \xb7 65 Reviews</div>',
         u'<div class="trust-val amber">5.0 ★ \xb7 {n} Reviews</div>',
         u'<div class="trust-val amber">5.0 ★ on Google</div>'),
        (u'These are pulled from the live Google listing (5.0, 65 reviews)',
         u'These are pulled from the live Google listing (5.0, {n} reviews)',
         u'These are pulled from the live Google listing (rated 5.0)'),
        (u'5.0 stars across 65 Google reviews, first-timers',
         u'5.0 stars across {n} Google reviews, first-timers',
         u'5.0 stars on Google from first-timers'),
        (u'5.0 ★ \xb7 65 REVIEWS ON GOOGLE →',
         u'5.0 ★ \xb7 {n} REVIEWS ON GOOGLE →',
         u'5.0 ★ \xb7 READ THE REVIEWS ON GOOGLE →'),
    ]),
    ('lounge', 'things-to-do-in-tampa/index.html', 'site', [
        (u'<strong>5.0</strong> &nbsp;Across 65 Google reviews',
         u'<strong>5.0</strong> &nbsp;Across {n} Google reviews',
         u'<strong>5.0</strong> &nbsp;on Google'),
    ]),
]


def prose(html):
    """Markup only. A CSS `transparent 65%)` sitting a few characters before a
    `.reviews-grid` selector matches any naive count regex, which is how this
    gate first reported a review count that was never there."""
    return re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.S)


def main():
    fail = False
    for prop, rel, srcdir, edits in JOBS:
        bad = False
        src = os.path.join(ROOT, prop, srcdir, rel)
        dst = os.path.join(ROOT, prop, 'upload', rel)
        # a property may already have staged edits waiting in upload/
        staged = os.path.join(ROOT, prop, 'upload', rel)
        read_from = staged if (srcdir == 'upload' or os.path.exists(staged)) else src
        h = io.open(read_from, encoding='utf-8').read()
        for old, with_n, without_n in edits:
            new = u'' if with_n is None else (
                with_n.replace(u'{n}', COUNT) if COUNT else without_n)
            got = h.count(old)
            if got != 1:
                print('  !! %s/%s: expected 1, found %d for %r'
                      % (prop, rel, got, ' '.join(old.split())[:70]))
                bad = True
                continue
            h = h.replace(old, new)
            print('  %-7s %-34s %s' % (prop, rel,
                                       'removed' if with_n is None else 'updated'))
        if bad:
            fail = True
            continue
        # the number must directly precede the word, or "2014 Cochrane review"
        # and "60 minutes ... reviews" both read as review counts
        left = re.findall(r'\b\d{1,4}\s+(?:Google\s+)?[Rr]eviews?\b', prose(h))
        if left and not COUNT:
            print('  !! %s/%s still hardcodes a count: %s' % (prop, rel, left))
            fail = True
        if '"aggregateRating"' in h:
            print('  !! %s/%s still has AggregateRating' % (prop, rel))
            fail = True
        for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
                             h, re.S):
            try:
                json.loads(m.group(1))
            except ValueError as e:
                print('  !! %s/%s JSON-LD no longer parses: %s' % (prop, rel, e))
                fail = True
        d = os.path.dirname(dst)
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(dst, 'w', encoding='utf-8', newline='').write(h)
        print('           -> %s (%d bytes)' % (dst, len(h.encode('utf-8'))))
    return 1 if fail else 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        COUNT = sys.argv[1]
        print('  publishing count = %s' % COUNT)
    else:
        print('  no count given: linking to Google without a number')
    sys.exit(main())
