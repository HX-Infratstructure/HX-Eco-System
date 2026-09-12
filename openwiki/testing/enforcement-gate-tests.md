---
type: testing
title: Enforcement gate tests
description: The meta-check that proves the repository's own gates still fail on what they guard — a throwaway copy of the tree, one deliberate corruption per gate, and an asserted non-zero exit, including tests that a skip is a skip and not a hole.
tags: [testing, gates, meta-check, mutation, ci]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-4a10bba62772b26bb2a2e6b3
    resource: repo://.github/workflows/hx-checks.yml
  - id: openwiki-source-9507fc66f6719dc4c336f195
    resource: repo://tools/hx-doc/hx_gate_tests.py
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Enforcement gate tests

Every check in this repository enforces a written rule. The problem with a check
is that it can quietly stop checking — a regex that no longer matches, a
condition that can never be false, a skip that widened into a hole — and it will
keep printing `OK` while it does. The repository's phrase for that is that a
check which cannot fail looks like coverage and is not.

`tools/hx-doc/hx-gate-tests` is the answer. It breaks the thing each gate guards
and requires the gate to fail.

## How the harness works

Four small pieces, and nothing more:

- **`fresh()`** replaces a scratch copy of the whole repository, excluding
  `.git`, before every test, so no test can affect another. It then runs
  `git init` in the copy — because the documentation checker asks
  `git check-ignore` about the evidence path, and outside a work tree that exits
  128, which the checker correctly treats as a failure. Every test expected a
  non-zero exit anyway, so the harness had been checking documents in an
  environment where one of its checks could not pass, and never noticed.
- **`edit(rel, fn)`** rewrites one file in the scratch copy through a function.
- **`run(...)`** executes a tool inside the copy with the current interpreter and
  returns its exit status and combined output.
- **`check(label, cond, detail)`** records one result; the process exits
  non-zero if any test failed.

A baseline test runs first, asserting that the fleet check *passes* on an
unmodified copy. Without it, a harness whose scratch copy was broken in some
unrelated way would report every mutation test as a success.

Assertions test the exit status **and** a distinctive fragment of the output, so
a tool that fails for an unrelated reason does not count as the gate firing.

## What is mutated

Roughly two dozen tests, one or more per gate.

**Fleet generation.** Appending an unclosed marker must be reported as drift.
Renaming a column to an unknown name must be reported, with the bad name in the
output.

**Server records.** Leaving the template's `NOT STARTED | IN PROGRESS | PASS`
option list in a record must be drift, since a record states one value. Changing
a state to `NOT APPLICABLE` must be drift, which is the near-miss the old
substring comparison accepted for `NOT STARTED`. Deleting the state line
entirely must be drift too.

**Documentation checks.** A link that traverses out of the repository — to a
path that genuinely exists on the machine running the test — must still be
reported as broken.

**Upstream drift.** Duplicating a repository line in the skill registry, so the
repository and reviewed-commit counts no longer match, must be refused rather
than silently zipped into a wrong pairing.

**Preflight.** Emptying a version pin must fail with "no version pinned" rather
than being skipped.

**Server scaffolding.** A misspelled flag such as `--no-olama` must exit 2 with
an unknown-option message. Renaming a placeholder in the record template must be
refused, since a substitution that silently matches nothing would ship a record
still containing placeholders.

**Proof chain.** A duplicate phase marker in the roadmap must be drift, naming
the phase. A `requires` edge pointing at a step that does not exist must be
refused, naming the unknown id.

**HTML mirrors.** Editing a Markdown source without re-rendering must fail as
stale.

**Smoke-test linting.** Four separate mutations, because this check was
sharpened repeatedly: stripping every known-answer phrase must fail; removing
the retention statement must fail; cutting the evidence section to a bare
heading must fail; and — most instructively — replacing it with *"Do not retain
credentials in evidence, and do not retain secrets"* must also fail. That last
sentence contains both "evidence" and "retain", which is precisely why the check
is anchored to the standard retained-bundle path instead of to either word.

**Unit claims.** A block that reports a systemd unit nothing creates must fail.
And a block that reports a unit while merely *mentioning* its path — an `rm` of
the unit file — must still fail, so a mention cannot be mistaken for a creation.

## Two tests that guard a skip

The documentation checker deliberately skips generated trees, and a skip is one
edit away from becoming a hole. Two tests hold it in place. A broken link
written into a generated page must **not** be a finding and must not even appear
in the output. The same broken link written into an authored document must fail.
Together they assert that the exclusion excludes exactly what it is supposed to
and nothing more.

## Two tests that avoid testing a copy of themselves

The package-source rule is exercised by importing the shipped function directly
and calling it with five inputs: a Snap application, a Snap driver, an
Ubuntu-archive driver, an Ubuntu-archive application and a PyPI application. That
works without any network access because the rule was deliberately factored out
of the reporting loop — see
[version pins and upstream drift](../operations/version-pins-and-upstream-drift.md).

The version comparator is handled more unusually. Rather than reimplementing the
sort, the harness extracts the shipped comparator's source with a regex, executes
it, and asserts that `595.71.05` sorts above `595.9.05` — a case lexicographic
ordering gets wrong. The stated reason is that a test which reimplements the
logic it is checking proves only that the test is self-consistent. If the
comparator can no longer be found in the source, that itself is a recorded
failure.

## Where it runs

`hx-gate-tests` is the final step of the documentation job on every pull request
and push, immediately after the gates it tests, so a gate that has stopped
catching anything fails the change that broke it. See
[continuous integration workflows](../operations/continuous-integration-workflows.md).

## Adding a gate

The convention that follows is short: when a new check is added, add the test
that breaks what it guards. The tools it covers are described in
[repository consistency tooling](../operations/repository-consistency-tooling.md).
