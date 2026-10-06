# -*- coding: utf-8 -*-
"""Update the events memory entry and the handoff status doc."""
import io

MEM = 'C:/Users/malik/.claude/projects/C--Users-malik/memory/events-seo-build.md'
DOC = 'D:/AcademySimRacing/02-Handoffs-Audits/SEO-BUILD-STATUS-2026-08-29.md'


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# ---------------------------------------------------------------- memory ---
s = rd(MEM)
old = s[s.index('**Live as of 2026-08-29**'):s.index('**THE DEPLOY TECHNIQUE')]
new = (
    "**Live as of 2026-08-29: 20 sitemap URLs, up from 1.**\n"
    "- `/event-types/` hub + corporate-events, trade-shows, conventions, "
    "brand-activations, car-dealership-events, watch-parties\n"
    "- `/experiences/` hub + gt3, formula, nascar (stock car), imsa-endurance, drift, rally\n"
    "- `/locations/` hub + tampa, orlando, daytona-beach, sarasota\n\n"
    "Built by `events_pages.py` (template) + `events_content{,2,3,4}.py` (content), gated by "
    "`events_audit.py`: em dashes, AI tells, the `<body class>` scroll trap, GA4, canonical, tag "
    "balance, JSON-LD, broken internal links, **undenied \"official Formula 1/NASCAR/IMSA "
    "simulator\" claims**, and that every city page states it is not a branch. The audit "
    "deliberately ALLOWS \"Is this an official NASCAR simulator?\" when a denial follows within "
    "140 characters - that FAQ pattern is what the brief asks for, and a naive substring check "
    "flags it wrongly.\n\n"
)
s = s.replace(old, new)
wr(MEM, s)
print('memory updated: %d bytes' % len(s.encode()))

# ---------------------------------------------------------------- handoff --
s = rd(DOC)
s = s.replace('| Events | 30 | 1 |', '| **Events** | 30 | **20** |')

old = ("Events is first in the zip's own rollout order and is still at 1 URL. That is the\n"
       "obvious next property.")
new = """**Events went from 1 URL to 20 on 2026-08-29.** Built: the `/event-types/` hub and
six type pages, the `/experiences/` hub and six experience pages, and the
`/locations/` hub and four city pages.

Two deliberate scope calls, both agreed with Codex:

- **Four city pages, not ten.** Tampa, Orlando, Daytona Beach and Sarasota have
  genuinely different event economies. St. Petersburg, Clearwater, Wesley Chapel,
  Bradenton, Lakeland and Ocala wait for Search Console demand. Ten near-identical
  city pages is the biggest doorway-page risk in the handoff, and the README
  forbids mass-generating thin city pages.
- **New pages link to `/?ref=<slug>#quote` rather than duplicating the form.**
  The quote flow is two tested Netlify Forms on the homepage. Thirty copies of a
  form is thirty things to drift out of sync.

**One thing I need from you: the original events.academysim.com source folder.**
The site was drag-and-dropped, so there is no source tree, and Netlify serves
`index.html` 98 bytes smaller than it stores it because it rewrites pages
containing Netlify Forms. Redeploying a fetched copy could break form detection,
so I have not touched the homepage. That is why **the new sections are not yet
linked from the homepage** and are currently reachable through the sitemap and
internal links only.

Everything else deployed safely. I used Netlify's digest API to declare the 29
existing files by hash so they were reused byte-for-byte, and verified after every
deploy that the homepage SHA was unchanged and both forms were still present."""
assert s.count(old) == 1, 'handoff anchor not found once'
s = s.replace(old, new, 1)
wr(DOC, s)
print('handoff updated: %d bytes' % len(s.encode()))
