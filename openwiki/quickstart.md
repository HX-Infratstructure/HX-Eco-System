---
type: Routing map
title: Quickstart — Task Routing Map
description: Task-routing map and reading-order entry point for the HX Eco-System wiki. Routes every common agent question to the exact authority file or deeper wiki page, and reproduces the AGENTS.md truth order and required-reading order.
tags: [routing, quickstart, authority, reading-order, governance]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-15T22:39:27.588Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-939aa3b5c336cc69710945f5
    resource: repo://docs/00-control/hx-fleet.tsv
  - id: openwiki-source-7102ad22abc6e919967a4c88
    resource: repo://docs/00-control/hx-proof.tsv
  - id: openwiki-source-12296e6451a9d695ef6c70ca
    resource: repo://docs/03-runbooks/common/01-base-admin-network-updates.sh
  - id: openwiki-source-667355bbf619c0e53d4f76d4
    resource: repo://docs/03-runbooks/common/hx-base.env
  - id: openwiki-source-ba1aab5f4560124990f7b772
    resource: repo://docs/03-runbooks/HX-4/01-base-admin-network-updates.sh
  - id: openwiki-source-3bc721c8c10557b77c613ac1
    resource: repo://docs/03-runbooks/RUN-SHEET.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
generated: { by: "openwiki/0.5.1", at: "2026-09-15T22:39:27.588Z" }
---

> **This page is context, never authority.** It is a generated index whose
> only job is to route a question to the real authority file so an agent does
> not have to search the repository. It does not decide anything. Where this
> page and an authority file disagree, the authority file wins and this page is
> a defect to fix.

## The truth order (AGENTS.md section 2, verbatim)

Reproduced exactly from `AGENTS.md` section 2. **Source code and tests are not
in this list** — they are evidence, not authority. A generated block (including
any part of `openwiki/`) that calls source code or tests authoritative is a
defect; `hx-doc-check` refuses such a block.

1. Explicit current instruction from the infrastructure owner.
2. Current active control/architecture Markdown in `docs/` and the exact current
   component acceptance authority in `smoke-tests/` when testing.
3. Current live evidence from the server being worked on.
4. Current approved runbook/execution artifact.
5. Governed HX wrapper skill plus current official vendor guidance for
   product-specific expertise.
6. Historical/archive material, only as reference.
7. General model knowledge.

If current live evidence or current official vendor requirements contradict an
active document, stop treating the document as sufficient proof and report the
contradiction. Do not silently let a vendor skill redesign HX.

Authority: `repo://AGENTS.md#L28-L38`.

## Task-routing table — You are trying to ___ → read ___

Open one file, not search. Where a deeper wiki page exists, it is linked after
the primary authority file.

| You are trying to… | Read this (authority) | Deeper wiki page |
|---|---|---|
| **Build a server today** | `docs/03-runbooks/RUN-SHEET.md` — the one-page build-day run sheet with every exact command | [`/openwiki/workflows/build-day-flow.md`](/openwiki/workflows/build-day-flow.md) |
| **Decide something** (architecture, placement, a rule) | `docs/00-control/DECISIONS.md` — owner-approved, ratified vs proposed | [`/openwiki/authority-model.md`](/openwiki/authority-model.md) |
| **Find current fleet state** (which server is PASS / NEXT / NOT STARTED) | `docs/00-control/hx-fleet.tsv` — the single source of truth; regenerate tables with `tools/hx-doc/hx-fleet` | — |
| **Find current build/proof state** | `docs/00-control/BUILD-STATE.md` and `docs/00-control/CURRENT-STATE.md` | — |
| **Answer "may this proof step run?"** | `tools/hx-doc/hx-proof --ready <id>` against `docs/00-control/hx-proof.tsv`; `hx-smoke-promote` enforces the same DAG with no bypass | [`/openwiki/operations/proof-chain.md`](/openwiki/operations/proof-chain.md) |
| **Find what a smoke test must prove** | the exact `smoke-tests/<component>-smoke-test.md` authority — read it directly | [`/openwiki/workflows/smoke-test-execution.md`](/openwiki/workflows/smoke-test-execution.md) |
| **Find where code lives / how a helper works** | `graft_find_code` / `graft ask` (indexes `.sh`, `.py`, `.env`); for extensionless wrappers read the `.py` body beside them | — |
| **Find what a gate checks / refuses and what a failure means** | `tools/hx-doc/README.md` and the tool itself | [`/openwiki/operations/doc-gates.md`](/openwiki/operations/doc-gates.md) |
| **Change a doc or tool** | every change goes through a pull request: `coderabbit review --agent` before every push, then `tools/hx-doc/hx-doc-check && tools/hx-doc/hx-render-html` | [`/openwiki/operations/change-and-review-workflow.md`](/openwiki/operations/change-and-review-workflow.md) |
| **Use a governed skill** | `skills/SKILL-GOVERNANCE.md` then `skills/SKILL-REGISTRY.md` then the wrapper `skills/<component>/hx-<component>-advisor/SKILL.md` | [`/openwiki/concepts/governed-skills.md`](/openwiki/concepts/governed-skills.md) |
| **Validate (run a smoke test)** | `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` → `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md` → `smoke-tests/<component>-smoke-test.md` → `tools/hx-smoke-runner/AGENTS.md` | [`/openwiki/workflows/smoke-test-execution.md`](/openwiki/workflows/smoke-test-execution.md) |
| **Record or check a server record** | `docs/02-server-records/<HX-N>.md` (template: `_TEMPLATE.md`); check with `tools/hx-doc/hx-record-check` | [`/openwiki/operations/server-records-and-evidence.md`](/openwiki/operations/server-records-and-evidence.md) |
| **Understand the ecosystem before building or validating anything** | `docs/01-architecture/ARCHITECTURE-ORIENTATION.md` — the foundational orientation authority | [`/openwiki/architecture/ecosystem-orientation.md`](/openwiki/architecture/ecosystem-orientation.md) |
| **Find the build order** | `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md` (deployment order + BASE PASS boundaries) | [`/openwiki/architecture/ecosystem-orientation.md`](/openwiki/architecture/ecosystem-orientation.md) |
| **Find the proof order** | `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` and `docs/00-control/hx-proof.tsv` | [`/openwiki/operations/proof-chain.md`](/openwiki/operations/proof-chain.md) |
| **Use OpenWiki, CodeRabbit or graft** | `docs/06-tooling/` (read when you reach for the tool, not at startup) | — |
| **Read as a human** | `human-html/` — generated, **never** authority; edit the Markdown and run `tools/hx-doc/hx-render-html` | — |

### Three tools, three different mid-run questions

Knowing which tool answers which question saves reading files that will not
answer you (from `docs/03-runbooks/RUN-SHEET.md#L197-L224`):

| The question | Ask |
|---|---|
| Which block installs this? Where is that helper? | `graft_find_code` · `graft ask "<term>"` |
| May this proof step run yet? | `tools/hx-doc/hx-proof --ready <id>` |
| What must this step actually prove? | the `smoke-tests/` authority — read it directly |
| Is this server's record complete? | `tools/hx-doc/hx-record-check` |

Graft answers **where the code is**. `hx-proof` answers **whether you may run
it**. The smoke authority answers **what it must prove**. Graft does not index
the Markdown authorities, so an empty result from it says nothing about them.

## Required reading order (AGENTS.md section 1)

Learn the ecosystem before the skills, and the skills before validation. This
is the AGENTS.md section 1 order, condensed and pointing to the deeper wiki
pages. Before changing anything:

1. `README.md`
2. `docs/00-control/CURRENT-STATE.md` and `docs/00-control/BUILD-STATE.md`
3. `docs/00-control/DECISIONS.md` → [`/openwiki/authority-model.md`](/openwiki/authority-model.md)
4. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md` → [`/openwiki/architecture/ecosystem-orientation.md`](/openwiki/architecture/ecosystem-orientation.md)
5. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
6. The relevant current server record under `docs/02-server-records/`
7. The relevant runbook under `docs/03-runbooks/` → [`/openwiki/workflows/runbook-delegation-pattern.md`](/openwiki/workflows/runbook-delegation-pattern.md)
8. The relevant standard under `docs/04-application-standards/`
9. If a governed component skill exists: `skills/SKILL-GOVERNANCE.md`,
   `skills/SKILL-REGISTRY.md`, and the approved wrapper under
   `skills/<component>/` → [`/openwiki/concepts/governed-skills.md`](/openwiki/concepts/governed-skills.md)
10. **Only if validating:** `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`
    → [`/openwiki/operations/proof-chain.md`](/openwiki/operations/proof-chain.md)
11. `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md`
12. If executing a component smoke test, the exact authority under `smoke-tests/`
    → [`/openwiki/workflows/smoke-test-execution.md`](/openwiki/workflows/smoke-test-execution.md)
13. If using the HX-5 runner, `tools/hx-smoke-runner/AGENTS.md`
14. For an operational tool this repo depends on but does not contain (OpenWiki,
    CodeRabbit, graft), read its document under `docs/06-tooling/` first, when
    you reach for the tool rather than at startup.

Do not read `archive/` or `human-html/` as current authority unless explicitly
asked.

Authority: `repo://AGENTS.md#L5-L26`.

## The wiki map at a glance

The wiki is organized into four domains. This page is the entry point; each
domain page reproduces the relevant authority and explains the mechanism.

### Orientation & authority

- [`/openwiki/architecture/ecosystem-orientation.md`](/openwiki/architecture/ecosystem-orientation.md)
  — ecosystem planes, server/application map, foundational baseline, and
  model/data-placement rules. The orientation an agent must hold before
  building or validating anything.
- [`/openwiki/authority-model.md`](/openwiki/authority-model.md)
  — the truth order (above) and how a decision becomes binding: ratified
  versus proposed/superseded in `docs/00-control/DECISIONS.md`.

### Operations

- [`/openwiki/operations/doc-gates.md`](/openwiki/operations/doc-gates.md)
  — the `tools/hx-doc/` enforcement layer: what each gate checks, what it
  refuses, and what a failure means. Includes CI, graft limits, and the
  meta-gate that breaks checks on purpose.
- [`/openwiki/operations/proof-chain.md`](/openwiki/operations/proof-chain.md)
  — the proof DAG in `docs/00-control/hx-proof.tsv`, how a smoke step becomes
  eligible to run, and how promotion enforces the same chain with no bypass.
- [`/openwiki/operations/server-records-and-evidence.md`](/openwiki/operations/server-records-and-evidence.md)
  — server record structure, the record-check gate, the two evidence models
  (inline vs run-bundle), and evidence retention invariants.
- [`/openwiki/operations/change-and-review-workflow.md`](/openwiki/operations/change-and-review-workflow.md)
  — the pull-request-and-review workflow: branch creation, derived-output
  regeneration, the required `coderabbit review --agent` before push,
  stacked-PR and 100-file limits, and document lifecycle/supersede.

### Workflows

- [`/openwiki/workflows/build-day-flow.md`](/openwiki/workflows/build-day-flow.md)
  — the six-step build-day flow every server follows, from preflight through
  reboot-persistence validation and record closure, including what stops you
  per host.
- [`/openwiki/workflows/runbook-delegation-pattern.md`](/openwiki/workflows/runbook-delegation-pattern.md)
  — how per-host runbook wrappers delegate to the shared `common/` library,
  the `hx-app-lib.sh` helpers, the pinned values in `hx-base.env`, and the
  host guard that prevents cross-host damage.
- [`/openwiki/workflows/smoke-test-execution.md`](/openwiki/workflows/smoke-test-execution.md)
  — the end-to-end smoke-test workflow: CentCom activation at A5, pre-CentCom
  runs, the runner tools (`hx-smoke-new`/`promote`/`doctor`), remote execution
  rules, and cleanup/retention.

### Concepts

- [`/openwiki/concepts/governed-skills.md`](/openwiki/concepts/governed-skills.md)
  — the `skills/` governance layer: what skills may and may not do, the
  loading order, the registry, pinned upstream commits, and the drift check.

## Where things live — one line each

| Surface | Path | Status |
|---|---|---|
| Fleet single source of truth | `docs/00-control/hx-fleet.tsv` | edit here, regenerate with `tools/hx-doc/hx-fleet` |
| Proof DAG | `docs/00-control/hx-proof.tsv` | edit `requires`/`status` here, never bypass |
| Control / architecture / standards / records / runbooks | `docs/**/*.md` | current authority |
| Runbook shared library | `docs/03-runbooks/common/` | one implementation per block; pinned in `hx-base.env` |
| Per-host runbook wrappers | `docs/03-runbooks/HX-<N>/` | thin wrappers that `exec` the common block with the host name |
| Component acceptance authorities | `smoke-tests/*.md` | validation only; do not redefine architecture |
| Governed agent expertise | `skills/**` | subordinate to docs/runbooks/smoke authority |
| Repository tooling | `tools/hx-doc/`, `tools/hx-smoke-runner/` | the enforcement and runner layer |
| Generated human view | `human-html/**` | generated output, never authority; never hand-edit |
| Superseded history | `archive/**` | reference only, never current authority |

## Non-negotiable operating rules (AGENTS.md section 3)

KISS: build one server, validate it, record it, then move on. Native Linux +
systemd. No Docker, Podman, Kubernetes, or containerized workload deployment
unless explicitly approved. Do not impose firewall, access, TLS, segmentation,
or security-hardening changes, or change network architecture, without explicit
approval. Do not mount, wipe, repartition, or repurpose an old disk without
explicit approval. Do not import old HX-Infrastructure configuration or closure
claims into this clean rebuild. A server is not PASS/CLOSED until workload,
functional, cleanup (where applicable), and reboot-persistence gates are
satisfied and its server record is updated.

Authority: `repo://AGENTS.md#L40-L52`.

## What this page will not do

- It does not document anything under `archive/`, `human-html/`, or `graft/` —
  those are excluded by `.openwikiignore`. If one appears, the ignore file is
  wrong and should be fixed, not the page.
- It does not write one page per host. HX-4 through HX-17 are the same two
  runbooks with a different hostname; route all host questions to the
  build-day-flow and runbook-delegation-pattern pages.
- It does not restate policy. It points to the authority file.
