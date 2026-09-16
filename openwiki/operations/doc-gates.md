---
type: enforcement-layer
title: Documentation Gates and Enforcement Tools
description: The tools/hx-doc/ enforcement layer — what each gate checks, what it refuses, and what a failure means — plus the CI layer and the meta-gate that breaks every checker on purpose.
tags: [documentation-gates, ci, enforcement, hx-doc, proof-chain, graft, version-pins]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-15T22:39:27.588Z
sources:
  - id: openwiki-source-4a10bba62772b26bb2a2e6b3
    resource: repo://.github/workflows/hx-checks.yml
  - id: openwiki-source-6039b489b5096b4c78d1d80d
    resource: repo://.github/workflows/hx-upstream-drift.yml
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-031feb6606529a37844764d1
    resource: repo://tools/hx-doc/hx_doc_check.py
  - id: openwiki-source-7535508c0d148b08f4414508
    resource: repo://tools/hx-doc/hx_doc_supersede.py
  - id: openwiki-source-058667b14857202ef49933ce
    resource: repo://tools/hx-doc/hx_fleet.py
  - id: openwiki-source-9507fc66f6719dc4c336f195
    resource: repo://tools/hx-doc/hx_gate_tests.py
  - id: openwiki-source-97e1d90aab73bf6b59824395
    resource: repo://tools/hx-doc/hx_new_server.py
  - id: openwiki-source-3edf0d2c56c6b02f0e70353e
    resource: repo://tools/hx-doc/hx_preflight.py
  - id: openwiki-source-d3a3650a1878a8482b4c0fff
    resource: repo://tools/hx-doc/hx_proof.py
  - id: openwiki-source-bf6a46fe85337b9b2d7d499a
    resource: repo://tools/hx-doc/hx_record_check.py
  - id: openwiki-source-7e54593e1179ec2c375e54a7
    resource: repo://tools/hx-doc/hx_render_html.py
  - id: openwiki-source-363db13c90e3016aa0f261ab
    resource: repo://tools/hx-doc/hx_smoke_lint.py
  - id: openwiki-source-1b6936d3e99ab8243153e1c6
    resource: repo://tools/hx-doc/hx_upstream_drift.py
  - id: openwiki-source-66d9417f03ff09c95f5bfe2d
    resource: repo://tools/hx-doc/hx_version_pins.py
  - id: openwiki-source-f2994b36a477b8759d39a2a6
    resource: repo://tools/hx-doc/README.md
generated: { by: "openwiki/0.5.1", at: "2026-09-15T22:39:27.588Z" }
---

# Documentation Gates and Enforcement Tools

The `tools/hx-doc/` directory is a small set of Python tools (no third-party
dependencies — standard library only) that turn written rules into checks that
fail loudly. Each tool exists because the matching defect actually happened in
this repository, so each is paired with the failure it was built to catch. The
core principle, stated in AGENTS.md section 14, governs the whole layer:

> Written rules that nothing checks will drift. These tools are the enforcement
> layer; treat a failure as a real defect, not as noise to work around. If a
check is wrong, fix the check in a reviewed change. Do not bypass it and do not
weaken it to make an existing document pass.

This page is context, not authority. The tools themselves and AGENTS.md section
14 are the authority. When a check and this page disagree, the tool wins.

## How the layer fits together

Two pieces of control flow matter for an operator:

- **Before committing.** Every documentation change must run
  `tools/hx-doc/hx-doc-check` and `tools/hx-doc/hx-render-html` before it is
  committed. CI runs both and fails the change otherwise. The canonical
  regenerate-and-check sequence from AGENTS.md section 13 is
  `tools/hx-doc/hx-fleet && tools/hx-doc/hx-render-html && tools/hx-doc/hx-doc-check`.
- **On every PR.** `.github/workflows/hx-checks.yml` runs the documentation gate
  suite plus script-quality gates (shellcheck, CRLF/executable-bit, Python
  compile) and a secret scan. A second workflow, `.github/workflows/hx-upstream-drift.yml`,
  runs the two currency tools weekly.

The meta-gate `hx-gate-tests` (see [The meta-gate](#the-meta-gate-hx-gate-tests))
sits on top of all of this: it deliberately breaks every checking tool and
requires it to fail. A check that cannot fail is treated as a defect, not as
coverage.

### CI: `.github/workflows/hx-checks.yml`

The `documentation` job runs, in order: `hx-doc-check`, `hx-fleet --check`,
`hx-proof --check`, `hx-render-html --check`, `hx-record-check`,
`hx-smoke-lint --quiet`, and then `hx-gate-tests`. The `scripts` job installs
shellcheck and runs it (shell only — Python files are filtered out) over the
runbook `.sh` files, `hx-app-lib.sh`, `hx-base.env`, the smoke-runner scripts,
and the `tools/hx-doc` wrappers; it also checks that every `docs/03-runbooks/**/*.sh`
and `tools/hx-smoke-runner/hx-smoke-*` file is LF and executable, and runs
`python3 -m compileall -q tools/`. The `secrets` job installs a pinned,
checksum-verified gitleaks binary and scans both the working tree and full
history. The workflow checks out with `persist-credentials: false` because the
jobs run repository-controlled scripts and need no authenticated git.

### Weekly currency: `.github/workflows/hx-upstream-drift.yml`

Runs on a Monday cron (and on dispatch). It runs `hx-preflight --quiet`,
collects markdown tables from `hx-upstream-drift` and `hx-version-pins`, and
decides drift. Drift is **information, not a failure**: a drifted pin opens or
updates a GitHub issue (`upstream-drift` label) rather than failing the job. The
one thing that does fail the job is an upstream that could not be reached —
reporting an unreachable upstream as a clean run is exactly the "check that
cannot fail" the repository keeps removing, so `could not be reached` in the
report is an error.

## The gates

Each tool is a Python 3 body (e.g. `hx_doc_check.py`) beside a tiny extensionless
shell wrapper that resolves a Python 3 and execs the body. The wrappers are
intentionally not indexed by graft (see [Graft](#graft-a-finding-tool-not-a-gate)).

### hx-doc-check

`tools/hx-doc/hx_doc_check.py` — the broad documentation consistency check. It
runs eight named checks and exits non-zero if any fails:

- **links** — every internal Markdown link and backticked path reference
  resolves, unless the surrounding text declares an intentional forward
  reference (phrasings like `not yet created`, `authority gap`, `planned`,
  `external to this repository`). Upstream trees (`deploy/`, `docs/LightRAG`,
  `integrations/`, `.agents/`) are excluded, and candidate targets are clamped
  to the repository root so a `../../...` traversal that escaped the repo could
  not pass on whatever happened to exist on the running machine.
- **vocabulary** — `SKILL-REGISTRY.md` uses only lifecycle states that
  `SKILL-GOVERNANCE.md` section 4 defines.
- **frontmatter** — active control documents in `docs/00-control/` carry
  `document`, `status`, and `date`.
- **duplicates** — no versioned, dated, or `final-final`-style duplicate of an
  active document; active documents use stable filenames.
- **evidence** — `.gitignore` cannot swallow a retained evidence log
  (`docs/05-evidence/...`). It runs `git check-ignore` and treats any exit
  other than 0 (ignored) or 1 (not ignored) as a failure, so a git error
  outside a work tree cannot report the evidence path as committable.
- **units** — a runbook block may only report (`hx_app_done`) a systemd unit it
  actually creates; comments and `rm` lines do not count, so the check stays
  fail-able.
- **authority** — the generated `<!-- OPENWIKI:START -->…END -->` block in
  `AGENTS.md` may not call source code or tests authoritative. It parses the
  block sentence by sentence, in both word orders, with whole-word matching
  (`"attests"` must not match `"tests"`), and accepts a sentence that *denies*
  the claim. Naming `docs/` does not license calling code authoritative,
  because section 2's truth order has no entry for source code at all. A red
  build here means the OpenWiki generator regressed; correct
  `openwiki/INSTRUCTIONS.md`, never the generated block.
- **tooling** — every `docs/06-tooling/` document has the five required
  headings (`What it is`, `Why we have it`, `When to use it`, `How to use it`,
  `Upstream`) in the index's required order, with two distinct real links under
  `Upstream` (the documentation and the source — one link, or the same URL
  twice, is refused). The index is true: a table row naming a file has that
  file, and a file that exists is linked from a row. Fenced examples are
  ignored throughout (backtick and tilde fences, with CommonMark-correct
  closing rules). A backlog row (`not written yet`) is reported on every run,
  not failed — the gap stays visible — and the backlog count is still reported
  even when the check fails on something else.

Generated trees (`.git`, `archive`, `human-html`, `.claude`, `graft`,
`openwiki`) are skipped by `active_markdown()`: a broken link inside
`openwiki/` is a defect in the generator or its source, never a finding against
the repository, and `hx-gate-tests` proves the skip is a skip and not a hole.

### hx-proof

`tools/hx-doc/hx_proof.py` — generates and validates the smoke-test proof DAG
from `docs/00-control/hx-proof.tsv`. The TSV is the source; phase tables and the
mermaid DAG in the smoke-test roadmap are generated from it. `--check` is CI
mode (exit 1 if a generated block is stale, missing, or duplicated);
`--ready <id>` asks whether a step may run yet; `--list` prints every step with
readiness.

Validation refuses: a blank or duplicate step id; a missing TSV column; a
`requires` that names a step that does not exist (dangling dependency); an
`authority` file that does not exist; an `sut` that is not a host in
`hx-fleet.tsv`; an unrecognised `status` (only `NOT_RUN`, `PASS`, `FAIL`,
`NOT_EXECUTABLE`); and a cycle in the dependency graph. A missing or empty
fleet inventory is itself a failure rather than silently skipping the SUT check.
`hx-smoke-promote` reads the same TSV and refuses a PASS whose prior proof has
not passed and been cited; there is no bypass flag — a dependency that does not
apply is changed in the TSV through a reviewed pull request.

### hx-render-html

`tools/hx-doc/hx_render_html.py` — every `human-html/*.html` mirror must match
its Markdown source. `--check` (CI) reports `STALE` mirrors and `ORPHAN` HTML
files with no source, and exits 1 if either exists. `human-html/` is generated
output and never hand-edited; the correction is to edit the Markdown and run
`tools/hx-doc/hx-render-html`. Each rendered page carries a banner stating it is
a human mirror, not execution authority.

### hx-version-pins

`tools/hx-doc/hx_version_pins.py` — audits product version pins against what
upstream currently ships (Ollama, the NVIDIA driver, the reranker, Python/npm
dependencies, Hugging Face model revisions). It also enforces the
package-source policy through `source_problem()`:

- **Snap is never permitted, for anything** — an application or a driver pinned
  to Snap is refused with `never permitted` and a migration note (decision D-021).
- The **Ubuntu archive is allowed only for drivers** (and build toolchains /
  library headers, which are apt-installed inside runbook blocks and are not
  pins). An application pinned to the Ubuntu archive is reported as REVIEW with
  a migration note.
- Application sources `pypi`, `npm`, `github`, `source` (upstream tarball),
  `binary`, and `huggingface` are accepted.

The approved-source display phrases are derived from the `APP_SOURCES` set and
the module raises (not asserts — `python -O` strips asserts) if the phrases,
display order, and set drift apart, so the remediation message cannot drift
from the set it enforces.

### hx-upstream-drift

`tools/hx-doc/hx_upstream_drift.py` — the registry's reviewed commits are
still current. It reads pins directly out of `skills/SKILL-REGISTRY.md`
provenance blocks (so it cannot fall out of step with a second list), compares
each pinned SHA to upstream HEAD, and reports how many commits behind each pin
is. It refuses unpaired provenance: if a block lists a different number of
repository lines and reviewed-commit lines, it errors with `pair up` (because
`zip()` would silently drop the surplus and pair a repo with another entry's
commit). An unreachable upstream is reported, and under `--fail-on-drift` an
unreachable upstream fails rather than reading as current.

### hx-record-check

`tools/hx-doc/hx_record_check.py` — server records follow the template and
open gaps stay visible. It reports three kinds per record: `MISSING` (a
required section absent, modulo an explicit `**Not applicable:**` exemption),
`UNRESOLVED` (a field recorded as not yet known — a recorded gap, not an error),
and `DRIFT` (the record's `**Build state:**` disagrees with `hx-fleet.tsv`, or
the record is not in the TSV, or the State line is missing). The state
comparison is whole-value and normalised, because the old first-word match let
`NOT STARTED` be satisfied by `NOT APPLICABLE`. By default UNRESOLVED does not
fail; `--strict` fails the build on it.

### hx-smoke-lint

`tools/hx-doc/hx_smoke_lint.py` — smoke-test authorities in `smoke-tests/`
carry every required section. It checks for the six canonical sections (Title &
Purpose, Prerequisites, Test Steps, Sample Data, Expected Output, Cleanup /
Teardown), a known-answer marker (service health is not a smoke test), and a
mention of evidence retention. Evidence retention is anchored to the standard
bundle path `docs/05-evidence` in the body, not to the word "evidence" or
"retain", because a negated sentence like "do not retain credentials"
satisfies those; a bare `## Evidence` heading with nothing under it does not
satisfy the check.

### hx-fleet

`tools/hx-doc/hx_fleet.py` — every fleet table and the runbook IP map come
from `docs/00-control/hx-fleet.tsv`. A document opts in with an
`<!-- HX-FLEET:TABLE columns=... -->` / `<!-- /HX-FLEET:TABLE -->` marker pair.
The tool also writes `docs/03-runbooks/common/hx-fleet-ips.env` so runbooks read
the same source. `--check` (CI) fails on a stale, unclosed, orphan-closing, or
unknown-column marker.

### hx-new-server

`tools/hx-doc/hx_new_server.py` — a new server's runbook and record are
complete from the start. It scaffolds the runbook wrappers, the runbook README,
and the server record from `docs/02-server-records/_TEMPLATE.md` and the fleet
TSV. It refuses: a misspelled `--` flag (exit 2, `unknown option`); a host not
in the TSV; and a template placeholder that no longer matches exactly once
(returns 1 with `placeholder`), so a template edit cannot ship a record still
reading `HX-N` / `192.168.50.2NN`. The record is built and validated *before*
anything is written, so a template defect cannot leave wrappers on disk with
no record beside them. `--force` is required to overwrite; `--no-ollama` skips
the Ollama block for non-inference hosts.

### hx-doc-supersede

`tools/hx-doc/hx_doc_supersede.py` — the archive procedure runs the same way
every time. Given an active document and a `--suffix`, it copies the current
Markdown (and its committed `human-html/` mirror, if any) to
`archive/<today>/`, leaves the active file untouched for editing, and tells the
operator to re-render and check. It refuses: a missing `--suffix` (exit 2); a
path outside the repository; a path already under `archive/` or `human-html/`
(not an active document); and an archive target that already exists (choose
another suffix). `--dry-run` shows the plan without writing.

### hx-preflight

`tools/hx-doc/hx_preflight.py` — every pinned artifact is still fetchable, run
before build day. It HEAD/GET-checks direct download URLs, confirms pinned
PyPI versions still exist and are not yanked, confirms pinned npm versions,
confirms pinned Hugging Face model revisions resolve, and confirms the pinned
NVIDIA driver is still published for `noble/amd64` (comparing against the
binary, not the source package). It downloads nothing; about thirty seconds.
Run it the morning of a build so a dead pin is found before a machine is
touched. An empty `hx-base.env` fails outright (the guard tests the input, not
the output, because an empty result list could never occur).

## Graft: a finding tool, not a gate

Graft (`tools/hx-doc/hx-graft-bash` registers bash) is a code-graph index, not
a gate. It indexes only the part of the executable surface that carries a file
extension: **57 `.sh` runbook blocks/helpers, 13 `.py` tool bodies, and 2
`.env` files.** It does **not** index the Markdown authorities
(`smoke-tests/`, the roadmaps, the control documents) or the **17 extensionless
scripts** — which is every `tools/hx-doc` wrapper plus the four smoke-runner
scripts. A wrapper is a few lines that resolve a Python 3 and exec the `.py`
body beside it, and that body *is* indexed; the runner scripts are not, and
they matter during a smoke run.

Two consequences an operator must know:

- **An empty graft result means "not in the graph", never "does not exist."**
  It is a finding-tool limit, not a fact about the code.
- **`graft_trace_calls` finds no callers of a shell function** — a parser limit,
  not a fact about the code. Definitions are indexed; call edges for shell are
  not.

A workstation usually has two Graft installs (native and WSL), and whichever is
on PATH answers. If only one carries the bash registration, live queries come
back blind to shell while the on-disk cards still list shell symbols — which
reads as a Graft bug rather than a half-applied patch. So run
`tools/hx-doc/hx-graft-bash` **once per install**, and again after any
`graft upgrade`.

Prefer the MCP tools (`graft_find_code`, `graft_find_all`, `graft_trace_calls`,
`graft_file_api`, `graft_repo_map`, `graft_check_freshness`) when the host
exposes them; one call typically replaces several file reads.

## The meta-gate: hx-gate-tests

`tools/hx-doc/hx_gate_tests.py` is the gate over the gates. It copies the
repository into a throwaway scratch directory (made a git work tree, because
`hx-doc-check` runs `git check-ignore` and outside a work tree that exits 128),
then for every checking tool it **breaks the thing the tool guards and requires
the tool to fail.** A check that cannot fail looks like coverage and is not, so
each gate gets one test that asserts a non-zero exit on its own defect.

Each test calls `fresh()` to get a clean scratch copy, `edit()`s one file to
introduce the defect, runs the tool, and `check()`s that it failed with the
expected wording. Representative breakages it enforces:

- **hx-fleet**: an unclosed marker and an unknown column both fail.
- **hx-record-check**: an option-list state, a near-miss state (`NOT
  APPLICABLE` for `NOT STARTED`), and a missing State line all fail as DRIFT.
- **hx-doc-check**: a link target outside the repository is broken; a block
  reporting a unit nothing creates fails; naming a unit path without creating
  it still fails; a broken link inside `openwiki/` is *not* a finding (the skip
  works), but the same broken link outside a generated tree fails (the skip is
  not a hole); every authority-claim wording variant — both word orders,
  capitalised, the noun form, naming `docs/` — is refused, while the negated
  wording and a claim naming only `docs/` are accepted; a word merely
  containing "tests" (`attests`) is not a claim; every tooling-document defect
  (missing section, out-of-order headings, Upstream with no link / one link /
  duplicated URL, an index row for a missing file, an unlinked document, a
  substring-only filename, a heading inside a fence, a fence line with trailing
  text, a shorter run not closing a longer fence, a tilde fence, an indented
  fence line, a bare scheme) fails.
- **hx-upstream-drift**: unpaired repo/sha provenance lines are refused.
- **hx-preflight**: an empty pin fails instead of being skipped.
- **hx-new-server**: a misspelled flag is refused (exit 2) and a missing
  template placeholder is refused.
- **hx-proof**: a duplicate phase marker and a dependency on an unknown step
  both fail.
- **hx-render-html**: an edited source with a stale mirror fails.
- **hx-smoke-lint**: an authority with no known answer, no retention statement,
  a bare Evidence heading, and a negated retention sentence all fail.

### The five package-source checks

`hx-gate-tests` imports `hx_version_pins` and exercises `source_problem()`
directly (no network), holding five checks that pin the D-021 package-source
policy:

1. A Snap **application** is refused (`never permitted`).
2. A Snap **driver** is refused too — Snap is never permitted, driver included.
3. The Ubuntu archive is **allowed** for a driver.
4. The Ubuntu archive is **refused** for an application (migrate).
5. PyPI is accepted.

It also checks that both the Snap and Ubuntu-archive remediation messages name
every approved source (from `_SOURCE_PHRASES`, not a second copy, so a policy
change that keeps set, phrases, and rendering in agreement still passes), and
that the shipped version comparator sorts `595.71.05` above `595.9.05`
(numeric, not lexicographic) by `exec`ing the function body out of the module
under test rather than reimplementing it.

The harness removes its scratch directory at the end; a removal failure is
printed as a warning but does not change the exit status. It exits 1 if any
test failed, 0 otherwise.

## What a failure means

A red gate is a real defect, not noise to work around. The fix path is fixed by
AGENTS.md section 14:

- If the check is right, fix the document or artifact the check points at.
- If the check is wrong, **fix the check in a reviewed change** — do not bypass
  it and do not weaken it to make an existing document pass.

For the generated-block authority check specifically: a red `hx-doc-check`
`authority:` finding means the OpenWiki generator regressed. Correct
`openwiki/INSTRUCTIONS.md` (owner-authored, never rewritten by OpenWiki), which
steers what the generated block says — never edit the generated block itself,
because OpenWiki rewrites it on every run.

## Related pages

- [Change and review workflow](/openwiki/operations/change-and-review-workflow.md) — the pull-request and CodeRabbit review process these gates plug into.
- [Proof chain](/openwiki/operations/proof-chain.md) — the `hx-proof.tsv` DAG that `hx-proof` generates and validates.
- [Server records and evidence](/openwiki/operations/server-records-and-evidence.md) — what `hx-record-check` guards.
- [Runbook delegation pattern](/openwiki/workflows/runbook-delegation-pattern.md) — the wrapper/common-block structure `hx-new-server` scaffolds.
