# HX-5 Current Runbook

**Host:** hx-5  
**Expected IP:** `192.168.50.205`  
**Role:** CentCom / Ornith / DeepSeek Harness / dev-test / fleet smoke-test runner

## Execution

Steps 1-3 are the shared base blocks. Run them from this directory; each one
refuses to run on any host other than `hx-5`.

```bash
./01-base-admin-network-updates.sh    # reboots
./02-domain-nvidia.sh                 # reboots
./03-storage-ollama.sh
```

Implementation lives in `../common/`; version pins and the host -> IP map live
in `../common/hx-base.env`. Ollama and the NVIDIA driver are pinned to the
fleet baseline, and block 3 stops if the installed Ollama does not match the
pin. See `../README.md` before changing a pin.

## Sequence
1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install the pinned `nvidia-driver-595-server-open`; reboot.
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama; reboot/health validation.
4. Resolve/accept current GPU symmetry decision before workload placement assumptions.
5. Install Ornith model and close its model/inference BASE PASS.
6. Activate the CentCom smoke-test runner role before moving into HX-9 and later component builds:
   - verify the authenticated `HX-Infratstructure/HX-Eco-System` checkout on HX-5;
   - read `../../04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`;
   - execute `04-centcom-smoke-runner-bootstrap.sh` from this runbook directory/repository checkout;
   - install only the client/runner tools defined by the current toolset standard;
   - select and record `HX_SMOKE_ROOT`, `HX_SMOKE_VENV`, and `HX_ECO_REPO`;
   - run `hx-smoke-doctor`;
   - run `hx-smoke-doctor --remote` and require the known-good HX-2 response `HX-CENTCOM-RUNNER-PASS`;
   - keep disposable test projects, fixtures, scripts, manifests, logs, and cleanup verification on HX-5 rather than on the SUT;
   - follow `../../04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` for all later component runs.
7. Record the installed CentCom client-tool versions and remote activation evidence in the HX-5 server record. Do not mark the smoke-runner capability active from documentation alone.
8. Install DeepSeek Harness only at its scheduled priority after the model fleet/OmniRoute foundation is available. The Harness is not a prerequisite for CentCom smoke-runner activation.
9. Validate Harness runtime/CLI or service health.
10. Execute the required Harness meta-agent capability smoke test defined in `../../../smoke-tests/deepseek-harness-smoke-test.md` and `../../00-control/HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`:
   - Harness owns the top-level solution request and orchestration;
   - temporary sub-agents perform bounded planning, building, and review work;
   - sub-agents hand artifacts/context to one another;
   - the workflow produces and executes a small runnable AI application against one approved HX model;
   - an independent reviewer sub-agent validates the result;
   - Harness synthesizes the final evidence and PASS/FAIL result.
11. Prove Harness reboot persistence with a short delegated sub-agent invocation after reboot. The full solution-build test does not need to be repeated after reboot.
12. Update the HX-5 server record and `BUILD-STATE.md` only after the relevant HX-5 workload gates have passed.

## CentCom smoke-runner activation rule

```text
HX-5 base/domain/GPU state accepted
              AND
Ollama + Ornith inference PASS
              AND
HX-5 reboot persistence PASS
              AND
CentCom bootstrap complete
              AND
hx-smoke-doctor PASS
              AND
hx-smoke-doctor --remote PASS
              AND
client versions recorded
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
