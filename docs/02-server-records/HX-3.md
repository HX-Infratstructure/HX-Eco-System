# HX-3 — Coder-X Server Configuration

**Server:** HX-3  
**Role:** Coder-X / Ollama inference server  
**Build state:** PASS
**Rebuild date:** 2026-09-08  
**Build method:** KISS — build, verify, record, move on  
**Deployment standard:** Native Ubuntu Linux + systemd; no containers

---

## Foundation

Established by `docs/03-runbooks/common/00-foundation.sh`, gated by
`01-base-admin-network-updates.sh`, and proven from the operator workstation
rather than from inside a session this host had already authenticated.

| Control | Evidence | State |
|---|---|---|
| `hostname -f` | `hx-3.hx.local.arpa` | PASS |
| AD DNS A record | `192.168.50.203` on HX-1 | PASS |
| Time authority | `chronyc sources` shows `^* 192.168.50.200`; tracking reference `C0A832C8 (192.168.50.200)` | PASS |
| Fleet key | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk` in `/home/hxsa/.ssh/authorized_keys` | PASS |
| NOPASSWD sudo | `sudo -k -n true` succeeds, so a cached credential is not what proves it | PASS |
| SSH persistence | `ssh.socket` enabled; `ssh.service` disabled, which is correct on Ubuntu | PASS |
| External key-only login | `tools/hx-doc/hx-fleet-access hx-3` returns `hx-3` and `KEY+SUDO-PASS` | PASS |
| SSH host key | ed25519 `SHA256:gL4sPYzEbDjRjVSoa+Qt50/zMtEsO640f5l+o6PWpBI`<br>rsa `SHA256:G5o9yOkS+ZXUS27dk59Lt7t7UZzIaG+eiApG1kNiKN0` | PASS |

The SSH host key is recorded because a changed one is otherwise unanswerable.
When HX-2 and HX-3 presented new host keys, nothing in this repository could
distinguish a legitimate rebuild from anything else, and resolving it needed a
trip to each console. Read from the host itself over an already-trusted
session, and cross-checked against the operator's `known_hosts`.

Verified 2026-09-16 after the reboot at `2026-09-16 14:30:56`, so this is post-reboot state
rather than a live configuration that has never survived one.

<!-- Service principal names are deliberately absent. D-029 has not decided
     whether short-form principals are sufficient or FQDN SPNs must exist in
     AD, and the 2026-09-16 audit established neither. Do not add an SPN row
     until it is decided. -->

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
| Ollama version | `0.34.0` |
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

LAN API version validation returned Ollama `0.34.0` before final reboot. Ollama also confirmed:

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

### Primary model — Coder-X-GLM-Flash

Installed model:

```text
HX alias: Coder-X-GLM-Flash
Base model: GLM-4.7-Flash
Quantization: Q5_K_M
```

Provenance (all five fields per `docs/02-server-records/_TEMPLATE.md` section 6):

```text
HX alias:           Coder-X-GLM-Flash
Upstream identity:  zai-org/GLM-4.7-Flash (Q5_K_M quantisation)
Source URI:         hf.co/bartowski/zai-org_GLM-4.7-Flash-GGUF:Q5_K_M
Artifact SHA-256:   9e0156957bd07760644aa2a3b6d6791ac8796f2c1bc9c75a2cb07cef5ccb5764
Import method:      ollama pull of the GGUF, tagged coder-x-glm:glm47flash-q5km,
                    then GGUF import via Modelfile
```

**Artifact provenance.** The artifact is a community GGUF requant produced by
`bartowski` of zai-org's GLM-4.7-Flash. It is not weights published by
zai-org. Both facts are recorded separately because public model registries
carry community rebuilds under names close to the official ones: the Source
URI names where the blob came from, and the SHA-256 names exactly what is
running. Neither field alone establishes provenance.

Authored Modelfile (`~/Modelfile.coder-x-glm64k`):

```text
FROM coder-x-glm:glm47flash-q5km
PARSER glm-4.7
RENDERER glm-4.7
PARAMETER temperature 1
PARAMETER top_p 0.95
PARAMETER min_p 0.01
PARAMETER repeat_penalty 1
PARAMETER num_ctx 65536
```

What Ollama resolved after
`ollama create Coder-X-GLM-Flash -f ~/Modelfile.coder-x-glm64k`:

```text
FROM /srv/ollama/models/blobs/sha256-9e0156957bd07760644aa2a3b6d6791ac8796f2c1bc9c75a2cb07cef5ccb5764
TEMPLATE "[gMASK]<sop>{{ if .System }}<|system|>
{{ .System }}{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}{{ end }}<|assistant|>
{{ .Response }}"
RENDERER glm-4.7
PARSER glm-4.7
PARAMETER repeat_penalty 1
PARAMETER stop <|user|>
PARAMETER temperature 1
PARAMETER top_p 0.95
PARAMETER min_p 0.01
PARAMETER num_ctx 65536
```

The `stop` token `<|user|>` and the `TEMPLATE` block were **inherited from the
GGUF metadata**, not authored — the authored Modelfile above sets neither.
(HX-2's record makes the equivalent statement about having set no template or
parameter directives; both servers rely on GGUF metadata, but HX-3's import
shows exactly what was inherited.)

Context is recorded as two distinct facts:

```text
Default context:              65,536 (num_ctx in the Modelfile)
Extended validated context:   131,072, at 98% GPU / 2% CPU placement
```

131,072 is **validated, not the default**. The default remains 65,536.

### Retained rollback model — coder-x:qwen3-coder-30b-q6_k

The previous primary model is retained as the rollback path and is still
installed on disk.

```text
HX alias:           coder-x:qwen3-coder-30b-q6_k
Upstream identity:  Qwen3-Coder-30B-A3B-Instruct (Q6_K quantisation)
Source URI:         hf.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q6_K
Artifact SHA-256:   72a9b20a19c70db56e1ccd01fb35b0f0842d67d28e7c3bdff762df860120b769
Import method:      ollama pull, then `ollama cp` to the HX alias
```

> **Provenance gap — CLOSED on 2026-09-15.** The full artifact hash was
> recovered on HX-3 via `ollama show --modelfile coder-x:qwen3-coder-30b-q6_k`
> and recorded above. It matches the 12-character layer prefix `72a9b20a19c7`
> from the original pull transcript, confirming the blob on disk is the pulled
> artifact.
>
> Note: `lmstudio-community` is a third-party requantiser, not the Qwen
> project. That is an accepted choice, recorded here so it is a decision rather
> than an assumption. This is the precedent mirrored by the primary model's
> bartowski provenance statement above.

The model download for the retained rollback model completed successfully:

```text
pulling 72a9b20a19c7: 100%
verifying sha256 digest
writing manifest
success
```

CLI inference validation for the rollback model:

```text
HX-3 CODER-X PASS
```

The permanent HX alias was created with `ollama cp`. Both names initially referenced the same Ollama model ID, proving the alias did not duplicate the 25 GB model data.

After validation, the long Hugging Face manifest name was removed. The retained operational name is:

```text
coder-x:qwen3-coder-30b-q6_k
```

**Rollback model CLI inference: PASS**

## 8. API and Reboot Validation

The Ollama LAN API was validated at:

```text
http://192.168.50.203:11434
```

The final API generation test was reported successful by the owner during closeout. The exact generation response payload was not retained in the conversation evidence, so this record does not fabricate it.

After reboot, directly observed:

```text
ollama.service: active
Coder-X-GLM-Flash: present
coder-x:qwen3-coder-30b-q6_k: present (retained rollback)
```

This proves Ollama service startup and persistence of both the primary
Coder-X-GLM-Flash model and the retained rollback model across reboot.

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
| Ollama 0.34.0 | PASS |
| Ollama active / enabled | PASS |
| LAN API | PASS |
| Coder-X-GLM-Flash primary model | PASS |
| coder-x:qwen3-coder-30b-q6_k retained rollback | PASS |
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
Coder-X-GLM-Flash (primary)
coder-x:qwen3-coder-30b-q6_k (retained rollback)
```

Future work such as Ollama Cloud enablement or investigation of the longer boot time is explicitly outside this closeout and must be treated as a separate owner-directed task.
