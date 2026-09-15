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
**Scope:** Domain-client configuration; confirmed on HX-4 and HX-5  
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

### HX-5 recurrence — 2026-09-15

The same three failed socket units were observed on the freshly rebuilt HX-5:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

At the same time HX-5 passed all core domain checks:

```text
adcli testjoin -D hx.local.arpa       PASS
systemctl is-active sssd              active
getent passwd jarvisr@hx.local.arpa   PASS
```

This confirms the issue is not isolated to HX-4 and supports treating it as a
fleet domain-client configuration finding rather than an HX-4-specific build
failure.

### Disposition

DEFERRED.

No configuration change is made during the active server build because core
domain function is intact and correcting the responder activation model is a
separate fleet-standard decision.

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

## HX5-F01 — Fresh-install fstab comments name the wrong NVMe device

**Status:** OPEN / NON-BLOCKING  
**Severity:** Low  
**Scope:** HX-5 documentation hygiene only  
**Discovered on:** HX-5  
**Discovered during:** 2026-09-15 post-rebuild storage validation

### Finding

The active `/etc/fstab` entries use filesystem UUIDs and mount the correct
filesystems, but the installer-generated comments say the filesystems were on
`/dev/nvme0n1p*` while current enumeration shows those UUIDs on
`/dev/nvme1n1p*`.

Observed active mapping:

```text
/dev/nvme1n1p1  UUID=6DA4-AE41                             /boot/efi
/dev/nvme1n1p2  UUID=3e04ca1a-ccd0-4cc8-9bce-1d6e8f5bb532 /
/dev/nvme1n1p3  UUID=68d0e365-212c-456f-b42e-d908b445ae77 /srv/ollama
```

Observed stale comments:

```text
# / was on /dev/nvme0n1p2 during curtin installation
# /srv/ollama was on /dev/nvme0n1p3 during curtin installation
# /boot/efi was on /dev/nvme0n1p1 during curtin installation
```

### Functional impact

None. UUID-based mounts are correct and `/srv/ollama` is mounted read-write on
the intended 810.5 GB ext4 partition. The separate 476.9 GB `nvme0n1` device is
unmounted and is not authorized for build use.

### Disposition

NON-BLOCKING. Do not interrupt the HX-5 build to edit descriptive comments.
Correct the comments during a documentation/configuration hygiene pass if desired.
