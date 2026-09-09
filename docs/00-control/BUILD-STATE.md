# HX-Eco-System Build State

**Date:** 2026-09-09  
**Owner:** Jarvis Richardson  
**Method:** KISS / one server at a time

| Server | Role | State | Current Gate | Notes |
|---|---|---|---|---|
| HX-1 | Samba AD/DNS/Kerberos/NTP | PASS | CLOSED | Clean base retained |
| HX-2 | Qwen-X / Ollama | PASS | CLOSED | Qwen3.8-27B Q6_K; Ollama 0.33.3; LAN API; cloud currently disabled |
| HX-3 | Coder-X / Ollama | PASS | CLOSED | Qwen3-Coder-30B-A3B-Instruct Q6_K; dual RTX 5060 Ti; longer boot time recorded only, no action |
| HX-4 | Meta-X / GPT-OSS + embedding/rerank | NOT STARTED | NEXT | Clean rebuild |
| HX-5 | CentCom / Ornith / DeepSeek Harness / dev-test | NOT STARTED | — | Clean rebuild; GPU symmetry decision pending |
| HX-6 | OmniRoute | NOT STARTED | — | Clean rebuild |
| HX-7 | NGINX — dev/test only | NOT STARTED | — | Clean rebuild |
| HX-8 | Open WebUI | NOT STARTED | — | Clean rebuild |
| HX-9 | PostgreSQL / Redis + MCP | NOT STARTED | — | Clean rebuild |
| HX-10 | Qdrant + Web UI + MCP | NOT STARTED | — | Clean rebuild |
| HX-11 | LightRAG + MCP | NOT STARTED | — | Clean rebuild |
| HX-12 | Deep Agents | NOT STARTED | — | Clean rebuild |
| HX-13 | Mem0 | NOT STARTED | — | Clean rebuild |
| HX-14 | n8n + MCP | NOT STARTED | — | Clean rebuild |
| HX-15 | FastMCP | NOT STARTED | — | Clean rebuild |
| HX-16 | Docling + Granite-Docling + MCP | NOT STARTED | — | Clean rebuild |
| HX-17 | Crawl4AI + MCP | NOT STARTED | — | Clean rebuild |

## Closed-server notes

### HX-2
- Domain membership / SSSD: PASS
- NVIDIA 595.71.05: PASS
- 2 x GeForce RTX 4070 Ti SUPER 16 GB: PASS
- Dedicated `/srv/ollama` storage: PASS
- Ollama 0.33.3: PASS
- Qwen3.8-27B Q6_K: PASS
- CLI/API/LAN/reboot persistence: PASS
- Current Ollama cloud state is temporary local-only configuration.

### HX-3
- Ubuntu 24.04.5 / kernel 7.0.0-31: PASS
- Domain membership / SSSD: PASS
- NVIDIA 595.71.05: PASS
- 2 x RTX 5060 Ti 16 GB: PASS
- Dedicated `/srv/ollama` storage: PASS
- Ollama 0.33.3: PASS
- `coder-x:qwen3-coder-30b-q6_k`: PASS
- CLI/API/LAN/reboot persistence: PASS
- Longer boot time is informational only; do not diagnose/remediate unless explicitly asked.

## Operating rule

A server becomes `PASS / CLOSED` only after its required base, domain, workload, functional, and reboot-persistence gates are satisfied and its as-built server record is updated.
