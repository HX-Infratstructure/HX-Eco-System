---
document: HX Eco-System Base Implementation Priority
status: evergreen_current
version: 1.6
date: 2026-09-09
scope: HX-1 through HX-17
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Base Implementation Priority and Server Map

**Version:** 1.6  
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
9. assigned application-specific MCP server is installed and smoke-tested where applicable;
10. the defined component smoke test passes using only the minimum temporary integration required to prove primary function;
11. validation-only data, routes, connections, projects, and other temporary state are removed/disabled after the test unless explicitly approved as permanent;
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
| 1 | HX-4 | **Meta-X / Ollama / GPT-OSS 20B + shared embeddings/reranker** | Ollama, GPT-OSS, BGE-M3, Nomic Embed Text v1.5, BGE-family reranker, APIs, resource observation, reboot persistence |
| 2 | HX-5 | **CentCom Ollama / Ornith** | Accepted GPU state, Ollama, exact Ornith model, LAN inference, reboot persistence |
| 3 | HX-9 | **PostgreSQL + PostgreSQL MCP** | Native DB, persistent data, local/LAN DB test, MCP smoke test, reboot persistence |
| 4 | HX-9 | **Redis + assigned Redis MCP** | Native Redis, selected persistence/config, local/LAN test, MCP smoke test, reboot persistence |
| 5 | HX-10 | **Qdrant + Qdrant Web UI + Qdrant MCP** | Native Qdrant, persistent storage, API health, vector write/query/read smoke test, direct Web UI, MCP smoke test, cleanup, reboot persistence |
| 6 | HX-6 | **OmniRoute** | Native service/UI, curated provider/model controls, one temporary proven Ollama route, direct-vs-routed proof, cleanup, reboot persistence |
| 7 | HX-15 | **FastMCP** | Shared/custom MCP development runtime, test MCP server, service pattern, reboot validation |
| 8 | HX-5 | **DeepSeek Harness** | Runtime health plus meta-agent decomposition, sub-agent delegation, runnable AI artifact creation, independent validation, synthesis, cleanup, reboot delegated-task proof |
| 9 | HX-7 | **NGINX — development use only** | Native NGINX, active/enabled, simple development proxy smoke test; no ecosystem service routes |
| 10 | HX-16 | **Docling + Granite-Docling 258M + Docling MCP** | Native Docling, deterministic document conversion, Granite-Docling CPU-first proof, MCP smoke test, cleanup |
| 11 | HX-17 | **Crawl4AI + Crawl4AI MCP** | Native Crawl4AI, deterministic crawl/Markdown proof, MCP smoke test, cleanup |
| 12 | HX-11 | **LightRAG + LightRAG MCP** | Native LightRAG, health, synthetic ingest/retrieval/query proof, assigned MCP smoke test, cleanup, reboot persistence |
| 13 | HX-13 | **Mem0 + assigned MCP capability** | Native Mem0, local smoke test, persistent config, assigned MCP smoke test |
| 14 | HX-12 | **Deep Agents by LangChain** | Pinned environment, approved-model tool-calling probe, real LOB agent package, actual sub-agent delegation, known-answer business-rule result, thread continuity, independent validation, cleanup, reboot proof |
| 15 | HX-14 | **n8n + n8n MCP** | Native n8n, persistent data/config, direct UI, MCP smoke test, reboot persistence; workflows deferred |
| 16 | HX-8 | **Open WebUI** | Native UI/storage, direct LAN UI, temporary direct Ollama prompt/response proof, cleanup, reboot persistence |

## 5. Implementation waves

### Wave A — Inference plane
1. HX-4 Meta-X
2. HX-5 CentCom / Ornith

**Exit:** HX-2, HX-3, HX-4, and HX-5 each expose a proven local Ollama inference endpoint.

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

**Exit:** HX-12 proves creation and execution of a small LOB agent package with sub-agents, tools/files, known-answer business rules, disposable thread state, and independent validation. HX-14 operates independently. Production agent bindings/workflows remain deferred.

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

Detailed authority: `HX-ECO-SYSTEM-MODEL-PLACEMENT-AND-EMBEDDING-STANDARD.md`.

## 7. Component smoke-test authority

The roadmap defines **what must pass**. Standalone files under `/smoke-tests/` define **how the proof is executed**. This keeps the evergreen roadmap small and prevents component procedures from bloating the baseline document.

Temporary cross-service integration is permitted during BASE PASS only when it is:

- minimal and required to prove primary function;
- against an already-proven dependency where applicable;
- synthetic/disposable rather than production data;
- clearly labeled validation-only;
- removed/deleted/disabled after evidence capture unless explicitly approved as permanent.

| Server | Component | Executable smoke-test authority |
|---|---|---|
| HX-10 | Qdrant | `../../smoke-tests/qdrant-smoke-test.md` |
| HX-11 | LightRAG | `../../smoke-tests/lightrag-smoke-test.md` |
| HX-17 | Crawl4AI | `../../smoke-tests/crawl4ai-smoke-test.md` |
| HX-16 | Docling / Granite-Docling | `../../smoke-tests/docling-smoke-test.md` |
| HX-5 | DeepSeek Harness | `../../smoke-tests/deepseek-harness-smoke-test.md` |
| HX-12 | Deep Agents | `../../smoke-tests/deep-agents-smoke-test.md` |
| HX-6 | OmniRoute | `../../smoke-tests/omniroute-smoke-test.md` |
| HX-8 | Open WebUI | `../../smoke-tests/open-webui-smoke-test.md` |

DeepSeek Harness role/design authority remains `HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`. Deep Agents role/design authority remains `HX-ECO-SYSTEM-DEEP-AGENTS-IMPLEMENTATION-ADDENDUM.md`. Their `/smoke-tests/` files are the concise executable acceptance procedures.

Additional components should follow the same pattern as their smoke-test definitions mature.

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

| Server | IP | Assignment | Priority |
|---|---|---|---:|
| HX-1 | `192.168.50.200` | Samba AD / DNS / Kerberos / NTP | Complete |
| HX-2 | `192.168.50.202` | Qwen-X / Ollama / Qwen3.8-27B Q6_K | Complete |
| HX-3 | `192.168.50.203` | Coder-X / Ollama / Qwen3-Coder-30B Q6_K | Complete |
| HX-4 | `192.168.50.204` | Meta-X / GPT-OSS 20B + BGE-M3 / Nomic / BGE reranker | 1 |
| HX-5 | `192.168.50.205` | CentCom / Ornith / DeepSeek Harness / dev-test | 2, 8 |
| HX-6 | `192.168.50.206` | OmniRoute | 6 |
| HX-7 | `192.168.50.207` | NGINX dev/test only | 9 |
| HX-8 | `192.168.50.208` | Open WebUI | 16 |
| HX-9 | `192.168.50.209` | PostgreSQL + MCP / Redis + MCP | 3, 4 |
| HX-10 | `192.168.50.210` | Qdrant + Web UI + MCP | 5 |
| HX-11 | `192.168.50.211` | LightRAG + MCP | 12 |
| HX-12 | `192.168.50.212` | Deep Agents by LangChain — LOB agent factory/runtime harness | 14 |
| HX-13 | `192.168.50.213` | Mem0 + assigned MCP | 13 |
| HX-14 | `192.168.50.214` | n8n + MCP | 15 |
| HX-15 | `192.168.50.215` | FastMCP shared/custom MCP development host | 7 |
| HX-16 | `192.168.50.216` | Docling + Granite-Docling 258M + MCP | 10 |
| HX-17 | `192.168.50.217` | Crawl4AI + MCP | 11 |

## 11. Planned infrastructure follow-ons — lower priority

These items remain below the immediate server/application stand-up critical path.

### 11.1 Fleet SSH pass / non-interactive SSH configuration

Establish the approved fleet-wide SSH automation credential pattern so CentCom and authorized agentic tooling can perform non-interactive administration without repeated credential prompts.

Roadmap intent:

- define the approved fleet SSH authentication pattern;
- preserve working interactive SSH while adding an approved non-interactive mechanism;
- document credential/key sourcing and script consumption;
- validate from the designated control/administration host to fleet targets;
- do not introduce access restrictions or alter network policy without explicit owner approval.

**Priority:** Planned / lower priority — no immediate action required.

### 11.2 NFS mounts and shared filesystem configuration

Define the current HX shared NFS mount standard only after required server roles and storage sources are confirmed in the clean rebuild.

Roadmap intent:

- identify authoritative NFS export host(s), export paths, and intended consumers;
- define stable fleet mount points and persistence behavior;
- validate ownership/permissions and reboot persistence;
- document each approved mount in the applicable server record;
- do not automatically recreate historical prototype/HX-Infrastructure mounts unless explicitly approved.

**Priority:** Planned / lower priority — no immediate action required.

## 12. Integration readiness gate

Base-build completion requires current server records for HX-1 through HX-17 and independent proof of every assigned service, native Web UI, product-specific MCP endpoint, defined component smoke test, cleanup requirement, and reboot-persistence gate.

Only then does the program move to:

**HX Eco-System Integration and End-to-End Validation**

That later program will define permanent service contracts, credentials, OmniRoute routes, database schemas, Qdrant collections, RAG ingestion, MCP client registrations, agent tool bindings, Open WebUI backends, workflows, observability, and end-to-end operational tests.
