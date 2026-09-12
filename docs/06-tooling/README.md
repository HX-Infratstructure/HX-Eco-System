# Operational tooling

One document per tool that this repository depends on but does not contain.
CodeRabbit, OpenWiki and graft are tools, not components of the fleet, so they
do not belong in `01-architecture` or `04-application-standards`.

## Why this directory exists

CodeRabbit was adopted with its facts spread across `DECISIONS.md`,
`RUN-SHEET.md` and `AGENTS.md`, and nothing that said what it was or when to
use it. OpenWiki was then adopted the same way. Twice is a pattern, so the
rule is written down and checked instead of remembered. See **D-024**.

## What a document here must contain

Five sections, in this order. `hx-doc-check` refuses a document that is
missing one.

| Section | Answers |
|---|---|
| `## What it is` | One paragraph. What the tool does, and what it does not do. |
| `## Why we have it` | The problem in this repository that it solves. Cite the decision that adopted it. |
| `## When to use it` | The trigger. Also when not to. |
| `## How to use it` | Exact commands. Cost and irreversibility where they apply. |
| `## Upstream` | Canonical links: documentation and source. A reader must never have to search for the product's own docs. |

A tool that carries a per-agent operating guide splits it into a second file,
`<tool>-agents.md`, named in the index below. The human document carries the
shared facts; the agent document links to them rather than repeating them.

## Index

| Tool | Human | Agent | Adopted by |
|---|---|---|---|
| OpenWiki | [openwiki.md](openwiki.md) | [openwiki-agents.md](openwiki-agents.md) | D-023 |
| CodeRabbit | not written yet | — | — |
| graft | not written yet | — | — |

The two unwritten rows are the backlog, kept visible on purpose. A tool in
this index without a document is the condition `hx-doc-check` fails on.
