---
type: governance-architecture
title: Repository authority model
description: What this repository is and how its parts rank against each other — the agent operating contract, the truth order that settles conflicts, the ownership boundary of each top-level tree, and which surfaces are authored versus generated.
tags: [governance, authority, agents-contract, truth-order, repository-layout]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
  - id: openwiki-source-9e410f74688e3b2d6aa0c07e
    resource: repo://docs/00-control/CURRENT-STATE.md
  - id: openwiki-source-2c909f1605c16498627e565e
    resource: repo://docs/00-control/DOCUMENT-CONTROL.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Repository authority model

This repository holds no ecosystem application code. It is an authority system:
the set of documents, execution artifacts and checks that decide what the
[HX fleet](hx-fleet-and-ecosystem-layout.md) is, how a server gets built, what
counts as proof that it works, and what may be claimed about it afterwards.

Everything else on this wiki hangs off one question — **which surface wins when
two of them disagree** — so that is what this page answers.

## The contract an agent reads first

`AGENTS.md` is the operating contract. `CLAUDE.md` exists only to point at it,
deliberately kept short so that instructions cannot drift into two different
versions of the same policy. The contract does three things that matter more
than its individual rules:

1. **It fixes a reading order.** README, then current state, then build state,
   then decisions, then architecture orientation, then the build priority, then
   the specific record, runbook and standard for whatever is being touched.
   Validation material comes last, and only when validating.
2. **It names what is not authority.** `archive/` and `human-html/` are
   excluded from normal context loading unless someone explicitly asks for them.
3. **It states an ecosystem-first rule.** Before designing or running any
   validation, an agent must be able to state the component's owner server,
   target IP, role, current build state, applicable baseline, dependency
   boundaries, model placement rules and BASE PASS boundary. Not being able to
   answer those is itself a stop condition.

## Truth order

Conflicts are not resolved by recency or by whichever document was read last.
They are resolved by rank:

```text
1  explicit current instruction from the infrastructure owner
2  current active control/architecture Markdown in docs/  ·  the exact
   component acceptance authority in smoke-tests/ when testing
3  current live evidence from the server being worked on
4  current approved runbook / execution artifact
5  governed HX skill + current official vendor guidance
6  historical / archive material, as reference only
7  general model knowledge
```

Two properties of this ordering do real work.

**A document can be wrong.** When live evidence from a server, or a current
vendor requirement, contradicts an active document, the rule is not to obey the
document and not to silently follow the evidence either. It is to stop treating
the document as sufficient proof and report the contradiction, so the smallest
affected authority can be corrected through review.

**Model knowledge ranks last.** An agent's own prior belief about how
PostgreSQL or Qdrant is normally deployed loses to every repository surface
above it.

## What each tree owns

| Tree | Status | Owns |
|---|---|---|
| `docs/00-control/` | authority | current state, build state, decisions, roadmaps, the fleet and proof TSVs |
| `docs/01-architecture/` | authority | ecosystem orientation and the validation operating model |
| `docs/02-server-records/` | authority | as-built record per server |
| `docs/03-runbooks/` | authority + executable | the numbered build blocks and per-server wrappers |
| `docs/04-application-standards/` | authority | per-application and per-process standards |
| `docs/05-evidence/` | authority | retained proof bundles |
| `smoke-tests/` | authority, validation only | what each component must prove |
| `skills/` | advisory | governed agent expertise, subordinate to all of the above |
| `tools/` | enforcement | the checks and helpers that make written rules fail loudly |
| `human-html/` | generated | a human mirror; never execution authority |
| `archive/` | historical | superseded versions; never current authority |
| `openwiki/` | generated | this wiki |

The boundaries are stated as prohibitions as well as permissions. A smoke-test
authority says what a component must prove; it may **not** redefine ecosystem
placement, server roles, permanent integration or network architecture. A skill
may advise on planning, installation reasoning, troubleshooting and upgrade
paths; it may **not** authorise host placement, containerisation, topology,
network, storage or model-placement changes, nor alter PASS criteria. Those
limits are what let advisory material be consumed safely — see
[governed agent skills](../integrations/governed-agent-skills.md).

## Authored versus generated

Three trees in the table above are generated, and the distinction is enforced
rather than requested.

- `human-html/` mirrors `docs/`. Editing a mirror by hand is the finding, not
  the fix; the Markdown source changes and the renderer runs.
- `openwiki/` is produced by a scheduled job from the code and documents.
- Parts of otherwise-authored documents are generated too: fleet tables and the
  proof roadmap's phase tables and dependency diagram are written into marked
  blocks from two TSV files.

How that machinery works, and how continuous integration refuses stale output,
is covered in
[generated artifacts and single sources of truth](../concepts/generated-artifacts-and-single-source-of-truth.md).

## One current version, and no other

The document control standard allows exactly one active copy of any document.
Active files use stable filenames with no version or date in the name; version,
date and status live inside the file. Superseded copies move under
`archive/YYYY-MM-DD/`, mirroring their original path, and stop being authority
the moment they land there. Duplicates such as a dated copy, a `(1)` suffix or
a model-name-prefixed variant are prohibited outright, because two plausible
current documents is the failure this rule exists to prevent. The procedure and
its tooling are described in
[owner decisions and document lifecycle](../concepts/owner-decisions-and-document-lifecycle.md).

## Prose alone is not trusted

The contract's own framing is that written rules nothing checks will drift, so
the repository converts its rules into tooling: link and vocabulary checks,
fleet and proof regeneration checks, mirror comparison, server-record
completeness, smoke-authority completeness. A failing check is treated as a real
defect. Bypassing a check, or weakening it so an existing document passes, is
explicitly not allowed — the fix goes into the check, through review. Those
tools are described in
[repository consistency tooling](../operations/repository-consistency-tooling.md),
and the change path that runs them is in
[contributing and review](../workflows/contributing-and-review.md).

## Claims about state are bounded

The last property of the authority model is a habit rather than a mechanism:
the repository consistently separates what is designed from what is running.
Documentation exists for all seventeen servers; three are built. Planned
configuration must never be reported as as-built state, work is not complete
until the server record, build state and any affected decision or standard have
been updated, and tooling is not called installed until live evidence exists.
