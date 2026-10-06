# -*- coding: utf-8 -*-
"""Record the completed events event-types section."""
import io

MEM = 'C:/Users/malik/.claude/projects/C--Users-malik/memory/events-seo-build.md'
DOC = 'D:/AcademySimRacing/02-Handoffs-Audits/SEO-BUILD-STATUS-2026-08-29.md'


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# ---- memory ----------------------------------------------------------------
s = rd(MEM)
s = s.replace(
    '**Live as of 2026-08-29: 20 sitemap URLs, up from 1.**',
    '**Live as of 2026-08-29: 24 sitemap URLs, up from 1.**')
s = s.replace(
    '- `/event-types/` hub + corporate-events, trade-shows, conventions, '
    'brand-activations, car-dealership-events, watch-parties',
    '- `/event-types/` hub + **all ten types**: corporate-events, trade-shows, conventions, '
    'brand-activations, car-dealership-events, watch-parties, employee-appreciation, '
    'client-entertainment, private-parties, fundraisers')

warn = """
**REBUILDING REVERTS THE FIX SCRIPTS.** `events_content*.py` regenerate pages from source, but `fix_events_r1.py` (Codex review fixes) and `fix_events_specs.py` (rig dimensions and throughput) patch the *generated output* in `events_new/`. Re-run both after any rebuild, then `events_audit.py`, or you will silently reship the defects. This bit me once already and the audit is what caught it.

"""
if 'REBUILDING REVERTS' not in s:
    s = s.replace('**THE DEPLOY TECHNIQUE', warn.lstrip() + '**THE DEPLOY TECHNIQUE', 1)
wr(MEM, s)
print('  memory updated: %d bytes' % len(s.encode()))

# ---- handoff ---------------------------------------------------------------
s = rd(DOC)
s = s.replace('| **Events** | 30 | **20** |', '| **Events** | 30 | **24** |')
s = s.replace('**Events went from 1 URL to 20 on 2026-08-29.**',
              '**Events went from 1 URL to 24 on 2026-08-29.**')
s = s.replace(
    'Built: the `/event-types/` hub and\nsix type pages,',
    'Built: the `/event-types/` hub and\n**all ten** type pages,')
wr(DOC, s)
print('  handoff updated: %d bytes' % len(s.encode()))
