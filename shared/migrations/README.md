# One-shot migrations, kept for the audit trail

These ran once, on 2026-09-09, as part of F8. **Do not run them again.** Their output is
committed to `site/` and `source/`, and each is written to edit a tree that no longer looks the
way it did when they ran, so a second run would either no-op or double-insert.

They are here because the alternative was losing them. They are the only record of *how* a class
of live-only edit got back into version control, and that class is the reason F8 existed: content
that lived in no tree and no tool, applied by hand to the live sites, recoverable only by diffing
a rebuild against verified staging.

| script | what it pushed into the source trees |
|---|---|
| `push_hand_edits.py` | the `g.page/r/CSLLKCLuh-RlEBM` reviews link (lounge, builds x2, health), the three `?category=lessons_manual` CTAs on the lounge manual page, the lounge footer Membership and Thursday Night League links, and driver's `.html#demo` hrefs plus the Hours block |
| `push_builds_leaf_footers.py` | the footer hours block on 19 builds leaf pages, against the exact list the verified staging carried |
| `retrofit_hub_tools.py` | added `--tree site\|source\|upload` to the events, builds and health `add_hub_links.py` tools |

The lesson, not the code, is the thing worth keeping: **a fix applied only to `upload/` is
invisible to git, lost on a fresh checkout, and reverted by the next rebuild.** One applied only
to the live site is worse: nothing local knows it exists.

A guard against the recurrence now exists in `shared/tools/check_staged.py`.
