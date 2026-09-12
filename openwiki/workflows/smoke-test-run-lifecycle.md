---
type: workflow
title: Smoke-test run lifecycle
description: How one component proof is executed and retained — the runner-host gate and its pre-CentCom escape, a disposable run workspace with a frozen procedure copy and a manifest, readiness checking, remote-first execution patterns, cleanup that must be verified, UI capture that needs a live marker, and the promotion gates.
tags: [smoke-test, centcom, runner, evidence, cleanup, promotion, workflow]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-6226220589c444ca13d01a54
    resource: repo://docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md
  - id: openwiki-source-fdc27b8992ece736496bbc4b
    resource: repo://tools/hx-smoke-runner/AGENTS.md
  - id: openwiki-source-926fe669d7837b250ead4e0f
    resource: repo://tools/hx-smoke-runner/hx-smoke-doctor
  - id: openwiki-source-52d69566ca67b436f190d6ea
    resource: repo://tools/hx-smoke-runner/hx-smoke-new
  - id: openwiki-source-a77fea9320056a2d55a6f0f9
    resource: repo://tools/hx-smoke-runner/hx-smoke-promote
  - id: openwiki-source-e0dddbf96726dac45f2aa6bf
    resource: repo://tools/hx-smoke-runner/hx-smoke-ui-capture.py
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Smoke-test run lifecycle

A proof is not a command that returned zero. It is a run: created from a frozen
copy of an acceptance authority, executed against a named system under test with
cited prior evidence, cleaned up, verified clean, and promoted into the
repository only if every gate holds. Four helper scripts in
`tools/hx-smoke-runner/` carry that shape.

## Where a run happens

HX-5 CentCom is the standard remote execution station: harness code, fixtures,
manifests, logs and evidence assembly all live there, and the system under test
keeps only its installed application, approved configuration and explicitly
smoke-namespaced temporary state.

All three shell helpers enforce that with the same gate — they refuse to run
unless the short hostname is `hx-5`. There is one deliberate escape, because the
first four proof steps prove HX-4 and HX-5 *before* CentCom is activated, so no
station exists yet. Exporting `HX_SMOKE_ALLOW_HOST=<hostname>` authorises an
operator station explicitly, and the station actually used is written into the
manifest, so a pre-CentCom run stays distinguishable in the retained evidence.

## Before the run

```bash
hx-smoke-doctor            # is this station ready
hx-smoke-doctor --remote   # plus one known-answer call to a proven endpoint
```

The doctor checks the client tools the runs need — a PostgreSQL client, a Redis
client, `curl`, `jq`, `git`, `ssh`, Python 3 — then the runner virtual
environment, then the two Python packages by version. Its browser check is a
real one: it launches headless Chromium, sets a page to known content and
asserts that content came back, rather than merely importing the library.
`--remote` adds an end-to-end known-answer generation call against a proven
inference endpoint and compares the response exactly.

Readiness of the *step*, as opposed to the station, is a separate question
answered by `tools/hx-doc/hx-proof --ready <id>` — see
[the proof chain](../concepts/proof-chain-and-cumulative-evidence.md).

## Creating a run

```bash
RUN_DIR="$(hx-smoke-new hx-9 postgresql postgresql-smoke-test.md 192.168.50.209)"
```

Creation is where most of the discipline lives. The script validates its
arguments, then refuses to proceed unless the named acceptance authority exists,
**is tracked in git**, and has no uncommitted or staged changes — an
uncommitted authority cannot be cited by commit, so the run would not be
reproducible.

It then resolves which proof step the run satisfies. When the host and authority
identify exactly one step it derives the id and says so; when several steps share
one authority — as every MCP companion test does — it lists the candidates and
requires the operator to name one. An explicitly supplied id is bound to the run
by checking it against the host and authority, because a valid id belonging to
another host would otherwise put the wrong step in the manifest and make
promotion enforce the wrong dependency set.

The run directory is created with a restrictive umask and a fixed shape —
`procedure/`, `runner/`, `fixtures/`, `raw/`, `evidence/supporting/`,
`cleanup/` — under a run id of `<UTC timestamp>_<host>_<component>`. The
acceptance authority is **copied** into `procedure/`, and its SHA-256 recorded.

The manifest is written with the run identity, timings, operator, runner host,
system under test, component, proof step, the authority's path, the repository
commit and the procedure hash, plus fields left as `TO_RECORD` for the operator:
the component version, the transport or endpoint, the prior PASS evidence and
the limited integration plan. Placeholder `result.txt` and `cleanup.txt` files
are seeded as `IN_PROGRESS`.

## Executing

The lifecycle every component follows is fixed: read the ecosystem authority,
verify deployment readiness, resolve prior PASS evidence, plan the limited
integration, create the run, prove reachability, execute the authoritative test,
capture raw evidence, clean up, verify cleanup, determine status, prove reboot
persistence, promote, and delete the disposable workspace.

Execution is **remote-first**, in a documented preference order: a native
network protocol or HTTP API, then a native client run from the station, then a
remote shell invocation, with a separate pattern for a Web UI. Remote shell is
the exception, used only when local execution is intrinsic to the component's
contract.

The tests themselves are known-answer tests. The Qdrant authority, for example,
creates a `hx_smoke_`-prefixed collection over the HTTP API using only the
Python standard library, writes vectors, queries and removes it — and states
that no container is required or permitted.

Two rules bound what an agent may do mid-run: do not edit the copied procedure
to make a failing test pass, and do not alter the authoritative smoke-test file
during an in-progress run. A defective authority is corrected in a separate
reviewed change and the run starts again with a new id.

### UI proof

```bash
hx-smoke-ui-capture "http://<sut-ip>:<port>/" "<expected live text>" \
  "$RUN_DIR/evidence/supporting/ui-live-state.png"
```

The capture helper is not a screenshot tool. It navigates, then **waits for
specified text to become visible**, and only then captures a full-page image
with animations disabled. It writes a sidecar metadata file recording the UTC
time, the runner, the final URL, the page title, the expected text and the
result. The rule it implements is stated plainly in the runner's own
instructions: a screenshot without the expected live-state marker is not a
functional UI pass.

## Cleanup, and proving it

Cleanup runs the exact teardown the component authority defines — dropping
temporary objects, deleting smoke keys or collections, removing a temporary
route or connection, deleting a disposable workflow or workspace — and must not
touch anything the smoke test did not create.

Cleanup is then **verified**, not assumed from a successful delete command: the
system under test is queried again to prove the smoke-namespaced objects are
gone, and the verification is recorded. If cleanup cannot be verified, the
functional test may be a pass while the cleanup gate fails, and the overall
status is a failure. Base closure waits until the residue is resolved or
explicitly approved to remain.

## Promotion

```bash
hx-smoke-promote "$RUN_DIR" PASS
```

Promotion is the gate that turns a directory into evidence. Before it copies
anything it confirms the run directory is inside the configured runs root and
that the manifest, result and cleanup files exist; then it **re-hashes the
procedure copy** against the value recorded at creation, refusing the promotion
if the acceptance criteria changed during the run and telling the operator to
correct the authority in a reviewed change and start a new run id.

For a `PASS` it additionally requires the functional result to be a pass, the
cleanup result to be a pass or not-applicable, both proof-chain fields to be
recorded, the whole proof-chain enforcement described in
[the proof chain](../concepts/proof-chain-and-cumulative-evidence.md), and the
version, transport and address fields to be filled in. It scans for credential
patterns and refuses if one appears.

Only then does it stamp the final status and end time, copy the manifest,
result, cleanup file and any supporting captures to
`docs/05-evidence/<host>/<component>/<run-id>/`, refusing if that destination
already exists, and write a README summarising the run.

It deliberately stops there. Its closing output says to review the evidence and
commit explicitly — the script never auto-commits — and, for a pass, reminds the
operator to set the step's status in the proof TSV and regenerate.

## Stop conditions

The runner's instructions list when to stop and report rather than improvise:
unclear ecosystem ownership for the system under test; required prior evidence
that does not exist or is stale; live behaviour contradicting the architecture,
the record or the authority; a model, checkpoint or runtime still undecided; a
test that would need unapproved permanent integration; a test that would need a
general harness copied onto the system under test; cleanup that would risk
deleting non-smoke data; an unavailable credential; or a workaround that would
change network, security or storage architecture.

## Afterwards

Review the promoted bundle, commit it, update the step status, and update the
server record and build state. What the retained bundle must contain is in
[server records and evidence retention](../operations/server-records-and-evidence-retention.md);
the build path that produced the system under test is in
[server base-build runbooks](server-base-build-runbooks.md).
