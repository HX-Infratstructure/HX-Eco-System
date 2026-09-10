---
document: HX Eco-System Base Implementation Priority
status: evergreen_current
version: 1.7
date: 2026-09-09
scope: HX-1 through HX-17
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Base Implementation Priority and Server Map

**Version:** 1.7  
**Document type:** Evergreen roadmap — updated as verified information, owner decisions, and additional work become available.  
**Purpose:** Define the dependency-driven build order, BASE PASS boundaries, current server/application assignments, model placement, smoke-test authorities, and known follow-on infrastructure tasks for the clean HX Eco-System rebuild.  
**Scope boundary:** Base installation and standalone validation. Permanent cross-service integration is a later program.

This document is intentionally **not final or frozen**. The active file at this stable path is always the current roadmap. Superseded versions are archived according to `DOCUMENT-CONTROL.md`.

## 1. Governing build rule

```text
one server
→ verify base state
→ install assigned workload
→ prove primary function
→ reboot
→ record evidence
→ close PASS
→ move to next server
```

A component reaches **BASE PASS** only when:

1. the assigned host is cleanly rebuilt and joined to `hx.local.arpa`;
2. required OS packages are installed;
3. the application is installed natively on Linux;
4. long-running services use systemd where applicable;
5. the service is active and enabled;
6. expected local/LAN health endpoints respond;
7. required local storage is mounted and persistent;
8. application-specific Web UI is validated directly on its native endpoint where applicable;
9. assigned application-specific MCP server is installed and independently smoke-tested where applicable;
10. the defined component smoke test passes using only the minimum temporary integration required to prove primary function;
11. validation-only data, routes, connections, projects, collections, workflows, and other temporary state are removed/disabled after the test unless explicitly approved as permanent;
12. reboot persistence is proven;
13. the server record and `BUILD-STATE.md` are updated;
14. no unapproved network, storage, security, or cross-service architecture changes are introduced.

### Clean-room boundary

Historical HX-Infrastructure material may be consulted as reference evidence only. It does not establish current configuration, application state, or completion.

### Native deployment boundary

Native Linux + systemd is the deployment standard. No Docker, Podman, Kubernetes, or other containerized workload deployment unless the infrastructure owner explicitly changes this rule.

## 2. Application companion rule

Product-specific Web UIs and MCP servers are part of the parent application's base build where assigned.

Examples:

- PostgreSQL includes PostgreSQL MCP.
- Redis includes its assigned Redis MCP where applicable.
- Qdrant includes **Qdrant + Qdrant Web UI + Qdrant MCP**.
- LightRAG includes LightRAG MCP.
- n8n includes n8n MCP.
- Docling includes Granite-Docling 258M + Docling MCP.
- Crawl4AI includes Crawl4AI MCP.
- Mem0 includes its assigned MCP capability.

HX-15 FastMCP is the shared/custom MCP development and runtime host. It is **not a prerequisite** for product-specific MCP servers.

MCP client registration, agent tool binding, and permanent orchestration wiring remain integration-phase work.

## 3. Current accepted baseline

| Server | Current role | State |
|---|---|---|
| HX-1 | Samba AD / DNS / Kerberos / NTP | **PASS / CLOSED** |
| HX-2 | Qwen-X / Ollama / Qwen3.8-27B Q6_K | **PASS / CLOSED** |
| HX-3 | Coder-X / Ollama / Qwen3-Coder-30B Q6_K | **PASS / CLOSED** |
| HX-4 | Meta-X / GPT-OSS 20B + shared embedding/reranking | **NEXT — runbooks staged** |
| HX-5 | CentCom / Ornith + DeepSeek Harness / dev-test | **NOT STARTED — runbooks staged** |
| HX-6 through HX-17 | Assigned workloads below | **NOT STARTED** |

HX-2 and HX-3 establish the proven GPU-inference pattern: clean OS, domain membership, NVIDIA 595 Server Open, dedicated Ollama storage, LAN API, exact model, functional inference, and reboot persistence.

## 4. Dependency-driven implementation order

| Priority | Server | Base component | BASE PASS boundary |
|---:|---|---|---|
| 1 | HX-4 | **Meta-X / Ollama / GPT-OSS 20B + shared embeddings/reranker** | Ollama + GPT-OSS known-answer inference; BGE-M3 and Nomic embedding proof at approved dimensions; pinned BGE-family reranker known-answer ranking; APIs; resource observation; reboot persistence |
| 2 | HX-5 | **CentCom Ollama / Ornith** | Accepted GPU state, Ollama, exact Ornith model, known-answer LAN inference, reboot persistence |
| 3 | HX-9 | **PostgreSQL + PostgreSQL MCP** | Native DB, persistent service/data path, create/write/read disposable DB proof, MCP companion smoke test, reboot persistence |
| 4 | HX-9 | **Redis + assigned Redis MCP** | Native Redis, selected persistence/config, PING/SET/GET/DELETE proof, MCP companion smoke test, reboot persistence |
| 5 | HX-10 | **Qdrant + Qdrant Web UI + Qdrant MCP** | Native Qdrant, persistent storage, API health, vector write/query/read smoke test, direct Web UI live-state proof, MCP companion smoke test, cleanup, reboot persistence |
| 6 | HX-6 | **OmniRoute** | Native service/UI, curated provider/model controls, one temporary proven Ollama route, direct-vs-routed proof, cleanup, reboot persistence |
| 7 | HX-15 | **FastMCP** | Shared/custom MCP development runtime, custom test server/tool discovery/tool call, cleanup, service/reboot validation |
| 8 | HX-5 | **DeepSeek Harness** | Runtime health plus meta-agent decomposition, sub-agent delegation, runnable AI artifact creation, independent validation, synthesis, cleanup, reboot delegated-task proof |
| 9 | HX-7 | **NGINX — development use only** | Native NGINX, active/enabled, temporary private-IP development proxy proof, cleanup; no ecosystem service routes |
| 10 | HX-16 | **Docling + Granite-Docling 258M + Docling MCP** | Native Docling, deterministic document conversion, Granite-Docling CPU-first proof, MCP companion smoke test, cleanup, reboot persistence where applicable |
| 11 | HX-17 | **Crawl4AI + Crawl4AI MCP** | Native Crawl4AI, deterministic crawl/Markdown proof, MCP companion smoke test, cleanup, reboot persistence where applicable |
| 12 | HX-11 | **LightRAG + LightRAG MCP** | Native LightRAG, health, synthetic ingest/retrieval/query proof, assigned MCP companion smoke test, cleanup, reboot persistence |
| 13 | HX-13 | **Mem0 + assigned MCP capability** | Native Mem0, disposable store/search/delete memory lifecycle using approved dependencies, MCP companion smoke test, cleanup, persistent config/reboot validation |
| 14 | HX-12 | **Deep Agents by LangChain** | Pinned environment, approved-model tool-calling probe, real LOB agent package, actual sub-agent delegation, known-answer business-rule result, thread continuity, independent validation, cleanup, reboot proof |
| 15 | HX-14 | **n8n + n8n MCP** | Native n8n, persistent data/config, deterministic create/execute/save/reopen/delete workflow proof, direct UI, MCP companion smoke test, reboot persistence |
| 16 | HX-8 | **Open WebUI** | Native UI/storage, direct LAN UI, temporary direct Ollama prompt/response proof, cleanup, reboot persistence |

## 5. Implementation waves

### Wave A — Inference plane
1. HX-4 Meta-X
2. HX-5 CentCom / Ornith

**Exit:** HX-2, HX-3, HX-4, and HX-5 each expose a proven local Ollama inference endpoint. HX-4 additionally proves both assigned embedding models and the pinned reranker before its full workload gate closes.

### Wave B — State and retrieval foundations
3. HX-9 PostgreSQL + MCP  
4. HX-9 Redis + MCP  
5. HX-10 Qdrant + Web UI + MCP

**Exit:** relational, transient, and vector state services are independently healthy, including assigned MCP endpoints and Qdrant's native UI.

### Wave C — Routing, MCP development, control plane
6. HX-6 OmniRoute  
7. HX-15 FastMCP  
8. HX-5 DeepSeek Harness  
9. HX-7 NGINX dev/test only

**Exit:** routing, shared/custom MCP development, CentCom Harness, and dev-only NGINX operate independently. OmniRoute proves one temporary route to a known-good HX model. DeepSeek Harness proves bounded meta-agent solution construction through sub-agents.

### Wave D — Knowledge acquisition
10. HX-16 Docling + Granite-Docling + MCP  
11. HX-17 Crawl4AI + MCP

**Exit:** deterministic document conversion and deterministic web-content extraction operate independently with their assigned MCP endpoints.

### Wave E — RAG and memory
12. HX-11 LightRAG + MCP  
13. HX-13 Mem0 + assigned MCP

**Exit:** retrieval and memory applications operate independently. Limited disposable integration required by a smoke test is permitted; permanent ecosystem wiring remains deferred.

### Wave F — Agent/workflow consumers
14. HX-12 Deep Agents  
15. HX-14 n8n + MCP

**Exit:** HX-12 proves creation and execution of a small LOB agent package with sub-agents, tools/files, known-answer business rules, disposable thread state, and independent validation. HX-14 proves a saved/reopened deterministic workflow. Production agent bindings/workflows remain deferred.

### Wave G — User interaction
16. HX-8 Open WebUI

**Exit:** Open WebUI proves one temporary direct conversation against a known-good HX model and removes the validation-only connection afterward.

## 6. RAG and model placement

### RAG stack priority

```text
PostgreSQL + MCP / Redis + MCP
              ↓
     Qdrant + Web UI + MCP
              ↓
 Docling + MCP / Crawl4AI + MCP
              ↓
       LightRAG + MCP
              ↓
        Mem0 + MCP
              ↓
   Deep Agents / n8n consumers
```

No production corpus is ingested during base installation. Synthetic/throwaway objects are sufficient for smoke testing.

### HX-16 — Docling model

```text
Docling
└── Granite-Docling 258M
```

Granite-Docling is a document-understanding VLM, not the general HX text embedding model. Base validation is **CPU-first**. GPU acceleration is considered later only if measured performance justifies it. Do not route routine Granite-Docling inference through OmniRoute.

### HX-4 — shared retrieval inference

```text
Meta-X / GPT-OSS 20B
├── BGE-M3 — PRIMARY/default embedding model
├── Nomic Embed Text v1.5 — SECONDARY benchmark/fallback
└── BGE-family reranker
```

Default embedding dimensions:

```text
BGE-M3       1024
Nomic v1.5    768
```

Never mix embedding models within one Qdrant collection. Model changes require a new collection and complete re-embedding.

The exact BGE-family reranker checkpoint and serving runtime remain explicit implementation decisions and must be pinned before the reranker smoke test becomes executable.

Detailed authority: `HX-ECO-SYSTEM-MODEL-PLACEMENT-AND-EMBEDDING-STANDARD.md`.

## 7. Component smoke-test authority

The roadmap defines **what must pass**. Standalone files under `/smoke-tests/` define **how the proof is executed**. This keeps the evergreen roadmap small and prevents component procedures from bloating the baseline document.

Temporary cross-service integration is permitted during BASE PASS only when it is:

- minimal and required to prove primary function;
- against an already-proven dependency where applicable;
- synthetic/disposable rather than production data;
- clearly labeled validation-only;
- removed/deleted/disabled after evidence capture unless explicitly approved as permanent.

### Component procedures

| Server | Component | Executable smoke-test authority |
|---|---|---|
| HX-4 | GPT-OSS / Ollama inference | `../../smoke-tests/ollama-inference-smoke-test.md` |
| HX-4 | BGE-M3 + Nomic Embed Text v1.5 | `../../smoke-tests/embedding-models-smoke-test.md` |
| HX-4 | BGE-family reranker | `../../smoke-tests/reranker-smoke-test.md` — conditional until checkpoint/runtime are pinned |
| HX-5 | Ornith / Ollama inference | `../../smoke-tests/ollama-inference-smoke-test.md` |
| HX-9 | PostgreSQL | `../../smoke-tests/postgresql-smoke-test.md` |
| HX-9 | Redis | `../../smoke-tests/redis-smoke-test.md` |
| HX-10 | Qdrant | `../../smoke-tests/qdrant-smoke-test.md` |
| HX-11 | LightRAG | `../../smoke-tests/lightrag-smoke-test.md` |
| HX-13 | Mem0 | `../../smoke-tests/mem0-smoke-test.md` |
| HX-15 | FastMCP | `../../smoke-tests/fastmcp-smoke-test.md` |
| HX-7 | NGINX dev/test | `../../smoke-tests/nginx-smoke-test.md` |
| HX-14 | n8n | `../../smoke-tests/n8n-smoke-test.md` |
| HX-16 | Docling / Granite-Docling | `../../smoke-tests/docling-smoke-test.md` |
| HX-17 | Crawl4AI | `../../smoke-tests/crawl4ai-smoke-test.md` |
| HX-5 | DeepSeek Harness | `../../smoke-tests/deepseek-harness-smoke-test.md` |
| HX-12 | Deep Agents | `../../smoke-tests/deep-agents-smoke-test.md` |
| HX-6 | OmniRoute | `../../smoke-tests/omniroute-smoke-test.md` |
| HX-8 | Open WebUI | `../../smoke-tests/open-webui-smoke-test.md` |

### Reusable companion procedures

| Applies to | Companion proof | Authority |
|---|---|---|
| Assigned product-specific MCP servers | MCP discovery + safe known-answer tool call | `../../smoke-tests/mcp-companion-smoke-test.md` |
| Assigned native Web UIs | direct LAN UI + live backend state proof | `../../smoke-tests/native-web-ui-smoke-test.md` |

Companion tests supplement the parent component smoke test; they do not replace it.

DeepSeek Harness role/design authority remains `HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`. Deep Agents role/design authority remains `HX-ECO-SYSTEM-DEEP-AGENTS-IMPLEMENTATION-ADDENDUM.md`. Their `/smoke-tests/` files are the concise executable acceptance procedures.

## 8. OmniRoute provider and model catalog standard

```text
KNOWN TO OMNIROUTE
        !=
APPROVED HX PROVIDER
        !=
APPROVED HX MODEL
```

HX maintains two explicit controls:

1. **Provider allowlist** — only explicitly approved local/cloud providers are enabled or credentialed for HX use.
2. **Model allowlist** — within an approved provider, only specifically approved model IDs are exposed for normal HX selection/routing.

Approving a provider does not approve its entire catalog. Free/no-auth/discovered providers are not automatically active.

Initial local catalog:

```text
HX-2  Qwen-X
      qwen-x:qwen3.8-27b-q6_k

HX-3  Coder-X
      coder-x:qwen3-coder-30b-q6_k

HX-4  Meta-X
      GPT-OSS 20B — exact operational alias recorded at build

HX-5  CentCom
      Ornith — exact operational alias recorded at build
```

Only models from servers that have passed their own BASE PASS may enter the active catalog. Cloud providers/models require explicit owner approval.

## 9. NGINX decision

The former concept of HX-7 as a general reverse proxy is withdrawn.

```text
HX-7 NGINX
Purpose: development/test UI rendering only
Use: proxy an application UI being actively developed when useful
Do not use: normal routing for Qdrant, LightRAG, n8n, Open WebUI,
            databases, MCP servers, or other ecosystem services
```

Normal application UIs remain directly accessible on their own native server/port.

## 10. Current server/application map
<!-- HX-FLEET:TABLE columns=id,ip,role,state -->
| Server | IP | Assignment | State |
|---|---|---|---|
| HX-1 | `192.168.50.200` | Samba AD / DNS / Kerberos / NTP | **PASS** |
| HX-2 | `192.168.50.202` | Qwen-X / Ollama | **PASS** |
| HX-3 | `192.168.50.203` | Coder-X / Ollama | **PASS** |
| HX-4 | `192.168.50.204` | Meta-X / GPT-OSS 20B + BGE-M3 + Nomic + BGE reranker | **NOT STARTED** |
| HX-5 | `192.168.50.205` | CentCom / Ornith / DeepSeek Harness / dev-test | **NOT STARTED** |
| HX-6 | `192.168.50.206` | OmniRoute | **NOT STARTED** |
| HX-7 | `192.168.50.207` | NGINX dev/test only | **NOT STARTED** |
| HX-8 | `192.168.50.208` | Open WebUI | **NOT STARTED** |
| HX-9 | `192.168.50.209` | PostgreSQL + MCP / Redis + MCP | **NOT STARTED** |
| HX-10 | `192.168.50.210` | Qdrant + Web UI + MCP | **NOT STARTED** |
| HX-11 | `192.168.50.211` | LightRAG + MCP | **NOT STARTED** |
| HX-12 | `192.168.50.212` | Deep Agents (LangChain) LOB agent factory | **NOT STARTED** |
| HX-13 | `192.168.50.213` | Mem0 + assigned MCP | **NOT STARTED** |
| HX-14 | `192.168.50.214` | n8n + MCP | **NOT STARTED** |
| HX-15 | `192.168.50.215` | FastMCP shared/custom MCP development host | **NOT STARTED** |
| HX-16 | `192.168.50.216` | Docling + Granite-Docling 258M + MCP | **NOT STARTED** |
| HX-17 | `192.168.50.217` | Crawl4AI + MCP | **NOT STARTED** |
<!-- /HX-FLEET:TABLE -->


## 11. Planned infrastructure follow-ons — lower priority

These items remain intentionally below the main server/application stand-up sequence and are **not on the immediate critical path**.

### 11.1 Fleet SSH pass / non-interactive SSH configuration

Establish the approved fleet-wide non-interactive SSH administration pattern for CentCom and authorized agentic tooling while preserving working interactive SSH.

- define the approved authentication pattern;
- document credential/key sourcing and script consumption;
- validate from the designated administration/control host;
- do not introduce network/access restrictions without explicit owner approval.

**Priority:** Planned / lower priority — no immediate action required.

### 11.2 NFS mounts and shared filesystem configuration

Define the clean-rebuild shared filesystem standard after authoritative exports, consumers, and storage sources are confirmed.

- identify authoritative export host(s)/paths and intended consumers;
- define stable mount points and reboot persistence;
- validate ownership/permissions;
- record approved mounts in applicable server records;
- do not automatically recreate historical prototype mounts.

**Priority:** Planned / lower priority — no immediate action required.

## 12. Integration readiness gate

Base-build completion requires current server records for HX-1 through HX-17 and independent proof of every assigned service, native Web UI, product-specific MCP endpoint, defined component smoke test, cleanup requirement, and reboot-persistence gate.

Only then does the program move to:

**HX Eco-System Integration and End-to-End Validation**

That later program will define service contracts, credentials, OmniRoute permanent routes, database schemas, Qdrant production collections, RAG ingestion, MCP client registrations, agent tool bindings, Open WebUI permanent backends, workflows, observability, and end-to-end operational tests.
