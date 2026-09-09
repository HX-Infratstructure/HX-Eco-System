---
document: HX Eco-System DeepSeek Harness Implementation Addendum
status: evergreen_current
version: 1.0
date: 2026-09-09
parent_roadmap: docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md
applies_to: HX-5 CentCom / DeepSeek Harness
---

# HX Eco-System — DeepSeek Harness Implementation and Meta-Agent Smoke-Test Addendum

## 1. Purpose

This addendum extends the HX-5 DeepSeek Harness implementation requirement beyond simple runtime, CLI, or service health.

The Harness must prove that it can operate as the **HX meta-agent for AI agent and AI solution construction**. Worker agents created or invoked beneath the Harness are treated as **sub-agents** that perform bounded application-building tasks under Harness orchestration.

The objective is not to build the full HX Agent Factory during BASE PASS. The objective is to prove, with one small test, that the Harness can decompose a solution request, delegate work to sub-agents, receive their outputs, validate the result, and return a coherent final outcome.

## 2. Operating model

```text
Infrastructure Owner / Human
          ↓
DeepSeek Harness — META-AGENT
          ↓
  decomposes and delegates
          ↓
┌───────────────────────────────┐
│ temporary / test sub-agents   │
│                               │
│ Architect / Planner           │
│ Builder / Implementer         │
│ Reviewer / Validator          │
└───────────────────────────────┘
          ↓
 small runnable AI solution
          ↓
Harness synthesis + PASS/FAIL
```

For this smoke test:

- the Harness owns task decomposition and orchestration;
- sub-agents own bounded work packages;
- sub-agents do not become peer control-plane agents;
- the Harness collects and reconciles their outputs;
- the Harness returns the final result and evidence summary.

The temporary smoke-test sub-agent names are illustrative only. Permanent HX agent names, profiles, registries, skills, prompts, and governance are separate Agent Factory work.

## 3. Preconditions

Before running this test:

1. HX-5 base OS/domain/GPU state is accepted.
2. HX-5 Ollama and its assigned Ornith model have passed their own BASE PASS.
3. DeepSeek Harness is installed natively and its normal runtime/CLI or service entry point is healthy.
4. At least one approved HX model endpoint is available to the Harness.
5. A disposable local workspace is available for the generated test solution.

Preferred model order for the test:

1. HX-5 local approved model after HX-5 model BASE PASS;
2. an already-proven HX model such as HX-2 Qwen-X if needed for validation.

The smoke test must not require a new production database, NFS share, permanent MCP integration, permanent OmniRoute policy, or external cloud provider.

## 4. Required meta-agent smoke test

### 4.1 Test request

Give the Harness one bounded requirement similar to:

```text
Build a minimal native Python AI CLI named hx-agent-smoke.

The application must:
- accept one short text request from the command line;
- send the request to one approved HX Ollama model;
- return a structured result containing at least intent, answer, and model;
- include a short README;
- include one executable smoke test.

Use sub-agents to plan, build, and review the solution.
Return the final artifact locations and PASS/FAIL result.
```

The exact example application may change, but the replacement test must remain small and must prove the same orchestration capabilities.

### 4.2 Harness responsibilities

The Harness must:

1. interpret the solution request;
2. break it into discrete work packages;
3. delegate those packages to at least two distinct sub-agent roles, with three preferred for the initial test;
4. preserve enough shared context for downstream sub-agents to use upstream artifacts;
5. collect sub-agent results;
6. ensure the produced application is actually executed;
7. route the result through an independent review/validation step;
8. synthesize the work into one final completion report;
9. return an explicit PASS or FAIL against the acceptance criteria.

### 4.3 Suggested sub-agent roles

**Architect / Planner**
- writes `solution-spec.md`;
- defines acceptance criteria;
- identifies the approved model endpoint and simple application flow.

**Builder / Implementer**
- consumes the architect's specification;
- creates the minimal application;
- creates `README.md` and the smoke-test command/script.

**Reviewer / Validator**
- consumes the specification and built artifact;
- executes the smoke test independently;
- records whether each acceptance criterion passed;
- writes a short validation result.

The Harness remains responsible for the overall plan, delegation, sequencing, and final synthesis.

## 5. Minimum expected artifacts

A successful test should produce a small disposable workspace similar to:

```text
hx-harness-smoke/
├── solution-spec.md
├── app.py
├── README.md
├── test_smoke.py        # or equivalent executable smoke test
└── validation-result.md
```

Equivalent artifacts are acceptable if the Harness/runtime uses a different native project structure.

## 6. BASE PASS acceptance criteria

DeepSeek Harness does **not** receive its functional BASE PASS from process health alone.

The Harness smoke test passes only when all of the following are proven:

1. **Meta-agent control** — the Harness owns the top-level task and orchestration flow.
2. **Task decomposition** — the Harness breaks the requirement into multiple bounded tasks.
3. **Sub-agent delegation** — at least two distinct sub-agent roles receive separate work packages.
4. **Context/artifact handoff** — a downstream sub-agent successfully consumes an artifact or decision produced by an upstream sub-agent.
5. **Application creation** — the workflow produces a real runnable application artifact, not only prose or an agent response.
6. **AI execution** — the generated application successfully invokes one approved HX model and receives a usable result.
7. **Independent validation** — a reviewer/validator role checks the implementation against the defined acceptance criteria.
8. **Harness synthesis** — the Harness collects the sub-agent outcomes and returns one coherent final result.
9. **Evidence** — the build/delegation record, artifact paths, model/backend used, validation output, and final PASS/FAIL are captured.
10. **Reboot persistence** — after the normal Harness reboot-persistence check, the Harness can again execute a short delegated sub-agent task. The entire application-build test does not need to be repeated after reboot.

If the generated application cannot run, if the Harness cannot actually delegate work, or if the final result requires the human to manually complete the sub-agents' work, the Harness functional smoke test is **FAIL**.

## 7. Evidence to retain

Record at minimum:

- HX-5 host and timestamp;
- Harness version/revision;
- model/provider/backend used;
- top-level Harness request;
- sub-agent roles invoked;
- work package assigned to each role;
- artifact paths;
- application execution output;
- validation result;
- Harness final synthesis;
- final PASS/FAIL status.

Store durable evidence under the normal HX evidence structure and update the HX-5 server record and `BUILD-STATE.md` when the Harness gate is closed.

## 8. Explicit non-goals for this smoke test

This smoke test does **not** require:

- the full HX Agent Factory;
- permanent agent registry population;
- production application deployment;
- full fleet orchestration;
- permanent MCP client wiring;
- permanent OmniRoute routing policy;
- PostgreSQL, Redis, Qdrant, LightRAG, or Mem0 integration unless independently required by the chosen tiny test;
- NFS configuration;
- production secrets or production data.

Those capabilities are introduced through their own roadmap stages.

## 9. Closure rule

The DeepSeek Harness base implementation is considered functionally proven only when both are true:

```text
Harness runtime/service health = PASS
                 AND
Harness meta-agent solution-building smoke test = PASS
```

This addendum is part of the evergreen HX Eco-System roadmap and should evolve as the Harness implementation and Agent Factory design mature.
