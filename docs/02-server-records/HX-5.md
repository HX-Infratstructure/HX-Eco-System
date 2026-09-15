# HX-5 — CentCom / Ornith / DeepSeek Harness / dev-test Server Configuration

**Build state:** IN PROGRESS
**Gate:** DOMAIN / ADMIN ACCESS PASS
**IP:** `192.168.50.205`
**FQDN:** `hx-5.hx.local.arpa`
**Record updated:** 2026-09-15
> Scaffolded by `tools/hx-doc/hx-new-server hx-5`. Fill every section as the
> build proceeds. `tools/hx-doc/hx-record-check` reports what is still open.

## 1. Identity and Network

- Static hostname: `hx-5`
- FQDN: `hx-5.hx.local.arpa`
- IPv4: `192.168.50.205`
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
| Distribution / release | Fresh Ubuntu installation; exact release proof pending current baseline capture |
| Kernel | Pending current baseline capture |
| Firmware version | BIOS 1836 |
| sudo policy | `hxsa ALL=(ALL:ALL) NOPASSWD: ALL`; validated with `sudo -n true` |

## 3. GPU Configuration

Driver package **and exact version**, GPU models and count, `nvidia-smi` proof.
State the gate result: **GPU gate: PASS/FAIL**.

Known post-rebuild target/observed state prior to formal gate capture:

- NVIDIA driver: `595.99.02`
- GPU 0: NVIDIA GeForce RTX 5060, approximately 8 GB VRAM
- GPU 1: NVIDIA GeForce RTX 5060 Ti, approximately 16 GB VRAM
- Combined physical VRAM: approximately 24 GB

Formal current `nvidia-smi`, PCI, and module evidence remains to be captured in
this build pass before the GPU gate is closed.

## 4. Storage Layout

Devices, filesystems, mount points, and the dedicated application path.
State the gate result: **Storage gate: PASS/FAIL**.

## 5. Runtime

Package source, **exact installed version**, service unit, systemd overrides,
listener address and port.

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

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | IN PROGRESS |
| Domain join / SSSD | PASS |
| GPU driver and visibility | PENDING FORMAL CAPTURE |
| Dedicated storage | PENDING |
| Runtime version | PENDING |
| Service active / enabled | PENDING |
| Model / application loaded | PENDING |
| Known-answer functional proof | PENDING |
| Reboot persistence | PENDING |

## 9. Evidence References

Either a retained bundle path under `docs/05-evidence/<server>/<component>/<run-id>/`,
or an explicit statement that the proof is recorded inline in section 7 of this
record. See `docs/05-evidence/README.md` for which model applies.

Current inline evidence in this record covers the 2026-09-15 domain repair and
fleet-key/passwordless-sudo validation. GPU, storage, runtime, model, functional,
and reboot-persistence evidence remain open.
