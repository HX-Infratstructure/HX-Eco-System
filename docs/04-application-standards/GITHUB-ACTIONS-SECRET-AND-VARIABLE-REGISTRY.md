---
document: HX Eco-System GitHub Actions Secret and Variable Registry
status: current
version: 1.0
date: 2026-09-09
scope: HX-Eco-System repository automation identifiers
authority: HX-Eco-System clean rebuild
---

# GitHub Actions Secret and Variable Registry

## Purpose

Record the approved **names and intended use** of repository automation secrets and variables without storing sensitive values in Git history.

## Current automation status

Two workflows are active as of 2026-09-10:

| Workflow | Trigger | Secrets used |
|---|---|---|
| `.github/workflows/hx-checks.yml` | push, pull request | `GITHUB_TOKEN` only (automatic) |
| `.github/workflows/hx-upstream-drift.yml` | weekly schedule, manual | `GITHUB_TOKEN` only (automatic) |

Neither consumes `HXES_SECRET` or `HXES_VARIABLE` yet. Those identifiers stay
reserved with their handling rules fixed in advance, so a value is never
introduced ad hoc. Add a row above when a workflow starts using one.

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
