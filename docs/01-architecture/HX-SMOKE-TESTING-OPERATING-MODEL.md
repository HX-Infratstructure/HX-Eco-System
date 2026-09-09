---
document: HX Eco-System Smoke-Testing Operating Model
status: current
version: 1.0
date: 2026-09-09
scope: architecture and authority model for HX component smoke testing
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Smoke-Testing Operating Model

## 1. Purpose

This document explains how HX component smoke testing fits together across the repository, HX-5 CentCom, the system under test (SUT), and retained evidence.

It is the architecture-level map. It does **not** replace component smoke-test procedures, the HX-5 execution standard, or the CentCom runner implementation.

Current implementation state: the repository authorities and runner tooling are defined; the CentCom runner is **planned, not yet live**, until HX-5 is built and its activation evidence is captured.

## 2. Operating model at a glance

```text
CURRENT OWNER DECISION + ROADMAP
            |
            v
REPOSITORY AUTHORITIES
  docs/                 context / architecture / standards / runbooks
  smoke-tests/          exact component PASS criteria
  tools/hx-smoke-runner CentCom runner implementation + AI instructions
            |
            v
HX-5 CENTCOM
  disposable test project
  client/runner tools
  synthetic fixtures
  manifest
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

The design keeps test code and test-state management centralized on HX-5 while keeping each application host clean.

## 3. Authority model

Each layer answers one question.

| Authority | Question answered |
|---|---|
| `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md` | What is being built and in what dependency order? |
| `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md` | How does the HX smoke-testing architecture fit together? |
| `smoke-tests/<component>-smoke-test.md` | What must this component prove to pass its smoke test? |
| `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` | How does HX execute, clean up, and retain a smoke-test run? |
| `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md` | What permanent client toolset and bootstrap are used on HX-5? |
| `docs/03-runbooks/HX-5/04-centcom-smoke-runner-bootstrap.sh` | What executable bootstrap activates that HX-5 capability? |
| `tools/hx-smoke-runner/` | What repository-owned helper implementation performs the repeatable runner operations? |
| `docs/05-evidence/` | What observed proof supports the accepted state? |
| server record + `BUILD-STATE.md` | What is the current accepted as-built/closure state? |

No single layer should duplicate the others. The roadmap stays concise; component tests hold component details; the runner standard holds execution mechanics.

## 4. Roles and boundaries

### Repository

The repository is the durable instruction and evidence authority. It holds enough context for an AI infrastructure/coding agent to recover the intended operation without relying on chat history.

It owns:

- current context and owner-approved decisions;
- architecture and application standards;
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

### AI agent / operator

The executing agent/operator must:

1. load current repository context;
2. identify the exact component smoke-test authority;
3. create a new CentCom run workspace;
4. execute the known-answer test without rewriting acceptance criteria;
5. preserve evidence;
6. clean up validation-only state and prove it is gone;
7. promote evidence for review;
8. update as-built/BUILD-STATE only after the required gates actually pass.

## 5. Standard run lifecycle

```text
READ CURRENT AUTHORITY
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

The runner helpers support this lifecycle but do not replace judgment or the component authority.

## 6. Disposable test-project rule

Every test execution receives a unique timestamped workspace on HX-5, for example:

```text
$HX_SMOKE_ROOT/20260909T193000Z_hx-9_postgresql/
├── manifest.md
├── procedure/
├── runner/
├── fixtures/
├── raw/
├── evidence/
└── cleanup/
```

The workspace is temporary.

The durable artifacts are the accepted repository authorities and the reviewed evidence bundle. After evidence promotion and cleanup verification, the disposable run directory is removed.

## 7. PASS model

Process/service health is necessary but not sufficient.

For a normal component:

```text
SUT service/base health
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

`NOT EXECUTABLE` is appropriate when a required implementation decision or dependency is genuinely not established; it is not a substitute for a failing result.

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

- the dependency has already passed its own applicable base gate;
- the dependency is necessary to prove the component's primary function;
- test data is synthetic and disposable;
- validation-only objects/routes/connections are clearly identified;
- the temporary wiring/state is removed or explicitly approved to remain.

Examples include LightRAG using an already-proven vector store/LLM/embedding path, Mem0 using a disposable Qdrant collection, Open WebUI temporarily connecting to a proven Ollama endpoint, and OmniRoute temporarily routing to one proven model.

A smoke-test dependency does not automatically become permanent production architecture.

## 10. AI-centric repository contract

The repository is incomplete if an AI agent must reconstruct material operating rules from conversation history.

For smoke testing, an agent must be able to determine from the repository alone:

- current system state and build priority;
- the SUT's role and boundaries;
- the exact smoke-test acceptance criteria;
- the CentCom execution process;
- the runner commands and paths;
- allowed temporary integration;
- cleanup requirements;
- PASS/FAIL vocabulary;
- evidence destination;
- stop conditions and owner-decision boundaries.

Scoped instructions live near the implementation. `tools/hx-smoke-runner/AGENTS.md` governs runner behavior; the root `AGENTS.md` governs repository-wide behavior.

An AI agent must **not** change a smoke-test authority during the same in-progress run that is using it. If the authority is defective or stale, stop, correct it in a separate committed change, and begin a new run ID.

## 11. Activation sequence

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

DeepSeek Harness is **not** a prerequisite for CentCom smoke-runner activation. Its meta-agent smoke test remains a later HX-5 workload gate in the dependency roadmap.

## 12. What this model deliberately does not become

The smoke-testing system does not create:

- a container platform;
- a second deployment plane;
- a permanent cross-service integration mesh;
- a general reverse-proxy requirement;
- new firewall/TLS/DNS/network architecture;
- production test data;
- automatic evidence commits without review;
- permission to modify unrelated SUT state;
- a replacement for component-specific acceptance criteria.

## 13. Maintenance rule

When the testing system evolves:

1. update the smallest authoritative layer that owns the change;
2. preserve stable active filenames;
3. archive the superseded current document when replaced;
4. keep detailed component logic in `/smoke-tests/`, not the roadmap or this overview;
5. update scoped AI instructions when behavior changes;
6. validate execution helpers before promoting them;
7. do not claim the new capability is live until runtime evidence proves it.

## 14. Current status

As of 2026-09-09:

- the component smoke-test catalog is defined under `/smoke-tests/`;
- the HX-5 process/procedure standard is defined;
- the HX-5 toolset/bootstrap standard and repository-owned runner helpers are defined;
- the architecture described here is approved as the operating model;
- HX-5 remains `NOT STARTED`, so CentCom smoke-runner activation is **not yet an as-built fact**.

The next runtime use of this model occurs only after the build sequence reaches and accepts the HX-5 CentCom foundation.
