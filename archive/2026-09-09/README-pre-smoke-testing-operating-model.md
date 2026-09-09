# HX Eco-System

Authoritative repository for the clean-room HX Eco-System rebuild.

## Start here

Agentic tools and coding agents must read these files in order:

1. `AGENTS.md`
2. `docs/00-control/CURRENT-STATE.md`
3. `docs/00-control/BUILD-STATE.md`
4. `docs/00-control/DECISIONS.md`
5. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
6. The current server record and runbook for the server being worked on.
7. The relevant application standard.
8. If smoke-testing, the exact `/smoke-tests/*.md` authority and the scoped runner instructions under `tools/hx-smoke-runner/AGENTS.md`.

`CLAUDE.md` exists as a Claude Code entry point and points back to `AGENTS.md` so instructions do not drift.

## Authoritative surfaces

- `docs/**/*.md` = authoritative current control, architecture, standards, server records, runbooks, and evidence indexes.
- `smoke-tests/*.md` = authoritative current component smoke-test acceptance procedures.
- `docs/03-runbooks/**/*.sh` = approved server/bootstrap execution artifacts.
- `tools/hx-smoke-runner/` = repository-owned CentCom smoke-runner implementation with scoped AI instructions.
- `human-html/**/*.html` = human-readable mirrors for the infrastructure owner; not execution authority.
- `archive/**` = superseded historical versions; never current authority.

## AI-centric operating model

This repository must remain usable by an AI infrastructure/coding agent without reconstructing decisions from chat history.

For every material implementation surface, keep:

1. concise current context and boundaries;
2. explicit authority/read order;
3. deterministic runbook or helper commands where appropriate;
4. component-specific PASS criteria under `/smoke-tests/`;
5. evidence paths and cleanup requirements;
6. no duplicated competing implementation or instruction plane.

If an agent cannot determine what to read, what it may change, how to prove success, and where evidence belongs from the repository itself, the repository context is incomplete.

## Core build philosophy

KISS: one server, validate it, record it, then move on.

Native Linux + systemd. No Docker, Podman, or Kubernetes unless the infrastructure owner explicitly changes that rule.

Historical HX-Infrastructure material is reference-only. It does not establish current state, configuration, or closure.

## Current state

- HX-1: PASS / CLOSED — Samba AD/DNS/Kerberos/NTP
- HX-2: PASS / CLOSED — Qwen-X / Ollama
- HX-3: PASS / CLOSED — Coder-X / Ollama
- HX-4: NEXT — Meta-X base build plus shared embedding/reranking plane
- HX-5 through HX-17: pending clean rebuild/base application stand-up in dependency order.

HX-5 is planned as CentCom / Ornith / DeepSeek Harness / dev-test and, after its activation gate, the standard remote smoke-test runner for later components. Planned does not mean installed.

## Document lifecycle

Active documents use stable, unversioned filenames. Version/date/status live inside the document where applicable.

When a document is superseded:
1. archive the prior copy under `archive/YYYY-MM-DD/<original-path>/`;
2. replace the active file at the same stable path;
3. update the matching HTML mirror when one exists;
4. leave exactly one active version.
