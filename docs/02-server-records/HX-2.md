# HX-2 — Qwen-X Server Configuration

**Server:** HX-2  
**Role:** Qwen-X / Ollama inference server  
**Build state:** PASS  
**Build method:** KISS — build, verify, record, move on  
**Rebuild date:** 2026-09-08

---

## 1. Identity and Network

| Item | Configuration |
|---|---|
| Hostname | `hx-2` |
| Intended FQDN | `hx-2.hx.local.arpa` |
| IPv4 | `192.168.50.202/24` |
| Default gateway | `192.168.50.1` |
| DNS | `192.168.50.200` — HX-1 |
| Domain | `hx.local.arpa` |
| AD realm | `HX.LOCAL.ARPA` |
| Domain client | SSSD / realmd / adcli |
| SSH | Active, port `22` |

### Domain validation

Verified:

```text
realm: hx.local.arpa
configured: kerberos-member
server-software: active-directory
client-software: sssd
login-policy: allow-realm-logins
SSSD: active
```

Domain user resolution was tested successfully:

```text
jarvisr@hx.local.arpa
primary group: domain users@hx.local.arpa
```

**Domain join gate: PASS**

---

## 2. Operating System

| Item | Configuration |
|---|---|
| OS | Ubuntu 24.04.4 LTS |
| Kernel after rebuild | Linux 7.0.0-31-generic |
| Architecture | x86-64 |
| Hardware vendor | Micro-Star International Co., Ltd. |
| Hardware model | MS-7E34 |
| Firmware version | 1.A80 |
| Firmware date | 2025-01-07 |
| Linux admin | `hxsa` |
| sudo policy | `hxsa` has NOPASSWD sudo via `/etc/sudoers.d/90-hx-admin` |

Base OS was updated with:

```bash
sudo apt update
sudo apt upgrade -y
```

and rebooted before the NVIDIA driver installation.

---

## 3. GPU Configuration

Installed driver:

```text
NVIDIA Driver: 595.71.05
CUDA reported by nvidia-smi: 13.2
```

Detected GPU capacity:

```text
GPU 0: NVIDIA GeForce RTX 4070-class — 16,376 MiB
GPU 1: NVIDIA GeForce RTX 4070-class — 16,376 MiB
Total installed VRAM: approximately 32 GB
```

Both GPUs were visible and healthy after reboot.

**GPU gate: PASS**

---

## 4. Storage Layout

### NVMe — WD_BLACK SN850X 4000GB

```text
nvme0n1      3.6T
├─nvme0n1p1    1G  vfat  /boot/efi
├─nvme0n1p2  120G  ext4  /
└─nvme0n1p3  3.5T  ext4  /srv/ollama
```

Filesystem state at build:

```text
/             ~118 GB total
/srv/ollama   ~3.5 TB total, ~3.3 TB available
```

### SATA — Seagate ST8000DM004

```text
sda           7.3T
└─sda1        7.3T ext4
```

`/dev/sda1` is intentionally **not mounted** and was not altered during the HX-2 rebuild.

### Ollama model storage

Dedicated model path:

```text
/srv/ollama/models
```

Ownership:

```text
ollama:ollama /srv/ollama
ollama:ollama /srv/ollama/models
```

This keeps large model blobs off the 120 GB root filesystem.

**Storage gate: PASS**

---

## 5. Ollama Runtime

| Item | Configuration |
|---|---|
| Ollama version | `0.33.3` |
| Service | `ollama.service` |
| Service state | active |
| Startup state | enabled |
| API port | `11434` |
| Network listener | all interfaces (`*:11434`) |
| LAN API | `http://192.168.50.202:11434` |

Verified API response:

```json
{"version":"0.33.3"}
```

### systemd override

File:

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

The current `OLLAMA_NO_CLOUD=1` setting is **operationally temporary**, not a permanent HX architecture decision. HX-2 is intentionally running local-only while the base ecosystem is rebuilt.

### Future Ollama Cloud enablement

When cloud capability is intentionally enabled later:

1. Remove:
   ```ini
   Environment="OLLAMA_NO_CLOUD=1"
   ```
2. Preserve:
   ```ini
   Environment="OLLAMA_MODELS=/srv/ollama/models"
   Environment="OLLAMA_HOST=0.0.0.0:11434"
   ```
3. Reload and restart:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart ollama
   ```
4. Complete any required Ollama cloud authentication at that time.
5. Re-test local inference and cloud capability separately.

Cloud enablement is **future work** and must not replace the local Qwen-X model path.

---

## 6. Qwen-X Model

### Installed model

```text
Ollama name: qwen-x:qwen3.8-27b-q6_k
Model family: Qwen3.8
Parameter class: 27B
Quantization: Q6_K
Ollama model size: 23 GB
Ollama model ID: d319d311ac30
```

Source GGUF blob:

```text
Qwen3.8-27B-Q6_K.gguf
SHA-256:
7d590099e0a0fe7b8df812045faa2ae12bf4dbf3492b8eb7c7c7ab24c94d36ed
```

Stored under the dedicated Ollama model filesystem.

### Import method

The direct Hugging Face Ollama shortcut downloaded the GGUF blob but failed to complete the Ollama model manifest. The downloaded Q6_K blob was preserved and imported locally instead of being downloaded again.

Modelfile:

```text
/srv/ollama/Qwen-X.Modelfile
```

Content:

```text
FROM /srv/ollama/models/blobs/sha256-7d590099e0a0fe7b8df812045faa2ae12bf4dbf3492b8eb7c7c7ab24c94d36ed
```

Creation command:

```bash
ollama create qwen-x:qwen3.8-27b-q6_k -f /srv/ollama/Qwen-X.Modelfile
```

Result:

```text
parsing GGUF
verifying conversion
writing manifest
success
```

---

## 7. Functional Validation

### CLI inference

Command:

```bash
ollama run qwen-x:qwen3.8-27b-q6_k "Reply with exactly: HX-2 QWEN-X PASS"
```

Validated response:

```text
HX-2 QWEN-X PASS
```

**CLI inference: PASS**

### HTTP API inference

Model:

```text
qwen-x:qwen3.8-27b-q6_k
```

Validated generated response contained:

```text
HX-2 API PASS
```

**HTTP inference: PASS**

### LAN API

Validated:

```text
http://192.168.50.202:11434/api/version
```

Response:

```json
{"version":"0.33.3"}
```

**LAN API: PASS**

### Reboot persistence

After reboot:

```text
ollama.service: active
qwen-x:qwen3.8-27b-q6_k: present
LAN API: responding
```

**Reboot persistence: PASS**

---

## 8. Final HX-2 State

| Gate | Result |
|---|---|
| Clean Ubuntu rebuild | PASS |
| Base OS update/upgrade | PASS |
| Samba domain join | PASS |
| SSSD | PASS |
| Domain user resolution | PASS |
| NVIDIA 595 driver | PASS |
| Dual GPU visibility | PASS |
| Dedicated Ollama storage | PASS |
| Ollama 0.33.3 | PASS |
| Ollama service active/enabled | PASS |
| Qwen3.8-27B Q6_K | PASS |
| CLI inference | PASS |
| HTTP API inference | PASS |
| LAN API exposure | PASS |
| Reboot persistence | PASS |

# HX-2 FINAL STATUS: PASS

HX-2 is complete for the current clean-build scope.

The server is ready to provide local Qwen-X inference through:

```text
http://192.168.50.202:11434
```

using:

```text
qwen-x:qwen3.8-27b-q6_k
```

Future ecosystem integration, including OmniRoute and Ollama Cloud capability, will be performed as later explicit integration tasks.
