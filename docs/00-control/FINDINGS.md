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
**Scope:** Fleet-wide; confirmed on HX-2, HX-3, HX-4 and HX-5 on 2026-09-16  
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

### Fleet applicability, established 2026-09-16

Step 1 is done. Every domain-joined host carries this, so it belongs to the
shared join procedure rather than to HX-4:

```text
HX-2   sssd-nss.socket, sssd-pam-priv.socket, sssd-pam.socket   3 failed
HX-3   sssd-nss.socket, sssd-pam-priv.socket                    2 failed
HX-4   sssd-nss.socket, sssd-pam-priv.socket                    2 failed
HX-5   sssd-nss.socket, sssd-pam-priv.socket                    2 failed
```

The count varies, so a check asserting three failed units would pass on HX-2
and fail everywhere else. Identity resolution works on all four:
`getent passwd jarvisr@hx.local.arpa` returns the domain identity.

### Required follow-up

1. ~~Inspect SSSD responder configuration on existing joined hosts.~~ Done
   2026-09-16; the table above is the result.
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

**Status:** OPEN / PARTIALLY RESOLVED  
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

### Resolution, follow-up 1 only

`hx-smoke-new`, `hx-smoke-doctor` and `hx-smoke-promote` no longer call
`hostname -s`. They read `hostname` and strip the domain with `${VAR%%.*}`,
which is POSIX and works on the operator's Git Bash station:

```text
before:  hostname: unknown option -- s        rc=1
after:   RUNNER_HOST=HANA-X-JR0               rc=0
```

The runbook scripts still use `hostname -s`. They execute on the Linux servers
they configure, where the option exists, so they are outside this finding.

Follow-ups 2 and 3 are untouched: whether a system under test may ever be its
own runner is still undecided, and A1-A3 have not been re-run from HX-5.

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

**Status:** CLOSED  
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

CLOSED 2026-09-16.

The audit ran read-only across HX-2 through HX-5 and found the gap was wider
than "the older records are thinner". Three of four hosts did not use HX-1 as
their time source and could not resolve their own FQDN. The shared base block
had never configured either, so nothing had ever checked them - on any host.
All three were remediated and re-proven, and every server record now carries a
Foundation section that `hx-record-check` requires.

The condition this finding set for itself is met: HX-2, HX-3 and HX-4 each have
a retained result against the reconciled standard, and their records are
backfilled. What the audit exposed beyond that became findings of its own
rather than being folded in here.

### One audit claim was wrong, and is withdrawn

The audit reported that HX-2 and HX-3 retain no evidence, on the strength of
`docs/05-evidence/hx-2` and `hx-3` holding zero files, and concluded their PASS
labels could not be reproduced from anything the repository keeps.

That was a misreading of this repository's own standard.
`docs/05-evidence/README.md` states that HX-1, HX-2 and HX-3 use inline record
evidence, keeps their proof inside `docs/02-server-records/` as exact commands
and exact responses, calls it accepted evidence, and says explicitly: do not
retrofit these into run bundles. Both records carry it - 413 and 441 lines,
with 56 fenced evidence blocks each.

An empty evidence directory is the expected state for those three hosts, not a
gap. No bundles were created. Recorded here because the claim was circulated
before it was checked, and a reader who acts on it would be undoing a
deliberate decision.

## HX5-F03 — Shared Block 2 NVIDIA pin diverges from accepted HX-5 driver

**Status:** ACCEPTED / EXCEPTION  
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

### Decision

Accepted as a standing exception by the owner on 2026-09-15.

- HX-5 stays on `595.99.02`. It is not downgraded to the shared pin.
- Every other host stays on the shared Block 2 pin `595.71.05-0ubuntu0.24.04.1`.
  No host is upgraded to match HX-5.
- Block 2 is not rerun on HX-5.

The divergence is accepted rather than removed. This finding is not a pending
action; it is the record of the exception and the rule that goes with it.

## HX5-F04 — The link gate reads a server filesystem path as a repository reference

**Status:** CLOSED  
**Severity:** Low  
**Scope:** Repository gate; every server record that cites a configuration file  
**Discovered on:** HX-5  
**Discovered during:** PR #26 — Documentation consistency gate  
**Affected file:** `tools/hx-doc/hx_doc_check.py`

### Finding

`PATH_REF` matches any backticked string that contains a slash and ends in one
of `.md`, `.sh`, `.py`, `.html`, `.yaml` or `.txt`, then requires it to resolve
inside the repository. The test is driven by the extension, not by where the
path points.

The HX-5 record cites the file that holds its persistent network configuration:

```text
- Persistent network file: `/etc/netplan/50-cloud-init.yaml`
```

That is a path on HX-5. The gate read it as a repository reference and failed:

```text
FAIL  links: docs/02-server-records/HX-5.md:17 broken ref -> /etc/netplan/50-cloud-init.yaml
```

The gate does not skip fenced code blocks. Quoting the offending line in this
document reproduced the failure against this file. That is why this section's
subheading carries a `FORWARD_MARKERS` phrase: it is currently the only way to
write the defect down without tripping it.

`/etc/hosts`, two lines above it, passes only because it carries no extension
the pattern lists. Nothing about the rule distinguishes a server path from a
repository path.

### Resolution applied

The line now carries `not a repository path`, one of the phrasings
`FORWARD_MARKERS` already recognises. The gate passes and the reader is told
something true.

### Disposition

OPEN. The escape works, but it is per line. Every future server record that
cites a `.yaml`, `.sh` or `.txt` under `/etc`, `/srv` or `/var` will fail the
same way and need the same phrase added by hand. A location test — an absolute
path that resolves outside the repository is not a repository reference —
would close the class instead of the instance, and skipping fenced code blocks
would let the defect be documented plainly. Do these in a tooling pass, not on
a build day.

### Resolution

`hx_doc_check.py` now carries `SYSTEM_ROOTS`. An absolute target under `/etc/`,
`/var/`, `/usr/`, `/srv/`, `/opt/`, `/run/`, `/boot/`, `/proc/`, `/sys/`,
`/dev/` or `/tmp/` is a file on a server and is not resolved as a repository
reference. Root-relative repository paths such as `/docs/...` are not listed
and are still checked.

The per-line workaround is gone. This finding quotes the offending line plainly
and the gate passes, which is the demonstration that the class is closed rather
than the instance.

Two paired gate tests hold it: one requires the `/etc` path to be accepted, and
one requires a repository path that does not resolve to still fail, so the
exemption cannot widen into a hole.

## HX5-F05 — A failing gate hides every gate behind it in the same job

**Status:** CLOSED  
**Severity:** Low  
**Scope:** Repository CI; the Documentation consistency job  
**Discovered on:** HX-5  
**Discovered during:** PR #26 — reading why the job stopped  
**Affected file:** `.github/workflows/hx-checks.yml`

### Finding

The Documentation consistency job runs seven gates as seven sequential steps.
A step that exits non-zero fails the job, and the steps after it never run.

PR #26 failed on the first gate, `hx-doc-check`, for the reason recorded in
HX5-F04. Gates two through seven never executed. `hx-record-check` would have
reported two further defects in the same HX-5 record:

```text
docs/02-server-records/HX-5.md
  MISSING    no section for Final State
  DRIFT      record says 'IN PROGRESS — FOUNDATION AND ORNITH BASE PASS ...',
             hx-fleet.tsv says 'IN PROGRESS'
```

Both were present the whole time. Neither was visible until the first gate was
fixed and the job was allowed to reach step five.

Observed on Actions run 35036774672.

### Functional impact

None on correctness. Nothing merges while a gate is red, and every defect is
still caught eventually. The cost is round trips: a record carrying N defects
in N different gates needs N pushes to find them all, and each one costs a full
CI cycle and a context switch.

### Disposition

OPEN. Setting `continue-on-error: true` on each gate step, with a final step
that fails when any gate failed, would report every defect from one run. Worth
doing before the next server build. Not worth interrupting one.

### Resolution

Each gate step in the Documentation consistency job now carries an `id` and
`continue-on-error: true`, and a final `Fail if any gate failed` step with
`if: always()` reports every gate that did not succeed and sets the job's exit
status. One run now reports every defect instead of stopping at the first.

## HX5-F06 — The scheduled OpenWiki workflow that D-025 deleted came back

**Status:** PARTIALLY CLOSED / REMAINDER ON BACKLOG  
**Severity:** High  
**Scope:** Repository automation and secrets; the repository is public  
**Discovered on:** HX-5  
**Discovered during:** 2026-09-15 OpenWiki regeneration, before the push to main  
**Affected file:** `.github/workflows/openwiki-update.yml`

### Finding

The OpenWiki run scaffolded `.github/workflows/openwiki-update.yml` again, as
an untracked file. D-025 in `docs/00-control/DECISIONS.md`, ratified 2026-09-14,
deleted that path and withdrew scheduled generation entirely.

The file that reappeared claims more than the one D-025 removed:

```text
schedule:    cron "0 8 * * *"        daily, where D-023 was weekly
permissions: contents: write, pull-requests: write
secrets:     OPENROUTER_API_KEY, OPENWIKI_LANGSMITH_API_KEY, LANGSMITH_API_KEY
model:       z-ai/glm-5.2, a paid run, unattended
```

D-025 recorded why the file itself is the exposure, not its contents: a branch
that edits the workflow file can read the repository secrets, and no line
inside the file can prevent it. That risk goes away only with the file.

The file was deleted again and was never committed. It is absent from
`aa5364c`.

### Second part, still open

D-025 also recorded that revoking `OPENWIKI_PR_TOKEN` and `ANTHROPIC_API_KEY`
is a required owner action, not a hypothetical. `OPENWIKI_PR_TOKEN` was granted
Contents read and write and Pull requests read and write, on a public
repository.

Both were still listed in repository settings on 2026-09-15, observed by
listing the repository's Actions secrets through the GitHub API while this
finding was written. No settings evidence is retained for that observation, so
it is an assertion and not proof. Confirm in repository settings before acting
on it.

### Disposition

OPEN. Two actions, both owner-only:

1. Revoke `OPENWIKI_PR_TOKEN` and `ANTHROPIC_API_KEY`. Until this is done, the
   exposure D-025 described is still live, whatever the workflow file does.
2. Decide what stops the scaffold restoring the file. An `.openwikiignore`
   entry, or a gate that fails when the path exists, so the next run cannot
   reintroduce it silently.

### Resolution, the guard

Two changes, so the scaffold cannot restore the file unnoticed:

- `.openwikiignore` excludes `.github/**`. OpenWiki no longer scans or writes
  that tree, which is how the file reached the working copy.
- `hx_doc_check.py` carries `WITHDRAWN_PATHS` and fails when a path a ratified
  decision deleted exists again. A gate test creates the file and requires the
  refusal, so the guard is proven able to fire.

### Remainder

Revoking `OPENWIKI_PR_TOKEN` and `ANTHROPIC_API_KEY` is on the backlog by owner
decision of 2026-09-15. It is recorded here and is not scheduled.

## HX5-F07 — `net ads testjoin` disagrees with `adcli testjoin` by design

**Status:** CLOSED / EXPECTED
**Severity:** Informational
**Scope:** Every domain-joined host that was joined with adcli
**Discovered on:** HX-4 and HX-5
**Discovered during:** 2026-09-16 Layer 0/1 reconciliation audit

### Finding

The two tools disagree on every host where both are installed:

```text
adcli testjoin     Sucessfully validated join to domain hx.local.arpa
net ads testjoin   Join to domain is not valid: NT code 0xfffffff6
```

They read different stores. `adcli` uses the Kerberos keytab; `net ads` uses
Samba's secrets database, which an adcli-based join does not populate. Machine
trust is genuinely valid - `adcli testjoin` is the authority the control matrix
names, and it passes on every host.

The same cause makes `net ads dns register -P` fail with
`NT_STATUS_CANT_ACCESS_DOMAIN_INFO`, which is why DNS registration had to use a
Kerberos ticket from the keytab instead.

### Disposition

CLOSED as expected behaviour, written down so it is not re-investigated on
every audit. Do not "fix" it by re-joining with `net`. The join is valid.

## HX5-F08 — HX-2 could not register its own DNS record, and the reason is unknown

**Status:** OPEN / UNEXPLAINED
**Severity:** Low
**Scope:** HX-2 AD DNS registration
**Discovered on:** HX-2
**Discovered during:** 2026-09-16 AD DNS remediation

### Finding

HX-3 and HX-4 registered their own A records using their machine account from
the keytab. HX-2 refused, repeatedly:

```text
update failed: SERVFAIL
```

HX-2 has zone write permission. It created a throwaway name with the same
credential, which was then removed. Only `hx-2.hx.local.arpa` was refused, in
every form tried: add, delete-then-add, and the uppercase spelling.

The obvious explanation was a stale AD object owned by HX-2's previous machine
account, since HX-2's SSH host key had also changed at some point. **That
explanation was wrong.** Queried as Administrator, the node did not exist:

```text
ERROR(runtime): Record or zone does not exist. [WERR_DNS_ERROR_NAME_DOES_NOT_EXIST]
```

and a plain `samba-tool dns add` as Administrator succeeded first time. There
was no tombstone to clear.

### Functional impact

None. The record exists and resolves fleet-wide, confirmed from HX-1, HX-5 and
HX-6.

### Disposition

OPEN. The record is correct. What is unresolved is why the machine-account path
worked on two hosts and not on a third with an identical keytab shape and a
valid `adcli testjoin`. Left open rather than written up as settled, because
the first explanation was confident and wrong, and a fleet standard should not
rest on a cause nobody has established.

## HX5-F09 — samba-common-bin is absent on the hosts built to the older standard

**Status:** OPEN / OWNER DECISION
**Severity:** Low
**Scope:** HX-2 and HX-3
**Discovered on:** HX-2
**Discovered during:** 2026-09-16 AD DNS remediation

### Finding

Every host's own `realm list` names `samba-common-bin` among its
required-packages. Two hosts do not have it:

```text
HX-2   realm requires it   not installed
HX-3   realm requires it   not installed
HX-4   realm requires it   installed
HX-5   realm requires it   installed
```

The split is the older build against the newer one, the same pattern this
audit found everywhere else, rather than one host being odd. The audit first
reported HX-2 alone because only HX-2 and HX-4 had been probed; that was
wrong and is corrected here.

### Functional impact

None on domain membership. `adcli testjoin` passes and
`getent passwd jarvisr@hx.local.arpa` resolves on both hosts without it.

What it costs is diagnosis. `net` and `samba-tool` are absent, so Samba-side
AD queries cannot be run from those two hosts. During this audit that removed
one route to checking SPNs and forced DNS registration down a different path.

### Disposition

OPEN. One decision: is a package the host's own realm declares required part
of the HX standard, or is `adcli` sufficient and the declaration ignorable?

If it is required, `apt-get install samba-common-bin` on HX-2 and HX-3 closes
it, and the shared domain-join block should install it so this cannot recur.
Not done here: installing a package on a running host is a change, and this is
a standard question rather than a defect.

## HX5-F10 — no reverse DNS zone is served

**Status:** OPEN / HAS IMPACT
**Severity:** Low
**Scope:** Fleet-wide
**Discovered on:** All four audited hosts
**Discovered during:** 2026-09-16 Layer 0/1 reconciliation audit

### Finding

No host in scope has a PTR record. The audit reported this as uniform absence
and asked whether it was intentional. It is: there is no reverse zone at all.

A single SOA query is not enough to conclude a zone is unserved fleet-wide, so
the authoritative server set was established first. There is one DNS server and
one domain controller:

```text
dig +short NS hx.local.arpa @192.168.50.200
  hx-1.hx.local.arpa.

dig +short SRV _ldap._tcp.dc._msdcs.hx.local.arpa @192.168.50.200
  0 100 389 hx-1.hx.local.arpa.

resolvectl on every member
  Current DNS Server: 192.168.50.200
```

That single server serves the forward zone and returns nothing for the reverse
one:

```text
dig +short SOA 50.168.192.in-addr.arpa @192.168.50.200   ->   (no answer)
dig +short NS  50.168.192.in-addr.arpa @192.168.50.200   ->   (no answer)
```

So the absence is a property of the only domain controller, and no per-host
action could change it.

### It is not harmless, which this finding first claimed

The original disposition said nothing depends on reverse resolution. That was
wrong, and was written before anything had actually tried to use it.

GSSAPI over LDAP canonicalises the server hostname through reverse DNS before
asking the KDC for a ticket. With no PTR record the canonicalisation produces a
name that has no SPN, and the bind fails with a message that names the wrong
problem:

```text
ldap_sasl_interactive_bind: Local error (-2)
  GSSAPI Error: Unspecified GSS failure ... (Server not found in Kerberos database)
```

The same query with `LDAPSASL_NOCANON=on` succeeds immediately. So the missing
reverse zone breaks Kerberised LDAP by default, and the error points at
Kerberos rather than at DNS - which is why it read as an SPN problem during this
audit and cost time in the wrong place.

### Disposition

OPEN. Two things to decide, and no existing decision covers either: whether the
reverse zone is created on HX-1, and whether PTR records become part of the
reconciled Layer 0/1 baseline. Nothing in `docs/00-control/DECISIONS.md`
establishes a position today, so the previous "by design" was an assumption
rather than a recorded choice.

If the zone is not created, `SASL_NOCANON` has to be set wherever Kerberised
LDAP is used, and that belongs in the runbook rather than in an operator's
memory.

## HX5-F11 — HX-3's primary model displays as `:latest`, which is not a floating pin

**Status:** CLOSED / NOT A DEFECT
**Severity:** Informational
**Scope:** HX-3 model provenance
**Discovered on:** HX-3
**Discovered during:** 2026-09-16 Layer 0/1 reconciliation audit

### Finding

`ollama list` on HX-3 shows the primary model as `Coder-X-GLM-Flash:latest`,
which reads like the floating reference HX4-F04 was raised about.

It is not. The record names the alias without a tag:

```text
HX alias: Coder-X-GLM-Flash
```

`ollama create` applies `:latest` to an untagged name automatically, so the
suffix is how Ollama displays an untagged alias rather than a choice anyone
made. What sits behind it is pinned and recorded: the blob
`sha256-9e0156957bd07760644aa2a3b6d6791ac8796f2c1bc9c75a2cb07cef5ccb5764`,
which the sibling tag `coder-x-glm:glm47flash-q5km` also resolves to, and both
appear in the HX-3 record with their source URI.

### What is and is not protected

The blob is recorded, which means a change is *detectable* by comparison. It
does not mean a change is *detected*. Nothing in the repository or the build
compares the running digest against the recorded one, so if
`Coder-X-GLM-Flash` were recreated from a different source the tag would point
at a new blob and no gate would notice.

That is not specific to this alias. HX4-F04 already states the same limit: a
tag names a reviewed source reference, not an artifact, and artifact identity
comes from the install-time capture written into the record. It closed on a
rule - a closed record is never silently re-pulled or re-baselined - rather
than on a mechanism.

Approved artifact, recorded in full so a later comparison has something to
compare against:

```text
HX alias:     Coder-X-GLM-Flash
Source URI:   hf.co/bartowski/zai-org_GLM-4.7-Flash-GGUF:Q5_K_M
Blob SHA-256: 9e0156957bd07760644aa2a3b6d6791ac8796f2c1bc9c75a2cb07cef5ccb5764
```

### Disposition

CLOSED for the spelling, which was the question asked: `:latest` here is how
Ollama displays an untagged alias, not a floating pin anyone chose.

The gap it sits next to stays open under HX4-F04: no gate rejects a changed
digest on any host. Closing this one should not be read as closing that.

## HX5-F12 — three hosts hold only short-form SPNs, and a short dNSHostName

**Status:** OPEN / REMEDIATION
**Severity:** Low
**Scope:** HX-2, HX-3, HX-4
**Discovered on:** All four audited hosts
**Discovered during:** 2026-09-16 resolution of the open SPN question

### Finding

The audit left the AD-side SPN set unestablished because the local keytab holds
only short forms and no AD query had been run. Asking the KDC directly settles
it, with no credentials: `kvno` returns a ticket when the SPN exists and says
so plainly when it does not.

```text
                host/SHORT  host/FQDN  RestrictedKrbHost/SHORT  RestrictedKrbHost/FQDN
  hx-2              OK         OK               OK                     absent
  hx-3              OK         OK               OK                     absent
  hx-4              OK         OK               OK                     absent
  hx-5              OK         OK               OK                     OK
```

Asked independently from HX-4 and from HX-5; both agree. The absence is
explicit, not a timeout:

```text
kvno: Server not found in Kerberos database while getting credentials for
      RestrictedKrbHost/hx-4.hx.local.arpa@HX.LOCAL.ARPA

RestrictedKrbHost/hx-5.hx.local.arpa@HX.LOCAL.ARPA: kvno = 2
```

### Corrected: kvno is not the authority either

The table above was the first answer and it is incomplete. `kvno` asks whether
a ticket can be issued, which is not the same as asking what AD stores. Reading
the computer objects directly gives the real state:

```text
HX-2  dNSHostName: hx-2                   host/HX-2, RestrictedKrbHost/HX-2
HX-3  dNSHostName: hx-3                   host/HX-3, RestrictedKrbHost/HX-3
HX-4  dNSHostName: hx-4                   host/HX-4, RestrictedKrbHost/HX-4
HX-5  dNSHostName: hx-5.hx.local.arpa     host/HX-5, host/hx-5.hx.local.arpa,
                                          RestrictedKrbHost/HX-5,
                                          RestrictedKrbHost/hx-5.hx.local.arpa
```

Three hosts are missing **two** SPNs each, not one, and their `dNSHostName` is
the short name rather than the FQDN. `kvno host/hx-4.hx.local.arpa` succeeded
because Samba's KDC matches that form implicitly from the realm; it does not do
so for `RestrictedKrbHost/`, which is why only that one appeared absent.

**Neither the keytab nor kvno was the authority.** The keytab lists only short
forms; kvno reports what a KDC will issue. Only the directory says what is
stored, and it took a third method to see it.

### What this settles

D-029 asked whether short-form principals are sufficient or FQDN SPNs must
exist. HX-5 is the reconciled reference and carries all four forms, so the
standard is all four. The other three carry three of four.

### Functional impact

None observed. `RestrictedKrbHost/<fqdn>` is used for constrained delegation
and restricted-host scenarios; nothing in the fleet requests it today, which is
why this was invisible until asked for directly.

### Disposition

OPEN. On HX-2, HX-3 and HX-4: set `dNSHostName` to the FQDN, then add
`host/<fqdn>` and `RestrictedKrbHost/<fqdn>`. Order matters - AD validates an
SPN write against `dNSHostName`, so the SPNs are refused while it holds the
short name.

HX-5 shows the intended end state, so the shared domain-join block is where
this is fixed. A future server should not arrive with a short `dNSHostName`.

Not remediated here: this writes to Active Directory.

## HX5-F13 — HX-1 is recorded PASS / CLOSED with four foundation controls unproven

**Status:** OPEN / OWNER DECISION
**Severity:** Low
**Scope:** HX-1
**Discovered on:** HX-1
**Discovered during:** 2026-09-16 review of the Foundation backfill

### Finding

HX-1's record carries `**State:** PASS / CLOSED`, and
`docs/00-control/hx-fleet.tsv` agrees. Its Foundation section now records four
controls as NOT ESTABLISHED: its own upstream time source, its SSH host key,
its AD SPNs, and the SPN read that would confirm them.

A record should not claim closure while its own evidence is unresolved. That is
the objection, and it is correct.

### How it arose

The inconsistency is new, and it was created by improving the record rather
than by anything changing on the host. HX-1 previously declared its whole
Foundation section not applicable, so there were no unresolved rows and the
claim was internally consistent - by not asking the question.

Replacing that blanket exemption with real rows is what surfaced the gap. Four
controls that are genuinely applicable to a domain controller had never been
recorded either way.

### Why it is not resolved here

Three of the four need access this audit does not have. The host key can only
be confirmed at the console; the SPN read needs directory access to the DC's
own object; HX-1's upstream time source has never been observed.

The fourth constraint is procedural: `hx-record-check` compares the record's
state line against the fleet inventory, so changing one alone is drift. Moving
HX-1 off `PASS / CLOSED` is a decision about the domain controller's status,
not an edit.

### Disposition

OPEN. Either close the four controls with evidence from the console, or move
HX-1's state in both the record and `hx-fleet.tsv` together, deliberately.

Related: proof step `F0` is `NOT_RUN` on this branch. It is set to PASS by the
change that wires the foundation into the proof chain, which is a separate
pull request and had not merged when this was written.

