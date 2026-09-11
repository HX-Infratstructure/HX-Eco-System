# hx-doc — repository consistency tooling

Seven small tools. Each exists because the matching failure actually happened
here, and each converts a written rule into something that fails loudly.

No third-party dependencies. Python 3 standard library only.

| Tool | Replaces | Enforces |
|---|---|---|
| `hx-fleet` | six hand-typed server tables | every fleet table and the runbook IP map comes from `docs/00-control/hx-fleet.tsv` |
| `hx-proof` | a hand-drawn DAG that omitted 11 of 29 steps | every proof step and edge comes from `docs/00-control/hx-proof.tsv`, and a PASS cannot skip its prior proof |
| `hx-render-html` | hand-written HTML mirrors | a mirror always matches its Markdown source |
| `hx-doc-check` | proofreading | links resolve, vocabulary is defined, filenames are stable, evidence is committable |
| `hx-version-pins` | remembering to look | product pins match what upstream ships, and applications do not come from the Ubuntu archive or Snap |
| `hx-upstream-drift` | remembering to look | the registry's reviewed commits still match upstream |
| `hx-record-check` | hoping the template was followed | server records carry every required section, and open gaps stay visible |
| `hx-smoke-lint` | hoping | smoke-test authorities carry every required section |
| `hx-new-server` | copy and paste | a new server's runbook and record are complete from the start |
| `hx-doc-supersede` | six manual steps | the archive procedure happens the same way every time |
| `hx-preflight` | finding a 404 on a lab machine | every pinned artifact is still fetchable, checked from anywhere |

## The fleet is the source of truth

`docs/00-control/hx-fleet.tsv` holds the 17-server map: `id`, `ip`, `role`,
`state`, `gate`, `note`. Edit it, then run `hx-fleet`. That regenerates every
marked table in the documents and `docs/03-runbooks/common/hx-fleet-ips.env`,
which the runbooks source for the host to IP lookup.

A document opts in by carrying markers:

```text
<!-- HX-FLEET:TABLE columns=id,ip,role,state -->
<!-- /HX-FLEET:TABLE -->
```

## Everyday use

```bash
tools/hx-doc/hx-fleet              # after editing hx-fleet.tsv
tools/hx-doc/hx-render-html        # after editing any Markdown
tools/hx-doc/hx-doc-check          # before committing
tools/hx-doc/hx-record-check       # what is still open in the server records
```

## The proof chain

`docs/00-control/hx-proof.tsv` holds the 30 smoke steps and the dependency
between them. Edit it, then run `hx-proof` to regenerate the phase tables and
the dependency diagram in the smoke-test roadmap.

```bash
tools/hx-doc/hx-proof --list        # every step, and what it is waiting on
tools/hx-doc/hx-proof --ready B2    # can this run yet
tools/hx-doc/hx-proof --check       # CI: valid DAG, generated blocks current
```

It rejects a dangling `requires`, a cycle, a missing authority file, an unknown
host, and an unrecognised status. `hx-smoke-promote` reads the same file and
refuses a PASS whose prior proof has not passed and been cited.

The hand-maintained version it replaced had 19 nodes — the foundation plus 18
of the 29 steps — against 30 rows in the TSV:
every MCP companion gate, both Web UI gates and the reranker were missing from
the diagram, and nothing compared the two.

## A note on graft

`graft` indexes 70 of 388 files here — the Python tools and the shell blocks.
It does not read Markdown, and it produces no call edges for shell. An empty
`graft` result means "not in the graph", never "does not exist".

`archive/` is indexed and cannot currently be excluded, so six superseded
runbook blocks show up in results. Upstream issue: trailhq/Graft#353.

## Before a build day

```bash
tools/hx-doc/hx-preflight
```

Confirms every download the install blocks make still resolves, every pinned
PyPI and npm version still exists and is not yanked, every pinned Hugging Face
revision still resolves, and the pinned NVIDIA driver is still installable on
noble/amd64. Downloads nothing; about thirty seconds. Run it the morning of a
build so a dead pin is found before a machine is touched, not during.

## Version currency

```bash
tools/hx-doc/hx-version-pins       # Ollama, NVIDIA, reranker, Python deps
tools/hx-doc/hx-upstream-drift     # the 9 pinned skill commits
```

Both run weekly in CI and open one issue when something moves. Drift is
information, not a failure: a pin stays valid until the owner moves it.

`hx-version-pins` also enforces the package-source rule. Application software
comes from PyPI, a GitHub release, a direct binary, or Hugging Face. The Ubuntu
archive is for drivers only, and an application pinned there is reported as
REVIEW with a migration note.

## Starting a new server

```bash
tools/hx-doc/hx-new-server hx-9 --no-ollama
```

Creates the runbook wrappers, the runbook README, and the server record from
`docs/02-server-records/_TEMPLATE.md`. Use `--no-ollama` for any host that is
not an inference server. Existing files are never overwritten without `--force`.

## Superseding a document

```bash
tools/hx-doc/hx-doc-supersede docs/00-control/DECISIONS.md --suffix pre-d019
```

Archives the current copy and its mirror under `archive/<today>/`, leaves the
active file for you to edit, then tells you to re-render and check. Add
`--dry-run` to see what it would do.

## CI

`.github/workflows/hx-checks.yml` runs `hx-doc-check`, `hx-render-html --check`,
`hx-fleet --check`, `hx-record-check`, `hx-smoke-lint`, shellcheck, a
CRLF/executable-bit check, a Python compile, and a secret scan on every pull
request. `.github/workflows/hx-upstream-drift.yml` runs the two currency tools
weekly.
