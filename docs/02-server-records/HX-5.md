# HX-5 — CentCom / Ornith / DeepSeek Harness / dev-test Server Configuration

**Build state:** IN PROGRESS — Layer 0/1 closed; Ollama runtime complete; Ornith/model build pending  
**Gate:** LAYER 0/1 PASS / CLOSED; DOMAIN / ADMIN / GPU / STORAGE / OLLAMA RUNTIME PASS  
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

### Time synchronization

The clean OS initially used `systemd-timesyncd` and `ntp.ubuntu.com`. That was a Layer 0/1 rebuild gap because HX-1 is the fleet NTP source.

Corrected state:

```text
chrony: active / enabled
Reference ID: C0A832C8 (192.168.50.200)
Selected source: ^* 192.168.50.200
HX-1 source stratum: 3
HX-5 local stratum: 4
Leap status: Normal
```

Post-reboot proof showed HX-1 remained the selected source and the system clock remained synchronized.

**HX-1 NTP client gate: PASS**

### Post-rebuild SSH / administration access

The clean OS rebuild changed the HX-5 SSH host key. The stale Windows `known_hosts` entry was removed and the rebuilt host fingerprint was accepted after local verification.

Authoritative Windows fleet identity:

```text
Private key: C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519
Public key:  C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519.pub
```

`hx_fleet_admin` is not the fleet-key filename.

Fleet public-key authentication is installed in `hxsa`'s `~/.ssh/authorized_keys`.

Fleet public-key fingerprint:

```text
SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk hx-fleet-20260810
```

Key-only proof from the Windows control workstation:

```text
hx-5
KEY+SUDO-PASS
```

Post-reboot SSH state:

```text
ssh.service: active
ssh.socket: active
ssh.socket: enabled
port: 22
```

Ubuntu is using socket activation for persistence. SSH survived the Layer 0/1 reboot and remote access remained functional.

- Passwordless fleet-key SSH: PASS
- `hxsa` non-interactive sudo: PASS
- SSH runtime: PASS
- SSH reboot persistence: PASS

### Firewall posture

D-018 defines the HX LAN as a trusted lab segment with UFW disabled.

Corrected and post-reboot state:

```text
ufw status: inactive
ufw.service: disabled
ufw.service: inactive
firewalld: inactive / not found
```

No new firewall restrictions were introduced.

**D-018 host-firewall posture: PASS**

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

`apt update` / `apt upgrade -y` were executed during Layer 0/1 reconciliation.

Four Netplan packages remain listed as upgradeable:

```text
libnetplan1
netplan-generator
netplan.io
python3-netplan
```

Both simulated upgrade paths proved they are deferred solely by Ubuntu phased updates:

```text
The following upgrades have been deferred due to phasing:
  libnetplan1 netplan-generator netplan.io python3-netplan
0 upgraded, 0 newly installed, 0 to remove and 4 not upgraded.
```

`apt-mark showhold` returned no held packages. These phased updates are therefore **not a failed maintenance gate and are not blocking Layer 0/1 closure**.

**Base OS update/upgrade gate: PASS WITH NORMAL PHASED-UPDATES EXCEPTION**

## 3. GPU Configuration

Current post-rebuild evidence:

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
- `nvidia-smi`: PASS before and after reboot
- PCI enumeration: PASS

**GPU gate: PASS**

The current driver is intentionally `595.99.02`. The shared Block 2 pin still targets `nvidia-driver-595-server-open=595.71.05-0ubuntu0.24.04.1`, so Block 2 must not be rerun on HX-5 as written.

## 4. Storage Layout

Authoritative filesystem identities are UUID-based. Linux NVMe enumeration changed across reboot, which is expected and demonstrates why device names are not storage authority.

| Purpose | Filesystem | UUID | Mount |
|---|---|---|---|
| EFI | vfat | `6DA4-AE41` | `/boot/efi` |
| OS/root | ext4 | `3e04ca1a-ccd0-4cc8-9bce-1d6e8f5bb532` | `/` |
| Ollama/model storage | ext4 | `68d0e365-212c-456f-b42e-d908b445ae77` | `/srv/ollama` |

Pre-reboot `/srv/ollama` source was observed as `/dev/nvme1n1p3`; post-reboot it enumerated as `/dev/nvme0n1p3`:

```text
TARGET      SOURCE         FSTYPE OPTIONS
/srv/ollama /dev/nvme0n1p3 ext4   rw,relatime,stripe=128
```

Filesystem utilization at post-reboot proof:

```text
/dev/nvme0n1p3 ext4 797G 28K 757G 1% /srv/ollama
```

The UUID and mount remained correct across reboot. The separate approximately 476.9 GB NVMe device remains outside HX-5 build authority and must not be formatted, partitioned, mounted, or repurposed without explicit owner approval.

**Storage gate: PASS**

Installer-generated `/etc/fstab` comments naming old NVMe device paths remain descriptive-only and are tracked as HX5-F01. Active UUID mappings are correct.

## 5. Domain / SSSD Deferred Condition

Core domain function remains healthy:

```text
adcli testjoin: PASS
sssd.service: active
domain user resolution: PASS
```

The known responder/socket conflict remains non-blocking. Initial audit showed:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

After reboot, two failed units remained:

```text
sssd-nss.socket
sssd-pam-priv.socket
```

This is the existing HX4-F02 fleet-pattern finding and remains **DEFERRED / NON-BLOCKING**. Do not redesign SSSD inline during the HX-5 application build.

## 6. Runtime

Block 3 completed successfully on 2026-09-15.

| Item | As-built state |
|---|---|
| Ollama version | `0.34.0` |
| Install source | official Ollama Linux release archive |
| Archive SHA-256 | `cf95886728959aa09910bb34de5cca1cc5a8f68003b5597197d3f2c2d57c0804` |
| Archive verification | PASS |
| Service | `ollama.service` |
| Service state | active |
| Startup state | enabled |
| API listener | `*:11434` |
| LAN endpoint | `http://192.168.50.205:11434` |
| Model storage | `/srv/ollama/models` |
| Cloud state | disabled for current base build |

Systemd environment:

```text
OLLAMA_MODELS=/srv/ollama/models
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_NO_CLOUD=1
```

Block 3 validation returned:

```text
ollama --version: 0.34.0
ollama.service: active
autostart: enabled
listener: *:11434
localhost /api/version: {"version":"0.34.0"}
LAN /api/version:       {"version":"0.34.0"}
```

The existing two failed SSSD responder sockets remained visible during Block 3 and were accepted under HX4-F02; they did not block domain resolution, GPU validation, storage validation, Ollama installation, or API startup.

**OLLAMA RUNTIME GATE: PASS**

## 7. Model / Application Provenance

Pending Ornith installation.

The current repository defines the next HX-5 workload step as installation and BASE PASS of the Ornith model, but the current `main` runbook does not yet encode a pinned Ornith model reference or model-install script. Do not invent the upstream model identity from the role name alone.

Required fields at install time:

```text
HX alias:              <ollama name or service identifier>
Upstream identity:     <official model/product name and version>
Source URI:            <exact source reference>
Artifact SHA-256:      <resolved immutable artifact hash>
Import method:         <pull | GGUF import | other approved method>
```

## 8. Functional Validation

Current proof:

```text
hostname: hx-5                              PASS
hostname -f: hx-5.hx.local.arpa           PASS
persistent IPv4/gateway/DNS               PASS
live IPv4/gateway/HX-1 DNS                PASS
HX-1 NTP / chrony                          PASS
AD machine trust                           PASS
SSSD core function                         PASS
Samba DNS/dNSHostName/SPNs                 PASS after repair
NOPASSWD sudo                              PASS
passwordless fleet-key SSH                 PASS
SSH reboot persistence via ssh.socket      PASS
D-018 UFW disabled/inactive                PASS
NVIDIA driver 595.99.02                    PASS
RTX 5060 visibility                        PASS
RTX 5060 Ti visibility                     PASS
/srv/ollama dedicated mount                PASS after reboot
OS maintenance                             PASS; Netplan updates phased normally
Ollama 0.34.0 archive verification         PASS
Ollama service active/enabled              PASS
Ollama localhost API                       PASS
Ollama LAN API                             PASS
```

## 9. Layer 0/1 Closure State

| Gate | Result |
|---|---|
| Hostname / FQDN | PASS |
| Persistent IPv4 / gateway / DNS | PASS |
| Live network / HX-1 DNS | PASS |
| HX-1 NTP client | PASS |
| NOPASSWD sudo | PASS |
| Fleet SSH key | PASS |
| SSH runtime / port 22 | PASS |
| SSH reboot persistence | PASS — `ssh.socket` active/enabled |
| D-018 UFW disabled/stopped | PASS |
| Domain join / SSSD core function | PASS |
| Machine trust | PASS |
| Samba DNS / FQDN / SPNs | PASS after repair |
| SSSD socket cleanliness | DEFERRED / HX4-F02 |
| GPU driver and visibility | PASS |
| Dedicated storage | PASS |
| Base OS maintenance | PASS — only Ubuntu phased updates remain |
| Final post-reboot proof | PASS |

**HX-5 LAYER 0/1 STATUS: PASS / CLOSED**

Layer 0/1 closed on 2026-09-15 after the clean-rebuild reconciliation and post-reboot proof. HX4-F02 remains the sole known deferred Layer 0/1 condition and does not block the HX-5 application/runtime build.

## 10. HX-5 Workload Progress

| Workload gate | Result |
|---|---|
| Layer 0/1 foundation | PASS / CLOSED |
| Ollama runtime / Block 3 | PASS |
| Ornith model installed | PENDING |
| Ornith CLI inference | PENDING |
| Ornith HTTP/LAN inference | PENDING |
| Workload GPU-placement validation | PENDING |
| Ollama + Ornith reboot persistence | PENDING |
| CentCom smoke-runner activation | BLOCKED on Ornith + reboot persistence |
| DeepSeek Harness | FUTURE SCHEDULED WORK |

## 11. Evidence References

Primary Layer 0/1 evidence is recorded in:

```text
docs/00-control/HX-BASE-BLOCKS-1-2-CONFIGURATION-AUDIT.md
docs/05-evidence/hx-5/layer0-1/2026-09-15-closure.md
```

Block 3 evidence is recorded in this server record from the 2026-09-15 execution transcript. The current HX-5 runbook sequence is `docs/03-runbooks/HX-5/README.md`.
