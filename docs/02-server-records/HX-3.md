# HX-3 — Coder-X Server Configuration

**Server:** HX-3  
**Role:** Coder-X / Ollama inference server  
**Build state:** PASS  
**Rebuild date:** 2026-09-08  
**Build method:** KISS — build, verify, record, move on  
**Deployment standard:** Native Ubuntu Linux + systemd; no containers

---

## 1. Identity and Network

| Item | As-built configuration |
|---|---|
| Hostname | `hx-3` |
| IPv4 | `192.168.50.203/24` |
| Default gateway | `192.168.50.1` |
| DNS | `192.168.50.200` — HX-1 |
| Domain | `hx.local.arpa` |
| Realm | `HX.LOCAL.ARPA` |
| Domain client | SSSD / realmd / adcli |
| SSH | Active, port `22` |

Validated network state:

```text
eno1             UP   192.168.50.203/24
default via 192.168.50.1
Current DNS Server: 192.168.50.200
```

## 2. Operating System and Base State

| Item | As-built configuration |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| Kernel | Linux 7.0.0-31-generic |
| Architecture | x86-64 |
| Hardware vendor | Gigabyte Technology Co., Ltd. |
| Hardware model | X99-UD5 WIFI-CF |
| Firmware | F22 |
| Firmware date | 2016-06-13 |
| Linux administrator | `hxsa` |

Base administration validation:

```text
NOPASSWD sudo test: 0
UFW: disabled / inactive
nftables filter policies: accept
firewalld: inactive / not installed
SSH: active
SSH port: 22
failed systemd units: 0
```

After rebuild updates and reboot, Ubuntu reported:

```text
0 updates can be applied immediately.
```

No additional network restriction or firewall hardening was introduced.

## 3. Domain Membership

Installed domain-client components include `realmd`, `sssd-ad`, `sssd-tools`, `adcli`, and `krb5-user`.

Final realm state:

```text
hx.local.arpa
  type: kerberos
  realm-name: HX.LOCAL.ARPA
  domain-name: hx.local.arpa
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  login-formats: %U@hx.local.arpa
  login-policy: allow-realm-logins
```

Validation:

```text
SSSD: active
jarvisr@hx.local.arpa: resolves successfully
gid: domain users@hx.local.arpa
```

**Domain gate: PASS**

Operational note: the first `realm join` attempt returned a join failure; a subsequent join completed successfully and the final validated state above is authoritative.

## 4. GPU Configuration

Installed NVIDIA stack:

```text
NVIDIA-SMI: 595.71.05
Driver Version: 595.71.05
CUDA Version reported by nvidia-smi: 13.2
```

Detected GPUs:

```text
GPU 0: NVIDIA GeForce RTX 5060 Ti — 16,311 MiB
GPU 1: NVIDIA GeForce RTX 5060 Ti — 16,311 MiB
```

Total installed VRAM is approximately 32 GB. Post-reboot validation showed both GPUs available with no active compute processes.

**GPU gate: PASS**

## 5. Storage Layout

### Primary NVMe

```text
nvme0n1       3.6T  WD_BLACK SN7100 4TB
├─nvme0n1p1     1G  vfat  /boot/efi
├─nvme0n1p2   120G  ext4  /
└─nvme0n1p3   3.5T  ext4  /srv/ollama
```

Filesystem usage observed during rebuild:

```text
/             ~118 GB total, ~101 GB available
/srv/ollama   ~3.5 TB total, ~3.3 TB available
```

### Secondary SATA disk

```text
sda          596.2G  WDC WD6400AAKS-6
└─sda1       596.2G  ext4
```

`/dev/sda1` is intentionally **unmounted and untouched**. It was not required for the HX-3 rebuild.

### Ollama model store

Authoritative model storage:

```text
/srv/ollama/models
```

The dedicated 3.5 TB NVMe partition is used for Ollama rather than the 120 GB root filesystem.

**Storage gate: PASS**

## 6. Ollama Runtime

| Item | As-built configuration |
|---|---|
| Ollama version | `0.33.3` |
| Service | `ollama.service` |
| Service state | active |
| Startup state | enabled |
| API port | `11434` |
| LAN endpoint | `http://192.168.50.203:11434` |
| Model storage | `/srv/ollama/models` |
| Cloud state | disabled for current base build |

Systemd override:

```text
/etc/systemd/system/ollama.service.d/storage.conf
```

Current configuration:

```ini
[Service]
Environment="OLLAMA_MODELS=/srv/ollama/models"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NO_CLOUD=1"
```

Validated environment:

```text
OLLAMA_MODELS=/srv/ollama/models
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_NO_CLOUD=1
```

LAN API version validation returned Ollama `0.33.3` before final reboot. Ollama also confirmed:

```text
ollama cloud is disabled: web search is unavailable
```

### Future cloud enablement

`OLLAMA_NO_CLOUD=1` is a **current operational setting**, not a permanent architecture restriction. HX-3 is expected to gain cloud capability later when that integration is intentionally enabled.

At that time:

1. Remove `Environment="OLLAMA_NO_CLOUD=1"` from the override.
2. Preserve the dedicated model path and LAN listener.
3. Reload systemd and restart Ollama.
4. Complete any required Ollama cloud authentication.
5. Validate local Coder-X inference independently from cloud capability.

No cloud change is part of this server closeout.

## 7. Coder-X Model

Installed model:

```text
HX alias: coder-x:qwen3-coder-30b-q6_k
Base model: Qwen3-Coder-30B-A3B-Instruct
Quantization: Q6_K
Ollama model ID: efcb36ee7419
Size: 25 GB
```

Source model reference used during installation:

```text
HX alias:          coder-x:qwen3-coder-30b-q6_k
Upstream identity: Qwen3-Coder-30B-A3B-Instruct (Q6_K quantisation)
Source URI:        hf.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q6_K
Artifact SHA-256:  UNRESOLVED — see provenance gap below
Import method:     ollama pull, then `ollama cp` to the HX alias
```

> **Provenance gap — backfill required.** Only the 12-character layer prefix
> `72a9b20a19c7` from the pull transcript was recorded, not the full artifact
> hash. Recover it on HX-3 with
> `ollama show --modelfile coder-x:qwen3-coder-30b-q6_k` and the blob path
> under `/srv/ollama/models/blobs/`, then replace `UNRESOLVED`. Required by
> `docs/02-server-records/_TEMPLATE.md` section 6.
>
> Note: `lmstudio-community` is a third-party requantiser, not the Qwen
> project. That is an accepted choice, recorded here so it is a decision rather
> than an assumption.

The model download completed successfully:

```text
pulling 72a9b20a19c7: 100%
verifying sha256 digest
writing manifest
success
```

CLI inference validation:

```text
HX-3 CODER-X PASS
```

The permanent HX alias was created with `ollama cp`. Both names initially referenced the same Ollama model ID, proving the alias did not duplicate the 25 GB model data.

After validation, the long Hugging Face manifest name was removed. The retained operational name is:

```text
coder-x:qwen3-coder-30b-q6_k
```

**Coder-X CLI inference: PASS**

## 8. API and Reboot Validation

The Ollama LAN API was validated at:

```text
http://192.168.50.203:11434
```

The final API generation test was reported successful by the owner during closeout. The exact generation response payload was not retained in the conversation evidence, so this record does not fabricate it.

After reboot, directly observed:

```text
ollama.service: active
coder-x:qwen3-coder-30b-q6_k: present
model ID: efcb36ee7419
model size: 25 GB
```

This proves Ollama service startup and Coder-X model persistence across reboot.

**Reboot persistence: PASS**

## 9. Informational Observation — Boot Time

**State: INFORMATIONAL / DEFERRED — NO ACTION**

HX-3 has a noticeably longer boot time than the other HX servers.

Owner direction:

- record the observation;
- do **not** troubleshoot or remediate it as part of this rebuild;
- it is not attributed to the work completed during this build.

No causal claim is made in this record. The observation remains available for a future diagnostic task if the owner elects to investigate it.

## 10. Final Acceptance State

| Gate | Result |
|---|---|
| Ubuntu base rebuild | PASS |
| Base OS update state | PASS |
| Hostname / IP / DNS | PASS |
| Sudo / SSH baseline | PASS |
| UFW inactive / disabled | PASS |
| Domain membership | PASS |
| SSSD | PASS |
| Domain-user resolution | PASS |
| NVIDIA 595 driver | PASS |
| Dual RTX 5060 Ti detection | PASS |
| Dedicated Ollama NVMe storage | PASS |
| Ollama 0.33.3 | PASS |
| Ollama active / enabled | PASS |
| LAN API | PASS |
| Coder-X Q6_K model | PASS |
| CLI inference | PASS |
| Final API generation | PASS — owner confirmed |
| Reboot persistence | PASS |
| Boot-time observation | RECORDED — no action |

# HX-3 FINAL STATUS: PASS

HX-3 is complete for the current clean-build scope.

Operational inference endpoint:

```text
http://192.168.50.203:11434
```

Operational model:

```text
coder-x:qwen3-coder-30b-q6_k
```

Future work such as Ollama Cloud enablement or investigation of the longer boot time is explicitly outside this closeout and must be treated as a separate owner-directed task.
