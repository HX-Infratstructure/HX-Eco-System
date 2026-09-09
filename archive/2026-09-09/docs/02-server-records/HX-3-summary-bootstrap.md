# HX-3 — Coder-X Server Configuration

**Role:** Coder-X / Ollama inference server  
**State:** PASS / CLOSED  
**IP:** `192.168.50.203/24`

## Base
- Ubuntu 24.04.5 LTS
- Kernel 7.0.0-31-generic
- Gigabyte X99-UD5 WIFI-CF
- Domain: `hx.local.arpa`
- SSSD/realmd/adcli: PASS
- SSH port 22: active
- UFW inactive/disabled

## GPU
- NVIDIA driver 595.71.05
- CUDA reported: 13.2
- 2 x GeForce RTX 5060 Ti 16 GB
- Aggregate VRAM: approximately 32 GB
- Blackwell compute capability 12.0

## Storage
- WD_BLACK SN7100 4 TB NVMe
- Root: 120 GB ext4
- Dedicated `/srv/ollama`: approximately 3.5 TB ext4
- Separate SATA disk remains unmounted/untouched

## Ollama
- Version 0.33.3
- API: `http://192.168.50.203:11434`
- Models: `/srv/ollama/models`
- Current temporary local-only setting: `OLLAMA_NO_CLOUD=1`

## Model
- Alias: `coder-x:qwen3-coder-30b-q6_k`
- Qwen3-Coder-30B-A3B-Instruct Q6_K
- Model ID: `efcb36ee7419`
- Source GGUF SHA-256: `72a9b20a19c70db56e1ccd01fb35b0f0842d67d28e7c3bdff762df860120b769`

## Validation
- CLI inference: PASS
- HTTP/LAN API: PASS
- Reboot persistence: PASS

## Informational observation
HX-3 boot time is noticeably longer than other HX servers. Owner direction: record only. Do not diagnose or remediate unless explicitly asked.
