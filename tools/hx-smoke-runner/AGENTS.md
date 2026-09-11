# AGENTS.md — HX-5 CentCom Smoke Runner

These instructions apply to `tools/hx-smoke-runner/` and to AI agents using these helpers on HX-5.

## Mission

Use HX-5 CentCom as the **remote, disposable smoke-test execution station** for HX Eco-System base-build validation. Keep test harness code, fixtures, manifests, logs, and evidence assembly on HX-5. Keep the SUT limited to its installed application/configuration plus explicitly authorized `hx_smoke_*` temporary state.

The CentCom runner is a **validation layer on top of the HX ecosystem architecture**. It does not define server roles, network design, model placement, or permanent integration.

## Required context before a run

Read in this order:

1. repository root `AGENTS.md`;
2. `docs/00-control/CURRENT-STATE.md`;
3. `docs/00-control/BUILD-STATE.md`;
4. `docs/00-control/DECISIONS.md`;
5. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`;
6. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`;
7. relevant SUT server record and runbook;
8. relevant application/model standard;
9. `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`;
10. `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md`;
11. `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`;
12. `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`;
13. the exact component authority under `/smoke-tests/`.

Before starting a run, the agent must be able to state:

```text
SUT host + target IP
component role
current build state
architectural layer
applicable domain/network/deployment baseline
required dependencies
validation-only dependencies
BASE PASS boundary
required prior PASS evidence
```

If any of those are unclear, stop and resolve ecosystem context before validation.

Do not use archive or human HTML as execution authority.

## Proof-chain contract

Before executing a run, populate the manifest fields created by `hx-smoke-new`:

```text
prior_pass_evidence
limited_integration_plan
```

Use `NONE` when a field genuinely has no applicable dependency/integration.

For dependent tests, record the exact current retained evidence path(s) or accepted server record(s) required by the smoke roadmap. Do not use archive material as current proof.

If a dependency changed materially after its recorded PASS, revalidate it before relying on that evidence downstream.

## Agent execution contract

- Run from `hx-5` only.
- Use `hx-smoke-new` to create each run. Do not hand-build arbitrary long-lived test directories.
- Do not edit the copied procedure to make a failing test pass.
- Do not alter the authoritative smoke-test file during an in-progress run.
- Prefer remote API/protocol/native-client tests. SSH execution on the SUT is an exception.
- Do not leave general test scripts, virtual environments, fixtures, logs, or evidence bundles on the SUT.
- Use only synthetic/disposable test data and clearly smoke-namespaced server-side objects.
- Cleanup and cleanup verification are part of PASS.
- Preserve evidence from a materially useful failed run before remediation; retries receive new run IDs.
- Never put credentials in manifests, console captures, screenshots, helper arguments intended for retention, or Git.
- Use `hx-smoke-promote`; do not manually copy a partial evidence set and call it complete.
- Review promoted evidence before committing. Helper scripts never auto-commit.
- Never infer permanent architecture from temporary smoke-test wiring.

## Standard command flow

```bash
hx-smoke-doctor
RUN_DIR="$(hx-smoke-new <sut-host> <component> <smoke-test-file> [sut-ip])"
cd "$RUN_DIR"

# edit manifest.md:
# prior_pass_evidence: <current evidence paths/server records or NONE>
# limited_integration_plan: <brief temporary integration plan or NONE>

# execute the copied procedure and capture evidence
# normalize evidence/result.txt and cleanup/cleanup.txt

hx-smoke-promote "$RUN_DIR" PASS
```

For UI proof:

```bash
hx-smoke-ui-capture \
  "http://<sut-ip>:<port>/" \
  "<expected live text>" \
  "$RUN_DIR/evidence/supporting/ui-live-state.png"
```

A screenshot without the expected live-state marker is not a functional UI PASS.

## Status vocabulary

Use only:

```text
PASS
FAIL
NOT_EXECUTABLE
```

Translate `NOT_EXECUTABLE` in narrative evidence as `NOT EXECUTABLE — PREREQUISITE OR OWNER DECISION REQUIRED`.

## Stop conditions

Stop and report instead of improvising when:

- ecosystem architecture/ownership for the SUT is unclear;
- the smoke roadmap requires prior PASS evidence that does not exist or is stale;
- current live behavior contradicts the architecture, server record, or smoke-test authority;
- the required model/checkpoint/runtime is still TBD;
- a test would require permanent integration not yet approved;
- the test would require copying a general harness onto the SUT;
- cleanup would risk deleting non-smoke data;
- a required credential is unavailable;
- a proposed workaround changes network/security/storage architecture.

## AI-centric maintenance rule

When a helper's behavior changes:

1. update its scoped instructions/README if agent behavior changes;
2. syntax-check shell scripts and compile-check Python helpers;
3. keep the CLI stable where possible;
4. update the toolset standard when packages, paths, or gates change;
5. update the architecture operating model only when the subsystem boundary/authority model changes;
6. update the smoke-test roadmap when proof dependencies or permitted limited integrations change;
7. never create a second competing runner implementation outside this directory.

## Finding things during a run

Prefer the graft MCP tools over grep or whole-file reads; one call usually
replaces several. They cover the executable surface — the runbook blocks, the
wrappers, the hx-doc tools.

- `graft_find_code` — where a symbol lives, how something works.
- `graft_file_api` — a script's shape before you touch it.
- `graft_trace_calls` — what a change affects. Returns nothing for shell
  functions; that is a parser limit, not a fact about the code.
- `graft_repo_map` — orientation.

They do **not** index the smoke authorities under `smoke-tests/`, the roadmap,
or the control documents. Read those directly. An empty graft result means not
in the graph, never does not exist.

Three questions, three sources:

| Question | Source |
|---|---|
| where is the code | graft |
| may this step run | `tools/hx-doc/hx-proof --ready <id>` |
| what must it prove | the `smoke-tests/` authority |

`hx-smoke-promote` enforces the second one: a PASS is refused when a required
prior step has not passed and been cited.
