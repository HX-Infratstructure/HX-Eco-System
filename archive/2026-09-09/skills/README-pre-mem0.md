# HX Eco-System Skills Architecture

`skills/` is the canonical HX capability library for reusable AI-agent expertise.

Skills sit **between HX architecture and execution**. They help an agent reason about a component using current product/vendor expertise, but they do not own HX architecture, server placement, runbooks, smoke-test acceptance criteria, or credentials.

```text
HX OWNER DECISIONS + CURRENT ECOSYSTEM AUTHORITY
                     |
                     v
             HX COMPONENT CONTEXT
                     |
                     v
              HX SKILL WRAPPER
        stable HX rules + task workflow
                     |
                     +----> current official vendor/project guidance
                     |      product expertise only
                     v
             HX RUNBOOK / STANDARD
                     |
                     v
        HX SMOKE ROADMAP + EXACT TEST
                     |
                     v
                 EVIDENCE
```

## Purpose

Use this library to make HX agents more capable without allowing external skill content to become a second architecture authority.

A component skill may assist with:

- planning;
- native installation;
- configuration;
- troubleshooting;
- upgrades/migrations;
- product-specific diagnostics;
- validation preparation;
- interpreting smoke-test failures.

A skill does **not** grant permission to change server assignments, networking, security policy, storage architecture, model placement, permanent integration, or BASE PASS criteria.

## Canonical layout

```text
skills/
├── README.md
├── SKILL-GOVERNANCE.md
├── SKILL-REGISTRY.md
└── <component>/
    ├── README.md
    ├── upstream/
    │   └── SOURCE.md
    └── <hx-wrapper>/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── hx-context.md
            ├── authority-map.md
            ├── upstream.md
            └── community-candidates.md   # only when useful
```

The canonical HX copy lives here. Claude Code, Codex, OpenCode, or other agent-specific skill directories are **deployment targets**, not separate sources of truth.

Do not maintain divergent hand-edited copies per agent.

## Skill classes

| Class | Meaning |
|---|---|
| `HX_NATIVE` | Skill authored specifically for HX. |
| `VENDOR_OFFICIAL` | Skill or skill system published by the product vendor/project. |
| `COMMUNITY` | Third-party skill requiring explicit review before HX use. |
| `WRAPPER` | HX skill that combines HX context/governance with external expertise. |
| `META` | Skill that routes to or dynamically loads narrower skills. |

A skill can have more than one classification, such as `HX_NATIVE + WRAPPER` or `VENDOR_OFFICIAL + META`.

## Operating order

Before using a component skill:

1. read `README.md`, current state, build state, decisions, and architecture orientation;
2. establish the component's HX host, role, current state, dependency boundary, and BASE PASS expectation;
3. read the component's current server record/runbook/standard when it exists;
4. check `SKILL-REGISTRY.md` for the approved HX skill and upstream source;
5. load the HX wrapper;
6. consult current official vendor/project guidance as directed by the wrapper;
7. execute through HX runbook/standard authority;
8. validate through the smoke-test roadmap and exact smoke-test authority.

**Ecosystem first. Skill second. Execution third. Validation fourth.**

## Approved reference implementations

### Qdrant

```text
skills/qdrant/hx-qdrant-advisor/
```

Combines:

- HX-10 architecture and server placement;
- HX native/systemd and clean-room rules;
- HX vector-space/model placement policy;
- Qdrant build/validation authorities;
- live official Qdrant Advisor guidance from `skills.qdrant.tech`.

### LightRAG

```text
skills/lightrag/hx-lightrag-advisor/
```

Combines:

- HX-11 architecture, direct-LAN/native deployment, and RAG boundary;
- HX-10 Qdrant and HX-4 BGE-M3 dependency rules;
- LightRAG build/validation authorities and current authority gaps;
- current official `HKUDS/LightRAG` `AGENTS.md`, API/server docs, `env.example`, releases, and source/tests;
- reviewed community Claude/MCP projects as reference only.

No official Qdrant-style LightRAG `SKILL.md` catalog was found at the 2026-09-09 review, so the HX wrapper consumes the current official project repository rather than promoting a community skill to vendor authority.

### PostgreSQL

```text
skills/postgresql/hx-postgresql-advisor/
```

Combines:

- HX-9 placement, native/systemd and PostgreSQL/Redis shared-host boundaries;
- PostgreSQL BASE and MCP validation authorities;
- current PostgreSQL Global Development Group documentation, releases, versioning and Ubuntu packaging guidance as primary product truth;
- the open Agent Skills format from `agentskills.io`;
- reviewed Neon `neondatabase/postgres-skills` practitioner guidance as `COMMUNITY / expert reference`, not PGDG authority.

The wrapper deliberately does not choose the HX-9 PostgreSQL major, package source, data placement, listener/authentication pattern, HA/replication, PgBouncer, backup/PITR topology, or MCP implementation before the HX-9 runbook pins those choices.

### Redis

```text
skills/redis/hx-redis-advisor/
```

Combines:

- HX-9 placement, native/systemd and PostgreSQL/Redis shared-host boundaries;
- Redis BASE and MCP validation authorities;
- current official Redis documentation, source, releases and packaging guidance as primary product truth;
- reviewed official `redis/agent-skills` as `VENDOR_OFFICIAL` agent expertise;
- HX-specific curation for topology, security/network authority, standalone operation and evidence-based closure.

The wrapper does not install the upstream eight-skill bundle as a second HX source of truth. Core, connections, Search and observability guidance are accepted/adapted; Cluster/replication and Redis Cloud-only AI services remain reference-only for current BASE; TLS/firewall/bind/global-command hardening remains owner-controlled. The current upstream release/skill commit records provenance and does not by itself select the HX-9 runtime version, package source, data/persistence/memory policy, or Redis MCP implementation.

## Governance

`SKILL-GOVERNANCE.md` defines admission, trust, authority precedence, version/provenance, update, testing, secret-handling, deployment, and retirement rules.

`SKILL-REGISTRY.md` is the current inventory of approved, pilot, discovery, blocked, and retired component skills.
