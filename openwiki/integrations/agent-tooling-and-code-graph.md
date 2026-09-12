---
type: integration
title: Agent tooling and the code graph
description: The machine-facing surfaces an agent works through — the entry contract and its reading order, the registered code-graph MCP server with an honest statement of what it does and does not index, the local patch that puts shell into the graph, and the scheduled job that regenerates this wiki.
tags: [agents, mcp, graft, code-graph, openwiki, tooling]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-ea70eb6c045047448e446296
    resource: repo://.gitignore
  - id: openwiki-source-4ce527ba102d747ebc46110d
    resource: repo://.ignore
  - id: openwiki-source-f5a489e5822d87c0b8fc66ef
    resource: repo://.mcp.json
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-031feb6606529a37844764d1
    resource: repo://tools/hx-doc/hx_doc_check.py
  - id: openwiki-source-2909dda2204a0a08300a688c
    resource: repo://tools/hx-doc/hx-graft-bash
  - id: openwiki-source-f2994b36a477b8759d39a2a6
    resource: repo://tools/hx-doc/README.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Agent tooling and the code graph

The repository is explicitly built to be worked on by agents, and it exposes
three machine-facing surfaces to that end: a contract that says what to read and
in what order, a code graph that answers "where does this live" without reading
whole files, and this generated wiki. Each is described here with its limits,
because a context surface that overstates its coverage is worse than none.

## The entry contract

`AGENTS.md` is the operating contract; `CLAUDE.md` contains no policy and only
points at it, so the two cannot drift into different versions of the same rule.
Its reading order, truth order and boundary rules are described in
[the repository authority model](../architecture/repository-authority-model.md).

Two sections of it are aimed squarely at tooling. Section 14 lists the
enforcement commands and the proof-chain query, and states the rule that governs
all of them: a written rule nothing checks will drift, so a check failing is a
real defect rather than noise to work around. Section 15 fixes which files an
agent may edit — authoritative Markdown and approved execution artifacts — and
which are generated and must never be hand-edited.

## Graft, the code graph

A code graph is registered as an MCP server in `.mcp.json`, launched as
`graft mcp`, so a session opened in this repository gets its tools natively:
`graft_find_code`, `graft_find_all`, `graft_trace_calls`, `graft_file_api`,
`graft_repo_map` and `graft_check_freshness`. The equivalent CLI subcommands
work everywhere the MCP tools are not exposed.

| To find out | Use |
|---|---|
| where a symbol lives, how something works | `graft_find_code` · `graft ask` |
| every occurrence, not just the top hits | `graft_find_all` |
| a file's shape before editing it | `graft_file_api` · `graft skeleton` |
| who calls this, blast radius of a rename | `graft_trace_calls` · `graft callers` |
| orientation in the repo | `graft_repo_map` · `graft map` |
| whether the graph matches the tree | `graft_check_freshness` · `graft check` |

The measured benefit is concrete: one `graft_file_api` call on the shared
runbook helper library returned all six helpers for 88 tokens against 942 to
read the file whole, and a single `graft_find_code` query saved roughly 7,500
tokens.

### What it does not cover

The repository documents the graph's blind spots as carefully as its coverage,
because the failure mode is an agent reading an empty result as "does not
exist".

- **The Markdown authorities are not in the graph.** The smoke-test procedures,
  the roadmaps and the control documents must be read directly.
- **Shell call edges do not exist.** Shell function definitions are indexed, but
  tracing callers of a shell function returns nothing. That is a parser limit,
  not a fact about the code.
- **Seventeen extensionless scripts are unindexed** — every `tools/hx-doc`
  wrapper plus the four smoke-runner scripts. The wrappers matter little, since
  each is a few lines that resolve a Python 3 and exec the `.py` body beside it
  and that body *is* indexed. The runner scripts matter more: they are the ones
  used most during a smoke run.

The rule that follows is stated in one line in the contract: an empty result
means **not in the graph**, never **does not exist**.

### The bash patch, and why it has to be applied twice

Graft ships a tree-sitter bash grammar whose manifest registers it as `bash`,
but its own language table has no bash entry, so `.sh` files are skipped
entirely. `tools/hx-doc/hx-graft-bash` adds the one missing line to the
installed package.

The entry it inserts covers `.sh`, `.bash` **and** `.env`, because
`docs/03-runbooks/common/hx-base.env` is bash: it holds the host guard, the
verified-fetch helper and every fleet version pin, so leaving it out would omit
the most consulted file in the build path.

The script is a local patch to a third-party package, so it is written to fail
safely rather than guess. It is idempotent, refusing to act if bash is already
registered. It backs the file up before editing. It stops with an explanation if
the expected anchor in the language table is missing, on the grounds that the
upstream file has changed shape and may now register bash itself. It elevates
with `sudo` only when the target is not already writable, since a per-user npm
prefix needs none. It performs a literal string replacement in Python rather
than `sed`, avoiding a quoting mistake that silently matches nothing. And
`--revert` restores the shipped file from the backup.

One operational trap is called out explicitly: a workstation commonly has two
Graft installs, a native one and one inside WSL, and whichever is on `PATH`
answers the query. If only one carries the patch, live queries come back blind
to shell while the cards on disk still list shell symbols — which reads as a
Graft bug rather than a half-applied patch. Run the script once per install,
pointing `GRAFT_ROOT` at each, and again after any `graft upgrade`, which wipes
it.

The graph itself is local and regenerable: `/graft/` and `/.graft/` are both
gitignored. A companion `.ignore` file re-admits the card tree to ripgrep only,
since ripgrep reads `.ignore` before `.gitignore` — the cards stay greppable
without being committed.

## This wiki

`openwiki/` is generated. Its status in the repository mirrors `human-html/`:
the contract describes it as optional just-in-time context, not required startup
reading, and tells agents to treat source code and tests as authoritative rather
than the wiki's own text. A brief's unknowns and review items are verification
gaps, not automatic work items.

Regeneration runs weekly through a scheduled GitHub Actions workflow, and the
tree is excluded from review filters, documentation link checks and the active
document set for the same reason `human-html/` is: nothing in it is authored, so
a finding inside it belongs in the source it documents or in the generator. The
workflow itself, including its deliberate departures from the upstream example
and the secrets it needs, is described in
[continuous integration workflows](../operations/continuous-integration-workflows.md).

## Governed expertise is separate

The one machine-facing surface deliberately *not* covered here is the skills
library, because it is advisory rather than contextual: it carries product
expertise an agent may consult, under governance that stops it from redefining
anything. See
[governed agent skills](governed-agent-skills.md).
