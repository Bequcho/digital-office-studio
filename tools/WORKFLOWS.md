# Workflow safety checks (SEO Step 9.2)

The baseline site and build sources are commit `b200956` (Step 9.1).
No generated HTML, styles, assets, robots, sitemap or CRM are changed by this repair.

## Maintained generators

- Audit localization translates `audit/index.html`, then uses `seo_hreflang`,
  `seo_schema` (including the existing localized WebApplication) and `seo_social`.
  Sitemap discovery uses `build_sitemap`. It no longer rewrites homepages.
- Python replacement escaping is fixed in `scripts/localize_audit.py` itself;
  Actions no longer patch the script at runtime.
- The older industry SEO workflows now call the maintained `tools/build.py`
  and its regression suite instead of obsolete one-off upgrade scripts.
- Audit entry / free tools navigation and lead-system installation also use the
  maintained build. Lead installation no longer scans CRM, tools or redirect HTML.
- Historical PDF fixes use the current PDF v3 installer rather than overwriting
  the current inline JS / contact markup.
- RUB and Georgian budget migrations recognize already-applied changes.
- Whole-tree legacy migrations explicitly exclude CRM.
- Portfolio rendering preserves the existing hreflang serialization order.

`add-audit-entry-home.yml` formerly had unindented multiline CSS breaking YAML;
its inline installer also added a second audit block. Using maintained homepage
components fixes both issues.

## Validation and safe simulation

Install `tools/requirements-workflows.txt`, then run:

```
python tools/test_workflows.py
python tools/test_build.py
 git diff --check
```

`validate-workflows.yml` runs these checks with read-only repository permissions
on main pushes and pull requests. Audit localization validates before its existing
commit/push step. Other publishing steps are not executed locally.

The validator checks all YAML (including duplicate keys), shell syntax with
`bash -n`, embedded Python syntax, permissions and the expressions currently used
in this repository. It deliberately rejects expressions outside its small supported
set rather than pretending to implement the whole GitHub expression language.
This is not a complete actionlint implementation or a GitHub-hosted runner test.

Simulation runs only extracted local Python generation steps in a temporary copy.
It does not run checkout/setup/install actions, shell publishing steps, git commands,
IndexNow or API calls. Python audit hooks block network/process creation and writes
outside the copy. Every file is compared to the baseline after every workflow;
localized audit generation is also run a second time. Separate regression tests
cover SEO Steps 1–8 and byte-identical full builds. CRM API/form submissions are
never exercised.

All 30 write workflows are simulated. The two read-only workflows are validation
itself and IndexNow; the latter has separate offline tests with fake HTTP.

## IndexNow: manual only, dry-run by default

There are no push, schedule, deployment or other automatic submission triggers.
`indexnow.yml` has only `workflow_dispatch`, with a required boolean `dry_run`
defaulting to `true`. The existing public key and IndexNow JSON authentication
fields are unchanged. The script also defaults to dry-run; real submission
requires `dry_run=false` plus the GitHub `workflow_dispatch` context on `main`.

### Operator procedure

1. Publish the intended site changes through the existing Pages process and wait
   for that deployment to finish successfully. Verify the intended version is
   available on `https://beqson.com/`. This workflow does not deploy anything or
   prove that a particular commit SHA has been deployed.
2. Open **Actions → IndexNow manual sitemap validation → Run workflow**.
   Select branch **main** and leave **dry_run** checked (`true`).
3. Inspect the log: every accepted URL is marked `VALID`; rejected URLs are
   marked `SKIP` with a reason. A JSON summary lists accepted/skipped URLs,
   blocking errors and submission count. Dry-run performs production GET checks
   but never calls the IndexNow endpoint.
4. Only after a successful dry-run, manually run the same workflow on **main**
   with **dry_run** unchecked (`false`). All validations are repeated immediately
   before one submission; no cached dry-run URL list is trusted.
5. If the run is blocked or all URLs are skipped, nothing is submitted. Resolve
   the deployment/access problem before requesting another run.

### Validation and failure behavior

- Candidate URLs come only from the checked-out `sitemap.xml`, not git history.
- URLs must use exactly `https://beqson.com`, without query/fragment; duplicates,
  root redirects, private/technical and non-indexable local files are skipped.
- URLs must also exist in the **published** sitemap and be permitted by published
  robots.txt. Public SEO tools remain eligible when indexable/self-canonical.
- Production HTML must respond HTTP 200 without redirects, have one self-canonical
  in `<head>`, and have no meta/header noindex or HTML/JavaScript redirect.
- The existing key file must match locally and publicly. Key availability alone
  is never treated as evidence that pages have been deployed.
- Network failures, access blocks (including proxy 403), rate limits, server errors,
  unavailable sitemap/robots/key or malformed XML block the **entire batch**.
  A preceding accepted URL is never sent before the remaining checks finish.
- Individual 404/redirect/noindex/noncanonical pages are skipped with reasons.
- More than 10,000 accepted URLs blocks submission rather than silently truncating.

Offline tests (`python tools/test_indexnow.py`) use fake HTTP responses and block
real sockets. They cover the default dry-run, manual-send gate, URL filtering,
production failures and all 52 real sitemap entries. They never send IndexNow
requests. The validation workflow runs these tests automatically, not IndexNow.

Existing bot commits use checkout's default GITHUB_TOKEN, not a PAT or custom SSH
key. Such pushes normally do not trigger another push workflow, preventing recursive
runs. Parallel writers can still encounter a non-fast-forward push rejection;
there are no force pushes. The local simulation cannot verify repository rules,
Actions permissions, branch protection or the actual Pages deployment settings.
