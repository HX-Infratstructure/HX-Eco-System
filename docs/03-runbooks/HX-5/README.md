# HX-5 Current Runbook

**Host:** hx-5  
**Expected IP:** `192.168.50.205`  
**Role:** CentCom / Ornith / DeepSeek Harness / dev-test / fleet smoke-test runner

## Sequence
1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install `nvidia-driver-595-server-open`; reboot.
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama; reboot/health validation.
4. Resolve/accept current GPU symmetry decision before workload placement assumptions.
5. Install Ornith model and close its model/inference BASE PASS.
6. Activate the CentCom smoke-test runner role before moving into HX-9 and later component builds:
   - install only the client/runner tools actually required by the current smoke-test catalog;
   - select and record `HX_SMOKE_ROOT` on HX-5;
   - prove one remote smoke-runner invocation against an already-proven HX endpoint;
   - keep disposable test projects, fixtures, scripts, manifests, logs, and cleanup verification on HX-5 rather than on the SUT;
   - follow `../../04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`.
7. Install DeepSeek Harness only at its scheduled priority after the model fleet/OmniRoute foundation is available. The Harness is not a prerequisite for CentCom smoke-runner activation.
8. Validate Harness runtime/CLI or service health.
9. Execute the required Harness meta-agent capability smoke test defined in `../../../smoke-tests/deepseek-harness-smoke-test.md` and `../../00-control/HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`:
   - Harness owns the top-level solution request and orchestration;
   - temporary sub-agents perform bounded planning, building, and review work;
   - sub-agents hand artifacts/context to one another;
   - the workflow produces and executes a small runnable AI application against one approved HX model;
   - an independent reviewer sub-agent validates the result;
   - Harness synthesizes the final evidence and PASS/FAIL result.
10. Prove Harness reboot persistence with a short delegated sub-agent invocation after reboot. The full solution-build test does not need to be repeated after reboot.
11. Update the HX-5 server record and `BUILD-STATE.md` only after the relevant HX-5 workload gates have passed.

## CentCom smoke-runner activation rule

```text
HX-5 base/domain/GPU state accepted
              AND
Ollama + Ornith inference PASS
              AND
HX-5 reboot persistence PASS
              AND
smoke-runner client toolset present
              AND
HX_SMOKE_ROOT ready
              AND
one remote known-good validation PASS
              =
CENTCOM SMOKE-RUNNER ACTIVE
```

This activation is an HX-5 capability gate. It does not mark DeepSeek Harness PASS and does not alter the one-server-at-a-time build sequence.

## DeepSeek Harness closure rule

```text
Harness runtime/service health = PASS
                 AND
Harness meta-agent solution-building smoke test = PASS
```

The Harness does not close BASE PASS from process health alone.

Do not mount/wipe unrelated disks. Keep HX-5 headroom for CentCom/Harness/dev-test rather than moving shared embedding infrastructure here. Do not turn HX-5 into a second deployment/control plane; its smoke-test role is remote execution, evidence capture, and cleanup verification.
