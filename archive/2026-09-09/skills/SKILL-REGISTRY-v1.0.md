---
document: HX Eco-System Skill Registry
status: current
version: 1.0
date: 2026-09-09
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Skill Registry

This is the current inventory and trust/status registry for reusable AI-agent skills used by the HX Eco-System.

`SKILL-GOVERNANCE.md` controls admission and use. A registry entry does not supersede current HX architecture, runbooks, live evidence, or smoke-test authority.

## Active / approved

| Component | HX host | Canonical HX skill | Class | Upstream | Upstream mode | Status | HX use | Companion capability | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|
| Qdrant | HX-10 | `skills/qdrant/hx-qdrant-advisor/` | `HX_NATIVE + WRAPPER` | Qdrant `qdrant/skills` → `meta/qdrant-advisor` | live `skills.qdrant.tech` Advisor; reviewed commit `b0941d03eddf88629306aa16588383400e68230b` | **APPROVED** | plan, native install/config reasoning, validation preparation, troubleshoot, optimize, migrate, upgrade | Qdrant Web UI + Qdrant MCP | 2026-09-09 |

## Discovery backlog

These rows intentionally do not invent external sources. Add a source only after it is actually found and reviewed.

| Component | HX host | Canonical HX skill | Upstream source | Status | Expected use |
|---|---|---|---|---|---|
| Samba AD/DNS/Kerberos/NTP | HX-1 | TBD | TBD | `DISCOVERY` | foundation administration/troubleshooting |
| Ollama / inference | HX-2/3/4/5 | TBD | TBD | `DISCOVERY` | native install/config/model serving/troubleshooting |
| PostgreSQL | HX-9 | TBD | TBD | `DISCOVERY` | install/config/client/admin/performance/upgrade |
| Redis | HX-9 | TBD | TBD | `DISCOVERY` | install/config/persistence/client/performance/upgrade |
| OmniRoute | HX-6 | TBD | TBD | `DISCOVERY` | provider/model routing/configuration |
| NGINX | HX-7 | TBD | TBD | `DISCOVERY` | dev/test proxy configuration only |
| Open WebUI | HX-8 | TBD | TBD | `DISCOVERY` | native install/config/model connection/UI troubleshooting |
| LightRAG | HX-11 | TBD | TBD | `DISCOVERY` | native install/config/RAG/storage/model integration |
| Deep Agents | HX-12 | TBD | TBD | `DISCOVERY` | LOB agent factory/runtime/tool calling |
| Mem0 | HX-13 | TBD | TBD | `DISCOVERY` | memory providers/configuration/lifecycle |
| n8n | HX-14 | TBD | TBD | `DISCOVERY` | native workflow runtime/configuration/MCP |
| FastMCP | HX-15 | TBD | TBD | `DISCOVERY` | MCP server/tool design/runtime/client behavior |
| Docling / Granite-Docling | HX-16 | TBD | TBD | `DISCOVERY` | document conversion/VLM/native runtime |
| Crawl4AI | HX-17 | TBD | TBD | `DISCOVERY` | crawl/extraction/native runtime/MCP |
| BGE-M3 / Nomic / reranker | HX-4 | TBD | TBD | `DISCOVERY` | embedding/reranking serving/model migration |

## Qdrant provenance

Official source reviewed:

```text
Vendor: Qdrant
Repository: qdrant/skills
Current reviewed main: b0941d03eddf88629306aa16588383400e68230b
Official live catalog: https://skills.qdrant.tech
Official meta-skill: meta/qdrant-advisor
HX wrapper: skills/qdrant/hx-qdrant-advisor/
```

The Qdrant Advisor is consumed as current vendor expertise. The HX wrapper is the local control surface that preserves HX architecture and points the agent to current execution/validation authorities.

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
