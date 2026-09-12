---
type: operations
title: Server records and evidence retention
description: How as-built state is recorded and proven — the server-record template and its mandatory provenance fields, the checks that keep records honest against the fleet, the two accepted evidence models, the retained bundle shape, and the rules on unresolved values, failed runs and redaction.
tags: [server-records, evidence, provenance, as-built, retention, redaction]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-2c909f1605c16498627e565e
    resource: repo://docs/00-control/DOCUMENT-CONTROL.md
  - id: openwiki-source-939aa3b5c336cc69710945f5
    resource: repo://docs/00-control/hx-fleet.tsv
  - id: openwiki-source-3761302753ec5b6467935b61
    resource: repo://docs/02-server-records/_TEMPLATE.md
  - id: openwiki-source-ddec68f9f5dd49472409e0d0
    resource: repo://docs/05-evidence/README.md
  - id: openwiki-source-bf6a46fe85337b9b2d7d499a
    resource: repo://tools/hx-doc/hx_record_check.py
  - id: openwiki-source-52d69566ca67b436f190d6ea
    resource: repo://tools/hx-smoke-runner/hx-smoke-new
  - id: openwiki-source-a77fea9320056a2d55a6f0f9
    resource: repo://tools/hx-smoke-runner/hx-smoke-promote
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Server records and evidence retention

A server is not finished when the software starts. It is finished when a record
says what is actually running, and evidence exists that it was proven. This page
covers both halves.

## The server record

Every server has one record under `docs/02-server-records/`, scaffolded from
`_TEMPLATE.md`. The template opens with the build state, gate, address, fully
qualified name and record date, and then nine required sections: identity and
network, operating system, GPU configuration, storage layout, runtime, model or
application provenance, functional validation, final state, and evidence
references.

The template is explicit that every heading is required, and that a section may
be dropped only when it genuinely does not apply — with the reason stated in one
line rather than removed silently. `hx-record-check` enforces exactly that,
honouring a declared not-applicable line and otherwise reporting the missing
section.

Several sections demand a specific kind of rigour:

- **GPU and runtime** require the exact driver package version and the exact
  installed application version, not a branch or a "latest".
- **Functional validation** requires the exact command and the exact response
  for each of the known-answer, API, LAN and reboot-persistence proofs.
- **Final state** is a gate table, one row per gate, so a `PASS` claim is
  visibly supported by the gates beneath it.

The closed records show the intended level of detail: HX-2's record carries the
verified realm output, the resolved domain user, the driver and CUDA versions,
the exact VRAM per GPU, and a stated `Domain join gate: PASS` line.

### Provenance needs both a source and a hash

The provenance section is the one with the strongest rule. For any server
hosting a model or a downloaded artifact, five fields are mandatory: the HX
alias, the upstream identity, the source URI, the full artifact SHA-256, and the
import method. An imported rather than pulled artifact also requires the
Modelfile or build definition verbatim, including any template, parameter or
stop-token settings — and if none were set, saying so explicitly.

The template explains why both the URI and the hash are required: the hash
proves what is running, the URI proves where it came from, and public model
registries carry modified community rebuilds under names close to the official
ones, so neither field alone establishes provenance. The review configuration
enforces the same rule on every record change.

### Unknown is recorded, never omitted

An unknown value is written as `UNRESOLVED`, never left out, "because a missing
field cannot be told apart from a forgotten one". Two such gaps are live right
now and visible in the fleet inventory: HX-2's model source URI and HX-3's full
artifact hash.

`hx-record-check` surfaces every `UNRESOLVED` field as a soft finding — a
recorded gap rather than an error — while urging that it be closed while the
server is still reachable. `--strict` turns them into failures. It also reports
**DRIFT** when a record's stated build state disagrees with the fleet TSV, which
is what stops a record and the fleet table from telling different stories about
the same host.

## Two evidence models, both current

Which model applies depends on when the proof was taken.

**Inline record evidence — HX-1, HX-2, HX-3.** These closed before the CentCom
runner existed, so their proof is recorded inside the server record as exact
commands and exact responses. This is accepted evidence, and promotion
explicitly allows an accepted server record to be cited as prior PASS evidence
for that reason. They are not to be retrofitted into run bundles.

**Run-bundle evidence — everything from HX-4 onward.** Created by the runner,
promoted into the repository, retained under a per-run path.

## The retained bundle

```text
docs/05-evidence/<server>/<component>/<run-id>/
├── manifest.md
├── result.txt
├── cleanup.txt
└── supporting captures as required
```

Supporting files use a standard name shape:
`YYYYMMDDTHHMMSSZ_<server>_<component>_<gate>_<description>.<ext>`.

Every retained run must identify the runner host, the system under test, the
component version or revision, the smoke-test authority file, the repository
commit used, the known-answer input, the PASS or FAIL determination, the cleanup
result and its verification, and the reboot-persistence result where applicable.

Promotion enforces the subset that a script can check. For a `PASS` it refuses
to proceed while `component_version_or_revision`, `transport_or_endpoint` or
`sut_ip` still read `TO_RECORD`, requiring `NONE` where a field genuinely does
not apply — so "not applicable" is a stated choice rather than an empty field.

The station used is recorded too. `runner_host` distinguishes a pre-CentCom run
from a CentCom run in the retained evidence, which matters because the first
four proof steps necessarily run before the CentCom station exists.

## Failures are kept

A failed run is not overwritten by a later success: a retry receives a new run
ID, and failed evidence is retained where it is materially useful. Cleanup
failure keeps a run incomplete even when the functional action succeeded, so the
bundle records that honestly rather than being promoted as a pass.

## Secrets never enter evidence

If command output accidentally contains a token, password, private key or other
credential, it is redacted before promotion while the functional result is
preserved. Promotion also scans the manifest, evidence and cleanup directories
for the obvious credential shapes — personal access tokens, private key headers,
authorization headers, `sshpass -p`, cloud and API key prefixes, and
`PASSWORD=`-style assignments — and refuses to promote when one matches.

That scan is a backstop, not the control. The repository-wide secret scan in
continuous integration is the other layer; see
[continuous integration workflows](continuous-integration-workflows.md).

## Evidence does not outrank a decision

One boundary closes the loop. Evidence documents what was observed, and it sits
above runbooks in the truth order — but it does not independently override an
explicit owner decision. A surprising observation is a reason to report a
contradiction, not to quietly re-decide something. See
[the repository authority model](../architecture/repository-authority-model.md)
and
[owner decisions and document lifecycle](../concepts/owner-decisions-and-document-lifecycle.md).

How a bundle is created and promoted is in
[the smoke-test run lifecycle](../workflows/smoke-test-run-lifecycle.md); what
the cited prior evidence has to satisfy is in
[the proof chain](../concepts/proof-chain-and-cumulative-evidence.md).
