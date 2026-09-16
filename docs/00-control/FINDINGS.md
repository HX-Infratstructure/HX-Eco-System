---
document: HX Infrastructure Findings
status: current
date: 2026-09-15
---

# HX Infrastructure Findings

## HX4-F01 — Shared base-block network validation false failure

**Status:** CLOSED  
**Severity:** High  
**Scope:** Fleet-wide  
**Discovered on:** HX-4  
**Discovered during:** Block 1 — Base / Admin / Network / Updates  
**Affected file:** `docs/03-runbooks/common/01-base-admin-network-updates.sh`

### Finding

The shared base-build runbook validated IP address, default route, and DNS using pipelines of the form:

```bash
command | grep -q "value"
```

The script executes with `set -euo pipefail`.

When `grep -q` finds a match, it exits immediately and closes the pipe. If the producer still has output to write, the producer receives SIGPIPE and exits with status 141. Under `pipefail`, the pipeline therefore reports failure even though `grep` successfully matched the expected value.

HX-4 exposed the defect because `resolvectl status` continued emitting data for `wlp5s0` after the valid HX-1 DNS address had already been matched.

Observed evidence:

```text
Current DNS Server: 192.168.50.200
       DNS Servers: 192.168.50.200
STOP: expected HX-1 DNS 192.168.50.200 not found
```

```text
PIPESTATUS=141 0
```

`grep` returned 0; the producer returned 141.

### Resolution

The three checks were changed to capture command output completely before applying `grep`.

Original affected checks:

- IPv4 address
- default gateway
- HX-1 DNS

Existing exit codes 11, 12, and 13 were preserved.

### Verification

- Reproduced on HX-4: 5/5 occurrences before fix
- HX-4 Block 1 rerun: `SCRIPT_RC=0`
- No `STOP:` conditions
- Reboot completed successfully
- Post-reboot network state validated
- Repository gate tests: PASS
- CI: PASS

### Repository references

- PR: #21
- PR head commit: `c4e61a048d109199219e956a1e968f328b72d369`
- Merged commit: `f402ad0d1a43a02167c5f1cf7d3985f0e1b37f44`

The merged commit on `main` is the authoritative reference.

### Disposition

CLOSED.

The correction is now part of the shared runbook and must be used for HX-5 through HX-17.

"Fleet-wide" describes the block this finding names. One instance of the same
pattern remains elsewhere and is tracked separately as HX4-F05, where it is
measured and does not fire.

## HX4-F02 — SSSD responder and socket-activation conflict

**Status:** OPEN / DEFERRED  
**Severity:** Low  
**Scope:** Domain-client configuration; fleet applicability to be assessed  
**Discovered on:** HX-4  
**Discovered during:** Post-Block-2 validation

### Finding

After the HX-4 domain-join and NVIDIA block completed and the server rebooted, three systemd socket units were failed:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

Host logs reported:

```text
The nss responder has been configured to be socket-activated but it's still
mentioned in the services' line in /etc/sssd/sssd.conf.
```

The SSSD configuration file contains:

```text
services = nss, pam
```

The NSS and PAM responders are therefore configured for startup by `sssd.service` while their systemd socket units also attempt socket activation.

### Functional impact

No domain-join failure was observed.

Domain identity resolution succeeds:

```text
getent passwd jarvisr@hx.local.arpa
```

returned the expected domain identity.

Therefore:

- DOMAIN JOIN: PASS
- IDENTITY RESOLUTION: PASS
- SSSD RESPONDER/SOCKET CLEANLINESS: FAIL

### Disposition

DEFERRED.

No configuration change was made during HX-4 Blocks 1-3 because correcting the responder activation model was outside the approved build scope.

Before changing HX-4, compare the SSSD configuration and socket state across the existing domain-joined fleet and establish the intended HX-wide responder model.

### Required follow-up

1. Inspect SSSD responder configuration on existing joined hosts.
2. Determine whether HX standardizes on direct responder startup or socket activation.
3. Update the common domain-join runbook if the issue is fleet-wide.
4. Correct affected hosts under a separate approved change.
5. Close this finding with validation evidence.

## HX4-F03 — Provenance artifact hash could be written blank or as a path

**Status:** CLOSED  
**Severity:** Medium  
**Scope:** Any server whose models are installed by the Ollama model blocks  
**Discovered on:** HX-4  
**Discovered during:** Owner review of PR #20, before merge  
**Affected file:** `docs/03-runbooks/common/hx-base.env`

### Finding

`hx_ollama_provenance` emitted the Artifact SHA-256 field with a single
parameter expansion:

```bash
Artifact SHA-256:  ${blob##*/sha256-}
```

That expansion has no fallback. It fails in two ways:

- when `blob` is empty, it expands to an empty string, so the field is omitted
  rather than written `UNRESOLVED`;
- when `blob` is set but contains no `sha256-` segment, `##` finds no match and
  returns the whole value, so a filesystem path is printed under the
  `Artifact SHA-256:` label.

The second is the worse of the two. A blank field is visibly missing. A path
looks like evidence.

The helper's own contract states that an unknown value is recorded as
`UNRESOLVED`, never omitted. The record treats this field as evidence of which
artifact is running.

### Resolution

The digest is resolved explicitly before the here-document, and falls back to
`UNRESOLVED` in both failure cases.

### Verification

```text
blob="/usr/share/ollama/.ollama/models/blobs/sha256-abc123def" -> abc123def
blob=""                                                        -> UNRESOLVED
blob="/some/path/with-no-digest"                               -> UNRESOLVED
```

### Repository references

- PR: #20
- Fix commit: `e649490e7763a1b6cb5bae033e4b58336aaee235`
- Merged commit: `509566c8bfc2cc13b2ab38573a03175a1b7da43b`

The merged commit on `main` is the authoritative reference.

### Disposition

CLOSED. Caught in review; no server record was written from the defective
helper.

## HX4-F04 — A floating model reference was accepted as a pin

**Status:** CLOSED  
**Severity:** Medium  
**Scope:** Fleet-wide, for every Ollama model reference  
**Discovered on:** HX-4  
**Discovered during:** Owner review of PR #20, before merge  
**Affected files:** `docs/03-runbooks/common/hx-base.env`,
`docs/03-runbooks/common/05-gpt-oss.sh`,
`docs/03-runbooks/common/06-embeddings.sh`

### Finding

`HX_EMBED_PRIMARY_MODEL` was `bge-m3:latest`. `latest` is a name, not a pin: a
re-pull after upstream moves returns a different artifact under the same name.

The blocks checked only that a reference was non-empty, so a floating reference
satisfied a rule written to prevent exactly this.

The embedding dimension probe does not cover the gap. It proves the vector
length, and a same-dimension BGE-M3 revision has the same length. A later
revision could therefore replace the model a closed HX-4 record names, with
nothing in the build able to notice.

### Resolution

`hx_require_pinned_ref` refuses a reference that does not identify one
artifact, and treats a bare name with no tag as `:latest`, because they are the
same defect spelled two ways. Blocks 05 and 06 both call it in place of their
own non-empty checks. New exit code 31.

`HX_EMBED_PRIMARY_MODEL` was first left at `bge-m3:latest` so block 06 would
exit 31 rather than install a mutable artifact, then resolved to the explicit
variant tag `bge-m3:567m`, which passes the gate.

The tag is where the resolution stops. A tag names a reviewed source reference,
not an artifact, and `567m` is not guaranteed immutable either. The artifact
identity is the resolved Ollama model ID and blob SHA-256 that
`hx_ollama_provenance` captures at installation and writes into the server
record. That hash is the immutable truth; the tag is provenance context. A
closed record is never silently re-pulled or re-baselined against a later
artifact under the same tag.

### Verification

```text
rc=0   "gpt-oss:20b"     pinned tag
rc=31  "bge-m3:latest"   floating :latest
rc=31  "bge-m3"          no tag at all
rc=30  ""                empty
```

### Repository references

- PR: #20
- Fix commit: `e649490e7763a1b6cb5bae033e4b58336aaee235`
- Merged commit: `509566c8bfc2cc13b2ab38573a03175a1b7da43b`

The merged commit on `main` is the authoritative reference.

### Disposition

CLOSED. The gate is in place and proven, and the pin is resolved to
`bge-m3:567m`. HX-4 steps 4 and 5 are both runnable.

At the time of resolution `bge-m3:latest`, `bge-m3:567m` and `bge-m3:567m-fp16`
all resolved to the same registry manifest, `7907646426070047...`, pushed
2024-08-07. The Ollama registry does not serve manifests by digest, so a fixed
tag is the strongest reference the pin itself can carry; artifact-level
identity comes from the install-time capture described above.

## HX4-F05 — The HX4-F01 pattern survives in the domain-join block

**Status:** OPEN / MONITOR  
**Severity:** Low  
**Scope:** `docs/03-runbooks/common/02-domain-nvidia.sh`  
**Discovered on:** HX-4  
**Discovered during:** Post-fix sweep for other instances of HX4-F01

### Finding

HX4-F01 is recorded as fixed fleet-wide. That is true of the base block it
names, but one instance of the same pattern remains in the domain-join block:

```bash
if realm list | grep -q 'configured: kerberos-member'; then
```

This is the idempotency guard that decides whether to run `realm join`. A false
negative would re-run an interactive join on an already-joined host.

### Measured behaviour

Tested on HX-4, which is joined:

```text
run 1: rc=0 pipestatus=0 0
run 2: rc=0 pipestatus=0 0
run 3: rc=0 pipestatus=0 0
run 4: rc=0 pipestatus=0 0
run 5: rc=0 pipestatus=0 0
```

The guard works. `realm list` is not killed, so the defect does not fire here.

The discriminator is write cadence, not output size. `realm list` writes its
output in one go, so it has finished writing before `grep -q` leaves.
`resolvectl status`, which did fire, writes per link with a bus round trip
between, which leaves output pending when the match is found. Both outputs are
under 550 bytes, so size does not predict this.

### Disposition

DEFERRED, monitored rather than changed.

Recorded so that HX4-F01's fleet-wide wording is not read as "no instances
remain", and so a future change to `realm list` output or ordering is
recognised as able to trip it.

### Required follow-up

1. Convert the guard to the captured-output form when that block is next
   touched for another reason.
2. Do not open a change solely for this while the measurement above holds.

## HX4-F06 — infinity-emb pins itself but not click, and the reranker never starts

**Status:** CLOSED
**Severity:** High
**Scope:** Fleet-wide; `docs/03-runbooks/common/04-reranker.sh` is shared
**Discovered on:** HX-4
**Discovered during:** Step 6 — reranker install
**Affected files:** `docs/03-runbooks/common/04-reranker.sh`,
`docs/03-runbooks/common/hx-base.env`

### Finding

Block 6 exited 7. The curl health check refused to connect because the service
was crashing at startup and systemd was restarting it in a loop, so
`systemctl is-active` reported `active` only in the gaps between restarts.

`infinity-emb` pins its own version and nothing it depends on, so pip installs
whatever is current on build day. HX-4 received `click 8.5.0`. `click 8.2`
changed how a secondary flag is validated, and `typer 0.12.5`, which infinity
installs, builds flags the new click rejects:

```text
TypeError: Secondary flag is not valid for non-boolean flag.
hx-reranker.service: Main process exited, code=exited, status=1/FAILURE
```

The failure is at argument parsing, before the server exists, so nothing in the
service log mentions the model or the port.

### Resolution

`HX_RERANKER_CLICK_PIN="click<8.2"`, added to the pip install line.

### Verification

With the pin applied the CLI parses and startup proceeds to the next stage.
After both this and HX4-F07 were fixed, block 6 was re-run from the runbook on
a wiped venv and unit: `SCRIPT_RC=0`, service `active` and `enabled`, LAN health
answering on `192.168.50.204:7997`.

### Repository references

- PR: #24
- Merged commit: `663ba76ba7e0f3c1a79ba645f289636bbd012b2c`

### Disposition

CLOSED. HX-5 through HX-17 would have hit this identically.

## HX4-F07 — BetterTransformer is on by default and optimum is not installed

**Status:** CLOSED
**Severity:** High
**Scope:** Fleet-wide; `docs/03-runbooks/common/04-reranker.sh` is shared
**Discovered on:** HX-4
**Discovered during:** Step 6 — reranker install, behind HX4-F06
**Affected files:** `docs/03-runbooks/common/04-reranker.sh`,
`docs/03-runbooks/common/hx-base.env`

### Finding

With click held back the CLI parses, and startup then fails:

```text
NameError: name 'BetterTransformerManager' is not defined
ERROR:    Application startup failed. Exiting.
```

`bettertransformer` defaults to true in the installed package's environment
module, which is external to this repository, and the code path imports
`BetterTransformerManager` from `optimum`. The `torch` extra does not install
`optimum`, and HX-4 had no `optimum` at all.

### Resolution

The accelerator is turned off:
`HX_RERANKER_BETTERTRANSFORMER="false"`, written into the unit as
`Environment="INFINITY_BETTERTRANSFORMER=false"`.

Installing an older `optimum` was rejected as the wrong repair. Infinity's own
source states that BetterTransformer does not work with torch 2.5 or later, and
the fleet runs torch 2.14, so the accelerator could not have been used even if
the import had succeeded.

The environment variable was chosen over a `--no-bettertransformer` flag
because the variable is what was tested on the host.

### Verification

```text
HEALTH OK after ~50s
{"unix":1789449905.6480312}
INFO:     Uvicorn running on http://0.0.0.0:7997
INFO:     127.0.0.1 - "GET /health HTTP/1.1" 200 OK
```

### Repository references

- PR: #24
- Merged commit: `663ba76ba7e0f3c1a79ba645f289636bbd012b2c`

### Disposition

CLOSED.

Both faults share one cause worth stating separately: a version pin on a
package does not pin what that package installs. The runbook now pins the two
dependencies that broke; it does not pin the rest of the tree, so the same
class of failure can recur on a future build day.

## HX4-F08 — The smoke runner cannot run on the operator workstation

**Status:** OPEN / DEFERRED
**Severity:** Medium
**Scope:** `tools/hx-smoke-runner/hx-smoke-new`, `hx-smoke-promote`,
`hx-smoke-doctor`
**Discovered on:** HX-4
**Discovered during:** Step 7 — producing the A1-A3 run bundles

### Finding

`hx-smoke-new` resolves the runner-host gate with:

```bash
RUNNER_HOST="$(hostname -s)"
```

The operator workstation is Windows. Git Bash provides a `hostname` with no
`-s` option, so the command fails, and under `set -euo pipefail` the assignment
aborts the script before any argument is read:

```text
hostname: unknown option -- s
rc=1
```

This is not wrong on Linux. It makes the tooling unusable from a Windows
station, which is what the operator actually has.

### Consequence for HX-4

Roadmap steps A1-A4 run before CentCom exists, so there is no HX-5 station yet
and the workstation was the intended stand-in. With the workstation unusable,
HX-4 was authorised as its own runner. Each manifest records
`runner_host: hx-4`, so the runs are distinguishable in retained evidence.

The cost is real and is recorded in the HX-4 server record: runner and system
under test are the same host, so the LAN calls in A1-A3 were issued from HX-4
to its own address rather than from a separate station.

### Disposition

DEFERRED by owner decision, recorded rather than fixed during a server build.

### Required follow-up

1. Resolve the short hostname without `hostname -s`, so any POSIX station works.
2. Decide whether a SUT may ever be its own runner, or whether the gate should
   refuse it outright once a station exists.
3. Re-run A1-A3 from HX-5 after CentCom activation if a remote LAN proof is
   required for HX-4 closure to stand.

## HX4-F09 — The secret-scan gate rejected the evidence it exists to protect

**Status:** CLOSED
**Severity:** Medium
**Scope:** Repository gate; every server closed on run-bundle evidence
**Discovered on:** HX-4
**Discovered during:** Step 8 — opening the closure PR

### Finding

CI's secret scan failed the HX-4 closure with `leaks found: 3`.

Every smoke test is a known-answer test: it sends a fixed string and requires it
back verbatim. `.gitleaks.toml` already allowlisted those tokens, but only on
the path `^smoke-tests/.*\.md$`.

The token does not stay in the procedure. A passing run has to show the token it
got back, so the same string lands in the retained bundle, in the server record
that quotes the proof, and in the generated mirror of both:

```text
docs/02-server-records/HX-4.md
docs/05-evidence/hx-4/ollama-inference/<run-id>/result.txt
docs/05-evidence/hx-4/ollama-inference/<run-id>/supporting/smoke_stdout.txt
human-html/02-server-records/HX-4.html
```

Evidence model 2 came in for HX-4 onward, and HX-4 is the first server to
retain bundles, so nothing had exercised this before. The gate rejected the
first evidence it was ever shown.

### Resolution

The allowlist paths now include the retained evidence tree, server records, and
the generated mirrors.

The `condition = "AND"` is what makes that safe and it is unchanged. A finding
is allowed only when the file is on the paths list **and** the string matches
the HX known-answer token pattern. A real credential in a retained bundle does
not match that pattern and is still reported.

### Disposition

CLOSED. The rule is not weakened; its path list now matches where evidence
actually lands.

### Note

The alternative — redacting the token out of retained evidence — was rejected.
The token appearing in the response is the proof. Removing it would leave a
bundle that cannot demonstrate what it claims.
## HX5-F01 — NVMe device names are not stable storage authority

**Status:** OPEN / NON-BLOCKING  
**Severity:** Low  
**Scope:** HX-5 documentation/configuration hygiene  
**Discovered on:** HX-5  
**Discovered during:** 2026-09-15 post-rebuild storage validation

### Finding

The active `/etc/fstab` entries use filesystem UUIDs and mount the correct filesystems. Installer-generated comments reference `/dev/nvme0n1p*`, but live Linux device enumeration changed across reboots:

```text
Observed before one reboot: /srv/ollama -> /dev/nvme0n1p3
Observed after next reboot: /srv/ollama -> /dev/nvme1n1p3
```

The authoritative `/srv/ollama` filesystem UUID remained:

```text
68d0e365-212c-456f-b42e-d908b445ae77
```

and the mount remained correct and read-write.

### Functional impact

None. This is direct evidence that `/dev/nvmeXnY` naming must not be treated as persistent storage identity.

The installed Ornith model remained present after reboot on `/srv/ollama`, confirming the UUID-backed mount is functioning correctly.

### Disposition

NON-BLOCKING.

Do not interrupt the build to rewrite descriptive installer comments. Correct comments during a future hygiene pass if desired, but keep UUID as the only storage authority.

## HX5-F02 — Layer 0/1 evidence standard drift across inference hosts

**Status:** OPEN / PLANNED AUDIT  
**Severity:** Medium  
**Scope:** HX-2, HX-3, HX-4 retrospective foundation evidence  
**Discovered on:** HX-5  
**Discovered during:** 2026-09-15 clean-rebuild Layer 0/1 reconciliation

### Finding

HX-5 exposed that successful completion of the shared Blocks 1 and 2 does not by itself prove the complete HX Layer 0/1 foundation. The reconciled HX-5 standard now explicitly proves controls that are not consistently retained in the older HX-2/HX-3/HX-4 records.

The evidence gap includes some combination of:

- HX-1 NTP source selection;
- persistent Netplan/IP/gateway/DNS proof;
- fleet SSH-key proof;
- SSH reboot persistence mechanism;
- `adcli testjoin` machine-trust proof;
- Samba DNS A record;
- AD `dNSHostName` and required SPNs;
- failed systemd-unit classification;
- final foundation reboot proof.

This is an **evidence-standard gap**, not evidence that HX-2, HX-3, or HX-4 are presently malfunctioning.

### Owner direction

Complete HX-5 first. After the current HX-5 closeout boundary, perform a **read-only retrospective Layer 0/1 audit of HX-2, HX-3, and HX-4** against the reconciled HX-5 foundation standard.

Do not rebuild working servers or change configuration merely to make records look symmetrical.

### Acceptance method

For each host, capture and classify:

```text
hostname / FQDN
persistent IP / gateway / HX-1 DNS
HX-1 NTP
NOPASSWD sudo
fleet SSH key
SSH persistence
D-018 UFW state
realm / SSSD core
machine trust
Samba DNS / dNSHostName / SPNs
failed units
GPU runtime where applicable
approved storage mounts
OS maintenance state
final reboot persistence
```

### Disposition

OPEN / PLANNED AUDIT.

This finding closes when HX-2, HX-3, and HX-4 each have a retained audit result against the reconciled standard and their server records are backfilled accordingly.

## HX5-F03 — Shared Block 2 NVIDIA pin diverges from accepted HX-5 driver

**Status:** OPEN / NON-BLOCKING  
**Severity:** Medium  
**Scope:** HX-5 rerun safety / shared Block 2 applicability  
**Discovered on:** HX-5  
**Discovered during:** 2026-09-15 clean rebuild

### Finding

The accepted HX-5 NVIDIA runtime is:

```text
595.99.02
```

The shared Block 2 pin remains:

```text
595.71.05-0ubuntu0.24.04.1
```

Therefore rerunning Block 2 on HX-5 would attempt to impose a different driver baseline from the accepted as-built server state.

### Functional impact

None on the current HX-5 build. GPU runtime, dual-GPU visibility, Ornith inference, and post-reboot GPU placement all pass with 595.99.02.

### Disposition

NON-BLOCKING FOR CURRENT HX-5; RERUN GUARD REQUIRED OPERATIONALLY.

Do not rerun Block 2 on HX-5 merely for confirmation. A future fleet decision should determine whether the shared NVIDIA pin is changed, host-specific exceptions are encoded, or the driver-install phase is separated from reusable domain validation.
