# HX Qdrant Authority Map

Read these from the active `HX-Infratstructure/HX-Eco-System` repository. Do not use archived or human-HTML copies as execution authority.

## Foundation and current state

1. `README.md`
2. `AGENTS.md`
3. `docs/00-control/CURRENT-STATE.md`
4. `docs/00-control/BUILD-STATE.md`
5. `docs/00-control/DECISIONS.md`
6. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`

## Deployment authority

- `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
- Current HX-10 server record under `docs/02-server-records/` when it exists/has been updated for the rebuild.
- Current HX-10 runbook under `docs/03-runbooks/` when staged.
- Applicable model/vector standards under `docs/04-application-standards/` or `docs/00-control/`.

Do not create missing server/runbook facts from historical material. Historical HX-Infrastructure content is reference only.

## Validation authority

Read in this order after the SUT is installed/ready:

1. `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`
2. `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md`
3. `smoke-tests/qdrant-smoke-test.md`
4. `smoke-tests/native-web-ui-smoke-test.md`
5. `smoke-tests/mcp-companion-smoke-test.md`
6. `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`
7. `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`
8. `tools/hx-smoke-runner/AGENTS.md` when CentCom is used.

Current smoke-roadmap position for Qdrant:

```text
B5  HX-10 Qdrant core
B6  HX-10 Qdrant Web UI
B7  HX-10 Qdrant MCP
```

The Qdrant core test intentionally uses deterministic raw vectors so Qdrant can be isolated from embedding-model behavior. Downstream LightRAG/Mem0 tests may later cite accepted Qdrant PASS evidence and introduce their own minimum temporary integrations.

## Conflict rule

If live evidence, current official Qdrant requirements, and active HX authority disagree:

- do not silently choose one;
- identify the exact contradiction;
- preserve the owner-approved HX architecture unless the owner changes it;
- update the smallest affected HX authority in a separate reviewed change before execution;
- never rewrite smoke-test acceptance criteria during the run that uses them.
