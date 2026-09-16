# HX-5 Current Runbook

**Host:** hx-5  
**Expected IP:** `192.168.50.205`  
**Role:** CentCom / Ornith / DeepSeek Harness / dev-test / fleet smoke-test runner  
**Current state:** Layer 0/1 CLOSED; Ollama/Ornith BASE PASS complete; CentCom smoke-runner activation NEXT

## Current accepted as-built state

```text
Layer 0/1 foundation                 PASS / CLOSED
Ollama 0.34.0                       PASS
OLLAMA_HOST=0.0.0.0:11434          PASS
OLLAMA_MODELS=/srv/ollama/models   PASS
ornith-1.5:35b                      PASS
CLI inference                       PASS
localhost API inference             PASS
LAN API inference                   PASS
GPU placement                       PASS — observed 17% CPU / 83% GPU
RTX 5060 + RTX 5060 Ti active       PASS
Ollama/model/storage after reboot   PASS
CentCom smoke-runner                PENDING / NEXT
DeepSeek Harness                    FUTURE SCHEDULED WORK
```

Authoritative Ornith identity captured during install:

```text
Ollama reference:      ornith-1.5:35b
Ollama model ID:       9f3b89b25219
Model architecture:    qwen35moe
Parameters:            35.5B
Quantization:          Q4_K_M
Advertised context:    262144
Validated run context: 32768
Model blob SHA-256:    aaeb640f98a892980ef54876024293cc8d6987a86523aa1b947ffa9274ef800a
Projector SHA-256:     d9ce31026d1cb1f3f8d5152e2e2a014d9d2b302b6c93a7dc07bb0a0487f52837
```

The earlier `ornith-1.5:9b` assignment is stale and must not be used for HX-5.

## Execution

Steps 1-3 are the shared base blocks. They are already complete on the current HX-5 build and must not be rerun merely for confirmation.

```bash
./01-base-admin-network-updates.sh    # COMPLETE
./02-domain-nvidia.sh                 # COMPLETE; do not rerun on HX-5 because its accepted driver is 595.99.02
./03-storage-ollama.sh                # COMPLETE
```

Implementation lives in `../common/`; version pins and the host -> IP map live in `../common/hx-base.env`.

## Sequence

1. Base/admin/network validation; apt update + upgrade; reboot. **COMPLETE**
2. Join `hx.local.arpa`; validate SSSD/domain user; establish accepted NVIDIA runtime; reboot. **COMPLETE**
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama. **COMPLETE**
4. Accept the current mixed-GPU configuration for HX-5 workload placement. **COMPLETE** — RTX 5060 8 GB + RTX 5060 Ti 16 GB.
5. Install `ornith-1.5:35b` and close model/inference BASE PASS. **COMPLETE** — CLI/API/LAN/placement/reboot all PASS.
6. Activate the CentCom smoke-test runner role before moving into HX-9 and later component builds:
   - verify the authenticated `HX-Infratstructure/HX-Eco-System` checkout on HX-5;
   - read `../../04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md`;
   - execute `04-centcom-smoke-runner-bootstrap.sh` from this runbook directory/repository checkout;
   - install only the client/runner tools defined by the current toolset standard;
   - use `HX_ECO_REPO=$HOME/src/HX-Eco-System` unless intentionally overridden;
   - use the standard `HX_SMOKE_ROOT=$HOME/hx-smoke-runs` and `HX_SMOKE_VENV=$HOME/.venvs/hx-smoke-runner` unless intentionally overridden;
   - run `hx-smoke-doctor`;
   - run `hx-smoke-doctor --remote` and require the known-good HX-2 response `HX-CENTCOM-RUNNER-PASS`;
   - record installed client versions and activation evidence in the HX-5 server record.
7. After the CentCom runner activation evidence is accepted, update `BUILD-STATE.md` and the HX-5 server record for the current closeout boundary.
8. Perform the owner-approved read-only reconciled Layer 0/1 audit of HX-2, HX-3, and HX-4 after HX-5 current closeout.
9. Install DeepSeek Harness only at its scheduled priority after the model fleet/OmniRoute foundation is available. The Harness is not a prerequisite for CentCom smoke-runner activation.
10. Validate Harness runtime/CLI or service health.
11. Execute the required Harness meta-agent capability smoke test defined in `../../../smoke-tests/deepseek-harness-smoke-test.md` and `../../00-control/HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`.
12. Prove Harness reboot persistence with a short delegated sub-agent invocation after reboot. The full solution-build test does not need to be repeated after reboot.

## CentCom smoke-runner activation rule

```text
HX-5 base/domain/GPU state accepted        PASS
              AND
Ollama + Ornith inference                  PASS
              AND
HX-5 reboot persistence                    PASS
              AND
CentCom bootstrap complete                 PENDING
              AND
hx-smoke-doctor                            PENDING
              AND
hx-smoke-doctor --remote                   PENDING
              AND
client versions recorded                   PENDING
              =
CENTCOM SMOKE-RUNNER ACTIVE
```

This activation is the current remaining HX-5 gate. It does not mark DeepSeek Harness PASS and does not alter the one-server-at-a-time build sequence.

## DeepSeek Harness closure rule

```text
Harness runtime/service health = PASS
                 AND
Harness meta-agent solution-building smoke test = PASS
```

DeepSeek Harness is later scheduled work. It is not required to establish the CentCom smoke-runner capability.

## Evidence

Current HX-5 evidence includes:

```text
docs/05-evidence/hx-5/layer0-1/2026-09-15-closure.md
docs/05-evidence/hx-5/ornith/2026-09-15-ornith-35b-pull-and-provenance.md
docs/05-evidence/hx-5/ornith/2026-09-15-ornith-35b-inference-and-gpu-placement.md
docs/05-evidence/hx-5/ornith/2026-09-15-ornith-35b-api-validation.md
```

The post-reboot persistence proof is also recorded in the HX-5 server record.
