# HX-5 — CentCom / Ornith / DeepSeek Harness / dev-test Server Configuration

**Build state:** IN PROGRESS
**Gate:** DOMAIN / ADMIN / GPU / STORAGE PASS
**IP:** `192.168.50.205`
**FQDN:** `hx-5.hx.local.arpa`
**Record updated:** 2026-09-15
> Scaffolded by `tools/hx-doc/hx-new-server hx-5`. Fill every section as the
> build proceeds. `tools/hx-doc/hx-record-check` reports what is still open.

## 1. Identity and Network

- Static hostname: `hx-5`
- FQDN: `hx-5.hx.local.arpa`
- IPv4: `192.168.50.205/24` on `eno1`
- Default gateway: `192.168.50.1`
- AD DNS zone: `hx.local.arpa`
- Kerberos realm: `HX.LOCAL.ARPA`
- Samba computer object: `HX-5$`
- Samba `dNSHostName`: `hx-5.hx.local.arpa`
- Samba DNS A record: `hx-5.hx.local.arpa -> 192.168.50.205`
- Required SPNs present:
  - `host/HX-5`
  - `host/hx-5.hx.local.arpa`
  - `RestrictedKrbHost/HX-5`
  - `RestrictedKrbHost/hx-5.hx.local.arpa`
- `adcli testjoin -D hx.local.arpa`: PASS
- SSSD service state: `active`
- SSSD realm configuration: `kerberos-member`
- Domain user resolution proof: `jarvisr@hx.local.arpa` resolved by `getent passwd`.

**Domain join gate: PASS**

### Post-rebuild SSH / administration access

The 2026-09-15 clean OS rebuild changed the HX-5 SSH host key, so the stale
Windows `known_hosts` entry was removed and the rebuilt host fingerprint was
accepted after local verification.

Authoritative Windows fleet identity:

```text
Private key: C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519
Public key:  C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519.pub
```

`hx_fleet_admin` is not the fleet-key filename and must not be used in HX-5
operator instructions.

Fleet public-key authentication was installed into `hxsa`'s
`~/.ssh/authorized_keys`. Key-only proof from the Windows control workstation:

```powershell
ssh -o PasswordAuthentication=no -i $env:USERPROFILE\.ssh\hx_fleet_ed25519 hxsa@192.168.50.205 "hostname; sudo -n true && echo KEY+SUDO-PASS"
```

Observed result:

```text
hx-5
KEY+SUDO-PASS
```

Therefore:

- Passwordless fleet-key SSH: PASS
- `hxsa` non-interactive sudo: PASS
- Windows operator key identity: `hx_fleet_ed25519`

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | Ubuntu 24.04.5 LTS |
| Kernel | `7.0.0-31-generic` |
| Firmware version | BIOS 1836 |
| sudo policy | `hxsa ALL=(ALL:ALL) NOPASSWD: ALL`; validated with `sudo -n true` |

## 3. GPU Configuration

Current post-rebuild evidence captured 2026-09-15:

- NVIDIA driver version: `595.99.02`
- CUDA version reported by `nvidia-smi`: `13.2`
- Kernel module: `/lib/modules/7.0.0-31-generic/kernel/drivers/video/nvidia.ko`
- Kernel module version: `595.99.02`
- Kernel module license: `Dual MIT/GPL`
- GPU 0: NVIDIA GeForce RTX 5060, `8151 MiB`, PCI `00000000:01:00.0`
- GPU 0 UUID: `GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11`
- GPU 1: NVIDIA GeForce RTX 5060 Ti, `16311 MiB`, PCI `00000000:07:00.0`
- GPU 1 UUID: `GPU-11b1a30e-8c11-001b-7b8b-7b1e15ab6978`
- Combined physical VRAM: approximately 24 GB
- `nvidia-smi`: PASS; both GPUs visible and idle
- PCI enumeration:
  - RTX 5060 device `10de:2d05`, audio `10de:22eb`
  - RTX 5060 Ti device `10de:2d04`, audio `10de:22eb`

**GPU gate: PASS**

The current driver is intentionally `595.99.02`, installed during the clean-OS
rebuild after hardware troubleshooting. Do not replace it with the older shared
runbook package baseline merely to make HX-5 match a historical fleet pin.

## 4. Storage Layout

Current storage evidence captured 2026-09-15:

| Device | Size | Filesystem | UUID | Mount | Purpose |
|---|---:|---|---|---|---|
| `nvme1n1p1` | 1 GB | vfat | `6DA4-AE41` | `/boot/efi` | EFI system partition |
| `nvme1n1p2` | 120 GB | ext4 | `3e04ca1a-ccd0-4cc8-9bce-1d6e8f5bb532` | `/` | OS/root |
| `nvme1n1p3` | 810.5 GB | ext4 | `68d0e365-212c-456f-b42e-d908b445ae77` | `/srv/ollama` | Dedicated Ollama/model storage |
| `nvme0n1` | 476.9 GB | none observed | — | unmounted | Not authorized for HX-5 build use; leave untouched |

`/srv/ollama` proof:

```text
TARGET      SOURCE         FSTYPE OPTIONS
/srv/ollama /dev/nvme1n1p3 ext4   rw,relatime,stripe=128
```

Filesystem utilization at capture:

```text
/dev/nvme1n1p3 ext4 797G 28K 757G 1% /srv/ollama
```

The dedicated application filesystem is therefore mounted, writable, and
essentially empty. No formatting, repartitioning, or disk reassignment is
required before the Ollama installation block.

**Storage gate: PASS**

Note: `/etc/fstab` UUID entries are correct and resolve to the current devices,
but installer-generated comments still say the filesystems were on
`/dev/nvme0n1p*`. Those comments are stale descriptive text only; the active
UUID-based mounts are correct. This is tracked as a non-blocking finding.

## 5. Runtime

Package source, **exact installed version**, service unit, systemd overrides,
listener address and port.

Pending Ollama installation.

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

Current infrastructure proof:

```text
hostname: hx-5
hostname -f: hx-5.hx.local.arpa
IPv4: 192.168.50.205/24
AD machine trust: PASS
SSSD service: active
Domain user resolution: PASS
NOPASSWD sudo: PASS
Passwordless fleet-key SSH: PASS
NVIDIA driver 595.99.02: PASS
RTX 5060 visibility: PASS
RTX 5060 Ti visibility: PASS
/srv/ollama dedicated mount: PASS
```

Three failed SSSD responder socket units remain visible:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

This reproduces the already-deferred HX4-F02 responder/socket conflict while
core domain identity functions remain operational. It is non-blocking for the
HX-5 build and must not trigger an in-line redesign of SSSD during this build.

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | PASS WITH DEFERRED SSSD SOCKET FINDING |
| Domain join / SSSD core function | PASS |
| GPU driver and visibility | PASS |
| Dedicated storage | PASS |
| Runtime version | PENDING |
| Service active / enabled | PENDING |
| Model / application loaded | PENDING |
| Known-answer functional proof | PENDING |
| Reboot persistence | PENDING |

## 9. Evidence References

Current evidence is recorded inline in this server record from the 2026-09-15
post-rebuild validation pass. It covers identity/network, domain trust, SSSD
core function, Windows fleet-key/passwordless-sudo access, OS/kernel, NVIDIA
module/driver, dual-GPU PCI/runtime visibility, and dedicated Ollama storage.

Runtime, model provenance, model functional proof, multi-GPU inference proof,
and reboot-persistence evidence remain open.
