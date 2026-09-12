---
type: operations
title: Continuous integration workflows
description: The three GitHub Actions workflows — per-change documentation, execution-artifact and secret-scan jobs; a weekly pin-currency job that opens one issue; and a scheduled wiki regeneration job with a secret preflight, tightly scoped write paths and everything pinned.
tags: [ci, github-actions, gitleaks, shellcheck, secrets, scheduled-jobs]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-4a10bba62772b26bb2a2e6b3
    resource: repo://.github/workflows/hx-checks.yml
  - id: openwiki-source-6039b489b5096b4c78d1d80d
    resource: repo://.github/workflows/hx-upstream-drift.yml
  - id: openwiki-source-6d4b4e707b8d60b6ccfa3425
    resource: repo://.github/workflows/openwiki-update.yml
  - id: openwiki-source-727b56653fd0103b1858eee2
    resource: repo://.gitleaks.toml
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-a979ae6af698feebfb1aea53
    resource: repo://docs/04-application-standards/GITHUB-ACTIONS-SECRET-AND-VARIABLE-REGISTRY.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Continuous integration workflows

Three workflows run in this repository. Two enforce rules, one produces
documentation. All three are written on the same principle stated in the review
configuration: a workflow that always passes is worse than no workflow, because
it looks like coverage.

Every third-party action is pinned to a commit SHA with the version in a
trailing comment, and every checkout sets `persist-credentials: false` —
`actions/checkout` otherwise writes the job token into `.git/config`, and these
jobs then run repository-controlled scripts that have no need for authenticated
git.

## Per-change checks

`.github/workflows/hx-checks.yml` runs on pushes to the default branch, on every
pull request, and on manual dispatch. Its opening comment states the design
rule: every check corresponds to a defect actually found in this repository, so
a written rule fails loudly instead of drifting quietly.

**Documentation consistency** runs the whole hx-doc suite in sequence — the link,
vocabulary, filename and evidence check; the fleet regeneration check; proof-DAG
validation with its generated-block check; mirror comparison; server-record
completeness; and smoke-authority completeness. It then runs `hx-gate-tests`,
which breaks the thing each of those gates guards and requires the gate to fail.
That last step is the check on the checks, and it is described in
[enforcement gate tests](../testing/enforcement-gate-tests.md).

**Execution artifacts** covers the shell and Python surface:

- shellcheck at warning severity over the runbook blocks, the per-server
  wrappers, the shared library and environment file, the smoke-runner scripts
  and the hx-doc wrappers. The file list is assembled with globs and then
  filtered to exclude `.py`, because the `hx-*` globs also match the Python
  bodies, which shellcheck cannot parse;
- a line-ending and permission check that fails on any CRLF or non-executable
  shell script, since either would break execution on a server;
- `python3 -m compileall` over `tools/`.

**Secret scan** installs gitleaks and scans both the working tree and the full
history — which is why this job alone checks out with `fetch-depth: 0`. The
binary is installed rather than the action, because the gitleaks action requires
a paid licence for organisation-owned repositories while the binary is MIT and
free. It is pinned by version *and* verified by SHA-256 before installation,
with the installed version confirmed afterwards: `releases/latest` previously
installed whatever shipped that morning, unchecked, and this is the tool that
decides whether a credential reached the repository.

### One deliberate scanning exception

`.gitleaks.toml` extends the default rule set with a single narrow allowlist.
Every smoke test is a known-answer test that sends a fixed string and requires
it back verbatim, and those strings are named `TOKEN` in the procedures, so the
generic API key rule flags all of them.

The allowlist is worth reading closely because of one keyword. It sets
`condition = "AND"`, requiring both that the file is a smoke-test authority
**and** that the finding matches the HX known-answer token pattern. Without it
either condition alone sufficed, which switched the rule off for every
smoke-test document — a real credential pasted into one would have been ignored.

## Weekly pin currency

`.github/workflows/hx-upstream-drift.yml` runs Monday mornings and on demand. It
checks that every pinned artifact is still fetchable, then produces one Markdown
report combining the reviewed-commit drift for governed skills with the product
version pins, writes it to the job summary, and opens or comments on a single
issue titled *Version pins have drifted*.

Its treatment of failure is the interesting part. **Drift does not fail the
job**: a pin stays valid until the owner decides to move it, so a moved upstream
is information and gets an issue. **An unreachable upstream does fail the job**,
with an explicit error, because in that case nothing was compared and reporting
that as a clean run would be exactly the check-that-cannot-fail this repository
keeps removing. The tools behind it are described in
[version pins and upstream drift](version-pins-and-upstream-drift.md).

## Scheduled wiki regeneration

`.github/workflows/openwiki-update.yml` regenerates `openwiki/` weekly on Sunday
mornings and opens a documentation pull request. It is weekly rather than daily
because fleet documentation does not change daily and every run is billable, and
a concurrency group prevents a manual dispatch from racing the scheduled run for
the same branch.

Its header records four places where it deliberately departs from, or corrects,
the upstream example it was adapted from:

1. The upstream README says to create a separate pull-request token because a
   pull request opened with the default job token does not start `pull_request`
   workflows — then the example never passes it, so the required checks it exists
   to trigger still never run. The token is passed here.
2. The README says not to auto-merge changes to executable workflow files, yet
   the example's own write scope includes the workflow file, the agent contract
   and its pointer file. Here the write scope is the generated tree and nothing
   else.
3. The README says to pin every action and package; the example installs the
   generator unpinned. It is pinned here.
4. Third-party tracing is removed and telemetry disabled, so nothing about this
   repository is sent to an external trace store.

Two structural details matter. The secret check is a **separate job** that the
main job depends on, not a first step: two later steps carry `if: !cancelled()`
so that a partial run still opens a pull request, and that condition is also
true when an earlier step failed — as a step the check would refuse to start and
the job would open a pull request anyway with an empty token. And the checkout
pins `ref` to the default branch with full history, because the generator diffs
against the commit it last documented and a shallow clone hides it, producing an
empty change summary and no documentation.

Generation itself is allowed to fail part way. The step sets
`continue-on-error`, the transient run-state file is deleted, the pull request
is opened describing the outcome, and only then is the failure propagated —
because pages that completed are durable and become the baseline for the next
run, so merging is how that progress is kept.

## Secrets

The repository keeps a registry of approved Actions secret and variable
**names** and their handling rules, deliberately without values, so a credential
is never introduced ad hoc. Its standing rules are that secret values never
appear in Markdown, scripts, manifests, evidence, workflow logs or environment
examples; that a sensitive credential is never duplicated into a plaintext
Actions variable; that workflows reference identifiers by name only; and that an
exposed credential is rotated rather than reused.

The two secrets the wiki job needs — a repository-scoped fine-grained token with
contents and pull-request write, and a model API key — were authorised by a
ratified decision that records the accepted risk in full, including the residual
one no line in the workflow can remove: manual dispatch runs the workflow file
from the ref the operator chooses, so a branch that edits that file can read
both secrets. The stated control there is who holds write access, plus branch
protection, not anything inside the file. See
[owner decisions and document lifecycle](../concepts/owner-decisions-and-document-lifecycle.md).
