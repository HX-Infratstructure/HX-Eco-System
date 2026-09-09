---
document: HX Eco-System Deep Agents Implementation Addendum
status: evergreen_current
version: 1.0
date: 2026-09-09
parent_roadmap: docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md
applies_to: HX-12 Deep Agents by LangChain
upstream_reference: langchain-ai/deepagents
---

# HX Eco-System — Deep Agents Implementation and LOB Agent Factory Smoke-Test Addendum

## 1. Purpose

This addendum defines the BASE PASS boundary for **Deep Agents by LangChain on HX-12**.

Deep Agents is not installed merely so the Python package imports or a single agent returns text. HX-12 is intended to provide the **line-of-business (LOB) agent harness** used to create and run domain agents that power business applications.

The BASE PASS test must therefore prove that Deep Agents can take a bounded LOB requirement, create a small agent implementation, delegate domain work to sub-agents, use files/tools, execute the resulting agent flow against an approved HX model, preserve short-lived thread context, independently validate the result, and return a coherent PASS/FAIL outcome.

The test remains intentionally small. It does not build a production LOB application or the full future HX Agent Factory.

## 2. Role boundary — DeepSeek Harness vs. Deep Agents

The two harnesses have different responsibilities in the HX Eco-System.

```text
HX-5 DeepSeek Harness
META-AGENT / solution-building orchestrator
    |
    |  designs/builds broader AI solutions and agentic work
    v
HX-12 Deep Agents
LOB AGENT FACTORY / application-agent harness
    |
    |  creates and runs domain agents used by line-of-business applications
    v
LOB application agents
```

### HX-5 DeepSeek Harness

- remains the HX meta-agent / solution-building orchestration layer;
- decomposes broader AI-solution work and coordinates sub-agents;
- is validated by its own meta-agent solution-building smoke test.

### HX-12 Deep Agents

- is the application-agent harness for LOB use cases;
- creates/configures domain-specific Deep Agents and their sub-agents;
- provides the agent runtime pattern that LOB applications can call or embed;
- is validated by creating and running a small LOB agent package.

Deep Agents is not a replacement control plane for DeepSeek Harness, and DeepSeek Harness is not the runtime definition for every LOB application agent.

## 3. Current upstream facts that shape the test

As of 2026-09-09, the current stable Python release reviewed for this plan is **`deepagents==0.7.13`**, published 2026-09-02.

The implementation team must re-check the current stable release at installation time and pin the exact accepted version in the HX-12 server record. A newer release may be selected after verifying that its public API and sub-agent behavior remain compatible with this test.

Current Deep Agents architecture provides the following relevant harness capabilities:

- `create_deep_agent()` as the primary construction API;
- sub-agent delegation through the built-in `task` capability;
- built-in filesystem operations for reading, writing, editing, globbing, and searching files;
- planning/context-management behavior for long-running multi-step work;
- optional shell execution when the selected backend supports it;
- skills and persistent memory as optional extensions;
- custom tools and MCP-compatible tool surfaces;
- LangGraph-based state, checkpointing, streaming, and persistence patterns;
- model-agnostic operation with any compatible LangChain chat model that supports tool calling, including appropriately configured local/self-hosted models.

Current sub-agent behavior uses **`isolated`** as the normal/default mode. The `fork` mode is experimental. The BASE PASS test should use the stable isolated sub-agent pattern unless a later accepted version changes this recommendation.

## 4. Critical model-compatibility gate

Deep Agents depends on reliable **tool calling**. A model that can answer prompts but cannot call the harness tools reliably is not sufficient for this workload.

Before the full LOB smoke test:

1. configure one owner-approved HX model endpoint explicitly;
2. prove the model can invoke at least one Deep Agents filesystem operation;
3. prove the model can invoke the `task` sub-agent delegation capability;
4. record the exact model, endpoint, LangChain model adapter, and result.

Preferred approach:

- use an already-approved HX local model that has passed its own inference BASE PASS;
- use a direct known-good endpoint for validation unless a permanent OmniRoute path has already been approved;
- do not make an external cloud provider a requirement for the Deep Agents BASE PASS.

If the selected local model cannot perform the required tool calls, classify that result as **MODEL/HARNESS COMPATIBILITY NOT ESTABLISHED**. Do not mark Deep Agents PASS merely because ordinary chat completion succeeds.

## 5. Required LOB Agent Factory smoke test

### 5.1 Test objective

Use Deep Agents on HX-12 to create and run a disposable LOB agent package named approximately:

```text
hx-lob-agent-smoke
```

The exact name may change, but the replacement test must prove the same capabilities.

### 5.2 Synthetic business scenario

Use a simple **service-case routing** scenario with no production data.

Example input:

```json
{
  "case_id": "HX-SMOKE-001",
  "category": "outage",
  "severity": "critical",
  "summary": "Synthetic line-of-business service interruption",
  "requested_action": "route"
}
```

Provide a local `business-rules.md` with deterministic synthetic rules such as:

```text
category=outage + severity=critical -> queue=Operations, priority=P1
category=billing -> queue=Finance
category=access -> queue=Identity
```

No real customer, employee, financial, or operational data is required.

## 6. Builder-stage requirement

The HX-12 Deep Agent receives a bounded instruction similar to:

```text
Create a minimal Deep Agents line-of-business agent package named hx-lob-agent-smoke.

The generated application must:
- accept one synthetic service-case request;
- use a Deep Agent supervisor;
- define specialized sub-agents for intake/classification, business-rule analysis, and review/validation;
- use the local business-rules.md file;
- return a structured routing decision containing case_id, queue, priority, rationale, and validation_status;
- include a README and executable smoke test;
- run against one approved HX model with verified tool-calling support;
- use only synthetic data.

Create the files, report the artifact locations, and return PASS/FAIL against the requested acceptance criteria.
```

The builder-stage Deep Agent should use its filesystem capabilities to materialize the package rather than returning only prose or code blocks in chat.

## 7. Generated LOB agent structure

A successful builder stage should create a small workspace similar to:

```text
hx-lob-agent-smoke/
├── README.md
├── business-rules.md
├── agent.py
├── test_smoke.py
└── validation-result.md
```

Equivalent native project structures are acceptable.

The generated `agent.py` must configure a Deep Agent supervisor and at least two distinct sub-agent roles; three are preferred for the initial proof.

### Suggested sub-agents

**Intake / Classifier Agent**
- validates the synthetic request;
- classifies category/severity;
- returns a concise structured finding.

**Business Rule Agent**
- receives the classified case;
- reads or is provided the relevant business-rule artifact;
- recommends queue and priority.

**Reviewer / Validator Agent**
- independently checks the proposed decision against the synthetic rule set;
- returns explicit PASS/FAIL plus any discrepancy.

Use the stable isolated sub-agent pattern for the initial test. Do not make experimental fork semantics a prerequisite for BASE PASS.

## 8. Runtime smoke-test sequence

After the package is created:

1. instantiate the generated LOB Deep Agent using the pinned Deep Agents environment;
2. submit the synthetic service case;
3. confirm the supervisor delegates work through the Deep Agents sub-agent mechanism;
4. confirm downstream work consumes upstream classification/context;
5. confirm the business-rule artifact is actually consulted;
6. confirm the final result is structured and contains the expected deterministic routing decision;
7. run the independent validation step;
8. run `test_smoke.py` or equivalent deterministic acceptance test;
9. record the final artifact paths and PASS/FAIL result.

For the example critical outage case, the expected business result is:

```text
queue=Operations
priority=P1
validation_status=PASS
```

## 9. Short-lived thread/state continuity proof

Because Deep Agents is intended to power application agents, BASE PASS should also prove basic thread continuity without introducing a production database.

Using an in-memory or otherwise disposable LangGraph checkpointer for the smoke test:

1. run the initial case under a known thread identifier;
2. send one follow-up message under the same thread, for example:

```text
Add note: 50 users are affected. Keep the same case_id and reassess the recommendation.
```

3. confirm the agent retains the case identity and relevant prior context;
4. confirm the result remains consistent with the synthetic business rules.

This proves the application-facing state pattern only. Production persistence, PostgreSQL schemas, Mem0 wiring, and long-term memory remain integration work.

## 10. BASE PASS acceptance criteria

Deep Agents on HX-12 receives functional BASE PASS only when all of the following are established:

1. **Pinned native environment** — the accepted Deep Agents version and dependencies are recorded.
2. **Model tool-calling compatibility** — the selected HX model successfully invokes required Deep Agents tools.
3. **Harness construction** — `create_deep_agent()` or the accepted equivalent initializes successfully with an explicit model.
4. **Planning/decomposition** — the builder breaks the LOB build request into multiple concrete tasks.
5. **Filesystem use** — the builder creates or edits real project artifacts in the disposable workspace.
6. **LOB agent creation** — the workflow produces a real runnable Deep Agents application package, not just prose.
7. **Sub-agent configuration** — at least two distinct domain sub-agent roles are configured; three are preferred.
8. **Sub-agent delegation** — the LOB supervisor actually delegates work using the Deep Agents sub-agent mechanism.
9. **Context handoff** — downstream work successfully consumes upstream classification or decisions.
10. **Business-rule/tool use** — the generated LOB flow uses the supplied synthetic business-rule artifact or equivalent test tool.
11. **Correct business result** — the known-answer synthetic case returns the expected queue/priority result.
12. **Independent validation** — a reviewer role or deterministic validator checks the final outcome against the rule set.
13. **Thread continuity** — a same-thread follow-up preserves the case identity and relevant context using a disposable checkpointer.
14. **Harness synthesis** — the supervisor returns one coherent final result rather than exposing disconnected sub-agent fragments.
15. **Evidence capture** — version, model/backend, tool probe, delegated roles, artifacts, test output, and final PASS/FAIL are recorded.
16. **Reboot persistence** — after HX-12 reboot, the pinned environment and generated smoke package remain usable and one short LOB case can be executed again. The full build stage does not need to be repeated after reboot.

If the package cannot run, sub-agent delegation never occurs, the model cannot call required tools, the deterministic business result is wrong, or the human must manually complete the agent-building work, the functional smoke test is **FAIL**.

## 11. Evidence to retain

Record at minimum:

- HX-12 host and timestamp;
- Deep Agents version/revision;
- Python/environment details;
- selected model, endpoint, and LangChain model adapter;
- model tool-calling probe output;
- top-level builder request;
- generated artifact paths;
- configured sub-agent names/roles;
- delegation evidence;
- synthetic business rules;
- first case input/output;
- same-thread follow-up input/output;
- deterministic test output;
- reviewer/validator result;
- reboot retest result;
- final PASS/FAIL status.

Store durable evidence under the normal HX evidence structure and update the HX-12 server record and `BUILD-STATE.md` when the Deep Agents gate is closed.

## 12. Explicit non-goals for BASE PASS

The Deep Agents smoke test does **not** require:

- production LOB data;
- a production UI;
- production API deployment;
- the full HX Agent Factory;
- permanent MCP client wiring;
- permanent OmniRoute routing policy;
- PostgreSQL or Redis persistence;
- Qdrant/LightRAG retrieval;
- Mem0 long-term memory;
- NFS mounts;
- production secrets;
- external cloud models;
- experimental sub-agent fork mode;
- containerized execution.

Those capabilities are introduced only when their own roadmap stage or integration program requires them.

## 13. Closure rule

Deep Agents BASE PASS requires all three gates:

```text
Deep Agents environment/runtime health = PASS
                    AND
approved-model tool-calling compatibility = PASS
                    AND
LOB agent creation + execution smoke test = PASS
```

A successful package import or one plain model response is not sufficient.

This addendum is part of the evergreen HX Eco-System roadmap and should evolve as the Deep Agents upstream implementation and the HX LOB agent architecture mature.
