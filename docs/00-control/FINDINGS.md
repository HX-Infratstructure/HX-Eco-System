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
