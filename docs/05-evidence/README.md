# Evidence

Store current validation evidence by server/application.

## Which evidence model applies

HX has two evidence shapes. Both are current. Use the one that matches when the
proof was taken.

**1. Inline record evidence — HX-1, HX-2, HX-3.** These servers closed before
the CentCom runner existed. Their proof is recorded inside
the relevant record under `docs/02-server-records/` as exact commands and exact
responses. This is
accepted evidence. `hx-smoke-promote` accepts an accepted server record as
`prior_pass_evidence` for exactly this reason. Do not retrofit these into run
bundles.

**2. Run-bundle evidence — everything from HX-4 onward.** Created by
`hx-smoke-new`, promoted by `hx-smoke-promote`, retained under the path below.

### Running a bundle before CentCom exists

Smoke-roadmap steps A1-A4 prove HX-4 and HX-5 *before* CentCom is activated at
A5, so there is no HX-5 station yet. Run the tooling from the operator station
instead by authorising it explicitly:

```bash
export HX_SMOKE_ALLOW_HOST="$(hostname -s)"
export HX_ECO_REPO=~/src/HX-Eco-System
hx-smoke-new hx-4 ollama-inference ollama-inference-smoke-test.md 192.168.50.204
```

The station actually used is written to `runner_host` in the manifest, so a
pre-CentCom run is distinguishable from a CentCom run in the retained evidence.
After A5 passes, HX-5 is the station and this variable is not set.

## Standard naming

`YYYYMMDDTHHMMSSZ_<server>_<component>_<gate>_<description>.<ext>`

## Standard retained bundle

```text
docs/05-evidence/<server>/<component>/<run-id>/
├── manifest.md
├── result.txt
├── cleanup.txt
└── supporting captures as required
```

Every retained run must identify:
- runner host;
- system under test;
- component/version or revision;
- smoke-test authority file;
- repository commit used;
- known-answer input;
- PASS/FAIL determination;
- cleanup result and cleanup verification;
- reboot-persistence result when applicable.

Failed evidence is not overwritten by a later PASS. A retry receives a new run ID.

Secret values must not appear in retained evidence. If command output accidentally includes a token, password, private key, PAT, or other credential, redact that credential before promotion while preserving the functional result.

HX-5 CentCom is the standard remote smoke-test execution station after its activation gate. Detailed procedure: `../04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`.

Evidence supports current state but does not independently override explicit owner decisions.
