# HX-Eco-System Build State

**Date:** 2026-09-09  
**Owner:** Jarvis Richardson  
**Method:** KISS / one server at a time
<!-- HX-FLEET:TABLE columns=id,role,state,gate,note -->
| Server | Assignment | State | Gate | Notes |
|---|---|---|---|---|
| HX-1 | Samba AD / DNS / Kerberos / NTP | **PASS** | **CLOSED** | Clean base retained; foundation for the whole fleet |
| HX-2 | Qwen-X / Ollama | **PASS** | **CLOSED** | Qwen3.8-27B Q6_K; 2 x RTX 4070 Ti SUPER 16GB; model source URI UNRESOLVED |
| HX-3 | Coder-X / Ollama | **PASS** | **CLOSED** | Qwen3-Coder-30B-A3B-Instruct Q6_K; 2 x RTX 5060 Ti 16GB; full artifact hash UNRESOLVED |
| HX-4 | Meta-X / GPT-OSS 20B + BGE-M3 + Nomic + BGE reranker | **NOT STARTED** | **NEXT** | Shared embedding/reranking plane; reranker pinned in common/hx-base.env |
| HX-5 | CentCom / Ornith / DeepSeek Harness / dev-test | **NOT STARTED** | — | Becomes the smoke-test runner station after its own base closes |
| HX-6 | OmniRoute | **NOT STARTED** | — | Provider and model allowlists required (D-010) |
| HX-7 | NGINX dev/test only | **NOT STARTED** | — | Not the ecosystem reverse proxy (D-004) |
| HX-8 | Open WebUI | **NOT STARTED** | — | Last in build order; temporary Ollama link for base proof (D-008) |
| HX-9 | PostgreSQL + MCP / Redis + MCP | **NOT STARTED** | — | Two applications on one host; each closes separately |
| HX-10 | Qdrant + Web UI + MCP | **NOT STARTED** | — | One embedding identity per collection (D-005) |
| HX-11 | LightRAG + MCP | **NOT STARTED** | — | Needs HX-10 and HX-4 proof first |
| HX-12 | Deep Agents (LangChain) LOB agent factory | **NOT STARTED** | — | Prose runbook; pin deepagents version at implementation time |
| HX-13 | Mem0 + assigned MCP | **NOT STARTED** | — | MCP implementation not yet selected |
| HX-14 | n8n + MCP | **NOT STARTED** | — | Install from GitHub release or npm tarball, not Snap |
| HX-15 | FastMCP shared/custom MCP development host | **NOT STARTED** | — | Not a prerequisite for product-specific MCP servers |
| HX-16 | Docling + Granite-Docling 258M + MCP | **NOT STARTED** | — | Granite-Docling stays here, CPU-first (D-006) |
| HX-17 | Crawl4AI + MCP | **NOT STARTED** | — | Native install; official MCP bridge is Docker-coupled, needs a native choice |
<!-- /HX-FLEET:TABLE -->


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
