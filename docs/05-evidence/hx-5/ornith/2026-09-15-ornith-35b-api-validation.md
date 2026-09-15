# HX-5 Ornith 35B API Validation

**Host:** `hx-5`
**IP:** `192.168.50.205`
**Date:** 2026-09-15
**Model:** `ornith-1.5:35b`
**Ollama model ID:** `9f3b89b25219`

## Local HTTP API

Endpoint:

```text
http://127.0.0.1:11434/api/generate
```

Prompt requested the exact marker:

```text
HX-5 ORNITH API PASS
```

The generated response ended with the required marker and returned `done: true` / `done_reason: stop`.

**Result: PASS**

## LAN HTTP API

Endpoint:

```text
http://192.168.50.205:11434/api/generate
```

Prompt requested the exact marker:

```text
HX-5 ORNITH LAN PASS
```

The generated response ended with the required marker and returned `done: true` / `done_reason: stop`.

**Result: PASS**

## Post-API Placement

`ollama ps` after both API calls:

```text
NAME              ID              SIZE     PROCESSOR          CONTEXT
ornith-1.5:35b    9f3b89b25219    23 GB    17%/83% CPU/GPU    32768
```

Placement remained stable after local and LAN inference.

**GPU placement validation: PASS — 83% GPU / 17% CPU**

## Gate State

- Ornith model installation: PASS
- Provenance capture: PASS
- CLI inference: PASS
- Local HTTP API inference: PASS
- LAN HTTP API inference: PASS
- Mixed-GPU workload placement: PASS
- Reboot persistence: PENDING

The only remaining Ornith workload closure gate is reboot persistence.
