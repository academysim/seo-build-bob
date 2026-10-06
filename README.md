# Academy Subdomain SEO Build, modernized with IBM Bob

Submission for **Building with IBM Bob** (AngelHack x IBM, track: *Modernize What Matters*).

This is the static-site build system behind five live marketing subdomains of Academy Sim Racing
(lounge, events, builds, driver, health). It started as a pile of one-off generator scripts with copy-pasted
audits and hard-coded URLs. During the hackathon, IBM Bob refactored it into shared libraries, added a
one-command build, a byte-for-byte regression gate and a 171-test suite, **without changing a single byte
of the deployed output**.

- What Bob changed, commit by commit: [`BOB-COMMITS.txt`](BOB-COMMITS.txt)
- What was improved and how to check it: [`IMPROVEMENTS.md`](IMPROVEMENTS.md)
- The plan Bob worked from: [`MODERNIZATION-PLAN.md`](MODERNIZATION-PLAN.md)

## Quick start (offline, Python 3.10+, standard library only for these three commands)

```bash
python shared/tools/build_all.py              # rebuild every property, exit 0
python shared/tools/verify_baseline.py        # 263 deployed files byte-identical to the pre-Bob baseline
python -m unittest discover -s shared/tests   # 171 tests, OK
```

Deploy scripts exist for completeness but need credentials that are not in this repo; nothing here can
publish anything.

## Layout

```
<property>/tools/      generators, audits and deploy scripts
<property>/template/   nav/footer/css extracted from that site's live homepage
<property>/site/       the deployable output that is currently live
shared/tools/          cross-property libraries and utilities (audit_lib, hub_links_lib, constants, build_all)
shared/tests/          the test suite
BASELINE-*.txt         SHA-256 of every deployed file before Bob touched the code
```

## How a property is built

1. `<property>_pages.py` holds the page template and helpers.
2. `<property>_content*.py` holds the content and writes pages into `site/`.
3. `<property>_audit.py` gates the result. **Never deploy without it passing.**
4. `<property>_deploy.py` ships it. `--prod` to publish; without it you get a draft.

Rebuilding from `_content*.py` **reverts the `fix_*.py` patches**, which operate on generated output. Re-run them, then the audit, or you will silently reship fixed defects.

## Credentials

None are stored here. Deploy scripts read `NETLIFY_AUTH_TOKEN` from a local env file at runtime.

## The two things worth knowing

**Digest deploy.** Events, Builds, Driver and Health were created by drag-and-drop, so there is no upstream source and `_redirects` / `netlify.toml` cannot be fetched over HTTP. `*_deploy.py` uses Netlify's digest API: declare every existing file by its current SHA1, Netlify replies with only the hashes it lacks, and everything else is reused byte-for-byte. Existing files are carried across without ever needing their content. A `REPLACEABLE` allowlist means an existing file can only be overwritten deliberately.

**The 49-byte form rule.** Netlify's only edit when serving a drag-and-drop page is stripping `data-netlify="true" netlify-honeypot="bot-field"` from each form: exactly 49 bytes per form. That is why a fetched copy of a homepage is not the deployed file. `shared/tools/rebuild_index.py` restores those attributes to turn a fetched page back into deployable source, and `solve_form_order.py` brute-forces the attribute order against the deploy manifest's SHA1 when the size is right but the hash is not. Both homepages were reconstructed byte-identically this way and are now freely editable.

## Rules the audits enforce

Each property has non-negotiables baked into its audit rather than left to care:

- **all** — no em dashes in authored copy, no AI-tell phrasing, American spelling, GA4 present, one `<h1>`, canonical matching path, valid JSON-LD, balanced tags, no broken internal links
- **lounge** — no class on `<body>` that sets `overflow:hidden`; it propagates to the viewport and kills scrolling while leaving scripted scrolling working, so only a human with a mouse finds it
- **events** — an "official Formula 1/NASCAR/IMSA simulator" phrase must be followed by a denial; every city page must state it is not a branch
- **builds** — no price outside the five published builds
- **driver** — banned phrasings around school installations, and every page must carry the explicit "no simulators installed in any school" disclosure
- **health** — no outcome verb applied to a health noun, and every page must carry the "not a medical provider" scope disclaimer

## Verify

Run offline (no network required):

```bash
python shared/tools/verify_baseline.py
```

Checks that all 263 deployed files (127 in `site/` + 136 in `upload/`) are byte-identical to the pre-Bob baseline. Exits 0 on a clean repo, non-zero on any mismatch.

Run the full test suite:

```bash
python -m unittest discover -s shared/tests
```

171 tests across 10 files covering `audit_lib`, `hub_links_lib`, `constants`, `verify_baseline`, `stage`, `check_staged`, `gen_llms`, `netlify_form_rewrite`, `add_breadcrumbs`, and `build_all --dry-run`. All exit 0.

See [`IMPROVEMENTS.md`](IMPROVEMENTS.md) for the full audit trail and one-command verification of all checks.
