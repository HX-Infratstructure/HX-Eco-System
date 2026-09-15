---
document: HX Eco-System GitHub Actions Secret and Variable Registry
status: current
version: 1.2
date: 2026-09-14
scope: HX-Eco-System repository automation identifiers
authority: HX-Eco-System clean rebuild
---

# GitHub Actions Secret and Variable Registry

## Purpose

Record the approved **names and intended use** of repository automation secrets and variables without storing sensitive values in Git history.

## Current automation status

Two workflows are active as of 2026-09-14:

| Workflow | Trigger | Secrets used |
|---|---|---|
| `.github/workflows/hx-checks.yml` | push, pull request | `GITHUB_TOKEN` only (automatic) |
| `.github/workflows/hx-upstream-drift.yml` | weekly schedule, manual | `GITHUB_TOKEN` only (automatic) |

Correction of record: this table never recorded
`.github/workflows/openwiki-update.yml` or the two secrets D-023 authorised
for it (`OPENWIKI_PR_TOKEN`, `ANTHROPIC_API_KEY`), despite the rule below
requiring a row when a workflow starts using one. Both secrets **were**
created and the workflow **did** run: its scheduled run of 2026-09-13 passed
the secrets preflight, generated documentation with a paid model
(`claude-sonnet-5`), pushed branch `openwiki/update` (commit 5b20167), and
that branch is open as PR #16. The workflow was withdrawn by D-025 on
2026-09-14 and its file is deleted. Both secrets remain in repository
settings until revoked; revoking them is a required owner action. The gap is
recorded here rather than erased.

## Registered identifiers

| Name | GitHub type | Purpose | Value handling |
|---|---|---|---|
| `HXES_SECRET` | Actions secret | Sensitive credential/token used by HX-Eco-System automation when required | Store only in GitHub's encrypted secret mechanism or another owner-approved secret store. Never commit the value. |
| `HXES_VARIABLE` | Actions variable | Non-sensitive HX-Eco-System automation configuration | Plain text is permitted only when the value is genuinely non-sensitive. Never place a PAT, password, private key, API key, bearer token, or other credential here. |

## Rules

1. Secret values never appear in repository Markdown, scripts, manifests, evidence, workflow logs, or `.env` examples.
2. A secret and a variable may have related roles, but the same sensitive credential must not be duplicated into a plaintext Actions variable.
3. Workflow files reference identifiers by name; they do not embed credential values.
4. If a token or credential is exposed in plaintext during staging or troubleshooting, treat rotation/replacement as the clean follow-up before long-term use.
5. `.local.env.example` and similar templates contain names only and blank values.

## Source disposition

The temporary Drive staging file `00-Control/key.md` (external to this repository, not a repository path) supplied the identifiers `HXES_SECRET` and `HXES_VARIABLE`. Its sensitive value is intentionally not reproduced here. The staging file is archived after reconciliation and is not current authority.
