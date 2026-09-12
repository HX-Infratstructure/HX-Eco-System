---
type: validation-concept
title: Proof chain and cumulative evidence
description: The dependency graph that decides which smoke test may run next — how steps, phases and requires edges are recorded in one TSV, what the validator refuses, how readiness is queried, and how promotion enforces that a downstream PASS names the prior proof it rests on.
tags: [proof-chain, dag, smoke-test, evidence, gating, validation]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-99c35572fb1146ffd395e32a
    resource: repo://docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md
  - id: openwiki-source-7102ad22abc6e919967a4c88
    resource: repo://docs/00-control/hx-proof.tsv
  - id: openwiki-source-6f5cb78b5ab35b4725eaaccf
    resource: repo://docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md
  - id: openwiki-source-d3a3650a1878a8482b4c0fff
    resource: repo://tools/hx-doc/hx_proof.py
  - id: openwiki-source-a77fea9320056a2d55a6f0f9
    resource: repo://tools/hx-smoke-runner/hx-smoke-promote
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Proof chain and cumulative evidence

Building the fleet has an order. Proving it has a different one, and the second
is the subject of this page. Thirty smoke steps, from the existing foundation
proof through to Open WebUI, are held as rows in
`docs/00-control/hx-proof.tsv`, and that file is the only place the dependency
structure exists. Everything else — the roadmap's phase tables, its dependency
diagram, the readiness command, the promotion gate — reads from it.

## What a step is

Each row carries eight fields:

| Field | Meaning |
|---|---|
| `id` | the step identifier, `P0`, `A1`, `B5`, `E1` … |
| `phase` | which proof phase it belongs to, `0` and `A` through `G` |
| `sut` | the system under test, a host id from the fleet inventory |
| `component` | what is being proven |
| `authority` | the acceptance document that defines the known-answer test |
| `requires` | comma-separated ids of steps that must have passed first |
| `integration` | the temporary live coupling this proof is permitted to create |
| `status` | `NOT_RUN`, `PASS`, `FAIL` or `NOT_EXECUTABLE` |

The `integration` column is unusual and deliberate. It does not describe what
the component connects to in production; it bounds what the *test* is allowed to
wire up. Most rows say "None" with a reason — deterministic raw vectors avoid an
embedding dependency, session-scoped disposable data, a TTL-protected key —
because standalone proof gives better fault isolation. Where coupling is
genuinely needed the row says so and says it is temporary: one route to a proven
model, removed afterward.

## Cumulative proof, minimal live coupling

The governing rule is that a downstream test **reuses prior PASS evidence**
wherever an earlier capability is a real prerequisite, and creates only the
smallest temporary integration needed to prove its own contract. Forcing every
test to call every component tested before it would look thorough and make
failures far harder to diagnose.

Five dependency kinds are distinguished: a foundation prerequisite already
established outside the component test; a prior smoke PASS; a limited validation
integration; a companion gate; and no component dependency at all, chosen for
fault isolation. Only the second kind becomes a `requires` edge.

Companion gates are the reason the graph has more steps than components. A
product's Web UI and its MCP server are proven after the parent core passes, in
that order, and a companion PASS can never substitute for a failed parent. MCP
companion tests use the runner's own MCP client rather than the HX-15 FastMCP
server, and UI companion tests use the application's direct LAN endpoint rather
than HX-7's NGINX — so a companion gate does not silently import a dependency on
another server.

## What the validator refuses

`tools/hx-doc/hx-proof` validates before it renders anything, and every check
exists because the hand-maintained predecessor could get it wrong silently.

- **A blank or duplicate `id`.** Either one overwrote an earlier row, dropping a
  step from the tables and the diagram while validation still reported success.
- **A missing column.** The file is rejected rather than partially parsed.
- **A dangling `requires`.** An edge to a step that does not exist.
- **A missing authority file.** The acceptance document named by the row must be
  present in the repository.
- **An unknown host.** The `sut` must appear in `hx-fleet.tsv`. If that
  inventory is unreadable or empty, that is itself reported — an empty host set
  used to skip the check entirely and let a misspelled host validate clean,
  which is the "check that cannot fail" pattern this repository keeps removing.
- **An unrecognised status.**
- **A cycle.** A depth-first colouring walks the graph and reports the trail of
  any loop, since a proof chain that loops can never be satisfied.

Only after all of that does it regenerate the roadmap's phase tables and the
dependency diagram; see
[generated artifacts](generated-artifacts-and-single-source-of-truth.md).

## Asking whether a step may run

```bash
tools/hx-doc/hx-proof --ready B2      # can this run yet
tools/hx-doc/hx-proof --list          # every step, and what it is waiting on
```

Readiness is not just "dependencies passed". A step is runnable when none of its
required steps is short of `PASS` **and** it is not itself already passed or
marked `NOT_EXECUTABLE`. That last state means an implementation decision is
still open — the component's approach has not been settled — so the step cannot
be run regardless of how healthy its dependencies are.

## The gate that makes it real

A dependency graph nobody consults is decoration. The graph is enforced at the
moment a run is promoted into retained evidence, by
`tools/hx-smoke-runner/hx-smoke-promote`, and there is no bypass flag.

For a `PASS`, promotion:

1. requires a `proof_step` in the manifest whenever the proof TSV exists — a
   manifest without one used to skip the entire chain;
2. re-binds that step to this run, checking the step's `sut` and `authority`
   match the manifest's host and smoke-test file, so a hand-edited manifest
   cannot name a valid step belonging to another host and inherit its
   dependencies;
3. refuses a step whose status is `NOT_EXECUTABLE`;
4. walks the step's `requires` list and refuses if any dependency's status in the
   TSV is not `PASS`;
5. **and separately** requires the manifest's `prior_pass_evidence` to contain a
   `<step-id> -> <evidence>` entry for each of those dependencies.

Point five is the part that turns citation into a check. Recording
`prior_pass_evidence` was previously an honour system: the script confirmed the
field was non-empty and nothing more. A bare list of paths is now refused,
because a path alone cannot say which dependency it proves. The whole value must
sit inline on one line — a value indented across several lines reads as empty
and the promotion is refused.

The evidence cited must be a current retained evidence path or a current
accepted server record. An archive document is never acceptable as current
proof.

## When earlier proof stops counting

Passing once is not permanent. A material change to a prerequisite — an
embedding model revision or dimension change, a vector store upgrade that
affects vector behaviour, a model alias change, a major API or MCP contract
change, a rebuild of the system under test — may invalidate downstream reliance
on the old evidence, and the dependency must be revalidated before a downstream
PASS rests on it. Re-running a prerequisite produces a new evidence reference,
and downstream tests cite the current accepted proof.

Failure rules run in the same direction. A failed prerequisite prevents a
downstream PASS. A prerequisite never proven makes the downstream test not
executable rather than failed. Failed runs are retained when useful and a later
PASS does not erase them. And cleanup failure keeps a run incomplete even when
the functional action succeeded.

## What a PASS actually requires

The proof chain is one clause in a larger conjunction. A component reaches BASE
PASS only with service health **and** resolved prior PASS evidence **and** a
known-answer test **and** any applicable companion gate **and** successful
cleanup **and** verified cleanup **and** reboot persistence **and** reviewed
retained evidence. Only three outcomes may be recorded: `PASS`, `FAIL`, or
`NOT EXECUTABLE — PREREQUISITE OR OWNER DECISION REQUIRED`; the last is for a
genuinely unsettled prerequisite or decision, never a softer way to say a test
failed.

How a run is created, executed and promoted is in
[the smoke-test run lifecycle](../workflows/smoke-test-run-lifecycle.md); what
the retained bundle must contain is in
[server records and evidence retention](../operations/server-records-and-evidence-retention.md).
