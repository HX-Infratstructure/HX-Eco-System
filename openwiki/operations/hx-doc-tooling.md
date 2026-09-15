---
type: operations
title: hx-doc Repository Consistency Tooling
description: The 13 Python tools under tools/hx-doc/ that convert each written repository rule into a failing check — fleet and proof-DAG generators, doc-check, version-pins, upstream-drift, record-check, smoke-lint, new-server, supersede, preflight, graft-bash, and gate-tests — their enforcement role and CI placement.
tags: [hx-doc, tooling, ci, proof-chain, documentation, fleet, gate-tests, version-pins]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-14T19:05:42.087Z
sources:
  - id: openwiki-source-4a10bba62772b26bb2a2e6b3
    resource: repo://.github/workflows/hx-checks.yml
  - id: openwiki-source-6039b489b5096b4c78d1d80d
    resource: repo://.github/workflows/hx-upstream-drift.yml
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
  - id: openwiki-source-386db2e093752f65e4a2f48b
    resource: repo://tools/hx-doc/hx-doc-check
  - id: openwiki-source-f7324bb33154da97b8b9c716
    resource: repo://tools/hx-doc/hx-fleet
  - id: openwiki-source-2909dda2204a0a08300a688c
    resource: repo://tools/hx-doc/hx-graft-bash
  - id: openwiki-source-f2994b36a477b8759d39a2a6
    resource: repo://tools/hx-doc/README.md
  - id: openwiki-source-a77fea9320056a2d55a6f0f9
    resource: repo://tools/hx-smoke-runner/hx-smoke-promote
generated: { by: "openwiki/0.5.1", at: "2026-09-14T19:05:42.087Z" }
---

# hx-doc Repository Consistency Tooling

`tools/hx-doc/` is a set of **thirteen** small tools. Each one exists because the matching failure actually happened in this repository, and each converts a written rule into something that **fails loudly** instead of drifting silently. The recurring anti-pattern the whole set is built against is the *check that cannot fail*: a gate that looks like coverage but catches nothing. Several of these tools shipped as exactly that before they were hardened, and the comments embedded in each body record the specific defect that made the check necessary.

Two constraints shape the whole set:

- **No third-party dependencies.** Every tool is Python 3 standard library only — `csv`, `re`, `json`, `urllib`, `pathlib`, `subprocess`. Nothing is `pip install`ed, which keeps the documentation gates runnable on a bare CI runner and a lab machine alike.
- **Wrapper + body split.** Each `tools/hx-doc/hx-*` extensionless wrapper is a few lines of bash that resolve a real Python 3 interpreter and `exec` the `.py` body beside it. Graft indexes the `.py` body (which carries a file extension) but not the extensionless wrapper, so the executable surface stays searchable without duplicating symbols.

The fleet of tools, the defect each replaces, and what it enforces:

| Tool | Replaces | Enforces |
|---|---|---|
| `hx-fleet` | six hand-typed server tables | every fleet table and the runbook IP map comes from `docs/00-control/hx-fleet.tsv` |
| `hx-proof` | a hand-drawn DAG that omitted 11 of 29 steps | every proof step and edge comes from `docs/00-control/hx-proof.tsv`, and a PASS cannot skip its prior proof |
| `hx-render-html` | hand-written HTML mirrors | a mirror always matches its Markdown source |
| `hx-doc-check` | proofreading | links resolve, vocabulary is defined, filenames are stable, evidence is committable |
| `hx-version-pins` | remembering to look | product pins match what upstream ships, and applications do not come from the Ubuntu archive or Snap |
| `hx-upstream-drift` | remembering to look | the registry's reviewed commits still match upstream |
| `hx-record-check` | hoping the template was followed | server records carry every required section, and open gaps stay visible |
| `hx-smoke-lint` | hoping | smoke-test authorities carry every required section |
| `hx-new-server` | copy and paste | a new server's runbook and record are complete from the start |
| `hx-doc-supersede` | six manual steps | the archive procedure happens the same way every time |
| `hx-preflight` | finding a 404 on a lab machine | every pinned artifact is still fetchable, checked from anywhere |
| `hx-graft-bash` | a code graph that ignored every shell file | graft indexes `.sh`, `.bash` and `.env`, so the executable surface is searchable |
| `hx-gate-tests` | trusting that a check still checks | every checking tool above is broken on purpose and required to fail; a check that cannot fail is a defect |

## Everyday use

The four tools run in a fixed sequence during normal editing, and each one has a `--check` mode (or equivalent) that CI runs without writing anything:

```bash
tools/hx-doc/hx-fleet              # after editing hx-fleet.tsv
tools/hx-doc/hx-render-html         # after editing any Markdown
tools/hx-doc/hx-doc-check           # before committing
tools/hx-doc/hx-record-check        # what is still open in the server records
```

## CI placement

Two GitHub Actions workflows run the set:

- **`.github/workflows/hx-checks.yml`** runs on every push to `main`, every pull request, and on dispatch. Its `documentation` job runs `hx-doc-check`, `hx-fleet --check`, `hx-proof --check`, `hx-render-html --check`, `hx-record-check`, `hx-smoke-lint --quiet`, and then `hx-gate-tests`. A separate `scripts` job runs `shellcheck`, a CRLF/executable-bit check, and a `python3 -m compileall` over `tools/`. A `secrets` job runs a pinned, checksum-verified `gitleaks` scan of both the working tree and history.
- **`.github/workflows/hx-upstream-drift.yml`** runs weekly (Mondays 06:17 UTC). It runs `hx-preflight --quiet`, then `hx-upstream-drift --markdown` and `hx-version-pins --markdown` into a `drift.md` summary, and opens or comments on an `upstream-drift` issue when either reports drift.

A workflow that cannot reach an upstream is treated as a failure, not a clean run: if `drift.md` contains "could not be reached", the job emits a `::error::` and exits non-zero. Drift itself is *information*, not a failure — a pin stays valid until the owner moves it.

## The fleet is the source of truth

`docs/00-control/hx-fleet.tsv` holds the 17-server map with columns `id`, `ip`, `role`, `state`, `gate`, `note`. Edit the TSV, then run `hx-fleet`. That regenerates every marked table across `README.md`, `docs/`, and `skills/`, plus `docs/03-runbooks/common/hx-fleet-ips.env`, which the runbooks `source` for the host → IP lookup.

A document opts in by carrying a marker pair:

```text
<!-- HX-FLEET:TABLE columns=id,ip,role,state -->
<!-- /HX-FLEET:TABLE -->
```

`hx-fleet --check` (CI mode) exits 1 if any generated block is stale. Beyond content drift it also refuses **structural** defects that used to read as "current": an unclosed marker matches nothing and left the text unchanged; an orphan closing marker is the same defect from the other end; and an unknown column name once fell through to a heading of its own name and a row of em dashes, passing `--check` because the junk matched itself. The tool now counts opening markers, closing markers, and complete pairs and requires all three to agree, and it rejects any column not in its known heading set. `tools/` is excluded from the table-scan targets because its README documents the marker syntax and must not have a live table injected into the example.

## The proof chain

`docs/00-control/hx-proof.tsv` holds the 30 smoke-test steps (foundation `P0` plus phases A–G) and the `requires` edges between them. The hand-maintained version it replaced carried 19 nodes — the foundation plus 18 of the 29 steps — so 11 steps were missing from the picture: every MCP companion gate, both Web UI gates, and the reranker. The TSV is now the source; `hx-proof` regenerates the per-phase Markdown tables and the mermaid flowchart into `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`.

```bash
tools/hx-doc/hx-proof --list        # every step, and what it is waiting on
tools/hx-doc/hx-proof --ready B2    # can this run yet
tools/hx-doc/hx-proof --check       # CI: valid DAG, generated blocks current
```

`validate()` refuses a DAG that a hand-maintained version could silently get wrong and nothing would say so:

- a **dangling `requires`** — a dependency on a step id that is not in the TSV;
- a **cycle** in the dependency graph (detected by depth-first colouring that records the trail);
- a **missing authority file** — the `authority` column points at a path that does not exist;
- an **unknown host** — the `sut` column names a host not in `hx-fleet.tsv` (and an unreadable or empty fleet inventory is itself a problem, because it used to leave the host set empty and skip the SUT check entirely);
- an **unrecognised status** — anything other than `NOT_RUN`, `PASS`, `FAIL`, `NOT_EXECUTABLE`;
- a **blank or duplicate step id**, which silently overwrote an earlier row while validation still reported success.

`--ready <id>` answers whether a step may run now. A step is `NOT_RUNNABLE` when its status is `NOT_EXECUTABLE` (an implementation decision is still open) — dependencies are not the blocker in that case. A step that is already `PASS` is reported `ALREADY PASSED` rather than `READY`, so `--ready` and `runnable()` cannot disagree and invite a re-run that overwrites accepted evidence.

`--check` also requires the full marker set: a deleted or duplicated `HX-PROOF:TABLE` marker leaves the surrounding text untouched, so comparing content alone used to report success for a roadmap that had silently lost a phase table. Markers are counted (not collected into a set) precisely because a duplicated table reduced a set to one value and reported no drift.

### Proof-chain interplay with smoke promotion

`hx-proof --ready` and `hx-smoke-promote` (under `tools/hx-smoke-runner/`) read the same `hx-proof.tsv`. A `PASS` is refused when a required prior step has not passed *and been cited*: `hx-smoke-promote` requires a `proof_step` in the run manifest, binds that step to the run's `sut_host` + `smoke_test_file` (so a hand-edited manifest cannot borrow another host's step), refuses a `NOT_EXECUTABLE` step outright, and for every step in the `requires` column checks that the dependency's status is `PASS` **and** that `prior_pass_evidence` carries a matching `<step-id> -> <evidence>` entry. There is **no bypass flag**. If a dependency genuinely does not apply, the `requires` column is changed in the TSV via a reviewed PR — the rule is not weakened at promote time.

## HTML mirrors

`hx-render-html` generates the `human-html/` mirrors from the authoritative Markdown sources. The mirrors were once hand-written summaries that drifted; they are now generated so a mirror cannot silently lose content its source contains. It implements a minimal CommonMark/GFM subset (headings, lists, tables, fenced code, mermaid blocks, blockquotes, inline code/bold/italic/links) in the standard library, rewrites `.md` link targets to `.html` so mirror-to-mirror links keep working, and stamps each page with a banner stating the source is authoritative and the page is not execution authority.

`hx-render-html --check` exits 1 if any mirror is out of date, and additionally reports **orphan** HTML files — mirrors with no source — which a generation-only check would never catch.

## doc-check

`hx-doc-check` is the pre-commit gate. It runs seven named checks, each tied to a defect:

- **links** — every internal Markdown link and backtick path reference resolves, unless the surrounding text declares an intentional forward reference (`no active`, `planned`, `authority gap`, `future docs/`, …). References under upstream prefixes (`deploy/`, `docs/LightRAG`, `integrations/`, `.agents/`) are skipped, and candidates are constrained to be inside the repo root so a traversal such as `../../../../Windows/...` cannot pass on whatever happens to exist on the machine.
- **vocabulary** — `skills/SKILL-REGISTRY.md` uses only lifecycle states that `skills/SKILL-GOVERNANCE.md` section 4 defines.
- **frontmatter** — active control documents in `docs/00-control/` carry `document`, `status`, and `date`.
- **duplicates** — no versioned or dated filename (`-v2`, `(3)`, `final-final`, `_20260914`) in the active tree; active documents use stable names.
- **evidence** — `.gitignore` cannot swallow retained evidence logs, probed via `git check-ignore` against a representative evidence path. Anything other than "ignored → fail" and "not ignored → ok" (e.g. running outside a work tree, exit 128) is itself a failure, because treating "anything but 0" as success once let a git failure report the path as committable.
- **units** — a runbook block may only `hx_app_done` a systemd unit that the same file actually creates (`hx_app_unit`, or a `tee`/`cp`/`install`/redirect write to the unit path). A comment naming the path, or an `rm` of it, does not satisfy the check.
- **authority** — the OpenWiki-generated block in `AGENTS.md` may not call source code or tests authoritative. The check works sentence by sentence and in both word orders ("source code is authoritative" and "authoritative sources include source code"), accepts a denial ("not authoritative"), and lets a word merely *containing* "tests" (e.g. "attests") pass. A claim naming only `docs/` is accepted; a claim naming `docs/` plus source code is still refused, because section 2 has no entry for source code at all.

`hx-doc-check` deliberately skips generated and vendored trees — `.git`, `archive`, `human-html`, `.claude`, `graft`, and `openwiki/` (written wholesale by the OpenWiki CLI). A broken link inside `openwiki/` is a defect in the generator or the source it documents, never something to fix in the generated page.

## Version currency

Two tools watch pins against upstream, and both run weekly in `hx-upstream-drift.yml`:

- **`hx-version-pins`** audits the *product* pins — Ollama, the NVIDIA driver, the reranker model and runtime, and the Python/npm dependencies — against what upstream currently ships. It collects pins from `docs/03-runbooks/common/hx-base.env`, `tools/hx-smoke-runner/requirements.txt`, and the HX-12 runbook. `--fail-on-outdated` exits 1 on `OUTDATED`; weekly CI calls it without that flag and opens an issue instead.
- **`hx-upstream-drift`** reports drift between the commits `skills/SKILL-REGISTRY.md` pins and the upstream repositories' current HEAD. It reads the pins out of the registry's provenance blocks (not a second hard-coded list, so it cannot fall out of step), compares the pinned SHA to `/repos/{repo}/commits?per_page=1`, and reports how many commits behind. `--fail-on-drift` exits 1 on drift *or* an unreachable upstream — an unreachable upstream is not evidence a pin is current.

### Package-source policy

`hx-version-pins` also enforces the package-source rule, kept in `source_problem()` so the rule can be tested without going near the network:

- Application software comes from PyPI, a GitHub release, a direct binary, Hugging Face, npm, or source.
- The Ubuntu archive is acceptable for **drivers only** (plus build toolchains and library headers, which are `apt`-installed inside runbook blocks and are not pins). An application pinned to the Ubuntu archive is reported as **REVIEW** with a migration note.
- **Snap is never permitted, for anything**, driver included. A Snap pin is reported as REVIEW with a migration note.
- Models from Hugging Face are reported as REVIEW when the upstream revision moves (the pin still resolves; re-review before changing it).

The NVIDIA driver comparison is against the *binary* actually installable on `noble/amd64` (queried from the Launchpad archive API, `Updates`/`Security`/`Release` pockets, `Proposed` excluded), not the source-package version — a source build can exist without a published binary, which would read as false drift. The comparator is numeric, not lexicographic, so `595.71.05` sorts above `595.9.05`.

## Server records and smoke authorities

- **`hx-record-check`** checks each `docs/02-server-records/*.md` against the template's required sections (Identity and Network, Operating System, GPU Configuration, Storage Layout, Runtime, Model/Application Provenance, Functional Validation, Final State), matched loosely so a record can word its own heading. It reports three classes: `MISSING` (a required section absent, unless the record declares it not applicable with a one-line reason), `UNRESOLVED` (a field explicitly recorded as not yet known — a visible gap, not an error), and `DRIFT` (the record's `**Build state:**` line disagrees with `hx-fleet.tsv`). The state comparison is on the whole normalised value, not the first word, so `NOT APPLICABLE` no longer satisfies `NOT STARTED`. `--strict` fails the build on `UNRESOLVED` as well as `MISSING`/`DRIFT`.
- **`hx-smoke-lint`** checks each `smoke-tests/*-smoke-test.md` for the six canonical sections (Title & Purpose, Prerequisites, Test Steps, Sample Data, Expected Output, Cleanup / Teardown), a known-answer marker (service health alone is not a smoke test), and a statement of evidence retention. Evidence retention is matched against the body, not a heading, and is anchored to the standard bundle path `docs/05-evidence` — a bare `## Evidence` heading with nothing under it, and a negated sentence like "do not retain credentials in evidence", both fail, because the word "evidence" appearing anywhere used to satisfy the check.

## Scaffolding and superseding

- **`hx-new-server`** creates, from `hx-fleet.tsv` and `docs/02-server-records/_TEMPLATE.md`, the per-host runbook wrappers (`01-base-admin-network-updates.sh`, `02-domain-nvidia.sh`, and `03-storage-ollama.sh` for inference hosts), the runbook `README.md`, and the server record. `--no-ollama` skips the Ollama block for non-inference hosts. Existing files are never overwritten without `--force`. Unknown `--flags` are refused (a misspelled `--no-olama` once scaffolded the Ollama block anyway), and every template placeholder must match exactly once (a missing placeholder would have shipped a record still reading `HX-N` and `192.168.50.2NN`). The record is built and validated *before* any file is written, so a template defect cannot leave runbook wrappers on disk with no record beside them.
- **`hx-doc-supersede`** performs the `DOCUMENT-CONTROL.md` supersession procedure in one command: it archives the current Markdown (and its committed HTML mirror, if any) under `archive/<today>/`, leaves the active file in place for editing, and reminds you to re-render and check. `--dry-run` previews; `--suffix` names the archived copy. It refuses to archive a path already under `archive/` or `human-html/`, and refuses a suffix that would collide with an existing archived file.

## Preflight

`hx-preflight` confirms every download the install blocks make still resolves, *before* build day, from anywhere — a 404 discovered on a lab machine costs lab time. In about thirty seconds it checks:

- every direct download URL the blocks fetch (HEAD, with a one-byte ranged GET fallback for CDNs that refuse HEAD);
- every pinned PyPI version still exists and is not yanked;
- every pinned npm version still exists;
- every pinned Hugging Face model revision still resolves;
- the pinned NVIDIA driver is still installable on `noble/amd64`.

It **downloads nothing** — it only asks whether the thing is there. It guards its input, not its output: an empty `hx-base.env` is the real failure case (every pin would then read as missing), whereas an empty result list could never occur. `hx-preflight --quiet` runs in the weekly drift workflow.

## Graft bash registration

`hx-graft-bash` is a local patch to a third-party package. Graft ships `tree-sitter-bash.wasm` and registers it as `bash` in its grammar manifest, but graft's own language table has no bash entry, so `.sh` files are skipped entirely. The script inserts one line — `{ name: "bash", exts: [".sh", ".bash", ".env"], wasm: "bash" }` — into `dist/graph/generic.js`, anchoring on the existing `zig` entry and stopping loudly if the upstream file has changed shape rather than guessing. `.env` is included because `docs/03-runbooks/common/hx-base.env` is bash (it holds `hx_require_host`, `hx_ip_for`, and every fleet version pin).

It is idempotent and reversible (`--revert`). A workstation commonly has two graft installs — a native one and one inside WSL — and whichever is on `PATH` answers queries, so the patch must be applied to **every install that answers queries**, pointed at each via `GRAFT_ROOT`. Re-run after any `graft upgrade` or reinstall, which wipes the patch.

## Gate-tests

`hx-gate-tests` is the meta-check: every checking tool above is broken on purpose and required to fail on the case it guards. A check that cannot fail looks like coverage and is not, so each gate gets one test that introduces the defect and asserts a non-zero exit.

It runs against a **throwaway copy** of the repository (`tempfile.mkdtemp` + `shutil.copytree`, excluding `.git`, then `git init` so `hx-doc-check`'s `git check-ignore` works), and `fresh()` replaces that copy before every test so tests cannot affect each other. The harness itself was hardened against its own class of bug: the scratch copy was made a git work tree because `hx_doc_check` runs `git check-ignore` against the repo root, and outside a work tree that exits 128 — which every earlier test expected to be non-zero anyway, so the harness never noticed it was checking documents in an environment where one check could not pass.

Representative gates: `hx-fleet` rejects an unclosed marker and an unknown column; `hx-record-check` rejects an option-list state and a near-miss state; `hx-doc-check` rejects an out-of-repo link target, a unit nothing creates, and (in a battery of cases) every wording class of the generated authority claim in both word orders, the noun form, capitalised, and accepts the denial and a `docs/`-only claim; `hx-upstream-drift` refuses unpaired repo/SHA provenance lines; `hx-preflight` fails an empty pin instead of skipping it; `hx-new-server` refuses a misspelled flag and a missing template placeholder; `hx-proof` rejects a duplicate phase marker and a dependency on an unknown step; `hx-render-html` flags a stale mirror; `hx-smoke-lint` rejects a missing known answer, a missing retention statement, a bare Evidence heading, and a negated retention sentence; and `hx-version-pins`' numeric comparator is exercised by `exec`-ing the shipped `vkey`, not a reimplementation of it.

## If a check is wrong

The standing rule, stated across the tools and the CI workflow: **if a check is wrong, fix the check in a reviewed change; do not bypass or weaken it to make a document pass.** The check is the thing that stops the defect coming back. A `--force` here or a commented-out assertion there is the same drift the whole set exists to remove.
