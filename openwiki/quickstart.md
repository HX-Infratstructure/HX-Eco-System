---
type: quickstart
title: Quickstart
description: Task-based routing for this repository — what it is, which page answers which question, the commands you actually run, and the handful of rules that catch people out on the first day.
tags: [quickstart, orientation, routing, commands]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-3bc721c8c10557b77c613ac1
    resource: repo://docs/03-runbooks/RUN-SHEET.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-f2994b36a477b8759d39a2a6
    resource: repo://tools/hx-doc/README.md
  - id: openwiki-source-fdc27b8992ece736496bbc4b
    resource: repo://tools/hx-smoke-runner/AGENTS.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Quickstart

This repository is the authority for a clean-room rebuild of the **HX
Eco-System**: seventeen native-Linux servers built one at a time, each proven
and recorded before the next begins. It contains no ecosystem application code.
It contains the documents that decide what gets built, the scripts that build
it, the procedures that prove it, and the checks that stop any of those three
drifting apart.

If you read only one source file, read `AGENTS.md` — it is the operating
contract, and `CLAUDE.md` exists only to point at it.

## Find your task

| You want to | Read |
|---|---|
| understand what the ecosystem *is* | [HX fleet and ecosystem layout](architecture/hx-fleet-and-ecosystem-layout.md) |
| know which source wins when two disagree | [Repository authority model](architecture/repository-authority-model.md) |
| build a server today | [Server base-build runbooks](workflows/server-base-build-runbooks.md) |
| run or promote a component proof | [Smoke-test run lifecycle](workflows/smoke-test-run-lifecycle.md) |
| know whether a proof step may run yet | [Proof chain and cumulative evidence](concepts/proof-chain-and-cumulative-evidence.md) |
| change a document or open a pull request | [Contributing and review](workflows/contributing-and-review.md) |
| fix a failing repository check | [Repository consistency tooling](operations/repository-consistency-tooling.md) |
| work out why a table or mirror is "stale" | [Generated artifacts and single sources of truth](concepts/generated-artifacts-and-single-source-of-truth.md) |
| record or retire a decision | [Owner decisions and document lifecycle](concepts/owner-decisions-and-document-lifecycle.md) |
| move a version pin, or read a drift report | [Version pins and upstream drift](operations/version-pins-and-upstream-drift.md) |
| write or close a server record | [Server records and evidence retention](operations/server-records-and-evidence-retention.md) |
| understand a CI job or its secrets | [Continuous integration workflows](operations/continuous-integration-workflows.md) |
| use a governed component skill | [Governed agent skills](integrations/governed-agent-skills.md) |
| find code fast, as an agent | [Agent tooling and the code graph](integrations/agent-tooling-and-code-graph.md) |
| know why the checks are trusted | [Enforcement gate tests](testing/enforcement-gate-tests.md) |

## The commands you actually run

```bash
# before touching a machine on build day
tools/hx-doc/hx-preflight

# building a server (each block refuses to run on the wrong host)
cd docs/03-runbooks
./common/01-base-admin-network-updates.sh hx-9     # reboots
./common/02-domain-nvidia.sh hx-9                  # reboots
./common/10-postgresql.sh hx-9                     # the application

# may this proof step run yet
tools/hx-doc/hx-proof --ready B2

# one component proof, from HX-5 CentCom
hx-smoke-doctor
RUN_DIR="$(hx-smoke-new hx-9 postgresql postgresql-smoke-test.md 192.168.50.209)"
hx-smoke-promote "$RUN_DIR" PASS

# changing anything in the repository
tools/hx-doc/hx-fleet && tools/hx-doc/hx-render-html && tools/hx-doc/hx-doc-check
coderabbit review --agent
git push -u origin HEAD && gh pr create
```

## Rules that catch people out

**The fleet lives in one file.** `docs/00-control/hx-fleet.tsv` is the source
for every server table and for the runbooks' host lookup. Edit the TSV, then run
the generator. Editing a rendered table is a defect.

**`human-html/` and `openwiki/` are generated.** So is the runbook IP map, and
so are the marked blocks inside otherwise-authored documents. Change the source
and re-render; a change appearing in a mirror without its source changing is
itself the finding.

**Everything goes through a pull request.** The default branch is not a working
branch, even for a one-line fix, and the local reviewer runs *before* the push,
not after.

**Design readiness is not as-built completion.** All seventeen servers are
documented; three are built. A pinned version and a written runbook mean the
work is planned, not running.

**Validation during a build is exactly two questions** — does the service start,
and does it survive a reboot. Deeper proof belongs to the smoke-test subsystem,
where a known answer, verified cleanup and retained evidence are all required.

**`archive/` is never current authority**, and neither is any generated tree.
Agents are told not to load them during normal work.

## Where the authorities are

| Path | What it holds |
|---|---|
| `AGENTS.md` | the operating contract and reading order |
| `docs/00-control/` | current state, build state, decisions, roadmaps, the two TSVs |
| `docs/01-architecture/` | ecosystem orientation, validation operating model |
| `docs/02-server-records/` | one as-built record per server |
| `docs/03-runbooks/` | the build blocks, wrappers and the build-day run sheet |
| `docs/04-application-standards/` | per-application and per-process standards |
| `docs/05-evidence/` | retained proof bundles |
| `smoke-tests/` | what each component must prove |
| `skills/` | governed agent expertise, advisory only |
| `tools/` | the checks and the smoke runner |

## If a check fails

Treat it as a real defect. Bypassing a check, or weakening it so an existing
document passes, is explicitly not allowed — if the check itself is wrong, fix
the check in a reviewed change. Every check here exists because the matching
failure actually happened, and a separate meta-check breaks each one on purpose
to prove it can still fail.
