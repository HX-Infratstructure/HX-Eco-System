---
document: HX Eco-System Skill Registry
status: current
version: 1.2
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

## Discovery backlog

These rows intentionally do not invent external sources. Add a source only after it is actually found and reviewed.

| Component | HX host | Canonical HX skill | Upstream source | Status | Expected use |
|---|---|---|---|---|---|
| Samba AD/DNS/Kerberos/NTP | HX-1 | TBD | TBD | `DISCOVERY` | foundation administration/troubleshooting |
| Ollama / inference | HX-2/3/4/5 | TBD | TBD | `DISCOVERY` | native install/config/model serving/troubleshooting |
| Redis | HX-9 | TBD | TBD | `DISCOVERY` | install/config/persistence/client/performance/upgrade |
| OmniRoute | HX-6 | TBD | TBD | `DISCOVERY` | provider/model routing/configuration |
| NGINX | HX-7 | TBD | TBD | `DISCOVERY` | dev/test proxy configuration only |
| Open WebUI | HX-8 | TBD | TBD | `DISCOVERY` | native install/config/model connection/UI troubleshooting |
| Deep Agents | HX-12 | TBD | TBD | `DISCOVERY` | LOB agent factory/runtime/tool calling |
| Mem0 | HX-13 | TBD | TBD | `DISCOVERY` | memory providers/configuration/lifecycle |
| n8n | HX-14 | TBD | TBD | `DISCOVERY` | native workflow runtime/configuration/MCP |
| FastMCP | HX-15 | TBD | TBD | `DISCOVERY` | MCP server/tool design/runtime/client behavior |
| Docling / Granite-Docling | HX-16 | TBD | TBD | `DISCOVERY` | document conversion/VLM/native runtime |
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
