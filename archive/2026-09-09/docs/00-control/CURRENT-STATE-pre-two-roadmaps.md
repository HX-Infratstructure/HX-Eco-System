---
document: HX Eco-System Current State
status: current
date: 2026-09-09
authority: infrastructure-owner
---

# HX Eco-System — Current State

## Program objective

Clean-room rebuild of HX-1 through HX-17 into a verified base ecosystem. Current scope is base installation and standalone functional validation. Full interconnection is later.

## Current build state

| Server | Assignment | State |
|---|---|---|
| HX-1 | Samba AD / DNS / Kerberos / NTP | PASS / CLOSED |
| HX-2 | Qwen-X / Ollama / Qwen3.8-27B Q6_K | PASS / CLOSED |
| HX-3 | Coder-X / Ollama / Qwen3-Coder-30B Q6_K | PASS / CLOSED |
| HX-4 | Meta-X / GPT-OSS 20B + shared embeddings/reranker | NEXT |
| HX-5 | CentCom / Ornith / DeepSeek Harness / dev-test | NOT STARTED |
| HX-6 | OmniRoute | NOT STARTED |
| HX-7 | NGINX — dev/test only | NOT STARTED |
| HX-8 | Open WebUI | NOT STARTED |
| HX-9 | PostgreSQL + MCP / Redis + MCP | NOT STARTED |
| HX-10 | Qdrant + Web UI + MCP | NOT STARTED |
| HX-11 | LightRAG + MCP | NOT STARTED |
| HX-12 | Deep Agents by LangChain | NOT STARTED |
| HX-13 | Mem0 + assigned MCP capability | NOT STARTED |
| HX-14 | n8n + MCP | NOT STARTED |
| HX-15 | FastMCP shared/custom MCP development host | NOT STARTED |
| HX-16 | Docling + Granite-Docling 258M + MCP | NOT STARTED |
| HX-17 | Crawl4AI + MCP | NOT STARTED |

## Current execution order

Follow `HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`.

Dependency-driven sequence:
1. HX-4 Meta-X
2. HX-5 CentCom Ollama / Ornith
3. HX-9 PostgreSQL
4. HX-9 Redis
5. HX-10 Qdrant
6. HX-6 OmniRoute
7. HX-15 FastMCP
8. HX-5 DeepSeek Harness
9. HX-7 NGINX dev-only
10. HX-16 Docling
11. HX-17 Crawl4AI
12. HX-11 LightRAG
13. HX-13 Mem0
14. HX-12 Deep Agents
15. HX-14 n8n
16. HX-8 Open WebUI

## Important current constraints

- Clean-room build. Do not inherit old application state.
- Native Linux/systemd; no containers.
- No unapproved network/security restrictions.
- No unapproved disk changes.
- Application-specific MCP servers are installed with their parent applications.
- NGINX is not the ecosystem reverse proxy.
- HX-4 is the shared embedding/reranking host.
- Granite-Docling remains on HX-16.
- Open WebUI and OmniRoute receive lightweight temporary Ollama functional tests before BASE PASS.
