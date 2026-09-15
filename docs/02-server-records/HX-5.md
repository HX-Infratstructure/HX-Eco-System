# HX-5 — CentCom / Ornith / DeepSeek Harness / dev-test Server Configuration

**Build state:** IN PROGRESS — foundation and Ornith BASE PASS complete; CentCom smoke-runner activation next  
**Gate:** LAYER 0/1 CLOSED; OLLAMA / ORNITH BASE PASS; CENTCOM RUNNER PENDING  
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
- SSSD service: active
- Domain user resolution: `jarvisr@hx.local.arpa` PASS

### Time synchronization

HX-1 is the accepted fleet NTP source.

```text
chrony: active / enabled
Reference ID: C0A832C8 (192.168.50.200)
Selected source: ^* 192.168.50.200
HX-1 source stratum: 3
HX-5 local stratum: 4
Leap status: Normal
```

Post-reboot validation confirmed HX-1 remained selected.

**HX-1 NTP client gate: PASS**

### SSH / administration access

Authoritative Windows fleet identity:

```text
Private key: C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519
Public key:  C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519.pub
Fingerprint: SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk hx-fleet-20260810
```

Key-only external proof:

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

- Passwordless fleet-key SSH: PASS
- `hxsa` non-interactive sudo: PASS
- SSH reboot persistence: PASS

### Firewall posture

D-018 trusted-LAN posture:

```text
ufw status: inactive
ufw.service: disabled
ufw.service: inactive
firewalld: inactive / not found
```

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
| sudo policy | `hxsa ALL=(ALL:ALL) NOPASSWD: ALL` |

Layer 0/1 maintenance completed with no immediately applicable updates after final reboot.

Four Netplan packages were previously shown as upgradeable but both `apt-get -s upgrade` and `apt-get -s dist-upgrade` proved they were deferred solely by Ubuntu phased updates. No packages were held.

**Base OS maintenance gate: PASS WITH NORMAL PHASED-UPDATES EXCEPTION**

## 3. GPU Configuration

Accepted HX-5 mixed-GPU configuration:

- NVIDIA driver: `595.99.02`
- CUDA reported by `nvidia-smi`: `13.2`
- GPU 0: NVIDIA GeForce RTX 5060, `8151 MiB`, PCI `00000000:01:00.0`
- GPU 0 UUID: `GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11`
- GPU 1: NVIDIA GeForce RTX 5060 Ti, `16311 MiB`, PCI `00000000:07:00.0`
- GPU 1 UUID: `GPU-11b1a30e-8c11-001b-7b8b-7b1e15ab6978`
- Combined physical VRAM: approximately 24 GB

`nvidia-smi` passed before and after reboot.

The shared Block 2 NVIDIA package pin is not the accepted HX-5 driver state; Block 2 must not be rerun on HX-5 merely for confirmation.

**GPU gate: PASS**

## 4. Storage Layout

Filesystem identity is UUID-authoritative.

| Purpose | Filesystem | UUID | Mount |
|---|---|---|---|
| EFI | vfat | `6DA4-AE41` | `/boot/efi` |
| OS/root | ext4 | `3e04ca1a-ccd0-4cc8-9bce-1d6e8f5bb532` | `/` |
| Ollama/model storage | ext4 | `68d0e365-212c-456f-b42e-d908b445ae77` | `/srv/ollama` |

Observed before one reboot:

```text
/srv/ollama /dev/nvme0n1p3 ext4 rw,relatime,stripe=128
```

Observed after the next reboot:

```text
/srv/ollama /dev/nvme1n1p3 ext4 rw,relatime,stripe=128
/dev/nvme1n1p3 797G 22G 736G 3% /srv/ollama
```

The device-name renumbering confirms why UUID, not `/dev/nvmeXnY`, is authority. The mount persisted correctly and contains the installed 22 GB Ornith model data.

The separate approximately 476.9 GB ADATA NVMe remains outside the current HX-5 build scope.

**Storage gate: PASS**

## 5. Domain / SSSD Deferred Condition

Core domain function:

```text
adcli testjoin: PASS
sssd.service: active
domain user resolution: PASS
```

After final reboot two failed responder sockets remained:

```text
sssd-nss.socket
sssd-pam-priv.socket
```

This is tracked under HX4-F02 and remains **DEFERRED / NON-BLOCKING** because machine trust, SSSD service, and domain identity resolution all pass.

## 6. Ollama Runtime

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
| API binding | `0.0.0.0:11434` |
| Live listener | `*:11434` |
| LAN endpoint | `http://192.168.50.205:11434` |
| Model storage | `/srv/ollama/models` |
| Cloud state | disabled for current base build |

Systemd environment:

```text
OLLAMA_MODELS=/srv/ollama/models
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_NO_CLOUD=1
```

Local and LAN `/api/version` checks returned Ollama `0.34.0`.

After reboot:

```text
systemctl is-enabled ollama -> enabled
systemctl is-active ollama  -> active
ss -ltn                    -> *:11434
```

**OLLAMA RUNTIME GATE: PASS**

## 7. Ornith 1.5 35B — Model Authority and Provenance

Current owner-approved HX-5 inference model:

```text
ornith-1.5:35b
```

The prior `ornith-1.5:9b` assignment is stale and invalid for this build.

Installed model facts:

```text
Ollama reference:      ornith-1.5:35b
Ollama model ID:       9f3b89b25219
Reported size:         22 GB
Runtime loaded size:   23 GB
Architecture:          qwen35moe
Parameters:            35.5B
Quantization:          Q4_K_M
Advertised context:    262144
Validated run context: 32768
Embedding length:      2048
Capabilities:          tools, thinking, completion, vision
Import method:         native Ollama pull
```

Artifact identities:

```text
Model blob SHA-256:
aaeb640f98a892980ef54876024293cc8d6987a86523aa1b947ffa9274ef800a

Vision projector SHA-256:
d9ce31026d1cb1f3f8d5152e2e2a014d9d2b302b6c93a7dc07bb0a0487f52837
```

Pull transcript included:

```text
verifying sha256 digest
writing manifest
success
```

**ORNITH INSTALL / PROVENANCE GATE: PASS**

## 8. Functional Validation

### CLI inference

Known-answer prompt produced:

```text
HX-5 ORNITH PASS
```

**CLI inference: PASS**

### HTTP API inference

Local API:

```text
http://127.0.0.1:11434/api/generate
HX-5 ORNITH API PASS
```

LAN API:

```text
http://192.168.50.205:11434/api/generate
HX-5 ORNITH LAN PASS
```

**Local HTTP API inference: PASS**  
**LAN HTTP API inference: PASS**

### GPU placement

`ollama ps`:

```text
ornith-1.5:35b  9f3b89b25219  23 GB  17%/83% CPU/GPU  32768
```

During inference:

```text
RTX 5060     ~4.7 GB VRAM in use
RTX 5060 Ti  ~15.0 GB VRAM in use
llama-server active on both GPUs
```

This confirms the mixed-GPU workload is functioning as accepted. CPU offload is expected because the loaded model plus runtime overhead exceeds the available approximately 24 GB VRAM.

**GPU-placement gate: PASS**

### Reboot persistence

After reboot:

```text
hostname: hx-5
ollama.service: enabled / active
listener: *:11434
/srv/ollama: mounted by correct UUID
ornith-1.5:35b: present, same model ID 9f3b89b25219
post-reboot known-answer: HX-5 ORNITH REBOOT PASS
post-reboot placement: 17% CPU / 83% GPU
both GPUs active
```

**OLLAMA + ORNITH REBOOT PERSISTENCE: PASS**

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
| SSH reboot persistence | PASS |
| D-018 UFW disabled/stopped | PASS |
| Domain join / SSSD core function | PASS |
| Machine trust | PASS |
| Samba DNS / FQDN / SPNs | PASS |
| SSSD socket cleanliness | DEFERRED / HX4-F02 |
| GPU driver and visibility | PASS |
| Dedicated storage | PASS |
| Base OS maintenance | PASS |
| Final post-reboot proof | PASS |

**HX-5 LAYER 0/1 STATUS: PASS / CLOSED**

## 10. Workload Progress and Remaining HX-5 Work

| Workload gate | Result |
|---|---|
| Layer 0/1 foundation | PASS / CLOSED |
| Ollama runtime / Block 3 | PASS |
| `ornith-1.5:35b` install / provenance | PASS |
| Ornith CLI inference | PASS |
| Ornith localhost HTTP API | PASS |
| Ornith LAN HTTP API | PASS |
| Workload GPU placement | PASS |
| Ollama + Ornith reboot persistence | PASS |
| CentCom smoke-runner bootstrap | **PENDING / NEXT** |
| `hx-smoke-doctor` | **PENDING** |
| `hx-smoke-doctor --remote` | **PENDING** |
| CentCom client-version capture | **PENDING** |
| CentCom smoke-runner capability | **NOT YET ACTIVE** |
| DeepSeek Harness | FUTURE SCHEDULED WORK; not a prerequisite for current runner activation |

Current closeout boundary:

```text
FOUNDATION + ORNITH BASE PASS = CLOSED
CENTCOM SMOKE-RUNNER          = NEXT
HX-5 SERVER                   = IN PROGRESS until runner activation evidence is accepted
```

After the CentCom runner current closeout, the owner-approved next housekeeping activity is a read-only reconciled Layer 0/1 audit of HX-2, HX-3, and HX-4 against the stronger standard proven on HX-5.

## 11. Evidence References

```text
docs/00-control/HX-BASE-BLOCKS-1-2-CONFIGURATION-AUDIT.md
docs/05-evidence/hx-5/layer0-1/2026-09-15-closure.md
docs/05-evidence/hx-5/ornith/2026-09-15-ornith-35b-pull-and-provenance.md
docs/05-evidence/hx-5/ornith/2026-09-15-ornith-35b-inference-and-gpu-placement.md
docs/05-evidence/hx-5/ornith/2026-09-15-ornith-35b-api-validation.md
```

The runtime evidence from the final reboot is incorporated into this as-built record and should be retained in a dedicated reboot-persistence evidence artifact during the documentation finalization pass.
