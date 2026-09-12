---
type: design-concept
title: Generated artifacts and single sources of truth
description: How the repository stops duplicated facts from disagreeing — two TSV control files that drive every fleet table, the runbook host lookup and the proof roadmap, a marker-block protocol for injecting generated content into authored documents, HTML mirrors rendered from Markdown, and check modes that fail on stale output.
tags: [generation, single-source-of-truth, tsv, markers, ci-check, human-html]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-4a10bba62772b26bb2a2e6b3
    resource: repo://.github/workflows/hx-checks.yml
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-667355bbf619c0e53d4f76d4
    resource: repo://docs/03-runbooks/common/hx-base.env
  - id: openwiki-source-ef31bef39cb73c0c0eb61178
    resource: repo://docs/03-runbooks/common/hx-fleet-ips.env
  - id: openwiki-source-058667b14857202ef49933ce
    resource: repo://tools/hx-doc/hx_fleet.py
  - id: openwiki-source-d3a3650a1878a8482b4c0fff
    resource: repo://tools/hx-doc/hx_proof.py
  - id: openwiki-source-7e54593e1179ec2c375e54a7
    resource: repo://tools/hx-doc/hx_render_html.py
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Generated artifacts and single sources of truth

A fact written in six places agrees on the day it is written, and that is the
only day it is guaranteed to. The repository's answer is to keep one writable
copy of each such fact and generate every other appearance of it, then make
continuous integration refuse a commit where a generated copy has fallen behind.

Three generators exist, all Python 3 standard library only, each with a normal
mode that rewrites and a `--check` mode that reports and exits non-zero.

| Source of truth | Generator | Produces |
|---|---|---|
| `docs/00-control/hx-fleet.tsv` | `tools/hx-doc/hx-fleet` | every fleet table in the documents, plus `docs/03-runbooks/common/hx-fleet-ips.env` |
| `docs/00-control/hx-proof.tsv` | `tools/hx-doc/hx-proof` | the phase tables and dependency diagram in the smoke-test roadmap |
| `docs/**/*.md`, `README.md`, parts of `skills/` | `tools/hx-doc/hx-render-html` | the `human-html/` mirrors |

## The fleet TSV

`hx-fleet.tsv` carries one row per server with the columns `id`, `ip`, `role`,
`state`, `gate` and `note`. Everything that displays fleet facts reads from it.

A document opts in by carrying a marker pair and naming the columns it wants:

```text
<!-- HX-FLEET:TABLE columns=id,ip,role,state -->
...generated table...
<!-- /HX-FLEET:TABLE -->
```

The generator scans `README.md` and every Markdown file under `docs/` and
`skills/`, so different documents can show different column subsets of the same
row set — the build state file shows gates and notes, the architecture
orientation shows addresses. Rendering is uniform: addresses come out as code,
`state` and `gate` come out bold with underscores turned into spaces, and an
empty cell becomes an em dash.

The same run writes `docs/03-runbooks/common/hx-fleet-ips.env`, a generated
shell function `hx_ip_for` mapping each host to its address. This is how the
build scripts avoid carrying their own copy of the fleet map: the runbook
environment sources that file, and the host guard resolves the expected address
through it. The file says so in its own header, and hand-editing it is
overwritten on the next run.

### Failures the fleet generator refuses to hide

Two defects here are subtle enough to have needed explicit handling, and both
are worth knowing because they show what "stale" means in this repository.

An **unmatched marker** matches no block, so the substitution changes nothing
and the output compares equal to the input — which naively reads as "current".
The generator therefore counts opening markers, closing markers and complete
pairs separately and requires all three to agree.

An **unknown column name** used to fall through to a heading of its own name
with em dashes beneath it, and `--check` passed because that junk matched
itself. Unknown columns are now reported and the block is left alone.

Generation mode reports these as failures too, rather than printing a success
line for a document it actually skipped.

## The proof TSV

`hx-proof.tsv` holds one row per smoke-test step with its phase, system under
test, component, acceptance authority, `requires` edges, permitted limited
integration and status. `hx-proof` generates the roadmap's per-phase tables and
the whole dependency diagram from it, using its own marker pairs
(`HX-PROOF:TABLE phase=B` and `HX-PROOF:DAG`).

The check here goes beyond comparing content. A **deleted** marker leaves the
surrounding text untouched, so content comparison alone would report a roadmap
that had silently lost a phase table as current; a **duplicated** marker renders
the same table twice. So the generator requires exactly one table block per
phase that has steps, exactly one diagram block, and no table marker for a phase
with no steps.

That strictness has already paid: the hand-maintained diagram this replaced
carried nineteen nodes against thirty rows in the TSV, quietly omitting every
MCP companion gate, both Web UI gates and the reranker, and nothing compared the
two. The semantics of the file — what `requires` means and how a PASS is gated
on it — are covered in
[the proof chain](proof-chain-and-cumulative-evidence.md).

## The HTML mirrors

`human-html/` is a complete generated mirror for human reading: `README.md`,
every non-template document under `docs/`, and the top-level plus per-component
skill READMEs. The renderer implements only the Markdown subset these documents
actually use, keeping the standard-library-only rule intact, and stamps each
page with a banner naming its source path and saying plainly that the page is
not execution authority.

Its check mode reports two distinct problems. A **stale** mirror no longer
matches what its source would render. An **orphan** is an HTML file under
`human-html/` with no source at all — the residue of a document that was
renamed or removed — and it fails the check just as loudly, because an orphan is
exactly the kind of plausible-looking stale page a reader might trust.

## What this buys, and the rules that follow

Three rules fall directly out of the design, and all three are enforced rather
than merely stated:

1. **Never hand-edit a generated surface.** That means `human-html/`, the
   generated IP map, the marked blocks, and this wiki. A change appearing in a
   mirror without its source changing is itself the finding; the review
   configuration says so explicitly.
2. **Change the source, then regenerate.** Editing the TSV is the whole edit;
   running the generator is the second half of it.
3. **Commit the regenerated output.** Continuous integration runs `hx-fleet
   --check`, `hx-proof --check` and `hx-render-html --check` on every pull
   request, and each prints the stale paths and the command to fix them before
   exiting non-zero.

The day-to-day sequence is in
[contributing and review](../workflows/contributing-and-review.md); the wider
tool suite is in
[repository consistency tooling](../operations/repository-consistency-tooling.md);
and the jobs that run the checks are in
[continuous integration workflows](../operations/continuous-integration-workflows.md).
