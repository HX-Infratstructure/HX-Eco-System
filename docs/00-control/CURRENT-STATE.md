---
document: HX Eco-System Current State
status: current
date: 2026-09-09
authority: infrastructure-owner
---

# HX Eco-System — Current State

## Program objective

Clean-room rebuild of HX-1 through HX-17 into a verified base ecosystem. Current scope is base installation and standalone functional validation. Full permanent interconnection is later.

The **ecosystem architecture is the cornerstone**. Validation proves the ecosystem after its server role, configuration, ownership, and dependency boundaries are understood.

## Current build state
<!-- HX-FLEET:TABLE columns=id,role,state -->
| Server | Assignment | State |
|---|---|---|
| HX-1 | Samba AD / DNS / Kerberos / NTP | **PASS** |
| HX-2 | Qwen-X / Ollama | **PASS** |
| HX-3 | Coder-X / Ollama | **PASS** |
| HX-4 | Meta-X / GPT-OSS 20B + BGE-M3 + Nomic + BGE reranker | **NOT STARTED** |
| HX-5 | CentCom / Ornith / DeepSeek Harness / dev-test | **NOT STARTED** |
| HX-6 | OmniRoute | **NOT STARTED** |
| HX-7 | NGINX dev/test only | **NOT STARTED** |
| HX-8 | Open WebUI | **NOT STARTED** |
| HX-9 | PostgreSQL + MCP / Redis + MCP | **NOT STARTED** |
| HX-10 | Qdrant + Web UI + MCP | **NOT STARTED** |
| HX-11 | LightRAG + MCP | **NOT STARTED** |
| HX-12 | Deep Agents (LangChain) LOB agent factory | **NOT STARTED** |
| HX-13 | Mem0 + assigned MCP | **NOT STARTED** |
| HX-14 | n8n + MCP | **NOT STARTED** |
| HX-15 | FastMCP shared/custom MCP development host | **NOT STARTED** |
| HX-16 | Docling + Granite-Docling 258M + MCP | **NOT STARTED** |
| HX-17 | Crawl4AI + MCP | **NOT STARTED** |
<!-- /HX-FLEET:TABLE -->


## Current deployment order

Deployment/build authority:

`HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`

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

## Current validation order

Validation/proof authority:

`HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`

The smoke roadmap is subordinate to deployment readiness: a component cannot be smoke-tested before its SUT is installed and ready.

Current smoke position:

- Phase 0 foundation proof exists for HX-1, HX-2, HX-3.
- Phase A is next, beginning with HX-4 inference/retrieval-model proof and HX-5 inference/runner activation when the deployment sequence reaches those servers.
- After CentCom activation, later smoke tests run remotely from HX-5 where practical.
- Downstream tests reference current prior PASS evidence when their primary contract depends on earlier components.
- Temporary integrations are limited to the minimum required for proof and are cleaned up afterward.

## Important current constraints

- Ecosystem architecture/configuration context comes before validation.
- Clean-room build. Do not inherit old application state.
- Native Linux/systemd; no containers.
- No unapproved network/security restrictions.
- No unapproved disk changes.
- Application-specific MCP servers are installed with their parent applications.
- NGINX is not the ecosystem reverse proxy.
- HX-4 is the shared embedding/reranking host.
- Granite-Docling remains on HX-16.
- Open WebUI and OmniRoute receive lightweight temporary Ollama functional tests before BASE PASS.
- Smoke-test dependencies are proof dependencies unless the owner explicitly approves them as permanent architecture.
- Design/runbook readiness is not as-built completion.
