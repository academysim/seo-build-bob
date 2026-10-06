# -*- coding: utf-8 -*-
"""The canonical Academy Builds price ladder. Single source of truth.

Every published price on builds.academysim.com derives from this file: the
comparison tables built by builds_pages.py, the meta descriptions and prose in
builds_content*.py, and the allowlist the gate in builds_audit.py checks
pages against.

Why it exists. On 2026-08-31 twenty-two live pages were found advertising the
pre-2026-08-31 ladder while the homepage advertised the new one, so a customer
saw the Rookie $500 low or the Pole Position $3,000 high depending on which
page Google had sent them to. It survived because the ladder was typed out in
four separate files and the gate held its own fifth copy, so the gate approved
exactly the pages that were wrong and rejected the one that was right.

Change a price HERE and nowhere else, then regenerate. Nothing downstream may
hold its own copy of a number that appears in this file.
"""


def money(n):
    """7495 -> '$7,495'. The published format is always comma grouped."""
    return '$%s' % format(n, ',')


# ---- the five real builds, in ladder order -------------------------------
# Matches the homepage lineup and the Shopify products, both verified
# 2026-08-31. Club Motion ($29,995) is built but unpublished, and
# ACADEMY-SPORT is archived; neither is part of the ladder.
TIERS = (
    ('rookie',        'Rookie',         7495),
    ('base',          'Base',          11995),
    ('club-oled',     'Club OLED',     18995),
    ('club-triple',   'Club Triple',   21995),
    ('pole-position', 'Pole Position', 39995),
)

NAME = dict((slug, name) for slug, name, _ in TIERS)
PRICE = dict((slug, money(amt)) for slug, _, amt in TIERS)

# Base is quoted "From" because its display and haptics vary by room; the
# other four are specced to a fixed price.
FROM_PRICED = frozenset(['base'])


def tier_price(slug):
    """The price exactly as it is published for that build."""
    p = PRICE[slug]
    return ('From ' + p) if slug in FROM_PRICED else p


# The two ends of the ladder, used in prose: "five real builds from ENTRY",
# "builds to TOP". Derived, so they cannot drift from TIERS.
ENTRY = money(min(amt for _, _, amt in TIERS))
TOP = money(max(amt for _, _, amt in TIERS))

# ---- published prices that are not build tiers ---------------------------
# Configurations of an existing build, and add-ons. These appear in homepage
# copy rather than in the generated pages, but the gate must allow them.
CONFIGURATIONS = {
    money(16995): 'Rally Spec',
    money(12995): 'Full Custom Livery',
}

ADDONS = {
    money(1795): 'BDH H2SQ shifter, installed',
    money(1495): 'Simucube 3 Pro upgrade',
    money(1000): 'install service, from',
    money(995): 'custom vinyl wrap',
    money(549): 'Heusinkveld handbrake',
    money(395): 'additional wheel rim',
}

# Every price string that may legitimately appear anywhere on the site.
ALL_PRICES = (set(PRICE.values())
              | set(CONFIGURATIONS)
              | set(ADDONS))
