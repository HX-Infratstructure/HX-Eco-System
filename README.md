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

`CLAUDE.md` exists as a Claude Code entry point and deliberately points back to `AGENTS.md` so instructions do not drift.

## Authoritative surfaces

- `docs/**/*.md` = authoritative current agent/machine working documents.
- `human-html/**/*.html` = human-readable mirrors for the infrastructure owner.
- `archive/**` = superseded historical versions; never current authority.

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

## Document lifecycle

Active documents use stable, unversioned filenames. Version/date/status live inside the document.

When a document is superseded:
1. archive the prior copy under `archive/YYYY-MM-DD/<original-path>/`;
2. replace the active file at the same stable path;
3. update the matching HTML mirror when one exists;
4. leave exactly one active version.
