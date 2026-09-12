---
type: workflow
title: Contributing and review workflow
description: The mandatory change path — branch off the default branch, regenerate derived artifacts, run the local checks, run the command-line reviewer before pushing, then open a pull request — plus the review configuration, its path-scoped instructions, and the size limit that silently skips a review.
tags: [workflow, contributing, pull-request, code-review, coderabbit, checks]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-3c099d9af7cba6b30d6eaf07
    resource: repo://.gitattributes
  - id: openwiki-source-4a10bba62772b26bb2a2e6b3
    resource: repo://.github/workflows/hx-checks.yml
  - id: openwiki-source-ea70eb6c045047448e446296
    resource: repo://.gitignore
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-031feb6606529a37844764d1
    resource: repo://tools/hx-doc/hx_doc_check.py
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Contributing and review workflow

`main` is not a working branch. Every change goes through a pull request,
including a one-line fix, so that it is reviewed. The contract states this
plainly: review is not optional.

## The sequence

```bash
git checkout -b <type>/<short-name>

# work, then regenerate anything derived and check it:
tools/hx-doc/hx-fleet && tools/hx-doc/hx-render-html && tools/hx-doc/hx-doc-check

# commit before pushing - git push sends commits, not working-tree edits:
git add -A
git status          # confirm the diff is what you mean to submit
git commit

# review locally before the push, not after it:
coderabbit review --agent

git push -u origin HEAD && gh pr create
```

Each line earns its place.

**Regenerate before checking.** A change to the fleet TSV is only half an edit
until the generator has run; a change to any Markdown is only half an edit until
the mirrors are re-rendered. Continuous integration runs the `--check` modes and
will fail the change otherwise. See
[generated artifacts and single sources of truth](../concepts/generated-artifacts-and-single-source-of-truth.md).

**Commit before pushing.** Stated explicitly because `git push` sends commits,
not working-tree edits — a regenerated file left uncommitted simply does not
travel.

**Review locally, before the push.** This is required rather than convenient,
and the reasoning is specific. The hosted reviewer runs *after* the push, applies
the configuration from the **base** branch rather than the branch under review,
and on a public repository can refuse for the day once the review limit is
reached. The command-line reviewer has none of those limits: it reads the working
tree and the configuration as they are now. It runs from an API key, and
`coderabbit auth status` reports whether one is configured.

The cost of skipping it is on record. The first push of a day that skipped it
shipped two defects: a duplicate `with:` key that stopped a workflow starting at
all, and a filter entry that turned the filter list into an allow list and would
have excluded every file in the repository from review. The local reviewer had
reported both.

## Constraints on the pull request itself

**Keep it under 100 changed files.** The reviewer skips anything larger, and a
skipped review is the same as no review. Generated output and the archive are
already filtered out of the count, and it is usually those trees that push a
change over the line.

**Stacked branches are reviewed too.** The review configuration matches every
base branch, not only the default one. Naming only the default branch silently
skipped work stacked on another branch, which is an unreviewed change. There is
a trap in the fix, recorded in the configuration itself: the decision is made
from the pull request's *base* branch, so the corrected setting has to reach the
default branch to take effect — fixing it only on a stacked branch cannot rescue
that branch's own review.

**Act on findings.** When the reviewer raises something, fix it, whatever the
size. If a finding is wrong, say why on the thread rather than ignoring it.

## What the reviewer is told

`.coderabbit.yaml` is not a default configuration. Every path instruction in it
encodes a rule the repository already states in prose, so a reviewer enforces
them on every change instead of them holding only as long as someone remembers.
The tone is set deliberately: direct and specific, no praise, no restating the
diff, one concrete finding preferred over three vague ones.

Path-scoped instructions cover:

| Path | The reviewer is told to require |
|---|---|
| `docs/03-runbooks/**/*.sh` | strict shell settings, a host guard first, quoted expansions, no hard-coded host, IP or version, approved package sources, checksum verification, no containers — and *not* to raise firewall, TLS or listener hardening, which is a decided posture |
| `tools/**` | standard library only, no check that cannot fail, no silently swallowed errors, wrappers that resolve a working Python 3 |
| `human-html/**` | a change here without its Markdown source changing is itself the finding |
| `docs/00-control/**` | stable filenames, no as-built claim without evidence, no decision recorded as ratified without an owner deciding it |
| `docs/02-server-records/*.md` | both a source URI and a full hash for provenance, `UNRESOLVED` never omitted, no PASS unsupported by the recorded gates |
| `smoke-tests/*.md` | a known answer, a cleanup step, evidence retention; no redefining ecosystem placement |
| `skills/**` | defined lifecycle states, a reviewed upstream commit and date, never any credential |
| `.github/workflows/*.yml` | no unpinned actions, no secrets in logs, no check that cannot fail |

Two entries are worth reading as cautionary tales rather than settings.

The **path filter list** begins with `**`. A positive entry turns the list into
an allow list — the reviewer treats it as a sparse-checkout include set — so
naming only the two TSV files left every other file in the repository ignored.
The `**` keeps the whole tree in scope and the negated entries subtract from it:
generated HTML, the archive, this wiki, and the generated IP map.

The **two TSV files are re-included by name**, because the reviewer's own default
filters exclude `*.tsv` and had silently kept both source-of-truth files out of
every review — the fleet table and the proof chain, one of which gates every
smoke-test PASS.

## Line endings and file hygiene

`.gitattributes` forces LF on everything, and explicitly on `.sh`, `.py` and the
smoke-runner scripts, so an execution artifact runs on Linux regardless of the
contributor's platform or local git settings. Continuous integration checks the
same thing from the other side, failing on any CRLF or non-executable shell
script.

`.gitignore` is unremarkable except for two deliberate re-inclusions: retained
evidence logs are exempted from the blanket `*.log` rule, and the code graph's
local cache is ignored while remaining greppable. The documentation checker
independently probes that the ignore rules cannot swallow retained evidence.

## After the push

The pull request runs the documentation, execution-artifact and secret-scan
jobs, and the hosted reviewer comments. Both are described in
[continuous integration workflows](../operations/continuous-integration-workflows.md).

If the change supersedes a document, use the supersession tool rather than
moving files by hand, and land the edit and the archived copy in one commit —
see
[owner decisions and document lifecycle](../concepts/owner-decisions-and-document-lifecycle.md).

Before declaring the work complete, update the affected server record, the build
state and any affected decision or standard document.
