# HX-5 Ornith 1.5 35B — Reboot Persistence Evidence

**Date:** 2026-09-15  
**Host:** `hx-5` / `192.168.50.205`  
**Model:** `ornith-1.5:35b`  
**Ollama model ID:** `9f3b89b25219`

## Pre-reboot state

```text
ollama.service: enabled
ollama.service: active
ornith-1.5:35b present, model ID 9f3b89b25219, reported size 22 GB
/srv/ollama mounted read-write
```

A controlled reboot was executed.

## Post-reboot state

```text
hostname: hx-5
uptime: 1 minute at validation
ollama.service: enabled
ollama.service: active
listener: *:11434
```

Storage:

```text
TARGET      SOURCE         FSTYPE OPTIONS
/srv/ollama /dev/nvme1n1p3 ext4   rw,relatime,stripe=128
/dev/nvme1n1p3 797G 22G 736G 3% /srv/ollama
```

The prior observation had `/srv/ollama` enumerated as `/dev/nvme0n1p3`. The filesystem UUID remained authoritative and the intended filesystem remounted correctly despite Linux NVMe enumeration changing across reboot.

Model persistence:

```text
NAME              ID              SIZE
ornith-1.5:35b    9f3b89b25219    22 GB
```

Known-answer inference after reboot returned:

```text
HX-5 ORNITH REBOOT PASS
```

Loaded placement after reboot:

```text
ornith-1.5:35b  9f3b89b25219  23 GB  17%/83% CPU/GPU  CONTEXT 32768
```

GPU evidence during the post-reboot run:

```text
GPU 0 — NVIDIA GeForce RTX 5060
  VRAM used approximately 4714 MiB / 8151 MiB
  llama-server approximately 4704 MiB

GPU 1 — NVIDIA GeForce RTX 5060 Ti
  VRAM used approximately 15016 MiB / 16311 MiB
  llama-server approximately 15006 MiB
```

## Verdict

```text
Ollama autostart                     PASS
Ollama listener persistence          PASS
/srv/ollama mount persistence        PASS
Ornith model persistence             PASS
Ornith model identity persistence    PASS
Post-reboot inference                PASS
Mixed-GPU placement after reboot     PASS
```

**ORNITH 35B REBOOT PERSISTENCE: PASS**
