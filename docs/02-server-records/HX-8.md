# HX-8 — Open WebUI Server Configuration

**Build state:** PASS
**Gate:** CLOSED
**IP:** `192.168.50.208`
**FQDN:** `hx-8.hx.local.arpa`
**Record updated:** 2026-09-17

## Foundation

Established by `docs/03-runbooks/common/00-foundation.sh` before Block 1, and
gated by `01-base-admin-network-updates.sh`, which refuses to proceed without
it. Proven from the operator workstation before Layer 0/1 closes.

Every row below carries the date, the command, and the verbatim output. Rows
run from the workstation prove the control from outside the machine that
claims it.

| Control | Date | Command | Output |
|---|---|---|---|
| `hostname -f` | 2026-09-17 | `hostname -f` | `hx-8.hx.local.arpa` |
| AD DNS A record | 2026-09-17 | `nslookup hx-8.hx.local.arpa 192.168.50.200` | `Name: hx-8.hx.local.arpa` / `Address: 192.168.50.208` |
| Time authority | 2026-09-17 | `chronyc sources` | `^* 192.168.50.200  3  6  377  13  -186us[ -171us] +/- 71ms` |
| Fleet key | 2026-09-17 | foundation block key report | `256 SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk hx-fleet-20260810 (ED25519)` |
| NOPASSWD sudo | 2026-09-17 | `sudo -k -n true` | `NOPASSWD-OK` |
| SSH persistence | 2026-09-17 | foundation block persistence report | `enabled` |
| External key-only login | 2026-09-17 | `tools/hx-doc/hx-fleet-access hx-8` | `hx-8` / `KEY+SUDO-PASS` / `PASS  hx-8 is administrable by the fleet key, proven externally.` |
| SSH host key | 2026-09-17 | `ssh-keyscan` piped to `ssh-keygen -lf -` | `256 SHA256:DdUbVL+ISn1Lv5p0zw7DpFO0oLr5VIiRUrVtNx9kmQI 192.168.50.208 (ED25519)` |
| SPNs in AD | 2026-09-17 | `samba-tool computer show hx-8` on HX-1 | `host/HX-8`, `host/hx-8.hx.local.arpa`, `RestrictedKrbHost/HX-8`, `RestrictedKrbHost/hx-8.hx.local.arpa` |

All four SPN forms are present, which is what D-029 requires. `dNSHostName`
reads `hx-8.hx.local.arpa`.

Proof step `F0` in `docs/00-control/hx-proof.tsv` is satisfied.

**Reverse DNS is absent fleet-wide, not on this host.** A reverse lookup of
`192.168.50.208` returned nothing on 2026-09-17, and so did every other address
checked, including the domain controller's own `192.168.50.200`. No reverse zone
is served. The domain join and GSSAPI work because they use the SPNs, and all
four forms are present above. This is recorded as `HX8-F01` in
[`FINDINGS.md`](../00-control/FINDINGS.md) because it is a property of the
domain, not a defect against hx-8.

## 1. Identity and Network

| Item | Value |
|---|---|
| Hostname | `hx-8` |
| FQDN | `hx-8.hx.local.arpa` |
| IP | `192.168.50.208` on `eno1` |
| Domain | `hx.local.arpa`, realm `HX.LOCAL.ARPA` |
| Client software | SSSD |

Domain join, 2026-09-17, reported by
[`02-domain.sh`](../03-runbooks/HX-8/02-domain.sh):

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

SSSD active, and a domain user resolves:

```text
active
uid=218001148(jarvisr@hx.local.arpa) gid=218000513(domain users@hx.local.arpa) groups=218000513(domain users@hx.local.arpa)
```

**Domain join gate: PASS**

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | Ubuntu 24.04.5 LTS |
| Kernel | `7.0.0-31-generic` |
| Firmware version | HP `P21 Ver. 02.15`, dated `01/31/2018`, read from `/sys/class/dmi/id/` on 2026-09-17 |
| sudo policy | NOPASSWD for the admin account via `/etc/sudoers.d/90-hx-admin`, parsed OK during the foundation block |

Block 1 finished with `0 updates can be applied immediately` after its reboot.

## 3. GPU Configuration

HX-8 carries no GPU. Block 2 reported this and installed no driver:

```text
hx-8 carries no GPU, so Block 2 is domain join only here.
```

This is the expected result. `HX_GPU_HOSTS` is `hx-2 hx-3 hx-4 hx-5`, and
`hx_require_gpu_expectation` refuses a driver install on any host outside it.

**GPU gate: PASS — no GPU expected, none installed**

## 4. Storage Layout

```text
nvme0n1     238.5G
├─nvme0n1p1     1G vfat  /boot/efi
├─nvme0n1p2   120G ext4  /
└─nvme0n1p3 117.4G ext4  /srv/openwebui
```

`/srv/openwebui` is a dedicated filesystem, mounted by UUID in `/etc/fstab`.
Usage after the build and the reboot, 2026-09-17:

```text
/dev/nvme0n1p3  116G   12G   98G  11% /srv/openwebui
```

The volume was provisioned as `/srv/openwebui`, matching the fleet convention.
The block looked for `/srv/open-webui` and refused at exit 34 until the path was
corrected. The gate did its job: without it the install would have created a
plain directory on the root disk and left this volume empty.

**Storage gate: PASS**

## 5. Runtime

| Item | Value |
|---|---|
| Package source | PyPI wheel into a native venv |
| Installed version | `0.11.3`, read back from distribution metadata through the venv interpreter |
| Virtual environment | `/srv/openwebui/venv` |
| Service unit | `hx-open-webui.service` |
| Service identity | `User=openwebui` |
| Listener | `0.0.0.0:8081` |

```text
ExecStart=/srv/openwebui/venv/bin/open-webui serve --host 0.0.0.0 --port 8081
User=openwebui
ActiveState=active
UnitFileState=enabled
```

Listener proven at install time:

```text
LISTEN 0  2048  0.0.0.0:8081  0.0.0.0:*
```

Secrets live in an environment file the service identity never reads directly.
systemd reads it as PID 1 before dropping to `User=`:

```text
root:root 600 /srv/openwebui/open-webui.env
```

It holds `WEBUI_SECRET_KEY` only. No administrator password is generated,
prompted for, or stored. `DATA_DIR`, `HF_HOME`, `WEBUI_AUTH=True` and
`ENABLE_SIGNUP=False` are unit `Environment=` lines, not secrets.

The version is read from distribution metadata rather than from the CLI.
`open-webui` accepts no `--version` and exits 2 on it, observed on hx-8 against
0.11.3, which stopped the block at exit 31 until the read was corrected.

## 6. Model / Application Provenance

HX-8 hosts no model. It hosts the downloaded application artifact below.

```text
HX alias:              hx-open-webui
Upstream identity:     Open WebUI 0.11.3
Source URI:            https://files.pythonhosted.org/packages/4c/e4/28abecd6b75fa6fa40ae181d2fa9f57593e26d13309c90531dee5b4acc28/open_webui-0.11.3-py3-none-any.whl
Artifact SHA-256:      8436f9bb29c5accbdfd90d78470fcc917c882bd53f72ed88fed91b1ee97fa547
Import method:         package install
```

The hash was verified on 2026-09-17 by fetching that exact URL from the
workstation and hashing the bytes, rather than by quoting the index:

```text
bytes:  146072797
sha256: 8436f9bb29c5accbdfd90d78470fcc917c882bd53f72ed88fed91b1ee97fa547
```

That digest equals the one PyPI publishes for the wheel. It proves what the URL
serves. It does not re-prove the copy on hx-8: pip unpacks and discards, and a
search of the host on 2026-09-17 found no retained wheel to hash. pip verifies
the index digest during install, so the two agree, but this record states which
artifact was hashed and where.

No Modelfile, template, parameter or stop-token settings apply here, because no
model is imported on this host.

That same API record states `requires_python <3.13.0a1,>=3.11`, which confirms
`HX_OPEN_WEBUI_PY_MIN` and `HX_OPEN_WEBUI_PY_MAX` independently of the source
tree. The host runs Python 3.12.3, inside the range.

## 7. Functional Validation

**HTTP, from the workstation, 2026-09-17.** Off-host, so it proves the LAN path
and not only a loopback listener:

```text
health 200
version 0.11.3
auth True
enable_signup False
```

**Authentication posture.** Before the first account existed the public config
carried `onboarding: true`, which is what opens the create-administrator screen.
After the account was created the key is absent and `enable_signup` is still
`false`, so the one-account window opened and closed:

```text
before:  onboarding true    enable_signup false
after:   onboarding absent  enable_signup false
```

**D-008 base proof, 2026-09-17.** Open WebUI was pointed at proven Ollama
endpoints, prompts were sent from the UI, and responses rendered. Four models
across four hosts answered:

| Model in the UI | Endpoint | Host record |
|---|---|---|
| `qwen-x:qwen3.8-27b-q6_k` | `http://192.168.50.202:11434` | HX-2, PASS / CLOSED |
| `coder-x-glm:glm47flash-q5km` | `http://192.168.50.203:11434` | HX-3, PASS / CLOSED |
| `meta-x:gpt-oss-20b` and `gpt-oss:20b` | `http://192.168.50.204:11434` | HX-4, PASS / CLOSED |
| `ornith-1.5:35b` | `http://192.168.50.205:11434` | HX-5, Ollama 0.34.0 PASS |

Three of those endpoints were checked from the workstation before the proof and
each answered `{"version":"0.34.0"}` on `/api/version`.

D-008 asks for one temporary connection. Four were made, so the obligation to
remove them covers four entries rather than one. Removal is recorded in
section 8.

**Reboot persistence, 2026-09-17.** After `sudo reboot`:

```text
active
enabled
health 200
```

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | PASS |
| Domain join / SSSD | PASS |
| GPU driver and visibility | PASS — no GPU expected, none installed |
| Dedicated storage | PASS — `/dev/nvme0n1p3` at `/srv/openwebui` |
| Runtime version | PASS — `0.11.3` matches the pin |
| Service active / enabled | PASS |
| Model / application loaded | PASS — Open WebUI 0.11.3, no model on this host |
| Known-answer functional proof | PASS — D-008, four models rendered |
| Reboot persistence | PASS |

**Stated exception: the D-008 connections remain configured.** D-008 asks for a
temporary connection, removed once the proof is captured. On 2026-09-17 the
owner decided to keep the four Ollama connections in place, so this host still
holds direct links to HX-2, HX-3, HX-4 and HX-5 rather than reaching the
inference plane only through OmniRoute.

The functional proof above stands on its own: prompts were sent and responses
rendered, and that evidence does not depend on what happens to the connections
afterwards. The removal clause of D-008 is a separate obligation, and it is
recorded here as open rather than met. Nothing in this record should be read as
saying the connections were removed.

## 9. Evidence References

The proof is recorded inline in section 7 of this record. No retained bundle
applies: every control above is a command and its output, captured on
2026-09-17, and nothing here produced a run directory.
