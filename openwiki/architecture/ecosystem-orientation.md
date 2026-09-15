---
type: "Reference"
title: "Ecosystem Architecture — The Cornerstone"
openwiki_generated: true
verified:
  - by: openwiki/0.5.1
    at: 2026-09-14T19:05:42.087Z
sources:
  - id: openwiki-source-9e410f74688e3b2d6aa0c07e
    resource: repo://docs/00-control/CURRENT-STATE.md
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-c870862b3b5893a6926a9f29
    resource: repo://docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md
  - id: openwiki-source-a398c63710072d01f99c7156
    resource: repo://docs/01-architecture/ARCHITECTURE-ORIENTATION.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
generated: { by: "openwiki/0.5.1", at: "2026-09-14T19:05:42.087Z" }
---


# Ecosystem Architecture — The Cornerstone

The HX Eco-System is a **17-server, native-Linux AI platform** built one server at a time, each
validated and recorded before the next begins. Its architecture is the *cornerstone*: the
configuration, server roles, dependency planes, and placement rules defined here are what every
other system — runbooks, governed skills, smoke tests, runbooks, the CentCom runner — inherits.
Validation exists to prove the ecosystem; it does not define the ecosystem.

The correct mental model, which must not be inverted, is:

```text
FOUNDATION -> ECOSYSTEM SERVICES -> APPLICATION CAPABILITY -> VALIDATION
```

A smoke test is evidence that an assigned component behaves correctly *inside* the approved
architecture; it is never an architecture source. Before an agent changes or validates a
component it must be able to state that component's owner server, target IP, role, current state,
applicable foundation rules, dependency boundaries, model/data placement, and BASE PASS
expectation. If it cannot answer questions 1–7 of the orientation sequence below, it is not ready
to execute validation.

## Foundational baseline

The accepted clean-build baseline. HX-1 through HX-3 carry current as-built evidence; HX-4 through
HX-17 remain planned until each is rebuilt and verified. Planned configuration must never be
reported as as-built state.

| Foundation item | HX baseline |
|---|---|
| LAN | `192.168.50.0/24` |
| Default gateway | `192.168.50.1` |
| Infrastructure DNS | HX-1 at `192.168.50.200` |
| Active Directory domain | `hx.local.arpa` |
| Kerberos realm | `HX.LOCAL.ARPA` |
| Identity client pattern | SSSD / realmd / adcli |
| Foundation server | HX-1 — Samba AD / DNS / Kerberos / NTP |
| Deployment standard | Native Ubuntu Linux + systemd |
| Container policy | No Docker, Podman, or Kubernetes unless the owner explicitly changes this |
| Application UI pattern | Direct native application endpoint and port by default |
| NGINX boundary | HX-7 is development/test UI rendering only; not the ecosystem reverse proxy |

The build scripts encode this posture: the common base runbook disables `ufw` on every server
and Ollama listens on `0.0.0.0:11434` with no authentication — the HX LAN is treated as a trusted
lab segment, and firewall/segmentation/TLS changes are not imposed without owner approval. No
containers, no Snap; application software comes from PyPI, npm, a GitHub release, an upstream
tarball, a direct binary, or Hugging Face. The Ubuntu archive is used only for the NVIDIA driver
and build toolchains and library headers.

## Capability planes

The ecosystem is organized into capability planes. Each higher plane depends on the planes beneath
it; dependencies point upward in the diagram (bottom-to-top). The diagram is a
capability/dependency orientation, not a statement that every cross-plane relationship is already
permanently integrated — the current program is base stand-up, and permanent integration comes
later.

```mermaid
flowchart BT
    F["FOUNDATION / CORNERSTONE<br/>HX-1 · domain · DNS · Kerberos · NTP<br/>LAN · gateway · native Linux + systemd"]
    I["INFERENCE PLANE<br/>HX-2 Qwen-X · HX-3 Coder-X<br/>HX-4 Meta-X · HX-5 Ornith"]
    S["STATE / RETRIEVAL<br/>HX-9 PostgreSQL + Redis<br/>HX-10 Qdrant"]
    K["KNOWLEDGE / RAG / MEMORY<br/>HX-16 Docling · HX-17 Crawl4AI<br/>HX-11 LightRAG · HX-13 Mem0"]
    C["CONTROL / ROUTING / MCP DEV<br/>HX-6 OmniRoute · HX-15 FastMCP<br/>HX-5 DeepSeek Harness · HX-7 NGINX dev/test"]
    A["AGENT / WORKFLOW / UI<br/>HX-12 Deep Agents · HX-14 n8n<br/>HX-8 Open WebUI"]
    V["VALIDATION LAYER<br/>HX-5 CentCom remote smoke runner<br/>known-answer proof · cleanup · evidence"]

    F --> I
    I --> S
    S --> K
    I --> C
    S --> C
    K --> A
    C --> A

    V -. validates .-> I
    V -. validates .-> S
    V -. validates .-> C
    V -. validates .-> K
    V -. validates .-> A

    classDef foundation fill:#263238,color:#fff,stroke:#90a4ae,stroke-width:3px;
    classDef inference fill:#1565c0,color:#fff,stroke:#90caf9,stroke-width:2px;
    classDef state fill:#00695c,color:#fff,stroke:#80cbc4,stroke-width:2px;
    classDef control fill:#6a1b9a,color:#fff,stroke:#ce93d8,stroke-width:2px;
    classDef knowledge fill:#ef6c00,color:#fff,stroke:#ffcc80,stroke-width:2px;
    classDef app fill:#2e7d32,color:#fff,stroke:#a5d6a7,stroke-width:2px;
    classDef validation fill:#ad1457,color:#fff,stroke:#f48fb1,stroke-width:2px;

    class F foundation;
    class I inference;
    class S state;
    class C control;
    class K knowledge;
    class A app;
    class V validation;
```

*Capability planes and their dependency direction (bottom-to-top), with the validation layer
sitting on top and validating each plane rather than defining it.*

Two concerns cut across every plane and are deliberately not drawn, because cross-cutting lines
make the diagram less readable: **governed skills** (`skills/`) advise on any component but never
decide, and **validation** (`smoke-tests/`, run from HX-5 CentCom) proves any component but never
becomes an architecture layer of its own.

### Current server/application map

This is the owner-approved target assignment. State is shown separately so target architecture is
not confused with live configuration.

| Server | IP | Assignment | State |
|---|---|---|---|
| HX-1 | `192.168.50.200` | Samba AD / DNS / Kerberos / NTP | **PASS / CLOSED** |
| HX-2 | `192.168.50.202` | Qwen-X / Ollama / Qwen3.8-27B Q6_K | **PASS / CLOSED** |
| HX-3 | `192.168.50.203` | Coder-X / Ollama / Qwen3-Coder-30B Q6_K | **PASS / CLOSED** |
| HX-4 | `192.168.50.204` | Meta-X / GPT-OSS 20B + BGE-M3 / Nomic / BGE reranker | **NEXT** |
| HX-5 | `192.168.50.205` | CentCom / Ornith / DeepSeek Harness / dev-test | **NOT STARTED** |
| HX-6 | `192.168.50.206` | OmniRoute | **NOT STARTED** |
| HX-7 | `192.168.50.207` | NGINX dev/test only | **NOT STARTED** |
| HX-8 | `192.168.50.208` | Open WebUI | **NOT STARTED** |
| HX-9 | `192.168.50.209` | PostgreSQL + MCP / Redis + MCP | **NOT STARTED** |
| HX-10 | `192.168.50.210` | Qdrant + Web UI + MCP | **NOT STARTED** |
| HX-11 | `192.168.50.211` | LightRAG + MCP | **NOT STARTED** |
| HX-12 | `192.168.50.212` | Deep Agents (LangChain) — LOB agent factory/runtime | **NOT STARTED** |
| HX-13 | `192.168.50.213` | Mem0 + assigned MCP | **NOT STARTED** |
| HX-14 | `192.168.50.214` | n8n + MCP | **NOT STARTED** |
| HX-15 | `192.168.50.215` | FastMCP shared/custom MCP development host | **NOT STARTED** |
| HX-16 | `192.168.50.216` | Docling + Granite-Docling 258M + MCP | **NOT STARTED** |
| HX-17 | `192.168.50.217` | Crawl4AI + MCP | **NOT STARTED** |

The single source of truth for the fleet is `docs/00-control/hx-fleet.tsv`; the table above and
the runbook IP map are generated from it. Design readiness — a pinned version and a written
runbook — is not as-built completion.

## Dependency-driven build waves

The base program builds the ecosystem in dependency order, grouped into seven waves. **This is
dependency sequencing, not permanent integration wiring.** It does not authorize permanent
cross-service integration during base installation.

| Wave | Plane | Servers | Exit criterion |
|---|---|---|---|
| **A — Inference** | Inference | HX-4, HX-5 | HX-2, HX-3, HX-4, HX-5 each expose a proven local Ollama endpoint; HX-4 additionally proves both embedding models and the pinned reranker |
| **B — State & retrieval** | State/Retrieval | HX-9 (PostgreSQL), HX-9 (Redis), HX-10 (Qdrant) | Relational, transient, and vector state services are independently healthy, including assigned MCP endpoints and Qdrant's native UI |
| **C — Routing/MCP/control** | Control/Routing/MCP | HX-6, HX-15, HX-5 (DeepSeek Harness), HX-7 | OmniRoute proves one temporary route to a known-good HX model; FastMCP, Harness, and dev-only NGINX operate independently |
| **D — Knowledge acquisition** | Knowledge | HX-16, HX-17 | Deterministic document conversion and web-content extraction operate independently with assigned MCP endpoints |
| **E — RAG & memory** | RAG/Memory | HX-11, HX-13 | Retrieval and memory applications operate independently; limited disposable smoke integration permitted, permanent wiring deferred |
| **F — Agents/workflow** | Agent/Workflow | HX-12, HX-14 | HX-12 proves a bounded LOB agent package with sub-agents and known-answer rules; HX-14 proves a saved/reopened deterministic workflow |
| **G — User interaction** | UI | HX-8 | Open WebUI proves one temporary direct conversation against a known-good HX model, then removes the validation-only connection |

The flat deployment order interleaved across these waves is: HX-4 → HX-5 → HX-9 PostgreSQL →
HX-9 Redis → HX-10 → HX-6 → HX-15 → HX-5 DeepSeek Harness → HX-7 → HX-16 → HX-17 → HX-11 →
HX-13 → HX-12 → HX-14 → HX-8.

## Model and data placement

### Generative inference

- **HX-2 Qwen-X** — Qwen3.8-27B Q6_K; current PASS/CLOSED inference endpoint.
- **HX-3 Coder-X** — Qwen3-Coder-30B Q6_K; current PASS/CLOSED inference endpoint.
- **HX-4 Meta-X** — GPT-OSS 20B target plus shared retrieval inference.
- **HX-5 CentCom** — Ornith target plus development/test and DeepSeek Harness responsibilities.

Only models on servers that have passed their own applicable BASE PASS may enter the active HX
routing/model catalog. Even if HX-5 is upgraded to 2×16 GB GPUs, shared embedding/reranking stays
on HX-4; HX-5 headroom is reserved for CentCom, Ornith, DeepSeek Harness, and dev/test.

### Shared retrieval inference (HX-4)

HX-4 owns the shared retrieval-inference models:

```text
BGE-M3                  -> primary/default embedding model -> 1024 dimensions
Nomic Embed Text v1.5   -> alternate/fallback             -> 768 dimensions default
BGE-family reranker     -> shared reranking               -> exact checkpoint/runtime must be pinned
```

Qdrant on HX-10 stores vectors; it does not own the embedding models. **Never mix embeddings from
different model identities in the same Qdrant collection.** A model change requires a new
collection and complete re-embedding. The exact BGE-family reranker checkpoint and serving
runtime remain explicit implementation decisions and must be pinned before the reranker smoke test
becomes executable.

### Docling model (HX-16)

Granite-Docling 258M stays on HX-16 inside the Docling capability boundary. Base validation is
**CPU-first**; GPU acceleration is considered later only if measured performance justifies it. It is
a document-understanding VLM, not a general shared embedding or conversational model. Do not route
routine Granite-Docling inference through OmniRoute.

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

No production corpus is ingested during base installation; synthetic/throwaway objects are
sufficient for smoke testing.

## Application companion-service rule

Where assigned, a product-specific MCP server or native Web UI is part of the parent application's
**base build**, not a separate later deliverable:

- PostgreSQL includes PostgreSQL MCP.
- Redis includes its assigned Redis MCP.
- Qdrant includes Qdrant + Web UI + Qdrant MCP.
- LightRAG includes LightRAG MCP.
- Docling includes Granite-Docling + Docling MCP.
- Crawl4AI includes Crawl4AI MCP.
- n8n includes n8n MCP.
- Mem0 includes its assigned MCP capability.

**HX-15 FastMCP** is the shared/custom MCP development and runtime host. It is *not a prerequisite*
for these product-specific MCP servers. MCP client registration, agent tool binding, and
permanent orchestration wiring remain integration-phase work.

## Base-build vs integration boundary

### Current program — base stand-up

Each assigned component is installed natively, proven independently, reboot-validated,
documented, and closed before moving on. A component reaches **BASE PASS** only when the host is
cleanly rebuilt and joined to `hx.local.arpa`, required OS packages are installed, the application
runs natively under systemd where applicable, local/LAN health endpoints respond, required storage
is mounted and persistent, any native Web UI is validated directly on its native endpoint, any
assigned MCP server is independently smoke-tested, the defined component smoke test passes using
only the minimum temporary integration required, validation-only state is removed/disabled after
the test, reboot persistence is proven, and the server record is updated.

Small, reversible dependencies may be used only when required to prove a component's primary
function — and only against an already-proven dependency, using synthetic/disposable data, clearly
labeled validation-only, and removed afterward unless explicitly approved as permanent.

### Later program — ecosystem integration

Permanent service contracts, credentials, routing, production schemas/collections, RAG ingestion,
MCP client registrations, agent tool bindings, Open WebUI permanent backends, workflows,
observability, and true end-to-end tests belong to the later integration program. The
integration-readiness gate requires current server records for HX-1 through HX-17 and independent
proof of every assigned service, native Web UI, product-specific MCP endpoint, component smoke
test, cleanup requirement, and reboot-persistence gate.

**Do not mistake smoke-test wiring for permanent architecture.** Temporary smoke-test
dependencies do not automatically become permanent production architecture.

## Validation sits on top of the cornerstone

Validation inherits the ecosystem architecture; it must never redefine server placement, network,
model placement, or component ownership. The validation authorities are:

- `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` — ordered proof dependencies and permitted
  limited validation integration.
- `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md` — how the validation subsystem fits
  together.
- `smoke-tests/` — exact component acceptance procedures (validation only).
- `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` — how HX-5 executes
  and retains proof.
- `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md` — CentCom
  client tooling and bootstrap.

After HX-5 closes its own base inference foundation, CentCom becomes the standard remote execution
station for subsequent component smoke tests. The smoke roadmap is subordinate to deployment
readiness: a component cannot be smoke-tested before its system under test is installed and ready,
and downstream tests reference current prior PASS evidence when they rely on earlier capabilities.

## OmniRoute catalog standard

OmniRoute (HX-6) maintains two explicit controls: an approved **provider allowlist** and, within
an approved provider, an approved **model allowlist**. Discovery/support does not equal approval;
approving a provider does not approve its entire catalog. Free/no-auth/discovered providers are not
automatically active. The initial local catalog is the proven HX-2/HX-3/HX-4/HX-5 Ollama endpoints;
cloud providers/models require explicit owner approval.

## NGINX decision

The former concept of HX-7 as a general reverse proxy is withdrawn. HX-7 NGINX is development/test
UI rendering only — it may proxy an application UI being actively developed when useful, but it is
not the normal routing path for Qdrant, LightRAG, n8n, Open WebUI, databases, MCP servers, or any
other ecosystem service. Normal application UIs remain directly accessible on their own native
server/port.

## AI orientation sequence

Before changing or validating a component, an agent should be able to answer, from current
repository authority:

1. What is HX and what layer is this component in?
2. Which server owns it, at what target IP, and what is that server's current state?
3. What foundational network/domain/deployment rules apply?
4. What upstream dependencies are architecturally required versus validation-only?
5. What model/data placement rules apply?
6. What is the current build priority and BASE PASS boundary?
7. If validating, what prior PASS evidence does the smoke roadmap require?
8. What exact smoke test proves the component works?
9. How is evidence captured, cleanup verified, and closure recorded?

If the agent cannot answer 1–7, it is **not ready to execute validation**.

## Related pages

- `/openwiki/architecture/server-fleet-and-states.md` — per-server states and as-built records.
- `/openwiki/concepts/decisions-and-rules.md` — owner-approved decisions that govern this cornerstone.
- `/openwiki/operations/runbook-blocks-and-pins.md` — the shared runbook blocks and pinned versions.
- `/openwiki/testing/proof-dag-and-evidence.md` — the ordered smoke-test proof roadmap and evidence.
