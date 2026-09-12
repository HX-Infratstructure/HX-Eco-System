---
type: operations
title: Repository consistency tooling
description: The thirteen hx-doc tools that turn written rules into failing commands — what each one enforces, the wrapper-plus-Python-body structure and why the wrapper resolves its own interpreter, the standard-library-only constraint, and the specific defect behind each check.
tags: [tooling, checks, enforcement, hx-doc, python, cli]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-45924c2e46a6dbd9a7d521f8
    resource: repo://docs/03-runbooks/common/hx-app-lib.sh
  - id: openwiki-source-031feb6606529a37844764d1
    resource: repo://tools/hx-doc/hx_doc_check.py
  - id: openwiki-source-97e1d90aab73bf6b59824395
    resource: repo://tools/hx-doc/hx_new_server.py
  - id: openwiki-source-bf6a46fe85337b9b2d7d499a
    resource: repo://tools/hx-doc/hx_record_check.py
  - id: openwiki-source-363db13c90e3016aa0f261ab
    resource: repo://tools/hx-doc/hx_smoke_lint.py
  - id: openwiki-source-386db2e093752f65e4a2f48b
    resource: repo://tools/hx-doc/hx-doc-check
  - id: openwiki-source-f2994b36a477b8759d39a2a6
    resource: repo://tools/hx-doc/README.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Repository consistency tooling

`tools/hx-doc/` holds thirteen small tools. The suite's own framing is blunt:
each exists because the matching failure actually happened here, and each
converts a written rule into something that fails loudly. Treat a failure as a
real defect rather than noise to work around — fixing a wrong check is itself a
reviewed change, and weakening one so an existing document passes is not
allowed.

## Shape and constraints

Every tool is a pair: an extensionless bash wrapper that operators invoke, and a
`.py` body beside it holding the logic. The wrapper does one non-obvious thing —
it probes candidate interpreters and picks the first that actually reports
Python 3, rather than assuming `python3` is one. On Windows a `python3` App
Execution Alias sits on `PATH` and is not an interpreter, so the naive form
fails confusingly. If nothing works the wrapper says so and exits 1.

There are no third-party dependencies anywhere in the suite; the constraint is
Python 3 standard library only, matching the fleet's own minimal-dependency
posture, and the review configuration flags any new third-party import in
`tools/`.

## What each tool enforces

| Tool | Replaces | Enforces |
|---|---|---|
| `hx-fleet` | six hand-typed server tables | every fleet table and the runbook host lookup comes from the fleet TSV |
| `hx-proof` | a hand-drawn DAG that omitted 11 of 29 steps | the proof steps and edges come from the proof TSV, and a PASS cannot skip its prior proof |
| `hx-render-html` | hand-written HTML mirrors | a mirror always matches its Markdown source |
| `hx-doc-check` | proofreading | links resolve, vocabulary is defined, filenames are stable, evidence is committable |
| `hx-version-pins` | remembering to look | product pins match what upstream ships, and no application comes from the Ubuntu archive or Snap |
| `hx-upstream-drift` | remembering to look | the registry's reviewed commits still match upstream |
| `hx-record-check` | hoping the template was followed | server records carry every required section, and open gaps stay visible |
| `hx-smoke-lint` | hoping | smoke-test authorities carry every required section |
| `hx-new-server` | copy and paste | a new server's runbook and record are complete from the start |
| `hx-doc-supersede` | six manual steps | the archive procedure happens the same way every time |
| `hx-preflight` | finding a 404 on a lab machine | every pinned artifact is still fetchable, checked from anywhere |
| `hx-graft-bash` | a code graph that ignored every shell file | the executable surface is searchable |
| `hx-gate-tests` | trusting that a check still checks | every checking tool above is broken on purpose and required to fail |

The three generators are described in
[generated artifacts and single sources of truth](../concepts/generated-artifacts-and-single-source-of-truth.md);
the currency tools in
[version pins and upstream drift](version-pins-and-upstream-drift.md);
and the meta-check in
[enforcement gate tests](../testing/enforcement-gate-tests.md). The rest are
described below.

## hx-doc-check

Six checks over the active documentation set, which excludes the generated,
vendored and archived trees — a link or filename inside one of those is not a
finding against this repository.

**Links.** Every Markdown link and every backticked path reference must resolve.
Two refinements matter. A reference may be an intentional forward reference, and
the checker accepts one when the surrounding line *or its nearest preceding
heading* declares it — so an "authority gap" section covers the bullets beneath
it. And a traversal that resolves outside the repository is rejected rather than
satisfied by whatever happens to exist on the machine running the check.

**Vocabulary.** The skill registry may use only the lifecycle states the
governance document defines, read live from that document's registry-status
section rather than from a hard-coded list. If the section cannot be found, that
is itself a failure — a vocabulary check with nothing to check against would
pass everything.

**Frontmatter.** Control documents that carry frontmatter must carry
`document`, `status` and `date`.

**Duplicates.** No active Markdown filename may contain a version suffix, a
parenthesised number, `final-final` or an embedded date.

**Evidence.** A probe path is passed to `git check-ignore` to confirm
`.gitignore` cannot silently swallow retained evidence logs. The exit status is
read precisely: `0` means ignored and fails, `1` means committable and passes,
and anything else is reported as an error — treating "not zero" as success once
let a git failure report the evidence path as safe.

**Unit claims.** A runbook block may only tell the operator to check a systemd
unit that the block actually creates. Five blocks named a unit nothing in the
file creates, so the printed reboot check could only ever fail. The check strips
comment lines first — comments and an `rm` mention unit paths without creating
anything, and matching those would make the check unfailable — then requires a
real creation: the shared unit helper, or a `tee`, `cp`, `install` or redirect
writing the unit file.

## hx-record-check

Turns the server-record template from advice into a gate, and keeps recorded
gaps visible. It reports three kinds of problem per record:

- **MISSING** — a required section is absent. A record may declare sections
  genuinely not applicable, in one line with a reason, and those are exempted.
- **UNRESOLVED** — a field explicitly recorded as not yet known. These are
  *soft*: they are recorded gaps, not errors, and the tool says so while urging
  they be closed while the server is still reachable. `--strict` promotes them
  to failures.
- **DRIFT** — the record's stated build state disagrees with the fleet TSV.

The drift comparison is deliberately exact. It normalises both values and
compares them whole, because an earlier version took the first word of the fleet
value and asked whether it appeared anywhere in the record — under which `NOT
STARTED` was satisfied by `NOT APPLICABLE`, and `IN PROGRESS` by `INSTALLED`.
Records that predate the current scaffold write state and gate together as
`PASS / CLOSED`, so only the state part is compared.

## hx-smoke-lint

All nineteen smoke-test authorities share one shape, and one of them shipped
with no mention of evidence at all before anything noticed. The linter requires
six canonical sections — purpose, prerequisites, steps, sample data, expected
output, cleanup — plus two content anchors: a known-answer marker, because
service health is not a smoke test, and evidence retention.

The evidence anchor shows how carefully a check has to be phrased. Matching the
word "evidence" was satisfied by a warning *about* evidence; matching "retain"
was satisfied by "do not retain credentials". The anchor is now the standard
retained-bundle path, which a negated sentence cannot fake, and it is matched
against the body with headings stripped, because an empty `## Evidence` heading
used to satisfy the check on its own.

## hx-new-server

Scaffolds a server before its build starts: the runbook wrappers, the runbook
README and the server record, driven from the fleet TSV and the record template.
`--no-ollama` omits the storage and Ollama block for a non-inference host, and
existing files are never overwritten without `--force`.

Three of its behaviours came from real failures. Unknown `--` options are
rejected rather than silently dropped, because `--no-olama` scaffolded the
Ollama block anyway and `--fore` overwrote nothing while reporting success. The
record is built and validated **before** anything is written, since validating
last left runbook files on disk with no record beside them. And each template
substitution must match exactly once — `str.replace` on a missing placeholder
does nothing and says nothing, so a template edit would have shipped a record
still reading `HX-N` and a placeholder address.

## Everyday use

```bash
tools/hx-doc/hx-fleet              # after editing hx-fleet.tsv
tools/hx-doc/hx-render-html        # after editing any Markdown
tools/hx-doc/hx-doc-check          # before committing
tools/hx-doc/hx-record-check       # what is still open in the server records
tools/hx-doc/hx-preflight          # the morning of a build day
```

Continuous integration runs the checking subset on every pull request, so the
practical rule is to run them locally first — see
[contributing and review](../workflows/contributing-and-review.md) and
[continuous integration workflows](continuous-integration-workflows.md).
