# HX-12 Current Runbook

**Host:** hx-12  
**Expected IP:** `192.168.50.212`  
**Role:** Deep Agents by LangChain — LOB agent factory/runtime harness

## Sequence

1. Validate the HX-12 base OS, hostname/IP/DNS/gateway, domain membership, SSSD, updates, and failed-unit state using the standard clean-build pattern.
2. Install the native Python/runtime prerequisites required by the accepted Deep Agents release. No Docker, Podman, or Kubernetes.
3. Re-check the current stable `langchain-ai/deepagents` release at implementation time and pin the exact accepted version in the HX-12 server record. Planning reference as of 2026-09-09: `deepagents==0.7.13`.
4. Create the native Deep Agents Python environment and verify the package
   imports and the `create_deep_agent()` initialisation path:
   `../common/10-deep-agents.sh hx-12`
   The version is pinned in `../common/hx-base.env` and audited by
   `tools/hx-doc/hx-version-pins`.
5. Configure one explicit owner-approved HX model endpoint.
6. Run the required model/harness compatibility probe before the full smoke test:
   - prove at least one Deep Agents filesystem tool call;
   - prove `task` sub-agent delegation;
   - record the model, endpoint, LangChain adapter, and result.
7. If the selected model cannot call required tools reliably, stop and record `MODEL/HARNESS COMPATIBILITY NOT ESTABLISHED`; do not close Deep Agents BASE PASS from ordinary chat completion alone.
8. Execute the LOB Agent Factory smoke test defined in `../../00-control/HX-ECO-SYSTEM-DEEP-AGENTS-IMPLEMENTATION-ADDENDUM.md`:
   - Deep Agents builder receives the bounded synthetic LOB requirement;
   - it materializes a real disposable agent package using filesystem capabilities;
   - the generated LOB supervisor defines at least two distinct domain sub-agents, with three preferred;
   - the supervisor delegates classification, rule analysis, and validation work;
   - the generated application processes the known-answer synthetic case;
   - the business-rule artifact is consulted;
   - deterministic validation returns the expected queue/priority result;
   - a same-thread follow-up proves short-lived context continuity using a disposable checkpointer.
9. Capture the generated package, tool/delegation evidence, test outputs, model/backend details, and final PASS/FAIL result under the normal HX evidence structure.
10. Reboot HX-12 and prove that the pinned Deep Agents environment and generated smoke package remain usable by running one short LOB case again. The full builder stage does not need to be repeated after reboot.
11. Update the HX-12 server record and `BUILD-STATE.md` only after all Deep Agents closure gates pass.

## Deep Agents closure rule

```text
Deep Agents environment/runtime health = PASS
                    AND
approved-model tool-calling compatibility = PASS
                    AND
LOB agent creation + execution smoke test = PASS
```

A successful import, process start, or plain LLM response is not sufficient.

## Role boundary

HX-12 Deep Agents is the **LOB agent factory/application-agent harness**. HX-5 DeepSeek Harness remains the broader HX meta-agent/AI-solution orchestration layer. Do not create a second competing control plane on HX-12.

## Test boundaries

- Use synthetic data only.
- Use a disposable local workspace.
- Use stable isolated sub-agents for the initial BASE PASS; experimental fork mode is not required.
- Shell execution is optional and depends on the chosen backend; it is not a required BASE PASS feature.
- Production persistence, MCP wiring, OmniRoute permanent routing, Mem0, RAG, NFS, and LOB application deployment remain later work.
- Do not mount, wipe, or repurpose unrelated disks.
