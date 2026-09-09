---
document: HX-5 CentCom Smoke-Test Process and Procedures
status: current
version: 1.0
date: 2026-09-09
scope: HX-5 remote smoke-test execution for HX Eco-System base-build components
authority: HX-Eco-System clean rebuild
---

# HX-5 CentCom — Smoke-Test Process and Procedures

## 1. Purpose and boundary

HX-5 CentCom is the HX development/test server and the standard remote execution station for component smoke tests after HX-5's own inference workload has passed its BASE PASS.

The purpose is to make every later component test repeatable, evidence-driven, and clean without installing ad-hoc test code on the system under test (SUT).

```text
HX-5 CentCom
    |
    |-- disposable test workspace
    |-- smoke-test runner / client tooling
    |-- synthetic fixtures
    |-- run manifest
    |-- captured evidence
    |-- teardown / cleanup verification
    |
    +---- LAN / API / CLI / approved SSH ----> System Under Test
                                                |
                                                +-- application
                                                +-- approved service config
                                                +-- only smoke-namespaced temporary data
```

**Boundary:** HX-5 is the test runner, not a second deployment plane, configuration authority, reverse proxy, or permanent integration layer.

The SUT keeps only its installed application, approved runtime/service configuration, and any temporary application data explicitly required by the smoke test. Test scripts, fixtures, logs, manifests, screenshots, comparison files, and runner dependencies remain on HX-5.

## 2. Governing rules

1. **Remote-first.** Execute smoke tests from HX-5 whenever the component exposes a LAN API, protocol endpoint, browser UI, database client interface, or other remote surface.
2. **No test harness left on the SUT.** Do not copy general test scripts, Python virtual environments, fixture libraries, or evidence bundles onto the application host merely for convenience.
3. **Exception only when the product requires local execution.** A local command may be invoked remotely over approved SSH when the component's primary contract cannot be proven remotely. Any temporary local file created solely for the test must be removed before closure.
4. **Synthetic/disposable data only.** Base smoke tests do not use production corpora, production workflows, production memories, persistent agent projects, or unrelated application data.
5. **Smoke namespace.** Temporary server-side objects must use an obvious HX smoke-test name such as `hx_smoke_*` or the exact name defined by the component authority.
6. **Authoritative procedure.** The executable acceptance definition comes from the current file under `/smoke-tests/` in the HX-Eco-System repository. Do not improvise a different PASS rule during execution.
7. **Known-answer proof.** The test must prove the component's primary contract with an expected result. Process health alone is not a functional PASS.
8. **Cleanup is part of PASS.** A test that functionally succeeds but leaves validation-only state behind is not complete.
9. **Reboot persistence is separate.** After the component smoke test passes, execute the minimum post-reboot proof defined by the component/base-build authority. Do not automatically rerun a large destructive or expensive test when a shorter persistence proof is sufficient.
10. **No architecture creep.** Smoke testing must not introduce permanent routes, new firewalls, TLS requirements, DNS changes, service accounts, NFS dependencies, containers, or cross-service wiring unless explicitly approved.

## 3. CentCom workspace structure

Use one disposable directory per test execution.

Default parent:

```bash
export HX_SMOKE_ROOT="${HX_SMOKE_ROOT:-$HOME/hx-smoke-runs}"
mkdir -p "$HX_SMOKE_ROOT"
```

Run identifier:

```text
<UTC timestamp>_<server>_<component>
```

Example:

```text
20260909T193000Z_hx-9_postgresql
```

Recommended workspace:

```text
$HX_SMOKE_ROOT/20260909T193000Z_hx-9_postgresql/
├── manifest.md
├── procedure/
│   └── postgresql-smoke-test.md
├── runner/
│   └── disposable test script(s), if required
├── fixtures/
│   └── synthetic input only
├── raw/
│   └── command/API/UI capture
├── evidence/
│   └── normalized PASS/FAIL evidence
└── cleanup/
    └── teardown output and verification
```

The workspace is disposable. After evidence is promoted to the authoritative evidence location and cleanup is verified, delete the run directory.

Do not use the application host as the long-term location for any of these directories.

## 4. Standard execution lifecycle

Every component follows the same lifecycle.

```text
PREPARE
  -> PROVE REACHABILITY
  -> EXECUTE AUTHORITATIVE SMOKE TEST
  -> CAPTURE RAW EVIDENCE
  -> CLEAN UP TEMPORARY STATE
  -> VERIFY CLEANUP
  -> DETERMINE PASS / FAIL
  -> REBOOT-PERSISTENCE GATE
  -> PROMOTE EVIDENCE
  -> DELETE DISPOSABLE WORKSPACE
```

### Step 1 — Prepare

On HX-5:

1. confirm the SUT/server and component;
2. read the current server record, runbook, application standard, and `/smoke-tests/<component>-smoke-test.md`;
3. create a new timestamped workspace;
4. copy or check out the current smoke-test authority into `procedure/` without editing its acceptance criteria;
5. record the repository commit SHA used for the run;
6. create `manifest.md` before executing the test.

Minimum manifest fields:

```text
run_id
utc_start
operator
runner_host = hx-5
sut_host
sut_ip
component
component_version_or_revision
smoke_test_file
smoke_test_repo_commit
transport_or_endpoint
known_answer
validation_only_dependencies
cleanup_objects_expected
```

Never record passwords, PATs, API keys, private keys, bearer tokens, or other secret values in the manifest or retained console output.

### Step 2 — Prove reachability

Use only the surface required by the component test:

- HTTP/REST/gRPC endpoint;
- native database client;
- Redis protocol client;
- MCP client;
- browser/UI from HX-5 or operator workstation where visual proof is required;
- approved SSH only when a local command is genuinely required.

A successful ping or TCP connection is not the functional smoke test. It only proves the path is available.

### Step 3 — Execute the component authority

Run the current standalone test exactly enough to prove its defined contract.

Examples:

```text
PostgreSQL  -> create / write / read / cleanup
Redis       -> PING / SET / GET / DELETE
Qdrant      -> create collection / write / query / delete
MCP         -> discover tool / call safe tool / known result
Ollama      -> known-answer inference
Embedding   -> expected vector dimension + nonzero/repeatability
n8n         -> create / execute / save / reopen / execute / delete
```

Do not expand the test into integration testing, performance testing, security testing, or production acceptance unless that additional scope is explicitly requested.

### Step 4 — Capture raw evidence

Capture the smallest evidence set that proves what happened:

- UTC timestamp;
- HX-5 runner identity;
- SUT hostname/IP;
- application version/revision;
- endpoint or interface used;
- command/script identity;
- known-answer input;
- relevant response/output;
- explicit PASS/FAIL marker;
- temporary object names;
- cleanup result;
- reboot-persistence result when applicable.

For CLI/API tests, redirect stdout/stderr into `raw/` while preserving an operator-readable console result.

For Web UI tests, capture only the screenshots or exported evidence necessary to prove the UI loaded and displayed live backend state or the required known-answer result.

Do not capture secret values in evidence. Redact accidental secret output before promotion; do not edit the underlying functional result.

### Step 5 — Cleanup temporary state

Run the exact teardown defined by the component smoke-test file.

Cleanup may include:

- drop temporary PostgreSQL objects;
- delete Redis smoke keys;
- delete Qdrant smoke collections;
- delete synthetic Mem0 memories/collections;
- remove temporary OmniRoute routes;
- remove temporary Open WebUI connections;
- delete temporary n8n workflow;
- remove NGINX validation route;
- delete disposable agent/project workspaces.

Do not delete or alter anything that was not created by the smoke test.

### Step 6 — Verify cleanup

Cleanup is not assumed from a successful delete command. Query the SUT again and prove that the smoke-test object, route, workflow, collection, key, connection, or project is gone.

Record the verification in `cleanup/` and in the final evidence summary.

If cleanup cannot be verified:

```text
FUNCTIONAL TEST = PASS
CLEANUP GATE    = FAIL
OVERALL STATUS  = FAIL / INCOMPLETE
```

Do not close BASE PASS until the validation-only residue is resolved or explicitly approved to remain.

### Step 7 — Determine smoke-test status

Use only these states:

```text
PASS
FAIL
NOT EXECUTABLE — PREREQUISITE OR OWNER DECISION REQUIRED
```

A PASS requires:

```text
required endpoint/interface reachable
AND
primary known-answer function succeeds
AND
expected result is verified
AND
cleanup succeeds
AND
cleanup verification succeeds
```

A prerequisite gap is not silently converted into FAIL if the test is not executable by design. Example: the HX-4 reranker remains `NOT EXECUTABLE` until its exact checkpoint/runtime is pinned.

### Step 8 — Reboot-persistence gate

After the component functional test passes and cleanup completes:

1. reboot the SUT as required by the base-build runbook;
2. confirm the service returns active/enabled where applicable;
3. confirm the required storage/configuration persists;
4. execute the minimum post-reboot functional proof defined for that component;
5. capture evidence from HX-5.

Do not recreate the full temporary test dataset unless the component authority specifically requires it.

### Step 9 — Promote evidence

Evidence is retained under the repository/server evidence structure, not inside the disposable runner workspace.

Recommended retained bundle:

```text
docs/05-evidence/<server>/<component>/<run-id>/
├── manifest.md
├── result.txt
├── cleanup.txt
└── supporting captures as required
```

If the repository evidence policy later points to external/raw storage for large artifacts, retain only the authoritative index/manifest and link/reference there. Do not create a second truth plane.

### Step 10 — Remove disposable workspace

Only after evidence promotion and verification:

```bash
rm -rf -- "$HX_SMOKE_ROOT/<run-id>"
```

Delete only the exact run directory. Never run a broad wildcard removal against the parent smoke root.

## 5. Remote execution patterns

### Pattern A — Native network protocol or HTTP API

Preferred.

```text
HX-5 runner -> SUT LAN endpoint -> known-answer response
```

Use for Ollama, Qdrant, LightRAG, Crawl4AI service mode, embedding/reranking services, OmniRoute, MCP HTTP, and similar endpoints.

### Pattern B — Native client from HX-5

Install the minimum client tooling on HX-5, not the database/server package on the SUT merely for testing.

Examples:

```text
psql       -> PostgreSQL on HX-9
redis-cli  -> Redis on HX-9
FastMCP client -> product MCP endpoint
curl/Python stdlib -> HTTP APIs
```

Client versions and required packages are part of the HX-5 dev/test toolset and should be recorded in the HX-5 as-built record when installed permanently.

### Pattern C — Remote shell invocation

Use only where local execution is intrinsic to the product or no accepted remote interface exists.

```text
HX-5 -> SSH -> execute existing SUT command -> return stdout/stderr to HX-5
```

Prefer inline commands or existing installed application commands. If a temporary script must be copied to the SUT:

1. place it in a unique smoke-namespaced temporary path;
2. execute it;
3. capture its output back on HX-5;
4. remove the script immediately;
5. verify removal.

This is the exception, not the default.

### Pattern D — Web UI proof

The UI remains on its native application host/port. HX-5 may provide test data or API-side setup, but the visual proof is captured against the application's direct LAN UI unless the component specifically being tested is HX-7 NGINX.

NGINX is not inserted merely to make another component's UI smoke test work.

## 6. Evidence naming and retention

Base filename:

```text
YYYYMMDDTHHMMSSZ_<server>_<component>_<gate>_<description>.<ext>
```

Examples:

```text
20260909T193000Z_hx-9_postgresql_smoke_result.txt
20260909T193015Z_hx-9_postgresql_cleanup_result.txt
20260909T201100Z_hx-10_qdrant_ui_live-state.png
```

Every retained result must be traceable to:

- one SUT;
- one component;
- one smoke-test authority file;
- one repository commit;
- one run ID;
- one PASS/FAIL determination.

Evidence proves observed behavior. It does not independently override an explicit current owner decision or current active authority.

## 7. Secrets and test credentials

Smoke tests may reference credential **names**, paths, or environment-variable identifiers, but retained scripts/manifests/evidence must not contain actual secret values.

Use environment variables or another owner-approved secret mechanism on HX-5 at execution time. Never commit a `.local.env`, PAT, API key, private key, or plaintext password to the repository.

If a test credential is temporary, remove or disable it after the test when its only purpose was validation.

## 8. Failure and retry rule

On failure:

1. preserve the failed run's evidence before changing the SUT;
2. identify whether the failure is reachability, application behavior, dependency, test-runner defect, cleanup, or reboot persistence;
3. correct only the identified issue;
4. create a **new run ID** for the retry;
5. never overwrite failed evidence with the later PASS.

The server record may summarize the final accepted state, but the evidence trail should retain the materially relevant failed run when it explains a correction or architecture decision.

## 9. HX-5 activation gate

The CentCom smoke-runner role becomes available only after HX-5's own base inference workload is healthy enough to close its applicable foundation gate.

Before using HX-5 as the standard runner for HX-9 and later systems, record:

```text
HX-5 base/domain/GPU state accepted
HX-5 Ollama active/enabled
Ornith assigned model functional PASS
HX-5 reboot persistence PASS
smoke-runner client toolset installed
HX_SMOKE_ROOT selected and writable
remote test to one already-proven HX endpoint PASS
```

The smoke-runner role does **not** require DeepSeek Harness to be installed first. Harness remains at its scheduled implementation priority.

## 10. Closure rule

For each later component:

```text
SUT base/service health
        AND
component smoke test from HX-5
        AND
companion MCP/UI gate where assigned
        AND
cleanup + cleanup verification
        AND
reboot-persistence proof
        AND
retained evidence
        AND
server record / BUILD-STATE update
        =
BASE PASS / CLOSED
```

This procedure standardizes **how** HX proves components. The individual files under `/smoke-tests/` remain the authority for **what each component must prove**.
