# HX-5 Ornith 1.5 35B — Inference and GPU Placement Evidence

**Date:** 2026-09-15  
**Host:** `hx-5`  
**Model:** `ornith-1.5:35b`  
**Ollama model ID:** `9f3b89b25219`

## CLI inference

Command:

```bash
ollama run ornith-1.5:35b "Reply with exactly: HX-5 ORNITH PASS"
```

Observed final response:

```text
HX-5 ORNITH PASS
```

**CLI inference gate: PASS**

## Ollama placement

`ollama ps` reported:

```text
NAME              ID              SIZE     PROCESSOR          CONTEXT
ornith-1.5:35b    9f3b89b25219    23 GB    17%/83% CPU/GPU    32768
```

The installed artifact advertises a maximum context length of `262144`, while this validation run loaded with a runtime context of `32768`. These are distinct facts and are not treated as equivalent.

## GPU utilization during inference

NVIDIA runtime evidence while Ornith remained loaded:

```text
GPU 0: NVIDIA GeForce RTX 5060
VRAM: 4722 MiB / 8151 MiB
GPU utilization: 25%
Ollama llama-server VRAM: 4712 MiB

GPU 1: NVIDIA GeForce RTX 5060 Ti
VRAM: 15022 MiB / 16311 MiB
GPU utilization: 28%
Ollama llama-server VRAM: 15012 MiB
```

Both GPUs were actively used by the same Ollama `llama-server` process.

**Workload GPU-placement gate: PASS**

## Current Ornith gate state

- Model installed: PASS
- Provenance captured: PASS
- CLI inference: PASS
- Mixed-GPU placement: PASS — 83% GPU / 17% CPU
- Both physical GPUs active: PASS
- HTTP/LAN inference: PENDING
- Reboot persistence: PENDING
