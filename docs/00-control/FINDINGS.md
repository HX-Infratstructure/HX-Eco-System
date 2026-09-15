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

The script executes with `set -euo pipefail`. When `grep -q` finds a match, it can exit before the producer finishes writing, producing SIGPIPE/141 in the producer and a false pipeline failure under `pipefail`.

HX-4 exposed the defect on `resolvectl status` even though HX-1 DNS was present.

### Resolution

The three checks were changed to capture command output completely before applying `grep`. Existing exit codes 11, 12, and 13 were preserved.

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

### Disposition

CLOSED.

The correction is part of the shared runbook. One remaining instance of the same pattern is tracked separately as HX4-F05.

## HX4-F02 — SSSD responder and socket-activation conflict

**Status:** OPEN / DEFERRED  
**Severity:** Low  
**Scope:** Domain-client configuration; confirmed on HX-4 and HX-5  
**Discovered on:** HX-4  
**Discovered during:** Post-Block-2 validation

### Finding

HX-4 showed failed SSSD responder socket units while core SSSD/domain behavior remained functional. The configuration includes direct responder startup while systemd socket activation is also present.

### HX-5 recurrence — 2026-09-15

HX-5 initially showed:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

while all core domain checks passed:

```text
adcli testjoin -D hx.local.arpa       PASS
systemctl is-active sssd              active
getent passwd jarvisr@hx.local.arpa   PASS
```

After the final HX-5 reconciliation reboot, two failed sockets remained:

```text
sssd-nss.socket
sssd-pam-priv.socket
```

`sssd-pam.socket` no longer remained failed.

### Functional impact

No domain-join or identity-resolution failure is observed.

Therefore:

- DOMAIN JOIN: PASS
- MACHINE TRUST: PASS
- IDENTITY RESOLUTION: PASS
- SSSD CORE SERVICE: PASS
- RESPONDER/SOCKET CLEANLINESS: FAIL / DEFERRED

### Disposition

DEFERRED / NON-BLOCKING.

Do not redesign SSSD inline during active server builds. Resolve as a separate fleet-standard change.

### Required follow-up

1. Inspect SSSD responder configuration on existing joined hosts.
2. Determine whether HX standardizes on direct responder startup or socket activation.
3. Update the common domain-join runbook if fleet-wide.
4. Correct affected hosts under a separate approved change.
5. Close with validation evidence.

## HX4-F03 — Provenance artifact hash could be written blank or as a path

**Status:** CLOSED  
**Severity:** Medium  
**Scope:** Any server whose models are installed by the Ollama model blocks  
**Discovered on:** HX-4  
**Discovered during:** Owner review of PR #20, before merge  
**Affected file:** `docs/03-runbooks/common/hx-base.env`

### Finding

`hx_ollama_provenance` could emit an empty artifact hash or a filesystem path under the `Artifact SHA-256` label when the blob reference was missing or malformed.

### Resolution

The digest is now resolved explicitly and falls back to `UNRESOLVED` when it cannot be extracted safely.

### Repository references

- PR: #20
- Fix commit: `e649490e7763a1b6cb5bae033e4b58336aaee235`
- Merged commit: `509566c8bfc2cc13b2ab38573a03175a1b7da43b`

### Disposition

CLOSED. Caught in review; no server record was written from the defective helper.

## HX4-F04 — A floating model reference was accepted as a pin

**Status:** CLOSED  
**Severity:** Medium  
**Scope:** Fleet-wide, for every Ollama model reference  
**Discovered on:** HX-4  
**Discovered during:** Owner review of PR #20, before merge

### Finding

A floating `latest` reference could satisfy a non-empty model check even though it did not identify a stable reviewed source reference.

### Resolution

`hx_require_pinned_ref` rejects missing tags and `:latest`. Artifact-level identity is still established by the resolved Ollama model ID and blob SHA-256 captured at install time.

### Repository references

- PR: #20
- Fix commit: `e649490e7763a1b6cb5bae033e4b58336aaee235`
- Merged commit: `509566c8bfc2cc13b2ab38573a03175a1b7da43b`

### Disposition

CLOSED.

## HX4-F05 — The HX4-F01 pattern survives in the domain-join block

**Status:** OPEN / MONITOR  
**Severity:** Low  
**Scope:** `docs/03-runbooks/common/02-domain-nvidia.sh`  
**Discovered on:** HX-4

### Finding

The domain-join idempotency guard still uses:

```bash
if realm list | grep -q 'configured: kerberos-member'; then
```

Measured on HX-4, the pipeline returned `0 0` five times and did not reproduce HX4-F01 because `realm list` finishes writing before `grep -q` exits.

### Disposition

DEFERRED / MONITOR.

Convert the guard to captured-output form when Block 2 is next touched for another reason. Do not open a change solely for this while the measured behavior holds.

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
