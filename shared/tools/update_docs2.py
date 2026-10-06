# -*- coding: utf-8 -*-
"""Record the verified rig specs and the homepage throughput conflict."""
import io

MEM = 'C:/Users/malik/.claude/projects/C--Users-malik/memory/events-seo-build.md'
DOC = 'D:/AcademySimRacing/02-Handoffs-Audits/SEO-BUILD-STATUS-2026-08-29.md'

SPEC = """**VERIFIED RIG SPECS, safe to publish** (confirmed by Malik 2026-08-29):
- Frame is a **Trak Racer TR160 V5**: assembled **660 mm x 1445 mm (26 in x 57 in)**, 41 kg, from the manufacturer's own spec table. A 26 in frame clears a standard doorway, which is the thing that matters at private venues.
- **The widest part is the 49 inch ultrawide display**, not the frame.
- **Operating allowance is about 10 ft x 10 ft per simulator**, covering driver access and someone waiting. This already appears in the existing homepage FAQ and is consistent with the rig dimensions, so it was never wrong.
- **Throughput is 15 to 40 drivers per hour per simulator**, depending on session length.

**CONFLICT TO CLOSE: the existing homepage FAQ still says "15-30 racers per hour"** in both the visible copy and its FAQ JSON-LD. Malik's figure is 15-40 and the new pages use it, so the site currently states two ranges. Fixing the homepage needs the original source folder.

"""


def patch(path, anchor, block, once=True):
    s = io.open(path, encoding='utf-8', newline='').read()
    if block.strip().split('\n')[0] in s:
        print('  %s: already present' % path.split('/')[-1])
        return
    assert s.count(anchor) >= 1, 'anchor missing in ' + path
    s = s.replace(anchor, block + anchor, 1)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    print('  %s updated: %d bytes' % (path.split('/')[-1], len(s.encode())))


patch(MEM, '**THE DEPLOY TECHNIQUE', SPEC)
patch(DOC, '## RIG HARDWARE, SETTLED', SPEC.replace('**VERIFIED RIG SPECS, safe to publish**',
                                                    '## VERIFIED EVENT RIG SPECS\n\n**Safe to publish**') + '\n---\n\n')
