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
                     +----> current vendor skill/docs
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
            └── upstream.md
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
| `META` | Skill that routes to or dynamically loads more specialized skills. |

A skill can have more than one classification, such as `HX_NATIVE + WRAPPER` or `VENDOR_OFFICIAL + META`.

## Operating order

Before using a component skill:

1. read `README.md`, current state, build state, decisions, and architecture orientation;
2. establish the component's HX host, role, current state, dependency boundary, and BASE PASS expectation;
3. read the component's current server record/runbook/standard;
4. check `SKILL-REGISTRY.md` for the approved HX skill and upstream source;
5. load the HX wrapper;
6. consult current vendor guidance as directed by the wrapper;
7. execute through HX runbook/standard authority;
8. validate through the smoke-test roadmap and exact smoke-test authority.

**Ecosystem first. Skill second. Execution third. Validation fourth.**

## Initial reference implementation

Qdrant is the first governed HX component skill:

```text
skills/qdrant/hx-qdrant-advisor/
```

It combines:

- HX-10 architecture and server placement;
- HX native/systemd and clean-room rules;
- HX vector-space/model placement policy;
- Qdrant build/validation authorities;
- live official Qdrant Advisor guidance from `skills.qdrant.tech`.

See `skills/qdrant/README.md`.

## Governance

`SKILL-GOVERNANCE.md` defines admission, trust, authority precedence, version/provenance, update, testing, secret-handling, deployment, and retirement rules.

`SKILL-REGISTRY.md` is the current inventory of approved, pilot, discovery, blocked, and retired component skills.
