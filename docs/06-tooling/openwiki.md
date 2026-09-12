# OpenWiki

## What it is

OpenWiki generates and maintains a Markdown wiki about this repository, under
`openwiki/`. Upstream states the purpose plainly: coding agents "read a
curated wiki first, then inspect source only where they need more detail".
The primary audience is agents, not people.

Every material statement it writes is a **Claim**, pinned to exact lines with
a hash, for example
`repo://tools/hx-doc/hx_gate_tests.py#L1-L11` at
`repo-lines-v1:sha256:867db1b5...`. Change those lines and the Claim goes
stale on the next run and must be reconciled. That is real drift detection
between the wiki and the code.

What it does not do: it cannot watch hand-written documents, and it cannot
know why a tool was adopted. Intent is a decision, not something derivable
from source. That is why this document exists and is not generated.

## Why we have it

Without it, anyone arriving at this repository - person or agent - has to read
the whole thing to gain context, and a README does not close that gap. The
cost is paid again by every agent on every session.

Adopted by **D-023**, which also records the accepted risk of the two Actions
secrets on a public repository.

## When to use it

- **Run `--update`** after a change that alters how the repository works:
  a new gate, a changed runbook pattern, a new decision. Not after a typo.
- **Do not run `--init`** on this repository again. The wiki exists. `--init`
  regenerates the tree wholesale; `--update` diffs against the last documented
  commit and rewrites only what changed.
- **Read `openwiki/` before reading source** when the question is "how does
  this repository work". Read the control Markdown instead when the question
  is "what are we allowed to do" - see
  [openwiki-agents.md](openwiki-agents.md).

## How to use it

**Free, and the normal path.** Inside Claude Code, in this repository:

> Update OpenWiki for this repository.

The Claude Code integration hands authoring to the session's model, so no
provider key is used and nothing is billed. OpenWiki still owns the page
queue, Claims validation and finalization.

**Steering what it covers.** `openwiki/INSTRUCTIONS.md` is owner-authored and
OpenWiki never rewrites it, including across `--init`. Change coverage there,
not by editing generated pages.

**What it must not scan** is listed in `.openwikiignore`: `archive/`,
`human-html/`, `graft/`, `.claude/`.

**Viewing it.** OpenWiki ships its own viewer:

```bash
openwiki visualize
openwiki visualize --export ./out
```

This is separate from `graft viz`, which draws the code graph. Different tool,
different graph.

**Scheduled refresh.** `.github/workflows/openwiki-update.yml` runs weekly,
Sunday 08:00 UTC, and opens a pull request. It is not auto-merged.

> **This one costs money.** The scheduled job is headless, so it cannot borrow
> a Claude Code session. It uses `ANTHROPIC_API_KEY` from Actions secrets and
> bills on every run. A local `--update` costs nothing. Prefer local.

**Secrets in use:** `OPENWIKI_PR_TOKEN` (Contents and Pull requests, read and
write) and `ANTHROPIC_API_KEY`. Both recorded in D-023.

**Telemetry** is on by default and sends error categories to PostHog. Off
with:

```bash
echo "OPENWIKI_TELEMETRY_DISABLED=1" >> ~/.openwiki/.env
```

### Running it against the fleet's own model — VERIFICATION REQUIRED

A local run already costs nothing through the Claude Code integration, so this
is only needed for a headless run without a Claude session. OpenWiki reaches a
local Ollama through its `openai-compatible` provider, which is **not** the
same as `openai`:

```bash
OPENWIKI_PROVIDER=openai-compatible
OPENAI_COMPATIBLE_BASE_URL=http://192.168.50.202:11434/v1
OPENAI_COMPATIBLE_API_KEY=unused
OPENWIKI_MODEL_ID=<the model HX-2 serves>
```

If OpenWiki is ever pointed at OpenRouter instead, pin the upstream provider
with `OPENWIKI_OPENROUTER_PROVIDER_ONLY`. OpenRouter routes one model id to
several upstream providers and they do not behave identically; pinning removes
that variable. This repository uses Anthropic in CI, so the setting is
unused today and recorded so the option is not rediscovered later.

Some gateways accept only streaming; if so add
`OPENWIKI_OPENAI_COMPATIBLE_STREAMING=true`.

**This has never been run.** HX-2 is not reachable from the workstation and
the lab opens Saturday. The command is transcribed from upstream
documentation, not observed working. Prove it before relying on it.

Note this is OpenWiki's schema alone. graft uses different variable names and
has no `openai-compatible` value at all.

### Undoing it

Delete the workflow file and revoke both secrets. `openwiki/` can be removed
with `git rm -r openwiki` and the blocks in `AGENTS.md` and `CLAUDE.md`
deleted between their markers. Nothing else depends on it.

## Upstream

- Documentation: <https://docs.langchain.com/oss/openwiki/overview>
- Source: <https://github.com/langchain-ai/openwiki>
- Installed version: 0.5.1 (upstream tag `v0.5.1`, published 2026-09-10)

Upstream also ships example CI for **GitLab CI** and **Bitbucket Pipelines**
alongside GitHub Actions. This repository uses GitHub Actions; the others are
recorded so nobody concludes OpenWiki is GitHub-only.

OpenWiki also has a **Personal mode**, a separate local wiki in
`~/.openwiki/wiki` built from Gmail, Notion, Slack, X, web search, Hacker News
and local repositories. It is not used here and touches nothing in this
repository. Its `cron` scheduling is macOS only.
