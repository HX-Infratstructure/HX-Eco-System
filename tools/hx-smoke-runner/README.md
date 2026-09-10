# HX-5 CentCom Smoke Runner

Repository-owned helpers for executing HX Eco-System component smoke tests from HX-5.

## Authority hierarchy

The runner is validation tooling, not ecosystem architecture.

Read in this order before use:

1. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md` — ecosystem cornerstone and ownership.
2. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md` — deployment order and BASE PASS boundary.
3. `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` — ordered proof dependencies and permitted limited integration.
4. `/smoke-tests/*.md` — exact component acceptance procedure.
5. `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` — execution/evidence process.
6. `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md` — toolset/bootstrap.
7. `tools/hx-smoke-runner/AGENTS.md` — scoped AI operating contract.

## Commands

```text
hx-smoke-doctor       validate runner dependencies; --remote performs activation proof
hx-smoke-new          create a disposable run and proof-chain manifest
hx-smoke-ui-capture   capture deterministic direct-LAN UI evidence
hx-smoke-promote      validate proof/cleanup/dependency fields and promote evidence; never auto-commits
```

Bootstrap execution artifact:

```text
docs/03-runbooks/HX-5/04-centcom-smoke-runner-bootstrap.sh
```

## Proof-chain manifest

`hx-smoke-new` creates two fields that must be resolved before a run can be promoted as PASS:

```text
prior_pass_evidence: <current evidence paths/server records or NONE>
limited_integration_plan: <brief temporary integration plan or NONE>
```

Use the smoke-test roadmap to determine what upstream proof is required.

This gives downstream runs a reproducible evidence chain without forcing unnecessary live coupling between components.

## Boundaries

These tools are intentionally small. They do not:

- deploy applications;
- change ecosystem ownership or server placement;
- alter network architecture;
- create permanent integration;
- infer dependencies that are not in the roadmap/procedure;
- replace component-specific smoke tests;
- auto-commit evidence.
