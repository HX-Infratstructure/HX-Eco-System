# Docling Authority Map for HX

Use the current repository version of each path. Do not use `human-html/` or `archive/` as execution authority.

## Required preflight

1. `AGENTS.md`
2. `README.md`
3. `docs/00-control/CURRENT-STATE.md`
4. `docs/00-control/BUILD-STATE.md`
5. `docs/00-control/DECISIONS.md`
6. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`
7. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
8. `skills/AGENTS.md`
9. `skills/SKILL-GOVERNANCE.md`
10. `skills/SKILL-REGISTRY.md`
11. `skills/docling/README.md`
12. `skills/docling/hx-docling-advisor/SKILL.md`

## Execution authority

When created and current:

```text
docs/02-server-records/HX-16.md
docs/03-runbooks/HX-16/
```

At the 2026-09-09 review point these active authorities do not exist. The skill cannot substitute for them.

## Owner decisions that materially constrain Docling

- `D-001`: clean-room rebuild.
- `D-002`: native Linux + systemd; no containers unless owner changes the rule.
- `D-003`: product-specific MCP belongs to parent BASE where assigned.
- `D-006`: Granite-Docling 258M stays on HX-16; CPU-first BASE; GPU only after measured need.
- `D-014`: CentCom is the standard remote smoke runner after activation.
- `D-015`: architecture/context before validation.
- `D-016`: ordered cumulative smoke proof with minimum live coupling.
- `D-017`: governed skill layer is expertise, not architecture/execution authority.

## Validation authority

Read in this order when the SUT is ready:

1. `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`
2. `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md`
3. `smoke-tests/docling-smoke-test.md`
4. `docs/04-application-standards/MCP-STANDARD.md`
5. `smoke-tests/mcp-companion-smoke-test.md`
6. `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`
7. `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`
8. `tools/hx-smoke-runner/AGENTS.md` when CentCom is used.

Current proof chain:

```text
D1 HX-16 Docling + Granite-Docling
  requires: CentCom active + Granite model staged locally
  live integration: NONE
  fixture: self-generated local PDF
  proves: normal Docling conversion + Granite-Docling CPU path

D2 HX-16 Docling MCP
  requires: accepted D1 PASS
  live integration: parent Docling service only
  proves: MCP negotiation + tool discovery + safe known-answer call
```

Docling BASE closure also requires cleanup, reboot/persistence evidence where applicable, server-record update, and BUILD-STATE closure under current rules.

## Conflict rule

If current official Docling behavior, live HX-16 evidence, and active HX authority disagree:

- identify the exact contradiction;
- preserve owner-approved placement/native/CPU-first boundaries unless the owner changes them;
- stop before infrastructure-changing execution based on an upstream default;
- update the smallest affected HX authority in a separate reviewed change if the active authority is technically wrong;
- never rewrite smoke-test PASS criteria during the run that uses them.
