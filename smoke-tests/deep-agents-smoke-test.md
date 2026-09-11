# Deep Agents Smoke Test

## 1. Title & Purpose

Deep Agents by LangChain on HX-12 is the HX line-of-business (LOB) agent factory / application-agent harness. This smoke test validates that Deep Agents can use an approved tool-calling HX model to create and run a small disposable LOB agent package with real sub-agent delegation, file/tool use, deterministic business-rule handling, short-lived thread continuity, and independent validation.

**Scope:** Deep Agents LOB agent creation and runtime function only. Production LOB deployment, long-term memory, RAG, MCP wiring, and the full HX Agent Factory are outside this test.

## 2. Prerequisites

- HX-12 base OS/domain state is accepted.
- Deep Agents is installed natively in a pinned Python environment.
- The accepted Deep Agents version is recorded before execution.
- One owner-approved HX model endpoint is configured through a compatible LangChain model adapter.
- The selected model supports reliable tool calling.
- Before the full smoke test, prove the selected model can:
  - invoke at least one Deep Agents filesystem operation;
  - invoke the built-in `task` sub-agent delegation capability.
- A disposable workspace is available.
- Use the stable isolated sub-agent pattern for the initial BASE PASS unless the accepted upstream release changes that recommendation.
- A disposable in-memory or equivalent non-production LangGraph checkpointer is available for the thread-continuity step.
- No production PostgreSQL, Redis, Qdrant, LightRAG, Mem0, NFS, cloud model, permanent OmniRoute route, or container is required.

If the model cannot reliably call the required tools, stop and record:

```text
MODEL/HARNESS COMPATIBILITY NOT ESTABLISHED
```

A normal chat response is not sufficient.

## 3. Test Steps

1. Create or select a disposable workspace named approximately:

```text
hx-lob-agent-smoke/
```

2. Create the following local synthetic rules file as `business-rules.md`:

```text
category=outage + severity=critical -> queue=Operations, priority=P1
category=billing -> queue=Finance
category=access -> queue=Identity
```

3. Give the Deep Agents builder the following bounded request:

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

4. Confirm the builder uses filesystem capabilities to materialize a real project similar to:

```text
hx-lob-agent-smoke/
├── README.md
├── business-rules.md
├── agent.py
├── test_smoke.py
└── validation-result.md
```

Equivalent native project structures are acceptable.

5. Confirm the generated supervisor defines at least two distinct domain sub-agent roles; three are preferred:

```text
Intake / Classifier
Business Rule Agent
Reviewer / Validator
```

6. Submit the synthetic service case from Section 4.

7. Confirm the supervisor actually delegates work using the Deep Agents sub-agent mechanism and that downstream work consumes upstream classification/context.

8. Confirm the business-rule artifact is consulted and the final structured result contains the deterministic routing decision:

```text
queue=Operations
priority=P1
validation_status=PASS
```

9. Run the generated `test_smoke.py` or equivalent deterministic acceptance test.

10. Prove short-lived thread continuity using a disposable checkpointer. Reuse the same thread id and send:

```text
Add note: 50 users are affected. Keep the same case_id and reassess the recommendation.
```

11. Confirm the follow-up retains `case_id=HX-SMOKE-001` and remains consistent with the synthetic business rules.

12. Confirm the reviewer/validator independently checks the final outcome and writes an explicit PASS/FAIL result.

13. During the normal HX-12 reboot-persistence check, run one short LOB case again. The full builder stage does not need to be repeated after reboot.

14. Record the Deep Agents version, Python environment, model/endpoint/adapter, tool-call probe, generated artifacts, delegated roles, case output, thread-continuity output, reviewer result, and reboot retest with the normal HX evidence.

## 4. Sample Data

Synthetic case:

```json
{
  "case_id": "HX-SMOKE-001",
  "category": "outage",
  "severity": "critical",
  "summary": "Synthetic line-of-business service interruption",
  "requested_action": "route"
}
```

Synthetic business rules:

```text
category=outage + severity=critical -> queue=Operations, priority=P1
category=billing -> queue=Finance
category=access -> queue=Identity
```

Same-thread follow-up:

```text
Add note: 50 users are affected. Keep the same case_id and reassess the recommendation.
```

## 5. Expected Output

A passing first-case result contains at minimum:

```json
{
  "case_id": "HX-SMOKE-001",
  "queue": "Operations",
  "priority": "P1",
  "rationale": "...",
  "validation_status": "PASS"
}
```

Pass also requires:

- the selected HX model proves filesystem and `task` tool calling;
- a real runnable Deep Agents project is created;
- at least two distinct domain sub-agents are configured and actually delegated work;
- downstream work consumes upstream context;
- the supplied rules are used;
- the known-answer routing result is correct;
- the reviewer independently validates the result;
- the same-thread follow-up retains the case identity and relevant prior context;
- one short LOB case remains executable after the normal reboot check.

The final test status should be explicit, for example:

```text
DEEP_AGENTS_SMOKE_PASS
```

If the model cannot use required tools, delegation never occurs, the business result is wrong, the generated package cannot run, thread continuity fails, or the human must manually complete the agent-building work, the smoke test is **FAIL**.

## 6. Cleanup / Teardown

After evidence capture:

1. remove only the disposable `hx-lob-agent-smoke` project/workspace;
2. discard the in-memory/disposable smoke-test checkpoint state;
3. remove any temporary validation-only model/tool configuration created solely for this test;
4. retain the pinned Deep Agents environment and accepted HX-12 application configuration;
5. do not modify production databases, RAG stores, long-term memory, unrelated agent projects, or model services.

No containers are created by this test.

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the first-case JSON result and the sub-agent delegation trace.

Record the Deep Agents version, the HX model used, the project created, the
sub-agents configured and what each was delegated, the `HX-SMOKE-001`
routing result with its reviewer validation, the same-thread follow-up, and
confirmation that one short LOB case still ran after the reboot check.
