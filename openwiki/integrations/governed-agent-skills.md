---
type: integration
title: Governed agent skills
description: The skills library as an advisory layer between architecture and execution — wrapper structure and response pattern, classification and lifecycle states, what admission requires, the registry with its execution and validation bindings and reviewed upstream commits, and the changes a skill may never authorise.
tags: [skills, governance, vendor-guidance, wrappers, registry, upstream-pins]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-6ff476d421611f1f320003de
    resource: repo://skills/AGENTS.md
  - id: openwiki-source-8331ceaff0986ff6678a4efa
    resource: repo://skills/qdrant/hx-qdrant-advisor/SKILL.md
  - id: openwiki-source-a37606a33ef2633def123327
    resource: repo://skills/qdrant/upstream/SOURCE.md
  - id: openwiki-source-446437c63473d8e7dd04c604
    resource: repo://skills/README.md
  - id: openwiki-source-5c5fbd51a83e8c2377f4b8ef
    resource: repo://skills/SKILL-GOVERNANCE.md
  - id: openwiki-source-30873c060e08a1a79b2044e7
    resource: repo://skills/SKILL-REGISTRY.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Governed agent skills

`skills/` is the canonical HX library of reusable agent expertise. It exists so
agents can bring current product knowledge — how Qdrant is tuned, how Redis
persistence behaves, what Docling's converter expects — to work on the fleet,
without that external knowledge quietly becoming a second architecture
authority.

The layer sits in a fixed place in the chain:

```text
HX owner decisions and current ecosystem authority
        -> HX component context
        -> HX skill wrapper (stable HX rules + task workflow)
             -> current official vendor/project guidance, product expertise only
        -> HX runbook / standard
        -> HX smoke roadmap and exact test
        -> evidence
```

## What a skill may and may not do

A component skill may assist with planning, native installation, configuration,
troubleshooting, upgrades and migrations, product-specific diagnostics,
validation preparation and interpreting a smoke-test failure.

It grants no permission at all to change server assignments, networking,
security policy, storage architecture, model placement, permanent integration or
BASE PASS criteria. The governance document enumerates the prohibition
concretely: an external skill cannot authorise moving a workload to another
host, introducing a container platform, replacing native deployment with a
vendor cloud or embedded option, changing gateway, DNS, domain, NTP, routing or
topology, adding firewall or TLS restrictions without approval, repartitioning
disks, changing shared model placement, changing permanent integration, or
modifying PASS criteria during a run.

When vendor guidance recommends one of those, the wrapper does not silently
comply and does not silently refuse. It classifies the recommendation as
`OWNER_DECISION_REQUIRED` or `REJECT_FOR_HX` according to current owner
decisions.

Two further limits keep the layer honest. A skill may identify a defect in a
smoke test, but it cannot rewrite acceptance criteria during that run — the
correction goes through a reviewed repository change and a new run. And skills
never contain credentials of any kind: no passwords, PATs, API keys, bearer
tokens, private keys, service-account secrets or `sshpass` passwords.

## The wrapper pattern

Vendor skills are consumed through an HX-authored wrapper rather than installed
directly, because a vendor skill left to itself will happily recommend the
deployment shape its vendor prefers. A wrapper must identify the component's
host and architecture boundary, load HX authority *before* vendor advice,
explain how to reach current vendor guidance, distinguish accepted from adapted
from rejected recommendations, point at both the execution authority and the
smoke-test authority, define explicit stop conditions, avoid embedded
credentials, avoid general deployment code that bypasses the runbooks, and stay
short enough to load progressively.

For a material decision the wrapper answers in a fixed shape:

```text
HX CONTEXT
VENDOR GUIDANCE CONSULTED
RECONCILIATION: ACCEPT | ADAPT | REJECT_FOR_HX | OWNER_DECISION_REQUIRED
EXECUTION AUTHORITY
VALIDATION AUTHORITY
STOP CONDITIONS
```

Each component directory follows the same layout — a component `README.md`, an
`upstream/SOURCE.md` provenance record, and the wrapper itself holding
`SKILL.md`, an agent manifest and a `references/` directory where the bulk of
the HX context lives so that `SKILL.md` stays small.

The Qdrant advisor is the reference implementation and shows the pattern
working. Its own operating hierarchy restates the repository truth order with
vendor guidance placed sixth; it requires the agent to state the owner server,
build state, companion services, native deployment boundary, vector-space rules,
dependencies and BASE PASS boundary before any vendor guidance is loaded; and it
consumes the official advisor **live** from the vendor's catalogue rather than
vendoring the tree.

## Classification and lifecycle

Every source is classified: `HX_NATIVE`, `VENDOR_OFFICIAL`, `COMMUNITY`,
`WRAPPER` or `META`. Vendor-official is the preferred external class for product
expertise; community sources require explicit review of provenance, scope,
behaviour, links, scripts and architecture assumptions before moving beyond
discovery.

Lifecycle states are a closed vocabulary: `DISCOVERY`, `PILOT`, `APPROVED`,
`BLOCKED`, `RETIRED`, plus two states for sources HX consults but never installs
as a second authority — `APPROVED_AS_REFERENCE` for a reviewed expert reference,
and `REFERENCE_ONLY` for material retained for context or later evaluation.
Approval is scoped: a skill approved for troubleshooting is not thereby approved
to execute infrastructure changes.

One rule about the discovery backlog is worth naming, because it is a discipline
rather than a mechanism: a component stays in `DISCOVERY` with its source listed
as `TBD` until a real upstream is found and reviewed. Inventing a plausible
source is prohibited.

## The registry as a checkable record

`SKILL-REGISTRY.md` is the inventory. Seven components are approved — Qdrant,
LightRAG, PostgreSQL, Redis, Mem0, Docling with Granite-Docling, and Crawl4AI —
each row recording the HX host, the canonical wrapper path, the classification,
the primary upstream, the upstream consumption mode with its reviewed commit,
the approved scope of use, the companion capability and a last-reviewed date.

A second table records the **execution and validation bindings** the governance
document demands: for each component, its runbook directory, its smoke-test
authority, its companion authority and the wrapper validation result. Recording
them as fields rather than prose is what makes them auditable. The wrapper
validation entries are careful about what they claim — they state that the
wrapper's structure and frontmatter were reviewed and that no HX execution
authority was granted, and the registry says plainly that no skill approval
advances any server's build state.

The registry is also honest about what is not settled. Mem0's MCP implementation
is not yet selected; Crawl4AI's official MCP bridge is Docker-server-coupled so
its native HX implementation is still open. Both are recorded as open items
rather than smoothed over.

## Reviewed commits, and drift against them

Every approved skill records the exact upstream commit it was reviewed at, and
those pins were previously maintained by memory alone.
`tools/hx-doc/hx-upstream-drift` now parses the registry's provenance lines,
queries each upstream, and reports when a reviewed commit no longer matches.
A weekly workflow runs it and opens or updates one issue.

Drift is treated as information, not failure: a pin stays valid until the owner
decides to move it, and the response is to re-review the source and update both
the reviewed commit and the last-reviewed date. See
[version pins and upstream drift](../operations/version-pins-and-upstream-drift.md).

## Using a skill

The library's own contract sets the loading order: read the root contract and
README, establish current HX state for the component, read the governance
document, read the registry, read the component README, load the approved
wrapper, and load only the wrapper references the task needs.

Deployments into a specific agent's skill directory are derived from this
canonical source. Independently maintained, hand-edited copies for Claude, Codex
or any other agent are prohibited, for the same reason duplicate active
documents are — see
[owner decisions and document lifecycle](../concepts/owner-decisions-and-document-lifecycle.md).
