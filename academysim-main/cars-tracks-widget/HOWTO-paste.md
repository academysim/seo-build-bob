# Cars & Tracks widget crawlability fix — hand-paste instructions

## What this fixes
`academysim.com/pages/cars-tracks` renders its car/track catalog entirely via JS
(`DATA.filter(...).render()`). A raw fetch (no JS) of the live page confirms the
problem exactly as the 2026-09-04 addendum describes: `<div id="asrList"></div>` is
empty and `<strong id="asrCount">0</strong> results` — a crawler sees "0 results"
before any JS runs.

## What changed
Exactly two edits, both verified with a script-driven diff against the verbatim
original (see `custom_html_ORIGINAL_verbatim.html` for the untouched source, pulled
straight from the Shopify Admin API, not retyped):

1. `<div id="asrList"></div>` now contains a static, server-rendered preview: 21 real
   entries across 6 groups (Formula, GT3 & GT4, Prototype, NASCAR/Stock Cars, Road
   Courses, Ovals) — including every example the addendum named by name (GT3,
   Formula, stock cars, prototypes, Sebring, Daytona, Watkins Glen, Nürburgring).
   Names/categories/tags are copied verbatim from the live `DATA` array, not
   invented.
2. `<strong id="asrCount">0</strong>` → `21`, so the initial state is internally
   consistent (no "0 results" next to a visible list).

Nothing else changed: the 155-entry `DATA` array, all filtering/search JS, the intro
prose above the tool (already added 2026-08-31), and the outro are byte-identical to
what's live now. For every visitor with JS enabled, `render()` still runs
unconditionally on page load and immediately overwrites both spots with the full
interactive catalog — this only affects what a crawler or no-JS browser sees.

Verified: DATA entry count (155), car/track split (63/92), and div/ul/li tag balance
all match between the original and patched file — checked with a script, not by eye.

## How to ship it
Shopify MCP can read the main theme but blocks writes to it, so this is a hand
paste, not an API edit:

1. Shopify admin → Online Store → Themes → Edit code (or the theme customizer) on
   the **live** theme.
2. Open `templates/page.cars-tracks.json`, find block `ai_gen_block_3c36616_VeDfCj`
   (type `ai_gen_block_3c36616`), setting `custom_html` — or open it via the theme
   customizer on the Cars & Tracks page and edit that block's Custom HTML field
   directly (same underlying setting).
3. Select all existing content in that field and replace it with the full contents
   of `custom_html_PATCHED_2026-09-04.html` in this folder. Paste the whole file —
   don't try to hand-edit the two spots in the admin editor, since Shopify's editor
   can mangle indentation on a 30KB+ paste if you interleave manual edits.
4. Save / publish.

## How to verify after pasting
Raw fetch, not a browser render (JS will always show the full catalog and hide the
bug either way):

```
curl -s https://academysim.com/pages/cars-tracks | grep -o '<strong id="asrCount">[0-9]*</strong>'
curl -s https://academysim.com/pages/cars-tracks | grep -c 'class="asr-item"'
```
Expect `21` for the count and `21` for the item count. Then load the page in a
browser and confirm the interactive filter/search still works exactly as before —
`render()` should immediately replace the static 21 with the full live-filtered
list.
