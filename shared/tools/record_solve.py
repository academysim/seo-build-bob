# -*- coding: utf-8 -*-
"""Record the drag-and-drop source recovery, which is now solved."""
import io

MEM = 'C:/Users/malik/.claude/projects/C--Users-malik/memory/events-seo-build.md'
s = io.open(MEM, encoding='utf-8', newline='').read()

SOLVED = """**THE "NO SOURCE FOLDER" PROBLEM IS SOLVED (2026-08-29). Do not treat it as a blocker again.**

Netlify's only edit to a drag-and-dropped HTML file is that it strips `data-netlify="true" netlify-honeypot="bot-field"` from each form when serving, and normalises attribute order/quoting. That is **exactly 49 bytes per form**, which is why events lost 98 (two forms) and builds and health lost 49 (one each). Proved by diffing an old events deploy's zip against what that deploy's own permalink still serves.

**So any of these homepages can be reconstructed byte-identically from what the site serves:** fetch the served page, restore those two attributes to each `<form>`, and check the SHA1 against the live deploy manifest. If the size is right but the SHA is not, only the attribute ORDER differs; `solve_form_order.py` brute-forces the permutations against the target SHA. Solved orders found: events `name class method data-netlify netlify-honeypot action`; builds `name method data-netlify netlify-honeypot action class id`; health `class name method data-netlify netlify-honeypot id action`. Skip bare `<form>` tags with no name/method attribute or you will mangle them.

`_redirects`, `netlify.toml` and `__forms.html` still cannot be fetched over HTTP, but they were recovered SHA-verified from **deploy zips sitting in `C:\\Users\\malik\\Downloads`** (`deploy-6a72bc4716ddbdc9a46078da.zip`, `academy-events-ROCKWAY-CASE.zip`, `academy-builds-SPEC-CORRECTIONS.zip`). Even without them the digest deploy carries them across by SHA, so they are only needed if one has to CHANGE.

**Both homepages were then edited and shipped**: events now links `/event-types/`, `/experiences/` and `/locations/` and the throughput figure reads 15-40 in all three places it appears (visible FAQ, FAQ JSON-LD, and a prominent `aerial-stat-big` callout that a sentence-level find-and-replace missed). Builds links `/simulators/`, `/for/` and `/network/`. Forms verified still registered in `__forms.html` after deploy.

"""

anchor = '**THE DEPLOY TECHNIQUE'
if 'PROBLEM IS SOLVED' not in s:
    s = s.replace(anchor, SOLVED + anchor, 1)
    io.open(MEM, 'w', encoding='utf-8', newline='').write(s)
    print('  events memory updated: %d bytes' % len(s.encode()))
else:
    print('  already recorded')

IDX = 'C:/Users/malik/.claude/projects/C--Users-malik/memory/MEMORY.md'
m = io.open(IDX, encoding='utf-8', newline='').read()
old = ('holds the **Netlify digest-deploy** technique that adds pages to a drag-and-drop site without its '
       'source, and the reason `index.html` must NEVER be redeployed (Netlify serves form pages 98 bytes '
       'smaller than it stores them)')
new = ('holds the **Netlify digest-deploy** technique and the **solved** source-recovery method: Netlify '
       'strips exactly 49 bytes of form attributes per form when serving, so any drag-and-drop homepage '
       'can be rebuilt byte-identically from the live site and safely edited')
if old in m:
    m = m.replace(old, new, 1)
    io.open(IDX, 'w', encoding='utf-8', newline='').write(m)
    print('  index entry updated')
else:
    print('  index entry unchanged (anchor not found)')
