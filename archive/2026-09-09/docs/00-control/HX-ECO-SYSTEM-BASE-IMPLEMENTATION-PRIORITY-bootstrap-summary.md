---
document: HX Eco-System Base Implementation Priority
status: planning_current
version: 1.3
date: 2026-09-09
scope: HX-1 through HX-17
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Base Implementation Priority and Server Map

## 1. Governing rule
The current objective is to leave every assigned service in a known-good standalone state so later integration begins from verified components.

A component reaches **BASE PASS** when its host/base prerequisites, application, required local storage, systemd startup, direct local/LAN health, application-specific Web UI where applicable, application-specific MCP server where applicable, functional smoke test, and reboot persistence are proven.

Temporary cross-service wiring is allowed only as a lightweight reversible smoke test against an already-proven dependency. It must be recorded and removed/disabled before closure unless explicitly approved as permanent architecture.

## 2. Dependency-driven implementation order

| Priority | Server | Base component | BASE PASS boundary |
|---:|---|---|---|
| 1 | HX-4 | Meta-X / Ollama / GPT-OSS 20B + shared embeddings/reranker | GPT-OSS, BGE-M3, Nomic v1.5, BGE-family reranker, APIs, resource observation, reboot persistence |
| 2 | HX-5 | CentCom Ollama / Ornith | Accepted GPU state, Ollama, exact model, LAN inference, reboot persistence |
| 3 | HX-9 | PostgreSQL + PostgreSQL MCP | Native DB, persistent data, local/LAN test, MCP smoke test, reboot persistence |
| 4 | HX-9 | Redis + assigned Redis MCP | Native Redis, selected persistence/config, local/LAN test, MCP smoke test where assigned, reboot persistence |
| 5 | HX-10 | Qdrant + Qdrant Web UI + Qdrant MCP | Native Qdrant, persistent storage, API health, direct Web UI, MCP smoke test, reboot persistence |
| 6 | HX-6 | OmniRoute | Native service/UI/API, one temporary known-good Ollama route, direct-vs-routed functional proof, curated provider/model controls, cleanup, reboot persistence |
| 7 | HX-15 | FastMCP | Shared/custom MCP runtime, test MCP server, service pattern, reboot validation |
| 8 | HX-5 | DeepSeek Harness | Harness installed, native runtime/CLI or service health proven; fleet orchestration deferred |
| 9 | HX-7 | NGINX — development use only | Native NGINX, simple dev-proxy smoke test; no normal ecosystem service routes |
| 10 | HX-16 | Docling + Granite-Docling 258M + Docling MCP | Native Docling, Granite local to HX-16, CPU-first conversion/performance test, fallback pipeline, MCP smoke test |
| 11 | HX-17 | Crawl4AI + Crawl4AI MCP | Native Crawl4AI, representative crawl, MCP smoke test, service/API base if used |
| 12 | HX-11 | LightRAG + LightRAG MCP | Native LightRAG, local config/storage, health, MCP smoke test, reboot persistence; ecosystem wiring deferred |
| 13 | HX-13 | Mem0 + assigned MCP capability | Native Mem0, local smoke test, persistent config, MCP smoke test where assigned |
| 14 | HX-12 | Deep Agents by LangChain | Native environment, standalone agent smoke test; external tools/memory deferred |
| 15 | HX-14 | n8n + n8n MCP | Native n8n, persistent data/config, direct UI, MCP smoke test, reboot persistence; workflows deferred |
| 16 | HX-8 | Open WebUI | Native UI, persistent storage, direct LAN UI, temporary direct Ollama prompt/response proof, cleanup, reboot persistence |

## 3. Implementation waves

### Wave A — Complete inference
HX-4 Meta-X, then HX-5 CentCom/Ornith.

### Wave B — State and retrieval foundations
HX-9 PostgreSQL, HX-9 Redis, HX-10 Qdrant.

### Wave C — Routing, MCP development, control plane
HX-6 OmniRoute, HX-15 FastMCP, HX-5 DeepSeek Harness, HX-7 NGINX dev-only.

### Wave D — Knowledge acquisition
HX-16 Docling, HX-17 Crawl4AI.

### Wave E — RAG and memory
HX-11 LightRAG, HX-13 Mem0.

### Wave F — Agent/workflow consumers
HX-12 Deep Agents, HX-14 n8n.

### Wave G — User interaction
HX-8 Open WebUI.

## 4. MCP rule
Application-specific MCP servers are built with their parent applications. HX-15 FastMCP is the shared/custom MCP development host and is not a prerequisite for product-specific MCP servers.

## 5. Model placement
- HX-16: Granite-Docling 258M, local to Docling, CPU-first.
- HX-4: BGE-M3 primary embedding model, Nomic Embed Text v1.5 alternate, BGE-family reranker.
- Qdrant stores vectors; it does not own embedding inference.
- Never mix embeddings from different models in one collection.

## 6. OmniRoute validation and catalog control
BASE PASS includes one temporary route to a proven Ollama endpoint and a direct-versus-routed known-answer test. The temporary route is removed/disabled after evidence capture unless explicitly approved to remain.

HX uses two explicit controls:
1. approved provider allowlist;
2. approved model allowlist.

Known by OmniRoute is not the same as approved HX provider, and provider approval is not the same as approved HX model.

## 7. Open WebUI validation
BASE PASS includes one temporary direct connection to a proven Ollama endpoint, one selected model, one prompt and rendered response inside Open WebUI, evidence capture, then cleanup/removal of the temporary connection.

## 8. NGINX
HX-7 is not the common ecosystem reverse proxy. It is reserved for development/test rendering of applications under active development.

## 9. Current server map

| Server | IP | Assignment |
|---|---|---|
| HX-1 | 192.168.50.200 | Samba AD / DNS / Kerberos / NTP |
| HX-2 | 192.168.50.202 | Qwen-X / Ollama |
| HX-3 | 192.168.50.203 | Coder-X / Ollama |
| HX-4 | 192.168.50.204 | Meta-X / GPT-OSS + embeddings/reranker |
| HX-5 | 192.168.50.205 | CentCom / Ornith / DeepSeek Harness / dev-test |
| HX-6 | 192.168.50.206 | OmniRoute |
| HX-7 | 192.168.50.207 | NGINX dev/test only |
| HX-8 | 192.168.50.208 | Open WebUI |
| HX-9 | 192.168.50.209 | PostgreSQL / Redis + MCP |
| HX-10 | 192.168.50.210 | Qdrant + Web UI + MCP |
| HX-11 | 192.168.50.211 | LightRAG + MCP |
| HX-12 | 192.168.50.212 | Deep Agents |
| HX-13 | 192.168.50.213 | Mem0 |
| HX-14 | 192.168.50.214 | n8n + MCP |
| HX-15 | 192.168.50.215 | FastMCP |
| HX-16 | 192.168.50.216 | Docling + Granite-Docling + MCP |
| HX-17 | 192.168.50.217 | Crawl4AI + MCP |

## 10. Integration readiness gate
The base-build program is complete only when HX-1 through HX-17 have current server records and every assigned base service, companion UI/MCP component, functional test, and reboot-persistence gate is independently proven.
