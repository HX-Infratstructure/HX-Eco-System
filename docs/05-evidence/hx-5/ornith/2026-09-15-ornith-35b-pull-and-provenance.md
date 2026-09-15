# HX-5 Ornith 1.5 35B Pull and Provenance Evidence

**Date:** 2026-09-15  
**Host:** `hx-5`  
**Model:** `ornith-1.5:35b`  
**Runtime:** Ollama `0.34.0`

## Storage proof

Before the pull:

```text
/srv/ollama -> /dev/nvme0n1p3
Filesystem: ext4
Size: 797G
Available: 757G
Ollama service: active
```

Ollama is configured with:

```text
OLLAMA_MODELS=/srv/ollama/models
```

Therefore the model was stored on the dedicated `/srv/ollama` filesystem.

## Pull result

```text
pulling aaeb640f98a8: 21 GB
pulling d9ce31026d1c: 902 MB
verifying sha256 digest
writing manifest
success
```

## Ollama inventory

```text
NAME              ID              SIZE
ornith-1.5:35b    9f3b89b25219    22 GB
```

## Model metadata

```text
architecture        qwen35moe
parameters          35.5B
context length      262144
embedding length    2048
quantization        Q4_K_M
capabilities        tools, thinking, completion, vision
```

Projector metadata:

```text
architecture        clip
parameters          446.57M
embedding length    1152
dimensions          2048
```

## Immutable artifact identity

`ollama show --modelfile ornith-1.5:35b` resolved two immutable blobs:

```text
Model blob SHA-256:
aaeb640f98a892980ef54876024293cc8d6987a86523aa1b947ffa9274ef800a

Vision projector blob SHA-256:
d9ce31026d1cb1f3f8d5152e2e2a014d9d2b302b6c93a7dc07bb0a0487f52837
```

Resolved Modelfile:

```text
FROM /srv/ollama/models/blobs/sha256-aaeb640f98a892980ef54876024293cc8d6987a86523aa1b947ffa9274ef800a
FROM /srv/ollama/models/blobs/sha256-d9ce31026d1cb1f3f8d5152e2e2a014d9d2b302b6c93a7dc07bb0a0487f52837
TEMPLATE {{ .Prompt }}
```

## Provenance summary

```text
HX operational reference: ornith-1.5:35b
Ollama model ID:          9f3b89b25219
Model artifact SHA-256:   aaeb640f98a892980ef54876024293cc8d6987a86523aa1b947ffa9274ef800a
Projector SHA-256:        d9ce31026d1cb1f3f8d5152e2e2a014d9d2b302b6c93a7dc07bb0a0487f52837
Import method:            native `ollama pull ornith-1.5:35b`
Storage:                  /srv/ollama/models
Pull verification:        PASS (`verifying sha256 digest`)
```

## Gate state

- Model pull: **PASS**
- Artifact identity captured: **PASS**
- Dedicated storage placement: **PASS**
- CLI inference: **PENDING**
- HTTP/LAN inference: **PENDING**
- GPU placement: **PENDING**
- Reboot persistence: **PENDING**
