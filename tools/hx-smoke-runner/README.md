# HX-5 CentCom Smoke Runner

Repository-owned helpers for executing HX Eco-System component smoke tests from HX-5.

## Authority

- **What a component must prove:** `/smoke-tests/*.md`
- **How HX-5 executes/retains proof:** `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`
- **Toolset/bootstrap:** `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`
- **Scoped AI instructions:** `tools/hx-smoke-runner/AGENTS.md`

## Commands

```text
hx-smoke-doctor       validate runner dependencies; --remote performs activation proof
hx-smoke-new          create a disposable run and manifest
hx-smoke-ui-capture   capture deterministic direct-LAN UI evidence
hx-smoke-promote      promote reviewed normalized evidence; never auto-commits
```

Bootstrap execution artifact:

```text
docs/03-runbooks/HX-5/04-centcom-smoke-runner-bootstrap.sh
```

These tools are intentionally small. They do not deploy applications, alter network architecture, or replace component-specific smoke tests.
