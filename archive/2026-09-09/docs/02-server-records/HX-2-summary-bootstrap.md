# HX-2 — Qwen-X Server Configuration

**Role:** Qwen-X / Ollama inference server  
**State:** PASS / CLOSED  
**IP:** `192.168.50.202/24`

## Base
- Ubuntu 24.04.4 LTS
- Kernel 7.0.0-31
- Domain: `hx.local.arpa`
- SSSD/realmd/adcli: PASS
- SSH port 22: active
- UFW inactive/disabled

## GPU
- NVIDIA driver 595.71.05
- CUDA reported: 13.2
- 2 x GeForce RTX 4070 Ti SUPER 16 GB
- Aggregate VRAM: 32 GB

## Storage
- WD_BLACK SN850X 4 TB NVMe
- Root: 120 GB ext4
- Dedicated `/srv/ollama`: approximately 3.5 TB ext4
- Separate 8 TB SATA disk remains unmounted/untouched

## Ollama
- Version 0.33.3
- API: `http://192.168.50.202:11434`
- Models: `/srv/ollama/models`
- Current temporary local-only setting: `OLLAMA_NO_CLOUD=1`

## Model
- Alias: `qwen-x:qwen3.8-27b-q6_k`
- Qwen3.8 27B Q6_K
- Model ID: `d319d311ac30`
- Source GGUF SHA-256: `7d590099e0a0fe7b8df812045faa2ae12bf4dbf3492b8eb7c7ab24c94d36ed`

## Validation
- CLI inference: PASS
- HTTP API inference: PASS
- LAN API: PASS
- Reboot persistence: PASS
