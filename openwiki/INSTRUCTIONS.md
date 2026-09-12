---
type: Repository guide
title: HX Eco-System Wiki Instructions
description: Scope, priorities and writing rules for the generated wiki of the HX seventeen-server clean-room rebuild. Authored by the owner; OpenWiki must not rewrite this file.
tags: [documentation, infrastructure, governance]
---

This repository is a clean-room rebuild of a seventeen-server fleet. It is
governance first and code second. Write the wiki so an agent can answer
"where is the authority for this?" without reading the repository.

## Authority, and the one rule that must not be broken

`AGENTS.md` section 2 defines the truth order. Reproduce it; never restate it
differently, and never write that source code or tests are authoritative.
They are not in that list. The order is:

1. the infrastructure owner's current instruction;
2. current control Markdown in `docs/` and, when testing, the acceptance
   authority in `smoke-tests/`;
3. current live evidence from the server being worked on;
4. the current approved runbook or execution artifact.

Generated pages, this wiki included, are context. They are never authority.
Say so on any page that could be mistaken for a decision.

## Cover these, in this order

1. **Task routing.** Which question goes to which file. This is the most
   valuable page in the wiki, because the whole point is not reading the repo.
2. **The authority model** and how a decision becomes binding
   (`docs/00-control/DECISIONS.md`, ratified versus proposed).
3. **The runbook delegation pattern.** Per-host runbooks are thin wrappers;
   the logic lives in `docs/03-runbooks/common/`. Explain the wrapper, the
   shared library `hx-app-lib.sh`, and the pinned values in `hx-base.env`.
4. **The gates.** `tools/hx-doc/` enforces written rules. State what each
   check refuses and what a failure means.
5. **The proof chain** in `docs/00-control/hx-proof.tsv` and how a smoke step
   becomes eligible to run.
6. **Server records and evidence retention.**

## Write it this way

Name the exact file and, where it helps, the exact line span. An agent should
be able to open one file, not search.

Do not write one page per host. HX-4 through HX-17 are the same two runbooks
with a different hostname. One page covering the pattern is worth more than
fourteen near-identical pages.

Prefer the current state. Nothing in `archive/` describes what is true now.

State costs and irreversibility plainly where a page describes an action.

## Do not document

Anything under `archive/`, `human-html/` or `graft/`. `.openwikiignore`
excludes them; if one appears in a page, the ignore file is wrong and should
be fixed rather than the page.
