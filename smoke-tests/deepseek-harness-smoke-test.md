# DeepSeek Harness Smoke Test

## 1. Title & Purpose

DeepSeek Harness on HX-5 is the HX meta-agent / AI-solution-building orchestrator. This smoke test validates that the Harness can decompose one bounded solution request, delegate work to sub-agents, produce a runnable AI artifact, validate it independently, and synthesize a final PASS/FAIL result.

**Scope:** Harness orchestration and solution-building function only. This is not the full HX Agent Factory or fleet orchestration test.

## 2. Prerequisites

- HX-5 base OS/domain state is accepted.
- HX-5 Ollama and its assigned model have already passed their own BASE PASS.
- DeepSeek Harness is installed natively and its normal CLI/service entry point is healthy.
- At least one owner-approved HX model endpoint is available to the Harness.
- A disposable test workspace is available.
- Python 3 is available for the tiny generated application.
- The Harness can create/invoke at least two distinct sub-agent roles; three are preferred for the initial proof.
- No production database, NFS share, permanent MCP wiring, permanent OmniRoute route, cloud model, production secret, or container is required.

## 3. Test Steps

1. Create or select a disposable workspace named approximately:

```text
hx-harness-smoke/
```

2. Give DeepSeek Harness the following bounded request:

```text
Build a minimal native Python AI CLI named hx-agent-smoke.

The application must:
- accept one short text request from the command line;
- send the request to one approved HX Ollama model;
- return a structured result containing intent, answer, and model;
- include a short README;
- include one executable smoke test.

Use sub-agents to plan, build, and review the solution.
The planning output must be consumed by the builder.
The reviewer must execute the built application independently.
Return the final artifact locations and PASS/FAIL result.
```

3. Confirm the Harness decomposes the request and delegates separate work packages to at least two roles. Preferred initial roles:

```text
Architect / Planner
Builder / Implementer
Reviewer / Validator
```

4. Confirm the planning artifact is handed to the builder rather than recreated manually by the human.

5. Confirm the Harness produces a real disposable project similar to:

```text
hx-harness-smoke/
├── solution-spec.md
├── app.py
├── README.md
├── test_smoke.py
└── validation-result.md
```

Equivalent native project structures are acceptable.

6. The generated application's smoke test must submit the following known-answer request through the approved HX model:

```text
Reply exactly: HX-HARNESS-APP-PASS
```

7. Execute the generated application and its smoke test. The returned structured result must include:

```json
{
  "intent": "...",
  "answer": "HX-HARNESS-APP-PASS",
  "model": "<actual-approved-model>"
}
```

The exact `intent` value may vary, but `answer` must contain the exact token and `model` must identify the model actually used.

8. Confirm the reviewer/validator independently checks the produced application against the requested acceptance criteria and writes the validation result.

9. Confirm DeepSeek Harness collects the sub-agent outputs and returns one coherent final PASS/FAIL result with artifact locations.

10. During the normal HX-5 reboot-persistence check, run one short delegated sub-agent task again. The entire application-build test does not need to be repeated after reboot.

11. Record the Harness version/revision, model/backend, top-level request, sub-agent roles, artifact paths, application output, reviewer result, and final Harness synthesis with the normal HX evidence.

## 4. Sample Data

Top-level build request: the full prompt in Step 2.

Generated application known-answer request:

```text
Reply exactly: HX-HARNESS-APP-PASS
```

Expected known-answer token:

```text
HX-HARNESS-APP-PASS
```

## 5. Expected Output

A passing run proves all of the following:

- DeepSeek Harness owns the top-level task;
- the task is decomposed into multiple bounded work packages;
- at least two distinct sub-agent roles actually receive delegated work;
- a downstream role consumes an upstream artifact or decision;
- the workflow creates a real runnable application, not only prose;
- the application successfully invokes an approved HX model;
- the known-answer token `HX-HARNESS-APP-PASS` is returned;
- an independent reviewer/validator checks the application;
- the Harness synthesizes one final result and artifact list;
- a short delegated task still works after the normal reboot check.

The Harness should report an explicit final status similar to:

```text
DEEPSEEK_HARNESS_SMOKE_PASS
```

If delegation never occurs, the application cannot run, the reviewer does not independently validate it, or the human must manually complete sub-agent work, the smoke test is **FAIL**.

## 6. Cleanup / Teardown

After evidence capture:

1. remove only the disposable `hx-harness-smoke` project/workspace;
2. remove any temporary validation-only Harness configuration created solely for this test;
3. retain the installed Harness, accepted model configuration, and normal HX-5 service configuration;
4. do not delete or modify unrelated agent projects, models, credentials, or server data.

No containers are created by this test.

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the work-package breakdown, the delegation trace and the reviewer verdict.

Record the Harness version, the HX model invoked by the application, the
work packages and the roles that received them, the upstream artifact a
downstream role consumed, the known-answer token `HX-HARNESS-APP-PASS`, and
confirmation that the disposable `hx-harness-smoke` workspace and any
validation-only configuration were removed while the installed Harness
stayed in place.
