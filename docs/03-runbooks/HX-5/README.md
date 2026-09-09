# HX-5 Current Runbook

**Host:** hx-5  
**Expected IP:** `192.168.50.205`  
**Role:** CentCom / Ornith / DeepSeek Harness / dev-test

## Sequence
1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install `nvidia-driver-595-server-open`; reboot.
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama; reboot/health validation.
4. Resolve/accept current GPU symmetry decision before workload placement assumptions.
5. Install Ornith model and close its model/inference BASE PASS.
6. Install DeepSeek Harness only at its scheduled priority after the model fleet/OmniRoute foundation is available.
7. Validate Harness runtime/CLI or service health.
8. Execute the required Harness meta-agent capability smoke test defined in `../../00-control/HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`:
   - Harness owns the top-level solution request and orchestration;
   - temporary sub-agents perform bounded planning, building, and review work;
   - sub-agents hand artifacts/context to one another;
   - the workflow produces and executes a small runnable AI application against one approved HX model;
   - an independent reviewer sub-agent validates the result;
   - Harness synthesizes the final evidence and PASS/FAIL result.
9. Prove Harness reboot persistence with a short delegated sub-agent invocation after reboot. The full solution-build test does not need to be repeated after reboot.
10. Update the HX-5 server record and `BUILD-STATE.md` only after both Harness runtime health and the meta-agent solution-building smoke test have passed.

## DeepSeek Harness closure rule

```text
Harness runtime/service health = PASS
                 AND
Harness meta-agent solution-building smoke test = PASS
```

The Harness does not close BASE PASS from process health alone.

Do not mount/wipe unrelated disks. Keep HX-5 headroom for CentCom/Harness/dev-test rather than moving shared embedding infrastructure here.
