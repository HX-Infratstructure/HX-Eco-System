---
type: "Reference"
title: "Change and Review Workflow"
openwiki_generated: true
verified:
  - by: openwiki/0.5.1
    at: 2026-09-15T22:39:27.588Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-2da1ab191a44216863894518
    resource: repo://docs/06-tooling/openwiki-agents.md
  - id: openwiki-source-52e152e46e382b42e0c887c5
    resource: repo://docs/06-tooling/openwiki.md
  - id: openwiki-source-7535508c0d148b08f4414508
    resource: repo://tools/hx-doc/hx_doc_supersede.py
generated: { by: "openwiki/0.5.1", at: "2026-09-15T22:39:27.588Z" }
---


# Change and Review Workflow

> This page is **context, not authority**. The operating contract is
> [AGENTS.md section 13](repo://AGENTS.md#L167-L215), "Change rule — everything
> goes through a pull request." Where this page and section 13 disagree, section
> 13 wins and this page is a defect to fix.

## The one rule this workflow exists to enforce

`main` is not a working branch. Every change — including a one-line fix — goes
through a pull request so CodeRabbit reviews it. Review is not optional. There
is no "too small to review" carve-out and no direct push to `main`.

This holds because CodeRabbit is wired to review pull requests, and a change
that never becomes a pull request is a change that is never reviewed. The rest
of this page describes the exact sequence and the several ways a review can be
silently lost.

## The exact sequence

Section 13 fixes the order. Do not reorder it.

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

Each step exists for a reason that has cost real defects when skipped:

- **Branch first.** Work happens on `<type>/<short-name>`, never on `main`.
- **Regenerate derived output, then check it.** Three tools run in sequence
  ([`hx-fleet`](repo://AGENTS.md#L176), [`hx-render-html`](repo://AGENTS.md#L176),
  [`hx-doc-check`](repo://AGENTS.md#L176)). `hx-render-html` rebuilds the
  `human-html/` mirrors from Markdown; `hx-doc-check` validates links, registry
  vocabulary, control frontmatter, stable filenames, and committable evidence
  ([`AGENTS.md` section 14](repo://AGENTS.md#L217-L230)). CI runs both and fails
  the change otherwise ([`AGENTS.md` section 15](repo://AGENTS.md#L293-L309)),
  so running them locally first is cheaper than waiting for CI.
- **Commit before push.** `git push` sends commits, not working-tree edits.
  `git status` after `git add -A` is the last chance to confirm the diff is what
  you actually mean to submit.
- **Review before push, not after.** See below — this is the load-bearing step.
- **Push and open the PR.** `git push -u origin HEAD && gh pr create`.

## `coderabbit review --agent` before every push is required, not a convenience

The local CLI review runs **before** the push. The hosted reviewer runs
**after** the push. They are not interchangeable, and the timing matters.

The hosted reviewer has three limits the CLI reviewer does not:

1. **It applies the configuration from the pull request's base branch**, not the
   branch under review. A configuration fix made only on the feature branch
   cannot rescue that branch's own review — it has to reach `main` to take
   effect ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L29-L39)).
2. **On a public repository it can refuse for the day once the review limit is
   reached.** A review that ran yesterday may not run today.
3. **It can only see what was pushed.** It cannot catch a defect that you never
   committed.

The CLI reviewer reads the working tree and the configuration as they are now,
with none of those limits. It runs from a CodeRabbit API key; `coderabbit auth
status` reports whether one is configured ([`AGENTS.md` section 13](repo://AGENTS.md#L202-L203)).

The cost of skipping it is concrete. The first push of the day that skipped the
local review shipped **two defects** that the hosted reviewer would have
reported only after they reached the branch:

- a **duplicate `with:` key** that stopped a GitHub Actions workflow from
  starting at all; and
- a **`path_filters` entry that turned the filter list into an allow list** and
  would have excluded every file in the repository from review
  ([`AGENTS.md` section 13](repo://AGENTS.md#L196-L200)).

The command line reviewer reported both before they reached the branch. That is
why the step is required and sits before `git push`, not after it.

### When CodeRabbit raises a finding

When CodeRabbit raises something, fix it — small, medium, or large. If a
finding is wrong, say why on the thread rather than ignoring it
([`AGENTS.md` section 13](repo://AGENTS.md#L214-L215)). A finding left
unanswered on a review thread is not a finding resolved.

The repository's review posture is `assertive` with no praise and no restating
of the diff ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L9-L21)), so a
finding is meant to be specific and actionable.

## Stacked pull requests must still be reviewed

A pull request stacked on another branch is reviewed too. `.coderabbit.yaml`
matches **every base branch**, not just `main`: `auto_review.base_branches` is
`- ".*"` ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L38-L39)).

The configuration comment records why this matters. Naming only `main` there
added nothing (it was already the default) and excluded everything else; a pull
request stacked on another branch was skipped with "auto reviews are disabled on
base/target branches other than the default branch" — an unreviewed change,
which is the one outcome this repository does not accept
([`.coderabbit.yaml`](repo://.coderabbit.yaml#L29-L39)).

Because the decision is made from the pull request's base branch, a base-branch
fix has to reach `main` to take effect; fixing it only on a stacked branch
cannot rescue that branch's own review ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L35-L38)).

## The 100-file limit

Keep a pull request under 100 changed files. CodeRabbit skips anything larger,
and a skipped review is the same as no review
([`AGENTS.md` section 13](repo://AGENTS.md#L209-L212)).

Generated output and archive are already filtered out in `.coderabbit.yaml`
through `path_filters`, which is what usually pushes a change over the line:

- `!human-html/**` — generated HTML mirrors; a finding belongs in the Markdown
  source or the generator, never here
  ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L62-L63)).
- `!archive/**` — superseded history; never current authority
  ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L64-L65)).
- `!openwiki/**` — written by the OpenWiki CLI and replaced wholesale on
  `--init` ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L66-L68)).
- `!docs/03-runbooks/common/hx-fleet-ips.env` — generated from
  `docs/00-control/hx-fleet.tsv` ([`.coderabbit.yaml`](repo://.coderabbit.yaml#L69-L70)).

A positive `path_filters` entry turns the whole list into an allow list, so the
set begins with `- "**"` to keep the whole tree in scope and subtracts from it
([`.coderabbit.yaml`](repo://.coderabbit.yaml#L55-L60)). The two source-of-truth
TSV files (`hx-fleet.tsv`, `hx-proof.tsv`) are re-included by name because
CodeRabbit's own default filters exclude `**/*.tsv` and would otherwise keep
them out of every review — and they are the last files that should go unreviewed
([`.coderabbit.yaml`](repo://.coderabbit.yaml#L71-L77)).

## How `openwiki/` changes

`openwiki/` is generated. It is **not** edited by hand unless explicitly asked.

### Current generation: manual, from a host-agent session

As of **D-025** (ratified 2026-09-14), OpenWiki generation is manual, not
scheduled. The former `.github/workflows/openwiki-update.yml` was deleted, and
regeneration happens from a host-agent session using that session's model rather
than an API key ([`DECISIONS.md` D-025](repo://docs/00-control/DECISIONS.md#L287-L326)).

This supersedes **D-023**, which had authorized two Actions secrets
(`OPENWIKI_PR_TOKEN` and `ANTHROPIC_API_KEY`) so a weekly workflow could
regenerate `openwiki/` with a paid model run
([`DECISIONS.md` D-023](repo://docs/00-control/DECISIONS.md#L156-L196)).

Under the current, manual path:

- PRs are **not auto-merged**. A human reads the generated documentation before
  it lands ([`DECISIONS.md` D-023](repo://docs/00-control/DECISIONS.md#L188-L189);
  this non-merging condition carried into the manual model and is still how a
  generated change is treated).
- A write-capable token (`OPENWIKI_PR_TOKEN`) and `ANTHROPIC_API_KEY` are no
  longer used by a scheduled workflow; revoking both was a required owner action
  ([`DECISIONS.md` D-025](repo://docs/00-control/DECISIONS.md#L294-L303)).
- The normal path inside a Claude Code session is the instruction "Update
  OpenWiki for this repository," which hands authoring to the session's model so
  no OpenWiki provider key is used
  ([`docs/06-tooling/openwiki.md`](repo://docs/06-tooling/openwiki.md#L44-L60)).

The cost D-025 records is that refresh becomes a matter of discipline rather than
a cron: a generated tree nobody regenerates goes stale silently
([`DECISIONS.md` D-025](repo://docs/00-control/DECISIONS.md#L318-L322)).

### Never hand-edit generated pages

`openwiki/**/*.md` (except `INSTRUCTIONS.md`), `openwiki/.claims/**`, and the run
state files are regenerated; an edit there is lost on the next run
([`docs/06-tooling/openwiki-agents.md`](repo://docs/06-tooling/openwiki-agents.md#L40-L52)).
The OpenWiki markers in `AGENTS.md` and `CLAUDE.md`
(`<!-- OPENWIKI:START -->` … `<!-- OPENWIKI:END -->`) are also rewritten every
run, and any edit inside them is lost
([`AGENTS.md` section 16](repo://AGENTS.md#L312-L333)).

The supported way to change what the wiki covers is `openwiki/INSTRUCTIONS.md`,
which is owner-authored and never rewritten by OpenWiki — including across
`--init` ([`docs/06-tooling/openwiki.md`](repo://docs/06-tooling/openwiki.md#L57-L60)).

### Generated pages are never authority

Every page under `openwiki/` is written by a model from the code and is always
behind the working tree by at least one run. Source code and tests are evidence,
not authority; generated pages are context and never authority
([`docs/06-tooling/openwiki-agents.md`](repo://docs/06-tooling/openwiki-agents.md#L28-L38);
[`AGENTS.md` section 16](repo://AGENTS.md#L319-L333)). The authority for "what am
I allowed to do" is `AGENTS.md`, the control docs, and `smoke-tests/`, not the
wiki ([`docs/06-tooling/openwiki-agents.md`](repo://docs/06-tooling/openwiki-agents.md#L8-L25)).

## Document lifecycle and supersede

### Active documents use stable, unversioned filenames

Active documents use stable filenames with no version or date in the name;
version, date, and status live inside the document. A superseded version belongs
under `archive/YYYY-MM-DD/`. Do not create duplicate active documents with
timestamps, `(1)`, `final-final`, or model-name prefixes
([`AGENTS.md` section 15](repo://AGENTS.md#L293-L309);
[`.coderabbit.yaml` path_instructions for `docs/00-control/**`](repo://.coderabbit.yaml#L112-L118);
[`DECISIONS.md` D-011](repo://docs/00-control/DECISIONS.md#L39-L40)).

Only one current version of a document stays active; superseded versions go to
`archive/`. Active Markdown is agent authority; HTML is a human mirror
([`DECISIONS.md` D-011](repo://docs/00-control/DECISIONS.md#L39-L40)).

### Supersede in one command with `hx-doc-supersede`

[`tools/hx-doc/hx_doc_supersede.py`](repo://tools/hx-doc/hx_doc_supersede.py#L1-L18)
performs the supersession procedure in one command rather than six manual steps.
Given an active document and a `--suffix`, it:

1. creates `archive/<today>/<same-path>/`,
2. copies the current Markdown there with the suffix appended to the stem,
3. archives the matching `human-html` mirror if one is committed,
4. leaves the active file in place for you to edit, and
5. reminds you to re-render the mirror
   ([`tools/hx-doc/hx_doc_supersede.py`](repo://tools/hx-doc/hx_doc_supersede.py#L8-L17)).

It refuses a path under `archive/` or `human-html/` (those are not active
documents) ([`tools/hx-doc/hx_doc_supersede.py`](repo://tools/hx-doc/hx_doc_supersede.py#L60-L63)),
and refuses a `--suffix` whose archive copy already exists so you choose a
different one ([`tools/hx-doc/hx_doc_supersede.py`](repo://tools/hx-doc/hx_doc_supersede.py#L69-L72)).

After it runs, you edit the (untouched) active file, re-render with
`tools/hx-doc/hx-render-html` and `tools/hx-doc/hx-doc-check`, and commit the
edit and the archive copy together in one commit
([`tools/hx-doc/hx_doc_supersede.py`](repo://tools/hx-doc/hx_doc_supersede.py#L107-L112)).
This leaves exactly one active version, which is the lifecycle invariant.

### `human-html/**` is generated; never hand-edit a mirror

`human-html/**` is generated output. Never hand-edit it — edit the Markdown
source and run `tools/hx-doc/hx-render-html`
([`AGENTS.md` section 15](repo://AGENTS.md#L300-L308)). CI runs both
`hx-render-html` and `hx-doc-check` and fails the change otherwise
([`AGENTS.md` section 15](repo://AGENTS.md#L303-L304)). Accordingly, a change
that appears in `human-html/` without the matching Markdown source changing is
itself the review finding ([`.coderabbit.yaml` path_instructions for
`human-html/**`](repo://.coderabbit.yaml#L107-L110)).

## Summary of what a skipped step costs

| Step skipped | What it costs |
|---|---|
| Branch (work on `main`) | Change is never reviewed; violates the one rule. |
| `hx-render-html` / `hx-doc-check` | CI fails the change anyway; broken links or stale mirrors land if bypassed. |
| `coderabbit review --agent` before push | Defects reach the branch before review — e.g. a duplicate `with:` key and an allow-list `path_filters` both shipped unreviewed. |
| Under-100-file discipline | CodeRabbit skips the PR; a skipped review equals no review. |
| Base-branch config only on a stacked branch | Stacked PR stays unreviewed; the fix must reach `main` to take effect. |
| Answering findings | A finding left unanswered is not a finding resolved. |
| Stable filenames / supersede | Duplicate active documents; stale version read as authority. |
| Hand-editing `openwiki/**` or `human-html/**` | Edit is lost on the next run; a generated page is never authority. |
