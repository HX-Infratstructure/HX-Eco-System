# HX-2 — Qwen-X Server Configuration

**Server:** HX-2  
**Role:** Qwen-X / Ollama inference server  
**Build state:** PASS
**Build method:** KISS — build, verify, record, move on  
**Rebuild date:** 2026-09-08

---

## Foundation

Established by `docs/03-runbooks/common/00-foundation.sh`, gated by
`01-base-admin-network-updates.sh`, and proven from the operator workstation
rather than from inside a session this host had already authenticated.

| Control | Evidence | State |
|---|---|---|
| `hostname -f` | `hx-2.hx.local.arpa` | PASS |
| AD DNS A record | `192.168.50.202` on HX-1 | PASS |
| Time authority | `chronyc sources` shows `^* 192.168.50.200`; tracking reference `C0A832C8 (192.168.50.200)` | PASS |
| Fleet key | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk` in `/home/hxsa/.ssh/authorized_keys` | PASS |
| NOPASSWD sudo | `sudo -k -n true` succeeds, so a cached credential is not what proves it | PASS |
| SSH persistence | `ssh.socket` enabled; `ssh.service` disabled, which is correct on Ubuntu | PASS |
| External key-only login | `tools/hx-doc/hx-fleet-access hx-2` returns `hx-2` and `KEY+SUDO-PASS` | PASS |
| SSH host key | ed25519 `SHA256:mHQ3VD3YIDTmyXEHvpFLXPe+X6viQGCQYxVbHMVgHg0`<br>rsa `SHA256:FF3mCoVVk8sxy5yDyy47EcErROrNWONvNB9ZxDEfHWw` | PASS |
| SPNs in AD | `host/HX-2`, `host/hx-2.hx.local.arpa`, `RestrictedKrbHost/HX-2`, `RestrictedKrbHost/hx-2.hx.local.arpa`; `dNSHostName` is `hx-2.hx.local.arpa` | PASS |

The SSH host key is recorded because a changed one is otherwise unanswerable.
When HX-2 and HX-3 presented new host keys, nothing in this repository could
distinguish a legitimate rebuild from anything else, and resolving it needed a
trip to each console. Read from the host itself over an already-trusted
session, and cross-checked against the operator's `known_hosts`.

Verified 2026-09-16 after the reboot at `2026-09-16 14:30:31`, so this is post-reboot state
rather than a live configuration that has never survived one.

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
NVIDIA Driver: 595.91.07
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
| Ollama version | `0.34.0` |
| Service | `ollama.service` |
| Service state | active |
| Startup state | enabled |
| API port | `11434` |
| Network listener | all interfaces (`*:11434`) |
| LAN API | `http://192.168.50.202:11434` |

Verified API response:

```json
{"version":"0.34.0"}
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
HX alias:          qwen-x:qwen3.8-27b-q6_k
Upstream identity: Qwen3.8-27B (Q6_K quantisation)
Source URI:        UNRESOLVED — see provenance gap below
Artifact:          Qwen3.8-27B-Q6_K.gguf
Artifact SHA-256:  7d590099e0a0fe7b8df812045faa2ae12bf4dbf3492b8eb7c7c7ab24c94d36ed
Serving blob:      sha256-93f6e22ec01fcb87db640ca6c97a2f6a66e4c978a9259945183da1e73203ad39
Import method:     local GGUF import via Modelfile
```

> **Two hashes, two different objects.** `Artifact SHA-256` is the GGUF that
> was downloaded. `Serving blob` is what Ollama serves, and they differ because
> `ollama create` converts the source rather than copying it - the creation log
> below reads `parsing GGUF / verifying conversion / writing manifest`. Both are
> correct; neither substitutes for the other. Only the first was recorded until
> 2026-09-16, so the record could not be used to verify what this host serves.
> Confirmed against `ollama show --modelfile` on that date.

> **Provenance gap — backfill required.** The exact Hugging Face repository
> that supplied this blob was not recorded at build time. The hash above
> identifies the artifact but not its origin, and public `Qwen3.8-27B` GGUF
> repositories include community rebuilds alongside the official weights, so
> the hash alone does not establish that these are unmodified upstream weights.
> Recover the source repository from the HX-2 shell history or the browser/CLI
> download record and replace `UNRESOLVED`. Until then, treat the model
> identity as recorded-but-unverified. Required by
> `docs/02-server-records/_TEMPLATE.md` section 6.

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

No `TEMPLATE`, `PARAMETER`, or stop-token directives were set. The chat
template therefore comes from the GGUF metadata. Record the resolved template
here if chat behaviour is ever investigated.

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
{"version":"0.34.0"}
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
| Ollama 0.34.0 | PASS |
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
