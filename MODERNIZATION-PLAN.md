# Modernization Plan — academy-seo-build

**Hard constraint throughout:** every file listed in `BASELINE-site-hashes.txt`
must remain byte-identical after any refactor. No build output changes; only the
tools that produce those outputs change.

**This fork must never touch the network.** Do not run `release_check.py`,
`audit_discovery.py`, `gsc_monitor.py`, `deploy.py`, or anything in
`netlify_lib.py`. All verification is offline:

```
python shared/tools/verify_baseline.py          # exits 0 = site + upload files unchanged
python shared/tools/build_all.py                # full rebuild
python lounge/tools/audit_site.py               # exits 0
python events/tools/events_audit.py             # exits 0
python builds/tools/builds_audit.py             # exits 0
python driver/tools/driver_audit.py             # exits 0
python health/tools/health_audit.py             # exits 0
python -m unittest discover -s shared/tests     # exits 0
```

---

## 1. Codebase Map

```
seo-build-bob/
├── shared/tools/          # 25 scripts: the "engine"
│   ├── build_all.py       # orchestrator: clears upload/, runs STEPS list
│   ├── stage.py           # copies site/ → upload/ with extension allowlist
│   ├── check_staged.py    # loss gate: upload/ vs recorded inventory JSON
│   ├── release_check.py   # live smoke + Netlify manifest diff
│   ├── deploy.py          # digest deploy to Netlify (Malik runs, not CI)
│   ├── netlify_lib.py     # Netlify API: token, curl, live_manifest()
│   ├── audit_discovery.py # live crawl: 106 URLs, structured-data checks
│   ├── test_discovery_gate.py  # ← THE ONLY TEST FILE (13 assertions)
│   ├── add_breadcrumbs.py # derives BreadcrumbList schema from visible trail
│   ├── gen_llms.py        # generates llms.txt for all five properties
│   ├── gen_replace.py     # regenerates replace_<key>.txt from live manifest
│   ├── fix_review_counts.py  # P0 cross-property patch: Google review count
│   ├── fix_phase2.py      # P0 cross-property patch: canonical + title dedup
│   ├── hashdiff.py        # pre-deploy diff helper
│   ├── link_coverage.py   # reports homepage coverage of sitemap paths
│   ├── gsc_monitor.py     # Search Console daily snapshot + diff
│   └── ...                # preserve.py, update_docs*.py, solve_form_order.py
│
├── <key>/                 # lounge / events / builds / driver / health
│   ├── site/              # versioned HTML + assets (LOCKED: BASELINE-site-hashes.txt)
│   ├── source/            # (events, builds, driver, health) pre-stage source
│   ├── template/          # page template parts (_nav.html, _footer.html, etc.)
│   ├── upload/            # gitignored build artefact; deploy.py ships this
│   └── tools/             # per-property scripts (audit, pages, fix_*, add_*)
│
└── shared/migrations/     # DO NOT RERUN one-shot scripts
```

The five properties are **lounge, events, builds, driver, health**, each with its
own `tools/` directory. `shared/tools/` holds everything that touches more than
one property.

---

## 2. Duplicated Code

### 2.1 Audit boilerplate (~80% identical across all five audits)

**Files:**
- [`lounge/tools/audit_site.py`](lounge/tools/audit_site.py)
- [`events/tools/events_audit.py`](events/tools/events_audit.py)
- [`builds/tools/builds_audit.py`](builds/tools/builds_audit.py)
- [`driver/tools/driver_audit.py`](driver/tools/driver_audit.py)
- [`health/tools/health_audit.py`](health/tools/health_audit.py)

Every audit duplicates verbatim:

| Duplicated block | Lines per file |
|---|---|
| `AI = [...]` word list (17–18 entries, minor per-property variation) | 3 |
| `BRITISH = [...]` word list (13 entries, identical in 3 of 5) | 3 |
| Page walker (`os.walk` + `.html` filter, `pages.sort()`) | 6 |
| Zero-pages guard + `sys.exit(2)` | 4 |
| Sitemap coverage block (parses `site/sitemap.xml`, compares vs `pages`) | 22 |
| Internal-link checker with quote-agnostic `href` regex | 8 |
| JSON-LD validity loop | 6 |
| `G-SQL40ZS59K` GA4 presence check | 2 |
| Tag-balance check (`<div`, `<section`, `<p`) | 5 |
| Final `FAILURES: %d` / `ALL OK` / `sys.exit()` | 3 |

The per-property differences are small and clearly separable:
- **Property-specific forbidden lists** (`FORBIDDEN`, `OFFICIAL`, `BRANCHY`)
- **Default directory** (`site/` vs `upload/`)
- **Column widths** in `print()` calls
- **Additional checks** (e.g. `health` exempts attributed `research-desc` blocks;
  `builds` checks prices against `builds_prices.py`; `driver` checks `#fragment`
  anchors)

**Refactor target:** `shared/tools/audit_lib.py` with:
```python
def walk_pages(directory, extensions=('.html',)): ...
def check_zero_pages(pages, directory): ...
def check_ai_phrases(text, AI_LIST): ...
def check_british(text, BRITISH_LIST): ...
def check_tag_balance(html, tags=('<div','<section','<p')): ...
def check_json_ld(html): ...
def check_ga4(html, tag='G-SQL40ZS59K'): ...
def check_internal_links(html, known_paths): ...
def check_sitemap_coverage(pages, sitemap_path, base_url): ...
def run_audit(pages, checks, formatter): ...
```
Each per-property audit becomes a `main()` that defines its forbidden lists and
calls the shared helpers. **No output format change; no site-file change.**

### 2.2 `add_hub_links.py` — four near-identical copies

**Files:**
- [`lounge/tools/add_hub_links.py`](lounge/tools/add_hub_links.py) — 206 lines
- [`events/tools/add_hub_links.py`](events/tools/add_hub_links.py) — 180 lines
- [`builds/tools/add_hub_links.py`](builds/tools/add_hub_links.py) — 172 lines
- [`health/tools/add_hub_links.py`](health/tools/add_hub_links.py) — 165 lines

Every file duplicates:
- `--tree` argument parsing (~6 lines, identical)
- `rd()` / `wr()` helpers (2 lines, identical)
- `adapt()` CRLF helper (5 lines, **byte-for-byte identical** in events, builds,
  health; lounge lacks it because lounge's source is always LF)
- Footer-patch loop over `os.walk(UP)` (~20 lines, structurally identical)
- Template-file patch logic (~10 lines, structurally identical)

The differences are the `EXPLORE` HTML block and the `OLD_CONTACT`/`NEW_CONTACT`
strings — content, not code. These should be the only per-file content.

**Refactor target:** `shared/tools/hub_links_lib.py`:
```python
def parse_tree_arg(valid=('site','source','upload')): ...
def rd(p): ...
def wr(p, s): ...
def adapt(pattern, s): ...
def patch_homepage(tree_dir, anchor, section_html, sentinel): ...
def patch_footer(tree_dir, old_block, new_block): ...
def patch_template(template_path, old_block, new_block): ...
```
Each `add_hub_links.py` becomes ~40 lines: imports, content constants, calls.

### 2.3 `rd()` / `wr()` — copy-pasted in 7+ files

`io.open(p, encoding='utf-8', newline='').read()` and its write partner appear
as local helpers named `rd`/`wr` in every `add_hub_links.py` and several other
scripts. Should be in `shared/tools/fsutil.py` (or `audit_lib.py`).

### 2.4 `ROOT` / `HERE` path derivation — repeated 20+ times

```python
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
```
Appears in every shared tool. Scripts under `<key>/tools/` use a one-`..` variant:
```python
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
```
**Mixed convention:** shared tools set `ROOT` to the repo root; per-property tools
set `ROOT` to the property root. Scripts that are called from both contexts (e.g.
`add_hub_links.py`) make assumptions that break when the caller is wrong.

**Refactor target:** a `shared/tools/paths.py` module:
```python
def repo_root(): ...      # always the repo root, regardless of cwd
def prop_root(key): ...   # repo_root() / key
```

### 2.5 `HOSTS` / `SITES` / `BASE` — four separate dicts with identical data

- `netlify_lib.py: SITES` — maps key → Netlify site ID
- `release_check.py: HOSTS` — maps key → production URL
- `add_breadcrumbs.py: BASE` — maps key → production URL
- `audit_discovery.py: SITES` — maps key → production URL
- `gen_llms.py: SITES` — maps key → dict with `host`, `name`, `facts`

`HOSTS`, `BASE`, and `audit_discovery.SITES` all map the same five keys to the
same five URLs. Any URL change must be made in four places.

**Refactor target:** extend `netlify_lib.py`:
```python
HOSTS = {
    'lounge': 'https://lounge.academysim.com',
    ...
}
```
All consumers import from `netlify_lib`.

### 2.6 Sitemap URL parsing — repeated in 8 files

```python
xml = io.open(sm, encoding='utf-8').read()
locs = re.findall(r'<loc>\s*(.*?)\s*</loc>', xml)
```
This exact pattern (with minor regex variations) appears in:
`audit_site.py`, `events_audit.py`, `builds_audit.py`, `driver_audit.py`,
`health_audit.py`, `gen_llms.py`, `release_check.py`, `audit_discovery.py`.

**Refactor target:** `def parse_sitemap(path) -> list[str]` in `audit_lib.py`.

---

## 3. Hardcoded Paths and Values

### 3.1 GA4 measurement ID

`G-SQL40ZS59K` appears literally in every audit file (5×) and in
`audit_discovery.py`. One GA4 property rotation requires 6 edits.

**Fix:** define `GA4_TAG = 'G-SQL40ZS59K'` in `shared/tools/constants.py` (or
`netlify_lib.py`).

### 3.2 Academy contact details

`1421 Massaro Blvd`, `Tampa FL 33619`, `(813) 355-9071`, `info@academysim.com`
appear as string literals inside:
- `lounge/tools/add_hub_links.py` (OLD_FOOTER, NEW_FOOTER)
- `events/tools/add_hub_links.py` (OLD_CONTACT, NEW_CONTACT)
- `builds/tools/add_hub_links.py` (OLD_CONTACT, NEW_CONTACT)
- `health/tools/add_hub_links.py` (OLD_CONTACT, NEW_CONTACT)
- `shared/tools/gen_llms.py` (inline in the `facts` strings)

Hours (`Fri & Sat 2–10 PM`, etc.) also appear in at least 4 add_hub_links.py
files. A schedule change requires touching all four patch scripts, all four
`_footer.html` templates, and re-running the build.

**Fix:** `shared/tools/constants.py` with `ADDRESS`, `PHONE`, `EMAIL`, `HOURS`
as named constants. Long-term: extract hours into a single-source JSON that both
the build scripts and the audit scripts read.

### 3.3 Netlify site IDs in `netlify_lib.py`

Currently in code. Low-risk (they are not secrets and do not rotate), but they
are the right candidate for environment variables if the repo is ever moved.
**Current status: acceptable; document in README.**

### 3.4 Token file path in `netlify_lib.py`

The token path is deliberately disabled in this fork (`HACKATHON-FORK-NO-DEPLOY/`
does not exist). `netlify_lib.py` and all callers (`deploy.py`, `release_check.py`,
`gen_replace.py`, `hashdiff.py`) are **out of scope** for this fork — do not
edit them, and do not run them.

### 3.5 `fix_review_counts.py` — hardcoded verbatim HTML strings

`JOBS` in `fix_review_counts.py` holds exact multi-line HTML fragments from
three property source files. These break silently whenever a surrounding edit
changes the whitespace or attribute order. The script detects this (counts the
occurrences and prints `expected 1, found 0`) but the error message names the
fragment, not the cause.

**Partial fix:** add a diagnostic that prints a 3-line context diff when `found
== 0`, so the operator sees what changed rather than just that something did.

### 3.6 Hardcoded price ladder in `builds/tools/builds_prices.py`

This is already the right design — one source, imported by the audit. The audit
comment documents why. **No change needed.** Document the pattern in README as
the template for any future site with versioned content values.

---

## 4. Missing Tests

Only one test file exists: [`shared/tools/test_discovery_gate.py`](shared/tools/test_discovery_gate.py)
(13 assertions for `premises_claim()` and `PREMISES_OK` regex).

### 4.1 What has no tests

| Component | Risk if broken | Notes |
|---|---|---|
| `stage.py` DEPLOYABLE allowlist | High — the F8 regression class | Mutation-tested once by hand; no automated regression |
| `check_staged.py` verify/record logic | High — the loss gate | No test; relied on mutation test in F8 |
| `gen_llms.py` `build()` and `strip_brand()` | Medium — llms.txt correctness | Self-checks inside the script are not unit tests |
| `audit_lib` (proposed) helpers | Medium | Will have no tests if written the same way |
| `netlify_form_rewrite_only()` | Medium — false negatives report clean when dirty | No test |
| `add_breadcrumbs.py` `trail()` parser | Medium — BreadcrumbList correctness | No test |
| All five per-property audits | High — they ARE the quality gate | No test for the gate itself |
| `fix_review_counts.py` substitution logic | Medium | No test; runs in build |
| `adapt()` (CRLF helper, 4 copies) | Low-Medium | No test |

### 4.2 Recommended test suite

```
shared/tests/
├── test_stage.py               # DEPLOYABLE allowlist, SKIP_DIRS, JUNK regex
├── test_check_staged.py        # empty inventory fails, missing path fails, new path is a note
├── test_audit_lib.py           # shared audit helpers (once extracted)
├── test_gen_llms.py            # strip_brand(), NOTES gate, EM-DASH check
├── test_netlify_form_rewrite.py # netlify_form_rewrite_only() happy and negative paths
├── test_add_breadcrumbs.py     # trail() parsing with linked / unlinked crumbs
└── test_discovery_gate.py      # (already exists; move here)
```

**Runner:** stdlib `unittest` or `pytest` (no new deps needed for `unittest`).
Entry point: `python -m pytest shared/tests/` or `python -m unittest discover
-s shared/tests`.

Each test file mirrors the module it covers; no test crosses a module boundary
except for integration tests explicitly named `test_integration_*.py`.

### 4.3 Mutation-test protocol (for gates)

The F8 incident established that a gate not tested by breaking it is not trusted.
Document this as a CONTRIBUTING rule:

> For every gate: before merging, revert the thing it guards and verify the gate
> exits non-zero. Record the mutation in the test file as a comment.

---

## 5. Dependency and Packaging State

### 5.1 Python version requirement

Implicit. The scripts use:
- `f-strings` — requires Python 3.6+
- `glob(..., recursive=True)` — requires Python 3.5+
- `subprocess.run()` — requires Python 3.5+
- `sys.stdout.reconfigure()` — requires Python 3.7+
- No type annotations, no `match` statements

**Minimum: Python 3.7.** Not stated anywhere.

### 5.2 Runtime dependencies

All stdlib except:
- `curl.exe` — called as a subprocess in `release_check.py`, `deploy.py`,
  `audit_discovery.py`, `netlify_lib.py`. Must be on `PATH`. Not documented.
- Google Search Console API (`gsc_monitor.py`):
  - `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`,
    `google-api-python-client`
  - Version requirements: unstated
  - Not needed for the core build/audit/deploy pipeline

No `requirements.txt`, no `pyproject.toml`, no `setup.cfg` exists in the repo.

### 5.3 Packaging recommendation (minimal)

Add two files, no build system needed:

**`requirements.txt`** (runtime, core pipeline — stdlib only, no entries needed):
```
# Core pipeline: stdlib only (Python >= 3.7)
# curl.exe must be on PATH for: deploy.py, release_check.py, audit_discovery.py
```

**`requirements-gsc.txt`** (optional, only for gsc_monitor.py):
```
google-auth>=2.0
google-auth-oauthlib>=1.0
google-auth-httplib2>=0.1
google-api-python-client>=2.0
```

**`README.md` addition** — one section: "Prerequisites":
```
Python >= 3.7
curl.exe on PATH (ships with Windows 10 1803+; verify with: curl.exe --version)
For GSC monitoring only: pip install -r requirements-gsc.txt
```

### 5.4 No virtual environment

Scripts are run directly with the system Python. Acceptable for a single-
operator repo; document it as a deliberate choice rather than an oversight.

---

## 6. Prioritized Refactor List

Priority is `impact × safety`. Impact = how much ongoing cost does this avoid;
safety = how easily can the refactor be verified (BASELINE hashes + audit exits).

### P0 — Prerequisite (implement before anything else)

**P0: `shared/tools/verify_baseline.py` + `shared/tests/test_verify_baseline.py`**

Create the offline site-integrity gate. This is the first thing run before and
after every subsequent step.

`verify_baseline.py`:
- Reads every `sha256 *path` line from `BASELINE-site-hashes.txt`
- Computes SHA-256 of the file on disk; prints `CHANGED: <path>` or
  `MISSING: <path>` for each failure
- Exits 0 when all hashes match, 1 on any mismatch, 2 if it checked zero files

`shared/tests/test_verify_baseline.py`:
- Passes when all hashes match (golden path)
- Fails (exit non-zero) when a site file is altered — the mutation test
- Fails (exit 2) when the baseline file is empty

Verified by: `python shared/tools/verify_baseline.py` exits 0 on an unmodified
working tree.

**P1-B(i): `BASELINE-upload-hashes.txt` + extend `verify_baseline.py`** ✓ DONE (89952c3)

Gap: `verify_baseline.py` only covered `*/site/`. `build_all.py` writes
shippable output to `*/upload/`, and `add_hub_links` / `fix_*` patch it. A
regression there would pass the gate.

Fix:
- `BASELINE-upload-hashes.txt`: 136 SHA-256 hashes of every file under
  `*/upload/` produced by `build_all.py` at commit 8e5768e (the pre-Bob commit;
  built from the `_before` worktree at `G:\Projects\Hackathon\_before`).
- `verify_baseline.py` extended to check both baselines. `main()` reports each
  separately; exit codes unchanged (0/1/2).
- Two new tests in `test_verify_baseline.py`: `test_upload_mutation_caught_by_main`
  (tamper upload/ only → exit 1) and `test_upload_mutation_not_caught_without_upload_baseline`
  (documents the gap that motivated this change).

### P1 — Do first (high impact, safe to verify)

**P1-A: `shared/tools/constants.py`**

Extract: `GA4_TAG`, `HOSTS` dict (production URLs), `ADDRESS`, `PHONE`, `EMAIL`.
Update the 6+ files that hardcode them. No logic change, pure constant
extraction. Verified by: `python -m unittest shared/tests/` (once tests exist);
all five audit scripts still exit 0; BASELINE hashes unchanged.

**P1-C: `shared/tests/test_stage.py` + `shared/tests/test_check_staged.py`** ✓ DONE (84e096b)

Regression tests for the two highest-risk build gates (F8 incident protocol).

`test_stage.py` (35 tests):
- `TestDeployableAllowlist`: every deployable extension is present (`.html`,
  `.xml`, `.toml`, `.png`, `.webp`, `.css`, `.js`, `.txt`, `.json`, `.svg`,
  `.ico`, `.woff2`); `.py` and unknown extensions are excluded.
- `TestJunkExclusion`: JUNK regex matches `.bak-*`, `.orig`, `.tmp`, `.swp`,
  `.pyc`, `~`; normal files pass.
- `TestSkipDirs`: `tools/`, `backups/`, `backup/`, `node_modules/` are in
  SKIP_DIRS; dot-dirs and underscore-dirs are excluded; normal dirs are walked.
- `TestZeroStagedGuard`: verifies the zero-staged failure guard exists in source.

`test_check_staged.py` (8 tests):
- Missing inventory file → fails.
- Empty inventory → fails (a gate that checks nothing must not pass).
- Path in inventory absent from `upload/` → fails.
- New path in `upload/` not in inventory → note only, not a failure.
- Empty `upload/` directory → fails.
- All inventory paths present → passes.
- `record()` writes correct inventory; refuses to record empty `upload/`.

Note: the old `test_discovery_gate.py` stays in `shared/tools/` (not moved to
`shared/tests/`) to avoid breaking any existing references. Both paths are
discovered by the test runner.

Note: `test_netlify_form_rewrite.py` is still planned (P3-B) but `release_check.py`
itself must not be imported in this fork's test runs — import only the pure
function `netlify_form_rewrite_only` after confirming it has no side effects at
module level.

### P2 — Do second (medium impact, requires care)

**P2-A: `shared/tools/audit_lib.py`**

Extract the duplicated audit helpers (see §2.1). Port one audit at a time,
verifying each exits 0 before moving to the next. Lounge audit (`audit_site.py`)
differs most from the others (it checks `site/` not `upload/`); port it last.

Sequence: events → builds → health → driver → lounge

After each port: `python <key>/tools/<key>_audit.py` exits 0 (no site changes).
BASELINE hashes: unaffected (audits read, do not write).

**P2-B: `shared/tools/hub_links_lib.py`**

Extract `rd`, `wr`, `adapt`, `--tree` parsing, footer-patch loop, template-patch
logic. Each `add_hub_links.py` becomes a thin wrapper. Verified by: run
`python shared/tools/build_all.py` and confirm all five `check_staged.py`
inventories still match + BASELINE hashes unchanged.

**P2-C: Unify `HOSTS`/`BASE`/`SITES` URL dicts**

After P1-A, `add_breadcrumbs.py`, `audit_discovery.py`, and `gen_llms.py` all
import their URL map from `constants.py`. Update `release_check.py` at the same
time (its `HOSTS` is identical). Four files touched; zero logic change.

**P2-D: `paths.py` — repo_root() / prop_root()**

Replace the 20+ `HERE`/`ROOT` derivation blocks. Per-property tools can call
`prop_root('lounge')` without knowing their own path; shared tools call
`repo_root()`. Eliminates the mixed-convention bug (§3.2).

### P3 — Do third (lower urgency or higher complexity)

**P3-A: `test_gen_llms.py` — test strip_brand() and NOTES gate**

`strip_brand()` has two separators, multiple edge cases, and a "never return
empty" rule. None are currently tested. The NOTES gate (a builds circuit page
with no note fails the build) is tested only by running the full build.

**P3-B: `test_netlify_form_rewrite.py`**

`netlify_form_rewrite_only()` is the most complex pure function in the codebase
(~30 lines, a linewise diff). It is also the function that classifies a hash
difference as benign. A false positive here silently passes a real content
difference.

**P3-C: Add `--dry-run` to `build_all.py`**

Print the STEPS list without executing. Makes it possible to inspect the build
plan in CI without side effects. No logic change to any step.

**P3-D: Document one-shot / migration scripts**

`shared/migrations/` has a `README.md` that marks the three scripts `DO NOT
RERUN`. Extend it with: what each script did, what its output committed, and
why the output cannot be regenerated by the build.

**P3-E: Diagnostic improvement for `fix_review_counts.py`**

When `found == 0` for a substitution job, print a 3-line context diff of the
expected fragment vs what is actually in the file. Reduces "expected 1, found 0"
from a mystery to a diffable change.

**P3-F: `add_breadcrumbs.py` — write test for `trail()`**

The `trail()` function parses a visible breadcrumb HTML block. It is called on
every `site/**/index.html`. An off-by-one in the crumb parser would produce
BreadcrumbList schema that contradicts the visible page — a structured-data
violation. No current test.

---

## 7. What NOT to Refactor

These are correct and should not be touched:

**The STEPS ordering in `build_all.py`** — The comments document why every
ordering constraint exists. The F8 incident proved that changing this silently
breaks builds. Do not reorder.

**The `upload/` clear at the start of `build_all.py`** — Deliberately clears
stale artefacts. A "smarter" incremental copy would reintroduce the stale-file
class of bug.

**`deploy.py` using `live_manifest()` as the base digest** — This is what makes
the deploy a merge rather than a replace. Simplifying it to "just upload
`upload/`" would reintroduce the drag-and-drop regression class.

**`check_staged.py` inventory JSONs** — They are ground truth for the loss gate.
Do not auto-generate them on every build; they must be a deliberate `--record`
act after a verified staging.

**The `adapt()` CRLF function in each `add_hub_links.py`** — Even after
extraction to a lib, this must remain unchanged. `.gitattributes` pins `eol=lf`
on checkout but `builds/source/index.html` existed before the pin. The function
protects against mixed line endings in that one file.

**Per-property `FORBIDDEN` / `OFFICIAL` / `OUTCOME_VERB` lists in the audits** —
These are legal and compliance claims, not code. They must remain easy to audit
by a non-programmer. Do not move them into a shared data structure that obscures
which check applies to which property.

---

## 8. Execution Order Summary

```
P0       verify_baseline.py + test_verify_baseline.py   (gate; done e360df8)
P1-A     shared/tools/constants.py               (done b28ccb5)
P1-B(i)  BASELINE-upload-hashes.txt + extend verify_baseline.py (done 89952c3)
P1-C     test_stage.py + test_check_staged.py    (done 84e096b)
P2-C  Unify URL dicts (depends on P1-A)
P2-A  audit_lib.py, one property at a time    (events → builds → health → driver → lounge)
P2-B  hub_links_lib.py                        (after P2-A; same lib can absorb rd/wr)
P2-D  paths.py                                (after P2-B; only then is ROOT consistent)
P3-A  test_gen_llms.py
P3-B  test_netlify_form_rewrite.py            (import pure function only; do not import module)
P3-C  --dry-run for build_all.py
P3-D  migrations/ README extension
P3-E  fix_review_counts diagnostic
P3-F  test_add_breadcrumbs.py / trail()
```

**After every step:** run `python shared/tools/verify_baseline.py` (offline,
exits 0 immediately), then `python shared/tools/build_all.py` when the step
touches build logic. No step is complete until both pass.

**Never run in this fork:** `release_check.py`, `audit_discovery.py`,
`gsc_monitor.py`, `deploy.py`, `gen_replace.py`, `hashdiff.py`,
`netlify_lib.py`.
