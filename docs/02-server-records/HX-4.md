# HX-4 — Meta-X / GPT-OSS 20B + BGE-M3 + Nomic + BGE reranker Server Configuration

**Build state:** PASS
**Gate:** CLOSED
**IP:** `192.168.50.204`
**FQDN:** `hx-4.hx.local.arpa`
**Record updated:** 2026-09-15

## Foundation

Established by `docs/03-runbooks/common/00-foundation.sh`, gated by
`01-base-admin-network-updates.sh`, and proven from the operator workstation
rather than from inside a session this host had already authenticated.

| Control | Evidence | State |
|---|---|---|
| `hostname -f` | `hx-4.hx.local.arpa` | PASS |
| AD DNS A record | `192.168.50.204` on HX-1 | PASS |
| Time authority | `chronyc sources` shows `^* 192.168.50.200`; tracking reference `C0A832C8 (192.168.50.200)` | PASS |
| Fleet key | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk` in `/home/hxsa/.ssh/authorized_keys` | PASS |
| NOPASSWD sudo | `sudo -k -n true` succeeds, so a cached credential is not what proves it | PASS |
| SSH persistence | `ssh.socket` enabled; `ssh.service` disabled, which is correct on Ubuntu | PASS |
| External key-only login | `tools/hx-doc/hx-fleet-access hx-4` returns `hx-4` and `KEY+SUDO-PASS` | PASS |
| SSH host key | ed25519 `SHA256:IeymFmMJLaA+LvfRbvvZqAEXyQrwPSEfD4LU1ym6kFI`<br>rsa `SHA256:tJxGGf+ETnxFv/PEDHzRMac9e9louPY6T45PCZcDBxQ` | PASS |
| SPNs in AD | `host/HX-4`, `RestrictedKrbHost/HX-4` present; `host/hx-4.hx.local.arpa` and `RestrictedKrbHost/hx-4.hx.local.arpa` **absent**; `dNSHostName` is `hx-4`, not the FQDN | GAP, see HX5-F12 |

The SSH host key is recorded because a changed one is otherwise unanswerable.
When HX-2 and HX-3 presented new host keys, nothing in this repository could
distinguish a legitimate rebuild from anything else, and resolving it needed a
trip to each console. Read from the host itself over an already-trusted
session, and cross-checked against the operator's `known_hosts`.

Verified 2026-09-16 after the reboot at `2026-09-16 14:32:14`, so this is post-reboot state
rather than a live configuration that has never survived one.

## 1. Identity and Network

| Item | Value |
|---|---|
| Hostname | `hx-4` |
| FQDN | `hx-4.hx.local.arpa` |
| Interface | `eno1` |
| IPv4 | `192.168.50.204/24` |
| Default route | `default via 192.168.50.1 dev eno1 proto static` |
| DNS | `192.168.50.200` (HX-1) |
| Domain | `hx.local.arpa`, `configured: kerberos-member`, server software `active-directory` |
| SSSD | `active` |
| Domain user resolution | `id jarvisr@hx.local.arpa` -> `uid=218001148(jarvisr@hx.local.arpa) gid=218000513(domain users@hx.local.arpa)` |

**Domain join gate: PASS**

Three `sssd` socket units are failed on this host: `sssd-nss.socket`,
`sssd-pam-priv.socket`, `sssd-pam.socket`. `/etc/sssd/sssd.conf` names `nss` and
`pam` in its `services` line, so `sssd.service` starts those responders while
their socket units also attempt activation. Name resolution is unaffected and
`getent passwd jarvisr@hx.local.arpa` returns the expected identity. Tracked as
HX4-F02, deferred; the responder model is a fleet-wide decision.

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | Ubuntu 24.04.5 LTS |
| Kernel | `7.0.0-31-generic` |
| Firmware version | Gigabyte X99-UD5 WIFI-CF, F22 |
| sudo policy | `/etc/sudoers.d/90-hx-admin`: `hxsa ALL=(ALL:ALL) NOPASSWD: ALL` |

## 3. GPU Configuration

| Item | Value |
|---|---|
| Driver package | `nvidia-driver-595-server-open` |
| Exact version | `595.71.05-0ubuntu0.24.04.1` |
| Reported driver | `595.71.05` |
| GPUs | 2 x NVIDIA GeForce RTX 5060 Ti, 16311 MiB each |

```text
0, NVIDIA GeForce RTX 5060 Ti, 16311 MiB, 595.71.05
1, NVIDIA GeForce RTX 5060 Ti, 16311 MiB, 595.71.05
```

**GPU gate: PASS**

## 4. Storage Layout

| Device | Size | FS | Mount |
|---|---|---|---|
| `nvme0n1p1` | 1G | vfat | `/boot/efi` |
| `nvme0n1p2` | 120G | ext4 | `/` |
| `nvme0n1p3` | 3.5T | ext4 | `/srv/ollama` |

`/srv/ollama` was pre-existing, mounted and empty apart from `lost+found` before
block 3 ran. No disk was partitioned, formatted or mounted during this build.

Dedicated application path: `/srv/ollama/models`, owned `ollama:ollama`.

**Storage gate: PASS**

## 5. Runtime

### Ollama

| Item | Value |
|---|---|
| Package source | Upstream release archive `ollama-linux-amd64.tar.zst`, verified against the pinned SHA-256 before extraction. Not Snap, not the Ubuntu archive. |
| Exact installed version | `0.34.0` |
| Archive SHA-256 pin | `cf95886728959aa09910bb34de5cca1cc5a8f68003b5597197d3f2c2d57c0804` |
| Service unit | `/etc/systemd/system/ollama.service` |
| Drop-in | `/etc/systemd/system/ollama.service.d/storage.conf` |
| Listener | `0.0.0.0:11434` |

```text
OLLAMA_MODELS=/srv/ollama/models
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_NO_CLOUD=1
```

`systemctl is-active ollama` -> `active`; `systemctl is-enabled ollama` -> `enabled`.

### Reranker runtime

| Item | Value |
|---|---|
| Package source | PyPI, into `/srv/reranker/venv`. Not Snap, not the Ubuntu archive. |
| Runtime | `infinity-emb` |
| Exact installed version | `0.0.77` |
| Service unit | `/etc/systemd/system/hx-reranker.service` |
| Listener | `0.0.0.0:7997` |
| Dependency pins | `click<8.2`; `INFINITY_BETTERTRANSFORMER=false` |

`systemctl is-active hx-reranker` -> `active`; `systemctl is-enabled hx-reranker` -> `enabled`.

The two dependency pins are required, not optional. `infinity-emb` pins its own
version and nothing it depends on. Without them the service crashes at startup
and systemd restarts it in a loop. Recorded as HX4-F06 and HX4-F07 and fixed in
`docs/03-runbooks/common/04-reranker.sh`.

## 6. Model / Application Provenance

Required for every server that hosts a model or a downloaded artifact. All
five fields are mandatory — an unknown value is recorded as `UNRESOLVED`, never
omitted, because a missing field cannot be told apart from a forgotten one.

### Meta-X generation model

```text
HX alias:              meta-x:gpt-oss-20b
Upstream identity:     gpt-oss:20b
Source URI:            gpt-oss:20b
Ollama model ID:       17052f91a42e
Artifact SHA-256:      e7b273f9636059a689e3ddcab3716e4f65abe0143ac978e46673ad0e52d09efb
Import method:         ollama pull, then `ollama cp` to the HX alias
Blob path:             /srv/ollama/models/blobs/sha256-e7b273f9636059a689e3ddcab3716e4f65abe0143ac978e46673ad0e52d09efb
```

### Primary embedding model

```text
HX alias:              hx-embed-primary:bge-m3
Upstream identity:     BAAI/bge-m3
Source URI:            bge-m3:567m
Ollama model ID:       790764642607
Artifact SHA-256:      daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c
Import method:         ollama pull, then `ollama cp` to the HX alias
Blob path:             /srv/ollama/models/blobs/sha256-daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c
Native dimension:      1024
```

The tag is the reviewed source reference, not the artifact. At install time
`bge-m3:latest`, `bge-m3:567m` and `bge-m3:567m-fp16` all resolved to registry
manifest `7907646426070047...`, pushed 2024-08-07, and the Ollama registry does
not serve manifests by digest. The artifact identity of record is therefore the
blob SHA-256 above, captured on this host. This record is not re-baselined
against a later artifact published under the same tag.

### Alternate embedding model

```text
HX alias:              hx-embed-alt:nomic-v1.5
Upstream identity:     nomic-ai/nomic-embed-text-v1.5
Source URI:            nomic-embed-text:v1.5
Ollama model ID:       0a109f422b47
Artifact SHA-256:      970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6
Import method:         ollama pull, then `ollama cp` to the HX alias
Blob path:             /srv/ollama/models/blobs/sha256-970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6
Native dimension:      768
```

D-005: one embedding identity per collection. BGE-M3 at 1024 and Nomic at 768
are not mixed, and Nomic is not forced to 1024 to match.

### Reranker

```text
HX alias:              hx-reranker
Upstream identity:     BAAI/bge-reranker-v2-m3
Source URI:            BAAI/bge-reranker-v2-m3 @ 953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e
Artifact SHA-256:      UNRESOLVED
Import method:         infinity-emb 0.0.77 from PyPI, model fetched by the runtime at first start under HF_HOME=/srv/reranker/hf
Serving runtime:       infinity-emb 0.0.77, systemd unit hx-reranker, port 7997
```

`Artifact SHA-256` is `UNRESOLVED` and is not omitted. The checkpoint is pinned
to an immutable commit revision, which fixes the upstream content, but the
runtime fetches the checkpoint itself and the build captured no per-file hash
for it. Close this field while the host is reachable.

No model was imported by GGUF or built from source, so no Modelfile or build
definition applies. No template, parameter or stop-token settings were set on
any alias; `ollama cp` copied each pulled model unchanged.

## 7. Functional Validation

Evidence model 2 applies: run bundles, not inline proof. See section 9.

### A1 — Ollama inference

```text
$ OLLAMA_URL=http://192.168.50.204:11434 OLLAMA_MODEL=meta-x:gpt-oss-20b python3 ollama_inference_smoke.py
OLLAMA_SMOKE_PASS model=meta-x:gpt-oss-20b token=HX-OLLAMA-SMOKE-9271
```

HTTP 200, `done=true`, exact known-answer token returned. Resource observation
at completion: GPU0 12% / 9423 MiB, GPU1 58% / 9613 MiB; memory 5.6Gi of 62Gi used.

### A2 — Embedding plane

```text
EMBEDDING_SMOKE_PASS model=BAAI/bge-m3 dim=1024 cosine=1.000000
EMBEDDING_SMOKE_PASS model=nomic-ai/nomic-embed-text-v1.5 dim=768 cosine=1.000000
```

Both models returned numeric non-zero vectors at their approved dimensions.
Repeated identical input exceeded the 0.999 cosine minimum.

### A3 — Reranker

```text
run1 top=B scores={'B': 0.021615, 'A': 1.7e-05, 'C': 1.6e-05}
run2 top=B scores={'B': 0.021615, 'A': 1.7e-05, 'C': 1.6e-05}
RERANKER_SMOKE_PASS checkpoint=BAAI/bge-reranker-v2-m3@953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e run1_top=B run2_top=B
```

Passage B ranked first on both identical requests.

### LAN proof

```text
$ curl -fsS http://192.168.50.204:11434/api/version
{"version":"0.34.0"}

$ curl -fsS http://192.168.50.204:7997/health
{"unix":1789451046.3513517}
```

### Reboot persistence

Boot time moved from `2026-09-15 03:59:50` to `2026-09-15 05:43:28`.

```text
systemctl is-active ollama hx-reranker sssd   ->  active active active
systemctl is-enabled ollama hx-reranker       ->  enabled enabled
findmnt -n /srv/ollama                        ->  /srv/ollama /dev/nvme0n1p3 ext4 rw,relatime,stripe=64
getent passwd jarvisr@hx.local.arpa           ->  jarvisr@hx.local.arpa:218001148
curl http://192.168.50.204:11434/api/version  ->  {"version":"0.34.0"}
curl http://192.168.50.204:7997/health        ->  {"unix":1789451046.3513517}
```

All six models are present after reboot with unchanged IDs. The reranker
answers on the LAN about 15 seconds after boot; it loads its checkpoint at
start, so a health check issued immediately after boot can refuse the
connection before the service is ready.

The three failed `sssd` socket units survive the reboot. See section 1 and
HX4-F02.

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | PASS |
| Domain join / SSSD | PASS |
| GPU driver and visibility | PASS |
| Dedicated storage | PASS |
| Runtime version | PASS |
| Service active / enabled | PASS |
| Model / application loaded | PASS |
| Known-answer functional proof | PASS |
| Reboot persistence | PASS |

## 9. Evidence References

Retained run bundles, evidence model 2:

- A1 — `docs/05-evidence/hx-4/ollama-inference/20260915T054105Z_hx-4_ollama-inference`
- A2 — `docs/05-evidence/hx-4/embedding-models/20260915T054147Z_hx-4_embedding-models`
- A3 — `docs/05-evidence/hx-4/reranker/20260915T054239Z_hx-4_reranker`

CentCom does not exist yet, so roadmap steps A1-A3 were run before its
activation. HX-4 was authorised as the station for its own runs, and each
manifest records `runner_host: hx-4`. The operator workstation could not be
used: it is Windows, and the runner requires `hostname -s`, which Git Bash does
not provide. Tracked as HX4-F08.

Because runner and system under test are the same host for these three runs,
the LAN calls were issued from HX-4 to its own address. This is weaker than a
remote call from a separate station and is recorded as such rather than
presented as a remote proof.
