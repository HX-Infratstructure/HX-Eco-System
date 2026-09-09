# AGENTS.md — HX-5 CentCom Smoke Runner

These instructions apply to `tools/hx-smoke-runner/` and to AI agents using these helpers on HX-5.

## Mission

Use HX-5 CentCom as the **remote, disposable smoke-test execution station** for HX Eco-System base-build validation. Keep test harness code, fixtures, manifests, logs, and evidence assembly on HX-5. Keep the SUT limited to its installed application/configuration plus explicitly authorized `hx_smoke_*` temporary state.

## Required context before a run

Read:

1. repository root `AGENTS.md`;
2. `docs/00-control/CURRENT-STATE.md`;
3. `docs/00-control/BUILD-STATE.md`;
4. relevant SUT server record and runbook;
5. `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`;
6. `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`;
7. the exact component authority under `/smoke-tests/`.

Do not use archive or human HTML as execution authority.

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

## Standard command flow

```bash
hx-smoke-doctor
RUN_DIR="$(hx-smoke-new <sut-host> <component> <smoke-test-file> [sut-ip])"
cd "$RUN_DIR"

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

- current live behavior contradicts the smoke-test authority;
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
5. never create a second competing runner implementation outside this directory.
