# OpenWiki — agent operating guide

For an agent working in this repository. The human-facing document is
[openwiki.md](openwiki.md); costs, secrets and the schedule live there and are
not repeated here.

## Read this first: which question goes where

`openwiki/` answers "how does this repository work". It never answers "what am
I allowed to do".

| The question | The source | Authority? |
|---|---|---|
| How does this repository work? Where does X live? | `openwiki/quickstart.md`, then the section page | context |
| Where is this symbol, who calls it? | graft — `graft ask`, `graft callers` | context |
| What is the fleet, host by host? | `docs/00-control/hx-fleet.tsv` | **authority** |
| Is this decided, or still open? | `docs/00-control/DECISIONS.md` | **authority** |
| What must this smoke step prove? | the `smoke-tests/` authority for that component | **authority** |
| May this proof step run yet? | `tools/hx-doc/hx-proof --ready <id>` | **authority** |
| What are the rules for agents here? | `AGENTS.md`, section 2 for the truth order | **authority** |
| What is actually installed on a host? | the server record, plus live evidence | **authority** |

Start at `openwiki/` to orient. Move to the authority column before changing
anything or asserting a rule. Reading source is the last step, not the first;
that is the whole reason the wiki exists.

## Generated pages are never authority

Every page under `openwiki/` is written by a model from the code. It can be
wrong, and it is always behind the working tree by at least one run.

A Claim carries its evidence: `repo://<path>#L<start>-L<end>` and a hash of
those exact lines. If a page states something load-bearing, open its Claim,
open the cited lines, and trust the lines.

A **stale** Claim means the cited lines changed. It is a signal to recheck the
source, never a licence to delete the statement.

## Never hand-edit these

| Path | Why |
|---|---|
| `openwiki/**/*.md` except `INSTRUCTIONS.md` | regenerated; your edit is lost |
| `openwiki/.claims/**` | OpenWiki owns evidence reconciliation |
| `openwiki/.page-manifest.json`, `.last-update.json`, `.run.json` | run state |
| between `<!-- OPENWIKI:START -->` and `<!-- OPENWIKI:END -->` in `AGENTS.md` and `CLAUDE.md` | regenerated every run |

**Editable, and the supported way to change the wiki:**
`openwiki/INSTRUCTIONS.md`, `.openwikiignore`, and anything outside the
OpenWiki markers — including `AGENTS.md` section 16, which is where this
repository's authority statement lives precisely because it survives.

## The block hazard, and what to do about it

OpenWiki's first run wrote "Treat source code and tests as authoritative" into
the `AGENTS.md` block. `AGENTS.md` section 2 does not list source code at all.
A regeneration on 2026-09-12 put it back, which proves it recurs.

`hx-doc-check` refuses it. If that check fails:

1. Do not edit the block. The next run overwrites it.
2. Fix `openwiki/INSTRUCTIONS.md`, which states the truth order and tells the
   generator not to contradict it.
3. Re-run `--update` and confirm the check passes.

Section 16 of `AGENTS.md` sits outside the markers and governs regardless.

## Running it

Through the host integration, inside this repository:

> Update OpenWiki for this repository.

OpenWiki drives a resumable page-job lifecycle — `openwiki_begin`,
`openwiki_submit_plan`, then `openwiki_next_page` and `openwiki_submit_page`
per page, then `openwiki_finish`. The host agent researches and writes each
page with its own tools. If `openwiki_begin` returns `status=noop`, no update
is required: report that and stop.

Never run bare `openwiki --init` in a shell here. Two separate reasons.
It opens an interactive setup that asks for an inference provider, a model
and an API key - the CLI banner shows its defaults as OpenAI and
`gpt-5.6-terra` - none of which this repository needs, because the host
integration supplies the model. And `--init` replaces the wiki wholesale,
where `--update` rewrites only what changed.

## After any run

```bash
tools/hx-doc/hx-doc-check
```

`openwiki/` is a skipped tree, so a broken link inside a generated page is not
a finding — fix the generator or the source, not the page. A failure naming
`authority:` is the block hazard above.
