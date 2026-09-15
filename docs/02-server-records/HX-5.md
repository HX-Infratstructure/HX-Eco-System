# HX-5 — CentCom / Ornith / DeepSeek Harness / dev-test Server Configuration

**Build state:** IN PROGRESS
**Gate:** DOMAIN / ADMIN / GPU / STORAGE PASS; LAYER 0/1 RECONCILIATION OPEN
**IP:** `192.168.50.205`
**FQDN:** `hx-5.hx.local.arpa`
**Record updated:** 2026-09-15

## 1. Identity and Network

- Static hostname: `hx-5`
- FQDN: `hx-5.hx.local.arpa`
- `/etc/hosts`: `127.0.1.1 hx-5.hx.local.arpa hx-5`
- IPv4: `192.168.50.205/24` on `eno1`
- Default gateway: `192.168.50.1`
- DNS: HX-1 `192.168.50.200`
- Persistent network file: `/etc/netplan/50-cloud-init.yaml`
- Netplan IPv4: `192.168.50.205/24`
- Netplan default route: `192.168.50.1`
- Netplan DNS: `192.168.50.200`
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
- Domain user resolution: `jarvisr@hx.local.arpa` PASS

**Domain join gate: PASS**

### Time synchronization — OPEN

Current live state after the clean OS reinstall:

```text
System clock synchronized: yes
NTP service: active
chrony: not installed
systemd-timesyncd: active / enabled
Current NTP server: ntp.ubuntu.com / 91.189.91.157
```

HX architecture assigns **HX-1 (`192.168.50.200`) as the fleet NTP source**.
HX-5 is therefore synchronized, but not to the approved HX fleet source.

**HX-1 NTP client gate: FAIL / CONFIGURATION MISSING**

Layer 0/1 must not be closed until the HX-1 NTP client baseline is restored and
proven.

### Post-rebuild SSH / administration access

The clean OS rebuild changed the HX-5 SSH host key, so the stale Windows
`known_hosts` entry was removed and the rebuilt host fingerprint was accepted.

Authoritative Windows fleet identity:

```text
Private key: C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519
Public key:  C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519.pub
```

`hx_fleet_admin` is not the fleet-key filename.

Fleet public-key authentication was installed into `hxsa`'s
`~/.ssh/authorized_keys`.

Current fleet key fingerprint:

```text
SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk hx-fleet-20260810
```

Key-only remote proof:

```text
hx-5
KEY+SUDO-PASS
```

Therefore:

- Passwordless fleet-key SSH: PASS
- `hxsa` non-interactive sudo: PASS
- Windows operator key identity: `hx_fleet_ed25519`

SSH runtime audit:

```text
ssh.service: active
ssh.service enabled state: disabled
port: 22
```

Remote SSH works now, but reboot/startup persistence remains to be explicitly
proved. The current audit did not capture `ssh.socket`, so the persistence
mechanism is not yet established.

**SSH runtime: PASS**
**SSH reboot persistence: VERIFICATION REQUIRED**

### Firewall posture

Observed:

```text
ufw status: inactive
ufw.service: enabled
ufw.service: active
nftables ruleset: empty
firewalld: inactive / not found
```

Effective traffic filtering is absent, which matches the intended trusted-LAN
posture. However D-018 and Block 1 explicitly call for UFW to be disabled and
stopped.

**Effective no-firewall posture: PASS**
**UFW service-state compliance: FAIL / DRIFT**

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | Ubuntu 24.04.5 LTS |
| Kernel | `7.0.0-31-generic` |
| Architecture | x86-64 |
| Hardware vendor | iBUYPOWER |
| Hardware model | Intel Core i7-14700F system |
| Firmware version | BIOS 1836 |
| Firmware date | 2026-04-17 |
| sudo policy | `hxsa ALL=(ALL:ALL) NOPASSWD: ALL`; validated with `sudo -n true` |

Current package audit shows four Netplan-related updates still pending:

```text
libnetplan1
netplan-generator
netplan.io
python3-netplan
```

**Base OS update/upgrade gate: OPEN — package updates pending.**

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
- `nvidia-smi`: PASS
- PCI enumeration: PASS

**GPU gate: PASS**

The current driver is intentionally `595.99.02`. The shared Block 2 pin still
targets `nvidia-driver-595-server-open=595.71.05-0ubuntu0.24.04.1`, so Block 2
must not be rerun on HX-5 as written.

## 4. Storage Layout

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

Filesystem utilization:

```text
/dev/nvme1n1p3 ext4 797G 28K 757G 1% /srv/ollama
```

**Storage gate: PASS**

`/etc/fstab` UUID mappings are correct. Installer-generated comments refer to
`nvme0n1p*`; those comments are stale descriptive text only and are tracked as
a non-blocking finding.

## 5. Domain / SSSD Deferred Condition

Three failed responder sockets remain:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

At the same time:

```text
adcli testjoin: PASS
sssd.service: active
domain user resolution: PASS
```

This reproduces HX4-F02 and remains **DEFERRED / NON-BLOCKING** under the
existing disposition.

## 6. Runtime

Pending Ollama installation.

No Block 3/Ollama action is authorized until Layer 0/1 reconciliation is
completed.

## 7. Model / Application Provenance

Pending Ornith installation.

Required fields at install time:

```text
HX alias:              <ollama name or service identifier>
Upstream identity:     <official model/product name and version>
Source URI:            <exact source reference>
Artifact SHA-256:      <resolved immutable artifact hash>
Import method:         <pull | GGUF import | other approved method>
```

## 8. Functional Validation

Current infrastructure proof:

```text
hostname: hx-5                              PASS
hostname -f: hx-5.hx.local.arpa           PASS
persistent IPv4/gateway/DNS               PASS
live IPv4/gateway/HX-1 DNS                PASS
AD machine trust                           PASS
SSSD core function                         PASS
Samba DNS/dNSHostName/SPNs                 PASS after repair
NOPASSWD sudo                              PASS
passwordless fleet-key SSH                 PASS
NVIDIA driver 595.99.02                    PASS
RTX 5060 visibility                        PASS
RTX 5060 Ti visibility                     PASS
/srv/ollama dedicated mount                PASS
HX-1 NTP source                            FAIL / missing
UFW service disabled/stopped               FAIL / drift
OS package-current state                   FAIL / updates pending
SSH reboot persistence                     VERIFICATION REQUIRED
```

## 9. Layer 0/1 Closure State

| Gate | Result |
|---|---|
| Hostname / FQDN | PASS |
| Persistent IPv4 / gateway / DNS | PASS |
| Live network / HX-1 DNS | PASS |
| HX-1 NTP client | **FAIL — MISSING** |
| NOPASSWD sudo | PASS |
| Fleet SSH key | PASS |
| SSH runtime / port 22 | PASS |
| SSH reboot persistence | **VERIFICATION REQUIRED** |
| Effective no-firewall posture | PASS |
| UFW disabled/stopped | **FAIL — DRIFT** |
| Domain join / SSSD core function | PASS |
| Machine trust | PASS |
| Samba DNS / FQDN / SPNs | PASS after repair |
| SSSD socket cleanliness | DEFERRED / HX4-F02 |
| GPU driver and visibility | PASS |
| Dedicated storage | PASS |
| Base OS updates current | **FAIL — 4 UPDATES PENDING** |
| Final post-reboot proof | PENDING |

**HX-5 LAYER 0/1 STATUS: NOT CLOSED**

Remaining closure work:

1. Restore the approved HX-1 NTP client configuration.
2. Reconcile UFW service state to D-018 / Block 1: disabled and stopped.
3. Apply/resolve approved pending OS updates.
4. Verify the SSH startup mechanism and reboot persistence.
5. Reboot and perform final Layer 0/1 validation.

Only after those items pass should HX-5 proceed to Block 3 / Ollama.

## 10. Evidence References

Runtime evidence for the 2026-09-15 audit is recorded inline in this server
record and in:

```text
docs/00-control/HX-BASE-BLOCKS-1-2-CONFIGURATION-AUDIT.md
```

The detailed audit is the authority for Block 1/2 coverage gaps and the
corrected clean-build process shape.
