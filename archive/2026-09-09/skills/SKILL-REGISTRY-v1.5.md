---
document: HX Eco-System Skill Registry
status: current
version: 1.5
date: 2026-09-09
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Skill Registry

This is the current inventory and trust/status registry for reusable AI-agent skills used by the HX Eco-System.

`SKILL-GOVERNANCE.md` controls admission and use. A registry entry does not supersede current HX architecture, runbooks, live evidence, or smoke-test authority.

## Active / approved

| Component | HX host | Canonical HX skill | Class | Primary upstream | Upstream mode | Status | HX use | Companion capability | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|
| Qdrant | HX-10 | `skills/qdrant/hx-qdrant-advisor/` | `HX_NATIVE + WRAPPER` | Qdrant `qdrant/skills` → `meta/qdrant-advisor` | live `skills.qdrant.tech` Advisor; reviewed commit `b0941d03eddf88629306aa16588383400e68230b` | **APPROVED** | plan, native install/config reasoning, validation preparation, troubleshoot, optimize, migrate, upgrade | Qdrant Web UI + Qdrant MCP | 2026-09-09 |
| LightRAG | HX-11 | `skills/lightrag/hx-lightrag-advisor/` | `HX_NATIVE + WRAPPER` | official `HKUDS/LightRAG` repository; no official LightRAG `SKILL.md` catalog found | verify current release/main + `AGENTS.md`/docs/`env.example`; reviewed main `d964d92b1018c27983d1dcf6ca19ebbaebeb262e`, release `v1.5.7` | **APPROVED** | plan, native install/config reasoning, storage/model reconciliation, validation preparation, troubleshoot, migrate, upgrade; execution only through future HX-11 runbook | LightRAG MCP | 2026-09-09 |
| PostgreSQL | HX-9 | `skills/postgresql/hx-postgresql-advisor/` | `HX_NATIVE + WRAPPER` | PostgreSQL Global Development Group docs/releases + reviewed Neon `neondatabase/postgres-skills` | PGDG is product authority; Neon Agent Skill reviewed at `27fe45e0f71ea89a6eaf9ea4d2e4068957c81c26`; Agent Skills format from `agentskills.io` | **APPROVED** | plan, native install/config reasoning, SQL/schema/index/query expertise, diagnostics, validation preparation, backup/restore and upgrade planning; execution only through future HX-9 runbook | PostgreSQL MCP | 2026-09-09 |
| Redis | HX-9 | `skills/redis/hx-redis-advisor/` | `HX_NATIVE + WRAPPER` | Redis official docs/releases + official `redis/agent-skills` | Redis product guidance is primary; reviewed Agent Skills main `a84871d065f398fed55e1633f66b66f731eb4e2b`, plugin `redis-development` 1.4.0; latest non-prerelease Redis release at review 8.10.1 | **APPROVED** | plan, native standalone install/config reasoning, persistence/recovery, memory/eviction, data modeling/TTL, clients, Search/JSON/vector/RAG, Streams/coordination, observability, validation preparation, troubleshoot and upgrade; execution only through future HX-9 runbook | Redis MCP | 2026-09-09 |
| Mem0 | HX-13 | `skills/mem0/hx-mem0-advisor/` | `HX_NATIVE + WRAPPER` | official `mem0ai/mem0` docs/source + official six-skill graph | product docs/source primary; reviewed main `02f7a9b2c4fe38dedb96631e48c85c74ad58b605`; Python source 2.0.20, TypeScript source 3.1.6; official skills catalog 6; portable agent plugin 0.3.1 | **APPROVED** | plan, native OSS install/config reasoning, memory lifecycle/scoping, Qdrant/Ollama integration, SDK/framework expertise, validation preparation, troubleshooting and upgrade; Platform/Vercel/repository-writing pipelines gated; execution only through future HX-13 runbook | assigned Mem0 MCP — implementation not yet selected | 2026-09-09 |
| Docling / Granite-Docling | HX-16 | `skills/docling/hx-docling-advisor/` | `HX_NATIVE + WRAPPER` | official `docling-project/docling` docs/source + packaged usage skill + official `docling-project/docling-mcp` | product guidance primary; reviewed Docling main `cdc2477e12107f45bf8b6813571f31f9e795ba07`, release `v2.126.0`, usage SKILL blob `f6bdfa26aee4b0df5a4cdfb6b496286e3b9eedd6`; Docling MCP main `a8a41e6014ba3a148261702e760421086e9c80e3`, release 3.2.0 | **APPROVED** | plan, native install/config reasoning, multi-format conversion, OCR/tables/layout, Granite-Docling CPU-first VLM, extraction/RAG/package expertise when in scope, validation preparation, troubleshooting and upgrade; remote/managed/container/RAG integration gated; execution only through future HX-16 runbook | official Docling MCP source; exact mode/transport/service layout runbook-controlled | 2026-09-09 |

## Discovery backlog

These rows intentionally do not invent external sources. Add a source only after it is actually found and reviewed.

| Component | HX host | Canonical HX skill | Upstream source | Status | Expected use |
|---|---|---|---|---|---|
| Samba AD/DNS/Kerberos/NTP | HX-1 | TBD | TBD | `DISCOVERY` | foundation administration/troubleshooting |
| Ollama / inference | HX-2/3/4/5 | TBD | TBD | `DISCOVERY` | native install/config/model serving/troubleshooting |
| OmniRoute | HX-6 | TBD | TBD | `DISCOVERY` | provider/model routing/configuration |
| NGINX | HX-7 | TBD | TBD | `DISCOVERY` | dev/test proxy configuration only |
| Open WebUI | HX-8 | TBD | TBD | `DISCOVERY` | native install/config/model connection/UI troubleshooting |
| Deep Agents | HX-12 | TBD | TBD | `DISCOVERY` | LOB agent factory/runtime/tool calling |
| n8n | HX-14 | TBD | TBD | `DISCOVERY` | native workflow runtime/configuration/MCP |
| FastMCP | HX-15 | TBD | TBD | `DISCOVERY` | MCP server/tool design/runtime/client behavior |
| Crawl4AI | HX-17 | TBD | TBD | `DISCOVERY` | crawl/extraction/native runtime/MCP |
| BGE-M3 / Nomic / reranker | HX-4 | TBD | TBD | `DISCOVERY` | embedding/reranking serving/model migration |

## Community/reference candidates under review

| Component | Source | Classification | Status | Notes |
|---|---|---|---|---|
| PostgreSQL | `neondatabase/postgres-skills` → `postgres-best-practices` | `COMMUNITY / EXPERT REFERENCE` | `APPROVED_AS_REFERENCE` | Agent Skills-compatible practitioner guidance; PGDG remains product authority. Do not direct-install as a second HX source. |
| LightRAG | `zwovadis/lightrag-claude-skill` | `COMMUNITY` | `REFERENCE_ONLY` | Query-oriented Claude Code skill; not install/config authority; assumptions must be checked against current HKUDS API docs and HX network placement. |
| LightRAG | `butchokoy25/lightrag-claude-skills` | `COMMUNITY` | `REFERENCE_ONLY / LATER_INTEGRATION` | Seven Claude skills + session hooks/helpers/MCP config for persistent memory; not part of HX-11 BASE build. |
| LightRAG MCP | `desimpkins/daniel-lightrag-mcp` | `COMMUNITY` | `DISCOVERY` | Example community MCP candidate; exact HX LightRAG MCP implementation remains to be selected/reviewed. |

## Qdrant provenance

```text
Vendor: Qdrant
Repository: qdrant/skills
Current reviewed main: b0941d03eddf88629306aa16588383400e68230b
Official live catalog: https://skills.qdrant.tech
Official meta-skill: meta/qdrant-advisor
HX wrapper: skills/qdrant/hx-qdrant-advisor/
```

## LightRAG provenance

```text
Project: LightRAG
Organization: HKUDS
Repository: HKUDS/LightRAG
Current reviewed main: d964d92b1018c27983d1dcf6ca19ebbaebeb262e
Latest reviewed release: v1.5.7
Official LightRAG SKILL.md catalog found: NO
HX wrapper: skills/lightrag/hx-lightrag-advisor/
```

The LightRAG wrapper consumes current official project guidance directly. Community agent skills/MCPs remain subordinate reference candidates unless separately admitted.

## PostgreSQL provenance

```text
Project authority: PostgreSQL Global Development Group
Current upstream context at review: PostgreSQL 18.6; PostgreSQL 19 still beta
Agent Skills standard: https://agentskills.io/
Reviewed external skill: neondatabase/postgres-skills
Reviewed Neon main: 27fe45e0f71ea89a6eaf9ea4d2e4068957c81c26
Reviewed Neon skill blob: 1720cf9fb7e7c31795433756d4bea154b5512d0f
HX classification of Neon source: COMMUNITY / expert reference
HX wrapper: skills/postgresql/hx-postgresql-advisor/
```

PostgreSQL major version, package source, data placement, listener/authentication pattern, HA/pooling/backup topology, and exact PostgreSQL MCP implementation remain owner/runbook decisions for HX-9. Skill approval does not advance HX-9 build state.

## Redis provenance

```text
Project authority: Redis official documentation, source, and releases
Current upstream context at review: Redis 8.10.1, published 2026-08-17
Official Agent Skills: redis/agent-skills
Reviewed Agent Skills main: a84871d065f398fed55e1633f66b66f731eb4e2b
Reviewed plugin: redis-development 1.4.0
Reviewed source skills: 8
Upstream license: MIT
HX classification of upstream skill source: VENDOR_OFFICIAL
HX wrapper: skills/redis/hx-redis-advisor/
```

HX intentionally curates the official Redis bundle rather than direct-installing it as a second authority. `redis-core`, `redis-connections`, `redis-search`, and `redis-observability` are accepted/adapted. `redis-security` is adapted under owner-controlled network/security rules. `redis-clustering`, Redis Cloud LangCache, and managed Agent Memory guidance are reference-only for current BASE unless separately admitted. Redis skill approval does not advance HX-9 build state or select the runtime version/package source, service/data path, persistence/memory policy, network/auth topology, or exact Redis MCP implementation.

## Mem0 provenance

```text
Project authority: official Mem0 documentation and source
Repository: mem0ai/mem0
Reviewed main: 02f7a9b2c4fe38dedb96631e48c85c74ad58b605
Python source version: 2.0.20
TypeScript source version: 3.1.6
Official Agent Skills: 6
Reference skills: mem0 3.0.0; mem0-cli 1.1.0; mem0-vercel-ai-sdk 1.1.0
Pipeline skills: mem0-integrate 0.1.0; mem0-test-integration 0.1.0; mem0-oss-to-platform
Portable agent plugin: integrations/mem0-agent-plugin 0.3.1; stdio MCP
Standalone mem0ai/mem0-mcp: ARCHIVED
HX classification of upstream skill source: VENDOR_OFFICIAL
HX wrapper: skills/mem0/hx-mem0-advisor/
```

HX intentionally curates the official Mem0 six-skill graph rather than direct-installing it as a second authority. The `mem0` reference skill is adapted to the native/self-hosted HX-13 OSS role; CLI, Vercel, repository integration/testing pipelines, hosted Platform, and coding-assistant plugin/MCP guidance remain gated or reference-only unless separately admitted. `mem0-oss-to-platform` conflicts with the current HX-13 runtime and is not active guidance unless the owner changes the architecture. Mem0 skill approval does not advance HX-13 build state or select package version, environment/service layout, config/data paths, permanent Qdrant/model bindings, memory lifecycle policy, network/access pattern, or the exact assigned Mem0 MCP implementation.

## Docling provenance

```text
Project authority: official Docling documentation, source, and releases
Repository: docling-project/docling
Reviewed main: cdc2477e12107f45bf8b6813571f31f9e795ba07
Latest reviewed release: v2.126.0, published 2026-09-04
Official packaged Agent Skill: docling/.agents/skills/docling/
Reviewed usage SKILL blob: f6bdfa26aee4b0df5a4cdfb6b496286e3b9eedd6
Reviewed on-demand usage references: 6
Granite preset: granite_docling -> Granite-Docling-258M
Docling MCP repository: docling-project/docling-mcp
Reviewed MCP main: a8a41e6014ba3a148261702e760421086e9c80e3
Latest reviewed MCP release/package: v3.2.0, published 2026-09-01
Upstream licenses: MIT
HX classification of upstream skill and companion sources: VENDOR_OFFICIAL
HX wrapper: skills/docling/hx-docling-advisor/
```

HX intentionally curates the one packaged Docling usage skill rather than direct-installing it as a second authority. Local CLI/Python SDK, structured document, OCR/table/layout, and Granite-Docling expertise are accepted/adapted. `DocumentExtractor` beta, RAG/framework loaders, repository-root contributor skills, `library-skills` deployment, remote Service Client/VLM patterns, and `uvx` quickstarts remain gated or reference-only according to scope. Containerized Docling Serve and managed-service replacement conflict with current HX architecture. The official Docling MCP project is the preferred companion source, but exact package/mode/transport/service decisions remain future HX-16 runbook choices. The D1 Docling/Granite -> D2 Docling MCP smoke chain remains unchanged. Skill approval does not advance HX-16 build state or select package/extras, Python environment, model revision/cache, service/listener layout, or permanent RAG/MCP client integration.

## Registry update fields

When adding another technology, record at minimum:

```text
component
hx_host_or_scope
canonical_hx_skill
classification
provider/source
source_url_or_repository
reviewed_version_or_commit
live_or_pinned_consumption_mode
status
trigger/use_cases
execution_authority
smoke_test_authority
associated_mcp_plugin_hook
known_hx_conflicts
last_reviewed
```
