---
type: governance concept
title: Governed Skills Capability Layer
description: The skills/ capability layer — what skills may and may not do, the loading order, the registry, pinned upstream commits, classifications, and the drift check that reports when a pinned commit moves.
tags: [skills, governance, capability-layer, registry, drift, agent-expertise]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-15T22:39:27.588Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-6ff476d421611f1f320003de
    resource: repo://skills/AGENTS.md
  - id: openwiki-source-8331ceaff0986ff6678a4efa
    resource: repo://skills/qdrant/hx-qdrant-advisor/SKILL.md
  - id: openwiki-source-49a96b71ece2c9d316061511
    resource: repo://skills/qdrant/README.md
  - id: openwiki-source-446437c63473d8e7dd04c604
    resource: repo://skills/README.md
  - id: openwiki-source-5c5fbd51a83e8c2377f4b8ef
    resource: repo://skills/SKILL-GOVERNANCE.md
  - id: openwiki-source-30873c060e08a1a79b2044e7
    resource: repo://skills/SKILL-REGISTRY.md
  - id: openwiki-source-1b6936d3e99ab8243153e1c6
    resource: repo://tools/hx-doc/hx_upstream_drift.py
  - id: openwiki-source-f2994b36a477b8759d39a2a6
    resource: repo://tools/hx-doc/README.md
generated: { by: "openwiki/0.5.1", at: "2026-09-15T22:39:27.588Z" }
---

## What this layer is, and what it is not

`skills/` is the canonical HX capability library for reusable AI-agent
expertise. It sits **between HX architecture and execution**: it helps an agent
reason about a component using current product/vendor expertise, but it does
not own HX architecture, server placement, runbooks, smoke-test acceptance
criteria, or credentials. The layer was established by decision **D-017**,
which records that component skills may combine HX-native instructions with
current vendor-official expertise, but never supersede owner decisions, active
HX architecture, live evidence, runbooks, or smoke-test acceptance criteria.

This page is context, not authority. The authorities for this layer are
`skills/SKILL-GOVERNANCE.md`, `skills/SKILL-REGISTRY.md`, and `AGENTS.md`
section 6. A registry entry does not supersede current HX architecture,
runbooks, live evidence, or smoke-test authority.

The governing principle is one sentence: **skills augment HX expertise; they do
not define HX architecture.** If current official vendor guidance exposes a
real incompatibility in an HX runbook, the contradiction is reported and the
smallest affected HX authority updated through normal review — never silently
overridden from inside a skill.

## The governance files

Four files in `skills/` govern the layer. An agent reads them in this order
before operational use of a component skill:

| File | Role |
|---|---|
| `skills/README.md` | Entry point and orientation: what the library is, the canonical location, the classification table, the per-component wrapper inventory, and the loading steps. |
| `skills/SKILL-GOVERNANCE.md` | The rulebook: admission, trust/authority precedence, version/provenance, wrapper rule, architecture-conflict rule, execution-artifact rule, validation rule, secret handling, packaging/quality gate, update, and retirement. |
| `skills/SKILL-REGISTRY.md` | The live inventory and trust/status registry: approved, pilot, discovery, blocked, and retired skills, with pinned upstream commits and provenance blocks. |
| `skills/AGENTS.md` | Agent operating instructions scoped to `skills/`: reading order, non-negotiable rules, and the workflow for adding a component skill. |

The canonical HX skill library is the `skills/` directory itself:

```text
skills/
```

Agent-specific skill locations (Claude Code, Codex, OpenCode, etc.) are
**derived deployments only**, not separate sources of truth. Do not create or
maintain divergent hand-edited copies per agent; deploy from the canonical
directory or from a reviewed package built from it.

## The loading order

Skills are loaded after HX context, after the component runbook, and before
current vendor guidance is reconciled and executed. The full truth order for a
governed skill, as stated in `SKILL-GOVERNANCE.md`, is:

```text
    > CURRENT HX CONTROL / ARCHITECTURE
    > LIVE HX EVIDENCE
    > CURRENT HX RUNBOOK / STANDARD
    > GOVERNED HX SKILL + CURRENT OFFICIAL VENDOR GUIDANCE
    > HISTORICAL REFERENCE
    > GENERAL MODEL KNOWLEDGE
```

Stated as the operational sequence an agent follows:

```
HX context -> component runbook -> HX skill wrapper -> current vendor guidance
            -> reconcile with HX decisions -> execute from HX authority
```

Before using a component skill, an agent:

1. reads the component's HX architecture and runbook;
2. reads `skills/SKILL-GOVERNANCE.md`;
3. reads `skills/SKILL-REGISTRY.md`;
4. checks `SKILL-REGISTRY.md` for the approved HX skill and upstream source;
5. loads the HX wrapper `SKILL.md`;
6. loads only the wrapper references needed for the task;
7. executes through HX runbook/standard authority;
8. validates through the smoke-test roadmap and the exact smoke-test authority.

The load order is the point: HX context loads first, vendor advice loads after,
and HX wrappers load current HX context before vendor/community guidance.

## What skills may and may not do

A component skill **may assist with**:

- planning;
- native installation;
- native configuration reasoning;
- troubleshooting;
- upgrades/migrations;
- validation preparation.

A skill **does not** grant permission to change server assignments, networking,
security policy, storage architecture, model placement, permanent integration,
or BASE PASS criteria. External skills **cannot authorize**:

- moving a workload to another HX server;
- introducing Docker, Podman, Kubernetes, or another container platform;
- replacing local/native deployment with vendor Cloud or embedded deployment;
- changing gateway, DNS, AD/domain, NTP, routing, or network topology;
- adding firewall/TLS/access restrictions without owner approval;
- repartitioning/mounting/reusing disks outside current authority;
- changing shared model placement;
- changing permanent cross-service integration;
- modifying smoke-test PASS criteria during a run.

When vendor guidance recommends one of these, it is classified as
`OWNER_DECISION_REQUIRED` or `REJECT_FOR_HX` according to current owner
decisions.

A skill may contain deterministic helper scripts when they materially improve
repeatability, but infrastructure-changing code must not become hidden
execution authority inside a skill. Runbooks and approved execution artifacts
remain under the repository runbook/standards structure; skills tell agents what
to consider, what to check, and which authority to execute. No vendor installer
is run merely because a skill suggests it.

### Validation boundary

Skills can assist with validation reasoning, but HX smoke-test authorities
remain decisive. A vendor quickstart, health endpoint, or vendor skill does not
replace the smoke-test roadmap, the exact file under `smoke-tests/`, CentCom
cleanup/evidence rules, reboot persistence, or server-record/BUILD-STATE
closure. If a vendor skill reveals that an HX smoke test is technically invalid
for the current version, the run is stopped, the authority corrected in a
separate reviewed change, and a new run ID used.

Skill approval is **guidance only**. It never changes the build state of any
server; `Wrapper validated` in the registry records that the HX wrapper itself
was reviewed, not that the component was installed.

## Skill classifications

Every skill carries one or more classifications:

| Class | Meaning |
|---|---|
| `HX_NATIVE` | Authored for HX and governed entirely by HX. |
| `VENDOR_OFFICIAL` | Published by the software vendor/project; the preferred external source class for product expertise. |
| `COMMUNITY` | Published by a third party; requires explicit review of provenance, scope, behavior, links/scripts, and architecture assumptions before moving beyond `DISCOVERY` or `PILOT`. |
| `WRAPPER` | HX-authored skill that loads HX context first, then invokes or consults an external skill/source. The preferred pattern for vendor skills that may otherwise recommend architecture choices outside HX policy. |
| `META` | Skill that routes to or dynamically loads narrower skills; useful when the upstream knowledge base changes frequently. |

A skill can have more than one classification, such as `HX_NATIVE + WRAPPER` or
`VENDOR_OFFICIAL + META`. Vendor-official skills are preferred over community
skills for product-specific reasoning when both cover the same problem.

## The registry and its lifecycle states

`SKILL-REGISTRY.md` is the current inventory of approved, pilot, discovery,
blocked, and retired component skills. Use only these lifecycle states:

- `DISCOVERY` — source identified; not approved for operational use.
- `PILOT` — reviewed enough for bounded evaluation.
- `APPROVED` — validated for the stated HX scope.
- `BLOCKED` — known conflict/risk prevents use.
- `RETIRED` — no longer active; provenance/history retained as required.

Two further states apply to sources HX consults but never installs as a second
authority. They are registry states, not admission grades:

- `APPROVED_AS_REFERENCE` — reviewed and approved to be consulted as expert
  reference. It is not an HX authority and is not installed or deployed.
- `REFERENCE_ONLY` — retained for context or future evaluation; not approved
  for operational use. Add `/ LATER_INTEGRATION` when the source is expected to
  be re-evaluated for a later programme phase.

Approval is scoped: a skill approved for troubleshooting is not automatically
approved to execute infrastructure changes.

### Admission checklist

Before a new external skill becomes `APPROVED`, the registry records:
component and HX host/role, source organization/project, source URL/repository,
vendor/community classification, the exact reviewed version/commit when
available, live-update behavior if any, intended triggers and use cases,
associated runbook/standard, associated smoke-test authority, associated
MCP/plugin/hook, known conflicts with HX architecture, whether an HX wrapper is
required, and the validation result for the HX wrapper/package.

### Execution and validation bindings

Governance requires an associated runbook/standard, an associated smoke-test
authority, and a wrapper validation result for every `APPROVED` skill. These are
recorded as registry fields, not only in prose.

## Approved wrappers and pinned upstream commits

Seven governed wrappers are `APPROVED`. Each is `HX_NATIVE + WRAPPER`, each
consumes current upstream product guidance as live authority, and each pins
the exact upstream commit reviewed against. A pin records provenance; it does
not by itself select the HX runtime version, package source, data placement,
service topology, or MCP implementation — those remain owner/runbook decisions.

| Component | HX host | Wrapper | Upstream mode |
|---|---|---|---|
| Qdrant | HX-10 | `skills/qdrant/hx-qdrant-advisor/` | live `skills.qdrant.tech` Advisor; reviewed `qdrant/skills` commit `b0941d03…` |
| LightRAG | HX-11 | `skills/lightrag/hx-lightrag-advisor/` | official `HKUDS/LightRAG`; reviewed main `d964d92b…`, release `v1.5.7` |
| PostgreSQL | HX-9 | `skills/postgresql/hx-postgresql-advisor/` | PGDG primary; Neon `neondatabase/postgres-skills` reviewed at `27fe45e0…` as community reference |
| Redis | HX-9 | `skills/redis/hx-redis-advisor/` | official `redis/agent-skills` `VENDOR_OFFICIAL`; reviewed main `a84871d0…`, plugin `redis-development` 1.4.0 |
| Mem0 | HX-13 | `skills/mem0/hx-mem0-advisor/` | official `mem0ai/mem0` six-skill graph; reviewed main `02f7a9b2…` |
| Docling / Granite-Docling | HX-16 | `skills/docling/hx-docling-advisor/` | official `docling-project/docling`; reviewed main `cdc2477e…`, release `v2.126.0`; Docling MCP `a8a41e60…` |
| Crawl4AI | HX-17 | `skills/crawl4ai/hx-crawl4ai-advisor/` | official `unclecode/crawl4ai`; reviewed main `862f6bcc…`, release `v0.9.3`; `brettdavies/crawl4ai-skill` community reference |

Each provenance block in `SKILL-REGISTRY.md` names the repository and the
reviewed 40-character commit in plain text. The wrapper dispositions vary by
component — Redis accepts/adapts core, connections, Search and observability
while keeping Cluster/replication and Redis Cloud reference-only; Mem0 adapts
the `mem0` reference skill for OSS use and rejects `mem0-oss-to-platform` for
the current runtime; Docling rejects containerized Docling Serve; Crawl4AI
rejects the Docker-coupled MCP layout and does not copy the community SDK
mirror. In every case, gated items stay gated until an owner decision or the
future host runbook pins them.

## Qdrant: the reference implementation

Qdrant is the first approved reference implementation of the governed skill
architecture, at `skills/qdrant/hx-qdrant-advisor/`. It establishes the pattern
future component skills follow.

The wrapper is an HX-native wrapper around current official Qdrant expertise.
It establishes HX context first, then uses Qdrant's official Advisor model to
fetch only the current skill branch relevant to the task. The live Qdrant
Advisor pattern is the default whenever web/HTTP access is available; if live
access is unavailable, the official `qdrant/skills` repository is fallback
context and the guidance is explicitly flagged as possibly less current than a
live Advisor fetch. This live/meta-skill model is preferred over vendoring the
full tree, because Qdrant's Advisor is designed to load the current skill
hierarchy live and a static copy would create duplication and staleness risk.

Per D-017, the Qdrant wrapper consumes current official Qdrant Advisor guidance
live **while preserving HX-10 / native-systemd / vector-space / smoke-test
rules**. Vendor expertise may influence Qdrant-specific configuration and
diagnosis, but it cannot by itself change server placement: Qdrant
Cloud/embedded as a replacement for HX-10 is `REJECT_FOR_HX` unless the owner
changes placement, and horizontal cluster expansion is `OWNER_DECISION_REQUIRED`.
Vector-space integrity is preserved — vectors from different embedding model
identities are never mixed in one collection, and Qdrant named-vector capability
does not override that HX policy unless the owner changes it.

## The drift check

`tools/hx-doc/hx-upstream-drift` reports when a registry-pinned upstream commit
moves. Seven governed skills consume upstream product guidance as live
authority; the registry pins the exact commit each was reviewed at, alongside a
"Last reviewed" date, and nothing previously told the owner when an upstream
moved on.

The tool reads the pins out of the registry itself, so it cannot fall out of
step with the registry the way a second hard-coded list would. It parses each
`## <Component> provenance` block, pairs repository lines with reviewed-commit
lines, and errors out if a block lists an unequal number of repositories and
commits (because `zip()` would otherwise pair a repository with another entry's
commit and report drift against the wrong thing). For each pin it queries the
GitHub API for the upstream HEAD, compares it to the pinned SHA, and reports
`current`, `<n> behind -> <head>`, or an unreachable error.

```bash
tools/hx-doc/hx-upstream-drift              # human-readable report
tools/hx-doc/hx-upstream-drift --fail-on-drift   # exit 1 when any pin is behind
tools/hx-doc/hx-upstream-drift --markdown   # table for an issue body
```

`--fail-on-drift` also fails on an unreachable upstream: an unreachable upstream
is not evidence that a pin is current, so returning 0 on a network failure
would make the gate pass silently. The tool runs weekly in CI alongside
`hx-version-pins` and opens one issue when something moves.

**Drift is information, not a failure.** A pin stays valid until the owner
moves it. The report tells the owner to re-review the drifted sources, then
update the reviewed commit and "Last reviewed" date in `SKILL-REGISTRY.md`.
For live vendor meta-skills, a new upstream commit does not require copying new
vendor content into HX; re-review when upstream behavior, trust, or the
HX-relevant guidance materially changes.

## Secrets and credentials

Skills **never** contain actual passwords, PATs, API keys, bearer tokens,
private keys, service-account secrets, or `sshpass` passwords. A skill may
document credential **names**, environment-variable identifiers, secret-store
names, and the required access pattern. Credential handoff to agents is handled
through a separate owner-approved cornerstone completion/handoff process; the
skill library is not a secret store.

## Adding, updating, and retiring a skill

A new HX wrapper skill must have valid `SKILL.md` frontmatter, keep the name
lowercase and hyphenated, include required agent metadata where used by the
packaging workflow, remove unneeded template/example files, pass the current
skill validator, package successfully before being marked `APPROVED`, and
remain below the platform package-size limit. If scripts are included,
representative validation runs before approval. The Redis wrapper's
`redis-readonly-audit.sh` is an example helper: read-only, it discovers
Redis-named systemd units rather than assuming a package-specific name, and it
passes shell-syntax validation plus a representative no-Redis run.

When an HX skill changes: update the canonical source under `skills/`; update
the registry if scope/status/upstream provenance changed; validate and package
again; update agent deployment copies only from the canonical version; archive
superseded governance/registry documents under normal document control.

Retire a skill when the component leaves the HX architecture, the upstream
source is abandoned/untrusted, a better authoritative skill supersedes it, the
wrapper no longer matches HX architecture, or the skill creates unacceptable
ambiguity or duplicate authority. Mark it `RETIRED` in the registry before
removing active deployment copies.

## How this relates to the rest of the wiki

- The authority model and truth order live in `AGENTS.md` section 2 and
  `/openwiki/authority-model.md`; this layer is item 5 in that order.
- The documentation gates that enforce written rules, including the drift check,
  are described in `/openwiki/operations/doc-gates.md`.
- Skill-guided smoke validation is executed through the model in
  `/openwiki/workflows/smoke-test-execution.md`; skills never rewrite PASS
  criteria during a run.
- The ecosystem placement a skill must respect is oriented by
  `/openwiki/architecture/ecosystem-orientation.md`.
