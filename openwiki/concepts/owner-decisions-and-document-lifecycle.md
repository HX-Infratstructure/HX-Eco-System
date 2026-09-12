---
type: governance-concept
title: Owner decisions and document lifecycle
description: How binding choices become durable in this repository — a numbered decision register with ratification dates and stated blast radius, one active copy of every document under a stable filename, and a scripted supersession into a dated archive that keeps history without leaving a second plausible current version.
tags: [decisions, governance, document-control, archive, supersession, lifecycle]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-2c909f1605c16498627e565e
    resource: repo://docs/00-control/DOCUMENT-CONTROL.md
  - id: openwiki-source-939aa3b5c336cc69710945f5
    resource: repo://docs/00-control/hx-fleet.tsv
  - id: openwiki-source-098d1e6d061bc743d981e84b
    resource: repo://docs/00-control/REPOSITORY-STATUS.md
  - id: openwiki-source-12296e6451a9d695ef6c70ca
    resource: repo://docs/03-runbooks/common/01-base-admin-network-updates.sh
  - id: openwiki-source-031feb6606529a37844764d1
    resource: repo://tools/hx-doc/hx_doc_check.py
  - id: openwiki-source-7535508c0d148b08f4414508
    resource: repo://tools/hx-doc/hx_doc_supersede.py
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Owner decisions and document lifecycle

Two mechanisms keep the repository from accumulating contradictions. Decisions
are recorded once, in one register, with an identifier other documents can cite.
Documents have exactly one active version, and superseding one is a scripted
procedure rather than a habit.

## The decision register

`docs/00-control/DECISIONS.md` holds owner-approved decisions as numbered
entries `D-001` upward. An entry is not a summary of a discussion; it is the
authority itself, and other documents, scripts and review rules cite the number
rather than restating the reasoning. `hx-fleet.tsv` notes cite `D-005`, `D-006`
and `D-010`; the base runbook cites `D-018` in a comment beside the line it
justifies; the review configuration cites `D-018` to tell the reviewer not to
raise a decided topic.

The register's shape has evolved. The early entries are one or two sentences
fixing a position: native Linux and systemd with no containers, a clean-room
rebuild in which historical configuration is reference only, embedding and
reranking placement, Granite-Docling placement, the NGINX boundary. The later
ones carry a **RATIFIED** date and considerably more structure, because they
settle something contested or costly. They state what was decided, why the
alternative was rejected, where the authoritative values live, what the residual
risk is, and how to reverse it.

Three properties are worth naming because they change how the register is read.

**A decision states its own blast radius.** The firewall and listener decision
does not merely permit the posture; it says in plain terms what that posture
means — any host that can reach the LAN can call an inference endpoint without
credentials — and marks that as accepted. It also distinguishes intent from
survey: the statement describes what the build scripts produce, while each
server record states the posture actually observed as that server closes.

**A decision can close a topic.** The same entry ends by instructing readers not
to re-raise firewall or listener hardening as a finding, because it is a decided
position rather than an open item. That is what stops the same objection being
rediscovered every review.

**A decision can resolve a contradiction between two existing rules.** The Snap
prohibition exists because the review configuration said one thing and the
runbook environment and pin checker said another; the owner ratified one wording
and the pin checker was changed to match, with dedicated gate tests holding the
rule in place afterwards. See
[version pins and upstream drift](../operations/version-pins-and-upstream-drift.md).

Decisions are also recorded **before** the thing they authorise exists where
that is possible — the write-capable Actions token was minuted before the
secrets were created, not after.

## One active version

The document control standard permits exactly one current copy of a document in
the active tree. Active files:

- use stable filenames with no version number and no date in the name;
- carry `document`, `status` and `date` inside the file as frontmatter;
- live under `docs/`.

Duplicates of the familiar kinds — `-v1.2`, a dated copy, `(1)`, `final-final`,
a model-name-prefixed variant — are prohibited outright, and the pattern is
checked mechanically rather than trusted: `hx-doc-check` scans active Markdown
filenames for those shapes and fails on a match. It also requires every control
document that has frontmatter to carry the `document`, `status` and `date` keys.

The reason for the rule is the failure it prevents. Two plausible current
documents force a reader to guess which one is authority, and an agent guessing
wrong is indistinguishable from an agent being told the wrong thing.

## Superseding a document

Retiring a version is a six-step procedure in the standard: create the dated
archive directory mirroring the active path, copy the prior Markdown there,
archive the matching HTML mirror, replace the active Markdown at its stable
path, replace the mirror, and confirm exactly one active version remains.

Done by hand, that churned — the history shows six commits spent archiving one
README plus three stray marker files created and deleted. `hx-doc-supersede`
performs it in one command:

```bash
tools/hx-doc/hx-doc-supersede docs/00-control/DECISIONS.md --suffix pre-d021
```

It stamps `archive/<today>/<same-path>/`, copies the current Markdown there with
the suffix appended, archives the generated mirror when one is committed, and
**leaves the active file in place** to be edited. It then prints the two
commands that must follow — re-render the mirrors, run the document check — and
asks for the edit and the archive copy to land in one commit.

Its refusals are as informative as its actions. A path under `archive/` or
`human-html/` is rejected as not an active document; a path outside the
repository is rejected; an archive target that already exists is rejected rather
than overwritten, since silently replacing an archived copy would destroy the
history the procedure exists to keep. `--dry-run` prints the plan and writes
nothing.

## Archive is history, not authority

Everything under `archive/` is superseded by construction. It sits below live
evidence and runbooks in the
[truth order](../architecture/repository-authority-model.md), agents are told
not to load it during normal work, and changing an archived file is not a fix
for anything. The archive exists so a superseded version can be read
deliberately, not so it can be mistaken for the current one — which is exactly
why the supersession procedure moves the old copy out rather than leaving both
in place.

Documentation checks skip the archive tree entirely for the same reason: a link
or vocabulary rule that fired inside superseded material would generate noise
about documents nobody may act on.

## What a completed change touches

A decision on its own does not finish anything. Before work is called complete
the current server record, the build state and any affected decision or standard
document must all be updated. Recording state that has not been observed is the
error this guards against; `REPOSITORY-STATUS.md` demonstrates the intended
tone, listing what was reconciled alongside an explicit **intentional
limitations** section naming the gaps that remain and instructing readers not to
fabricate the missing detail from historical material.

The change path that carries all of this — regenerate, check, review, pull
request — is in
[contributing and review](../workflows/contributing-and-review.md).
