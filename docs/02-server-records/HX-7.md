# HX-7 — NGINX dev/test only Server Configuration

**Build state:** NOT STARTED
**Gate:** —
**IP:** `192.168.50.207`
**FQDN:** `hx-7.hx.local.arpa`
**Record updated:** 2026-09-10
> Scaffolded by `tools/hx-doc/hx-new-server hx-7`. Fill every section as the
> build proceeds. `tools/hx-doc/hx-record-check` reports what is still open.

## Foundation

Established by `docs/03-runbooks/common/00-foundation.sh` before Block 1, and
gated by `01-base-admin-network-updates.sh`, which refuses to proceed without
it. Proven from the operator workstation before Layer 0/1 closes.

| Control | Expected | State |
|---|---|---|
| `hostname -f` | `hx-7.hx.local.arpa` | NOT ESTABLISHED |
| AD DNS A record | the address recorded in `docs/00-control/hx-fleet.tsv` | NOT ESTABLISHED |
| Time authority | `chronyc sources` shows `^* 192.168.50.200` | NOT ESTABLISHED |
| Fleet key | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk` | NOT ESTABLISHED |
| NOPASSWD sudo | `sudo -k -n true` succeeds | NOT ESTABLISHED |
| SSH persistence | `ssh.service` or `ssh.socket` enabled | NOT ESTABLISHED |
| External key-only login | `tools/hx-doc/hx-fleet-access hx-7` returns `hx-7` and `KEY+SUDO-PASS` | NOT ESTABLISHED |
| SSH host key | recorded at build, so a later change is answerable from the repository | NOT ESTABLISHED |

This host is not built. Every row is filled from the build, and proof step F0
in `docs/00-control/hx-proof.tsv` must be satisfied before this server's own
phase can close.

<!-- SPNs deliberately absent pending D-029. -->

## 1. Identity and Network

Hostname, IP, gateway, DNS, domain join, SSSD, domain user resolution.
State the gate result: **Domain join gate: PASS/FAIL**.

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | |
| Kernel | |
| Firmware version | |
| sudo policy | |

## 3. GPU Configuration

Driver package **and exact version**, GPU models and count, `nvidia-smi` proof.
State the gate result: **GPU gate: PASS/FAIL**.

## 4. Storage Layout

Devices, filesystems, mount points, and the dedicated application path.
State the gate result: **Storage gate: PASS/FAIL**.

## 5. Runtime

Package source, **exact installed version**, service unit, systemd overrides,
listener address and port.

## 6. Model / Application Provenance

Required for every server that hosts a model or a downloaded artifact. All
five fields are mandatory — an unknown value is recorded as `UNRESOLVED`, never
omitted, because a missing field cannot be told apart from a forgotten one.

```text
HX alias:              <ollama name or service identifier>
Upstream identity:     <official model/product name and version>
Source URI:            <exact hf.co/... repo:file, package URL, or registry ref>
Artifact SHA-256:      <full 64-character hash of the downloaded artifact>
Import method:         <pull | GGUF import | package install | build from source>
```

If the artifact was imported rather than pulled, also record the Modelfile or
build definition verbatim, including any template, parameter, or stop-token
settings. If none were set, say so explicitly.

Why both Source URI and SHA-256 are required: the hash proves what is running,
and the URI proves where it came from. Public model registries carry modified
community rebuilds under names close to the official ones, so neither field
alone establishes provenance.

## 7. Functional Validation

Known-answer CLI proof, HTTP/API proof, LAN proof, reboot persistence. Include
the exact command and the exact response for each.

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | |
| Domain join / SSSD | |
| GPU driver and visibility | |
| Dedicated storage | |
| Runtime version | |
| Service active / enabled | |
| Model / application loaded | |
| Known-answer functional proof | |
| Reboot persistence | |

## 9. Evidence References

Either a retained bundle path under `docs/05-evidence/<server>/<component>/<run-id>/`,
or an explicit statement that the proof is recorded inline in section 7 of this
record. See `docs/05-evidence/README.md` for which model applies.
