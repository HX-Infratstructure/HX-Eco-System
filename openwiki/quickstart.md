---
type: "Reference"
title: "HX Eco-System Wiki — Quickstart"
openwiki_generated: true
verified:
  - by: openwiki/0.5.1
    at: 2026-09-14T19:05:42.087Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
generated: { by: "openwiki/0.5.1", at: "2026-09-14T19:05:42.087Z" }
---


# HX Eco-System Wiki — Quickstart

This repository is the **authoritative control plane for a clean-room 17-server
native-Linux AI ecosystem rebuild**, not a typical application codebase. Its
executable surface is small and intentional: shell runbook blocks that install
software on fleet hosts, Python consistency tools that turn written rules into
failing checks, shell smoke-runner scripts on HX-5 CentCom, TSV data sources
that are the single source of truth for the fleet and the proof DAG, and CI
workflows that re-run every check on each change. Markdown in `docs/` and
`smoke-tests/` is the machine/agent authority that governs that surface, while
`human-html/` is a generated mirror and is never execution authority.

This page is the **entry point and routing map**. It does not restate the
ecosystem, the rules, or the validation model in full — it tells you where each
of those lives and which page to open for a given task. Open the linked page and
read it before acting; the summaries here are navigation, not a substitute for
the authority.

## What kind of repository this is

The HX Eco-System is built **one server at a time, validated and recorded before
the next begins**. The repository encodes that discipline:

- `docs/00-control/hx-fleet.tsv` is the single source of truth for the fleet;
  generated fleet tables, the runbook IP map, and server records all derive from
  it.
- `docs/03-runbooks/**/*.sh` are the approved execution artifacts that actually
  install a host; versions are pinned and host-gated.
- `tools/hx-doc/` holds Python tools (standard library only) that regenerate
  derived artifacts and check the repository's own consistency.
- `tools/hx-smoke-runner/` holds the repository-owned smoke-runner helpers.
- `smoke-tests/*.md` are the component acceptance authorities — what each
  component must prove, run from HX-5 CentCom.
- `human-html/**` and `archive/**` are **not** current authority.

If you expected application source code, recalibrate: the "code" here is the
runbook blocks, the Python consistency tools, the smoke-runner scripts, the TSV
sources, and the CI workflows — everything else is governance in Markdown.

## Required reading order

Before changing anything, an agent follows the reading order defined in
`AGENTS.md` section 1. Do not skip ahead to tools or smoke tests without the
context the earlier documents provide:

1. `README.md`
2. `docs/00-control/CURRENT-STATE.md`
3. `docs/00-control/BUILD-STATE.md`
4. `docs/00-control/DECISIONS.md`
5. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`
6. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
7. The relevant current server record under `docs/02-server-records/`
8. The relevant runbook under `docs/03-runbooks/`
9. The relevant standard under `docs/04-application-standards/`
10. The relevant component smoke authority under `smoke-tests/` (when validating)

Do **not** read `archive/` or `human-html/` as current authority unless
explicitly asked. The deep rationale, including the validation-only steps that
sit between the runbook and the smoke authority, is in
[Truth Order, Authority Layers, and Document Control](/openwiki/concepts/truth-order-and-authority.md).

## Standing constraints

Every change is gated by a small set of non-negotiable rules. These are
elaborated in [Owner Decisions and Non-Negotiable Rules](/openwiki/concepts/decisions-and-rules.md)
and enforced by the tools and CI in
[CI, CodeRabbit Review, and Change Process](/openwiki/integrations/ci-and-review.md).

- **Native Linux + systemd.** No Docker, Podman, or Kubernetes unless the owner
  explicitly approves (decision D-002).
- **KISS — one server at a time.** Build it, validate it, record it, then move
  on. The build order is dependency-driven, not permanent integration wiring.
- **Everything goes through a pull request.** `main` is not a working branch.
  CodeRabbit review (`coderabbit review --agent`) runs before every push; review
  is not optional.
- **Run the consistency tools before committing.** Run
  `tools/hx-doc/hx-doc-check` and `tools/hx-doc/hx-render-html` (and regenerate
  any derived artifact you touched) so CI does not fail on stale output.
- **Do not hand-edit generated output.** `human-html/**` is generated; edit the
  Markdown source and re-render. Do not hand-edit generated `openwiki/` pages
  unless explicitly asked — update source and let it regenerate.

## Truth-order precedence

When sources conflict, authority is resolved in this strict order (from
`AGENTS.md` section 2):

1. Explicit current instruction from the infrastructure owner.
2. Current active control/architecture Markdown in `docs/` and the exact current
   component acceptance authority in `smoke-tests/` when testing.
3. Current live evidence from the server being worked on.
4. Current approved runbook/execution artifact.
5. Governed HX wrapper skill plus current official vendor guidance.
6. Historical/archive material, as reference only.
7. General model knowledge.

If live evidence or current vendor requirements contradict an active document,
**stop treating the document as sufficient proof and report the
contradiction** — do not silently resolve it. A vendor skill can never
redesign the HX architecture. See
[Truth Order, Authority Layers, and Document Control](/openwiki/concepts/truth-order-and-authority.md)
for the layered authority model and the active-document rule.

## Task-routing map

Find your task, then open the linked page.

| You want to… | Read this page |
|---|---|
| Understand the 17-server ecosystem, its capability planes, build waves, and the base-build vs integration boundary | [Ecosystem Architecture — The Cornerstone](/openwiki/architecture/ecosystem-orientation.md) |
| See how the fleet is defined, how state flows from the TSV through generated tables to server records, and the PASS/CLOSED progression | [Server Fleet Map and Build State](/openwiki/architecture/server-fleet-and-states.md) |
| Look up an owner decision (D-001–D-023) or the non-negotiable operating rules | [Owner Decisions and Non-Negotiable Rules](/openwiki/concepts/decisions-and-rules.md) |
| Decide which source to trust when documents or evidence conflict | [Truth Order, Authority Layers, and Document Control](/openwiki/concepts/truth-order-and-authority.md) |
| Build / validate one server on a build day (preflight → base blocks → app block → reboot-persistence → record → check → commit) | [Workflow — Build a Server](/openwiki/workflows/build-a-server.md) |
| Understand the runbook execution system — common base blocks, per-app blocks, the `hx-base.env` pin file, shared helpers, host-gating, verified fetch | [Runbook Blocks, Pins, and Install Helpers](/openwiki/operations/runbook-blocks-and-pins.md) |
| Run a component smoke test from HX-5 CentCom (readiness → run creation → execute → normalize → promote → retain → close) | [Workflow — Run a Smoke Test](/openwiki/workflows/run-a-smoke-test.md) |
| Understand the HX-5 smoke-runner implementation (`hx-smoke-new`, `hx-smoke-promote`, `hx-smoke-doctor`, `hx-smoke-ui-capture`) | [HX-5 CentCom Smoke Runner](/openwiki/operations/smoke-runner.md) |
| Understand the proof dependency graph, phases, cumulative-proof-with-minimal-coupling, evidence shapes, and closure gates | [Proof DAG, Cumulative Evidence, and Closure Gates](/openwiki/testing/proof-dag-and-evidence.md) |
| Read the structure/conventions of a per-component smoke authority under `smoke-tests/*.md` | [Component Smoke-Test Authorities](/openwiki/testing/smoke-test-authorities.md) |
| Refresh generated documentation after editing `hx-fleet.tsv` / `hx-proof.tsv` / Markdown (regenerate tables, proof DAG, HTML; run doc-check; supersede/archive) | [Workflow — Refresh Generated Documentation](/openwiki/workflows/refresh-generated-docs.md) |
| Edit the repository consistency tooling under `tools/hx-doc/` (what each tool enforces and why) | [hx-doc Repository Consistency Tooling](/openwiki/operations/hx-doc-tooling.md) |
| Change CI, CodeRabbit review, the PR-only change rule, or the OpenWiki update workflow | [CI, CodeRabbit Review, and Change Process](/openwiki/integrations/ci-and-review.md) |
| Orient in the code via the Graft code-graph (what it indexes, MCP tools, when to prefer it over grep/file reads) | [Graft Code-Graph Integration](/openwiki/integrations/graft-code-graph.md) |

## Where to start right now

If you have not read anything yet:

1. Read `README.md` and `AGENTS.md` in the repository root — they are the
   operating contract this page summarizes.
2. Open [Ecosystem Architecture — The Cornerstone](/openwiki/architecture/ecosystem-orientation.md)
   for the foundational mental model before any task.
3. Then jump to the row in the table above that matches your task.

The architecture is the cornerstone; validation proves it and never defines it.
Skills augment expertise; neither one rewrites the ecosystem.
