---
document: HX Eco-System Smoke-Testing Operating Model
status: current
version: 1.1
date: 2026-09-09
scope: architecture and authority model for HX component smoke testing
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Smoke-Testing Operating Model

## 1. Purpose and prerequisite context

This document explains how HX component smoke testing fits together across the repository, HX-5 CentCom, the system under test (SUT), prior proof dependencies, and retained evidence.

It is a **validation-layer architecture map**. It does **not** define the HX ecosystem itself.

Before using this model, establish current ecosystem context from:

1. `ARCHITECTURE-ORIENTATION.md` — ecosystem cornerstone, server ownership, baseline configuration, and capability planes;
2. `../00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md` — deployment/build order and BASE PASS boundary;
3. relevant current server record, runbook, and application/model standard;
4. `../00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` — ordered proof dependencies and permitted limited integration.

Only then select the exact component procedure under `/smoke-tests/`.

Current implementation state: the repository authorities and runner tooling are defined; the CentCom runner is **planned, not yet live**, until HX-5 is built and its activation evidence is captured.

## 2. Operating model at a glance

```text
HX ECOSYSTEM ARCHITECTURE / CURRENT STATE
            |
            v
BASE IMPLEMENTATION ROADMAP
  SUT installed and ready
            |
            v
SMOKE-TEST ROADMAP
  prior PASS evidence + permitted limited integration
            |
            v
COMPONENT SMOKE AUTHORITY
  exact known-answer acceptance procedure
            |
            v
HX-5 CENTCOM
  disposable test project
  client/runner tools
  synthetic fixtures
  manifest
  prior PASS evidence references
  raw captures
  cleanup proof
            |
      remote LAN/API/protocol/UI
      approved SSH only as exception
            |
            v
SYSTEM UNDER TEST
  installed application
  approved configuration
  temporary hx_smoke_* state only
            |
            v
KNOWN-ANSWER FUNCTIONAL RESULT
            |
            v
CLEANUP + CLEANUP VERIFICATION
            |
            v
REBOOT-PERSISTENCE PROOF
            |
            v
RETAINED EVIDENCE
  docs/05-evidence/<sut>/<component>/<run-id>/
            |
            v
SERVER RECORD + BUILD-STATE CLOSURE
```

The design centralizes validation tooling on HX-5 while keeping each application host clean.

## 3. Authority model

Each layer answers one question.

| Authority | Question answered |
|---|---|
| `ARCHITECTURE-ORIENTATION.md` | What is the HX ecosystem, how is it configured, and which server owns each capability? |
| `../00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md` | What is built, in what dependency order, and what is the component's BASE PASS boundary? |
| `../00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` | Which proof runs next, what prior PASS evidence is required, and what limited validation integration is permitted? |
| `../../smoke-tests/<component>-smoke-test.md` | What must this component prove and how is the known-answer test executed/cleaned up? |
| `../04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` | How does HX execute, clean up, and retain a smoke-test run? |
| `../04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md` | What permanent client toolset and bootstrap are used on HX-5? |
| `../../tools/hx-smoke-runner/` | What repository-owned helper implementation performs the repeatable runner operations? |
| `../05-evidence/` | What observed proof supports the accepted state? |
| server record + `../00-control/BUILD-STATE.md` | What is the current accepted as-built/closure state? |

No layer should silently replace another. The deployment roadmap is not the smoke roadmap; the smoke roadmap is not the component procedure; validation evidence is not architecture authority.

## 4. Roles and boundaries

### Repository

The repository is the durable instruction and evidence authority. It holds enough context for an AI infrastructure/coding agent to recover the intended operation without relying on chat history.

It owns:

- current context and owner-approved decisions;
- ecosystem architecture and application standards;
- deployment and smoke-test roadmaps;
- server runbooks;
- component smoke-test acceptance criteria;
- CentCom runner code and scoped agent instructions;
- retained evidence indexes/bundles;
- current server/build state.

### HX-5 CentCom

HX-5 is the standard development/test and smoke-test execution station after its activation gate passes.

It owns:

- permanent client tooling;
- disposable run workspaces;
- synthetic test fixtures;
- manifests and raw captures;
- prior PASS evidence references;
- browser/UI test automation where appropriate;
- cleanup execution and verification;
- evidence assembly and promotion.

HX-5 is **not** a second application deployment plane, network control plane, common reverse proxy, or permanent integration hub.

### System under test

The SUT owns only:

- its installed application/runtime;
- its approved service configuration;
- its real application interfaces;
- temporary smoke-namespaced application state explicitly required by the test.

General test harness code, Python environments, fixture libraries, logs, and retained evidence do not belong on the SUT.

## 5. Proof-chain model

The smoke roadmap uses **cumulative proof with minimal live coupling**.

A downstream run records:

```text
prior_pass_evidence
limited_integration_plan
```

Use `NONE` when genuinely not applicable.

Examples:

- OmniRoute cites a current approved model PASS and creates one temporary validation route.
- LightRAG cites Qdrant + embedding + approved LLM PASS and uses those services only for a synthetic disposable RAG proof.
- Mem0 cites Qdrant + embedding + approved LLM PASS and uses one disposable collection/memory lifecycle.
- MCP companion tests cite the parent application's core PASS; they do not depend on the HX-15 FastMCP server.
- UI companion tests cite the parent core PASS and use direct LAN access; they do not require HX-7 NGINX unless NGINX is the SUT.

Do not force a dependency merely to make tests appear connected. Standalone component proof remains standalone when that gives better fault isolation.

## 6. Standard run lifecycle

```text
READ ECOSYSTEM AUTHORITY
        -> VERIFY DEPLOYMENT READINESS
        -> RESOLVE PRIOR PASS EVIDENCE
        -> PLAN LIMITED INTEGRATION
        -> CREATE RUN
        -> PROVE REACHABILITY
        -> EXECUTE KNOWN-ANSWER TEST
        -> CAPTURE RESULT
        -> CLEAN UP
        -> VERIFY CLEANUP
        -> DETERMINE STATUS
        -> REBOOT-PERSISTENCE PROOF
        -> PROMOTE EVIDENCE
        -> REVIEW / COMMIT
        -> REMOVE DISPOSABLE RUN
```

The runner helpers support this lifecycle but do not replace judgment, roadmap authority, or the component procedure.

## 7. PASS model

Process/service health is necessary but not sufficient.

For a normal component:

```text
SUT service/base health
        AND
required prior PASS evidence resolved
        AND
known-answer component smoke test
        AND
assigned MCP/UI companion gate where applicable
        AND
cleanup succeeds
        AND
cleanup verification succeeds
        AND
reboot persistence
        AND
reviewed retained evidence
        =
BASE PASS / CLOSED
```

A functional success with failed or unverified cleanup is not a complete PASS.

Use only:

```text
PASS
FAIL
NOT EXECUTABLE — PREREQUISITE OR OWNER DECISION REQUIRED
```

`NOT EXECUTABLE` is appropriate when a required implementation decision or prerequisite proof is genuinely not established; it is not a substitute for a failing result.

## 8. Remote-first test patterns

Preferred order:

1. **LAN/API/protocol endpoint** — curl, Python, native API/client.
2. **Native client from HX-5** — for example `psql` or `redis-cli`.
3. **MCP client from HX-5** — discovery plus one safe known-answer tool call.
4. **Direct-LAN browser/UI proof** — Playwright-managed Chromium or operator capture where product authentication/navigation requires it.
5. **Approved SSH remote command** — exception only when local execution is intrinsic to the component.

Do not copy a general-purpose harness onto the SUT just to make a test convenient.

## 9. Limited integration rule

Base stand-up remains base stand-up, but some components cannot prove their primary contract in complete isolation.

Limited integration is allowed when all of the following are true:

- the dependency has already passed its own applicable gate;
- the dependency is required by the smoke roadmap/current accepted component configuration;
- the dependency is necessary to prove the component's primary function;
- test data is synthetic and disposable;
- validation-only objects/routes/connections are clearly identified;
- temporary wiring/state is removed or explicitly approved to remain.

Examples include LightRAG using an already-proven Qdrant/LLM/embedding path, Mem0 using a disposable Qdrant collection, Open WebUI temporarily connecting to a proven Ollama endpoint, OmniRoute temporarily routing to one proven model, and NGINX proxying one temporary HX-5 upstream.

A smoke-test dependency does not automatically become permanent production architecture.

## 10. Proof invalidation

A downstream test may rely only on current proof.

Material changes can stale prior evidence, including:

- model alias/revision/dimension changes;
- embedding/reranker changes;
- Qdrant or database upgrade/configuration changes affecting behavior;
- major API/MCP contract changes;
- SUT rebuild or persistent data/configuration replacement.

If a required proof is stale, revalidate it before downstream PASS.

## 11. AI-centric repository contract

The repository is incomplete if an AI agent must reconstruct material operating rules from conversation history.

Before smoke testing, an agent must be able to determine from the repository alone:

- current system state and build priority;
- the SUT's owner server/IP, role, and architecture layer;
- applicable foundational network/domain/deployment rules;
- model/data placement rules;
- required versus validation-only dependencies;
- the BASE PASS boundary;
- the required prior PASS evidence;
- the exact smoke-test acceptance criteria;
- the CentCom execution process;
- cleanup requirements;
- evidence destination;
- stop conditions and owner-decision boundaries.

Scoped instructions live near the implementation. `../../tools/hx-smoke-runner/AGENTS.md` governs runner behavior; the root `../../AGENTS.md` governs repository-wide behavior.

An AI agent must **not** change a smoke-test authority during the same in-progress run that is using it. If the authority is defective or stale, stop, correct it in a separate committed change, and begin a new run ID.

## 12. CentCom activation sequence

The CentCom runner is activated after HX-5's inference foundation is accepted and before later state/retrieval/application components rely on ad-hoc testing.

```text
HX-5 base/domain/GPU accepted
        AND
Ollama + Ornith PASS
        AND
HX-5 reboot persistence PASS
        AND
CentCom client toolset/bootstrap complete
        AND
hx-smoke-doctor PASS
        AND
remote known-good HX-2 activation probe PASS
        =
CENTCOM SMOKE-RUNNER ACTIVE
```

DeepSeek Harness is **not** a prerequisite for CentCom smoke-runner activation. Its meta-agent smoke test remains a later HX-5 workload gate in the deployment/smoke roadmaps.

## 13. What this model deliberately does not become

The smoke-testing system does not create:

- a container platform;
- a second deployment plane;
- a permanent cross-service integration mesh;
- a general reverse-proxy requirement;
- new firewall/TLS/DNS/network architecture;
- production test data;
- automatic evidence commits without review;
- permission to modify unrelated SUT state;
- a replacement for ecosystem architecture or component-specific acceptance criteria.

## 14. Current status

As of 2026-09-09:

- HX-1, HX-2, and HX-3 establish the current PASS/CLOSED cornerstone evidence;
- the base implementation roadmap is current;
- the ordered smoke-test roadmap is defined;
- the component smoke-test catalog is defined under `/smoke-tests/`;
- the HX-5 process/procedure and toolset/bootstrap standards are defined;
- repository-owned runner helpers are defined;
- HX-5 remains `NOT STARTED`, so CentCom smoke-runner activation is **not yet an as-built fact**.

The next runtime validation begins only as the deployment sequence builds HX-4 and HX-5.
