---
document: HX Base Blocks 1-2 Configuration Audit
status: current
date: 2026-09-15
scope: Layer 0/1 foundation prerequisites, current Block 1-2 implementation coverage, and HX-5 clean-rebuild audit
---

# HX Base Blocks 1-2 Configuration Audit

## 1. Purpose

This document reconciles the accepted HX foundation architecture with the actual implementation in:

- `docs/03-runbooks/common/01-base-admin-network-updates.sh`
- `docs/03-runbooks/common/02-domain-nvidia.sh`
- `docs/03-runbooks/common/hx-base.env`

It exists because the common scripts are currently described as the shared base blocks, but they do **not** establish the entire Layer 0/1 baseline from a clean OS. Some foundation state is assumed to exist before Block 1 starts, and some required foundation state is not currently configured or validated by either block.

HX-5's 2026-09-15 clean OS reinstall exposed these assumptions directly.

## 2. Authority hierarchy

1. Current owner-approved decisions and architecture.
2. Current repository runbooks and shared configuration.
3. Current as-built/runtime evidence.
4. Current server records and findings.
5. Historical material only where explicitly identified as historical evidence.

The architecture authority defines the HX foundation as:

```text
HX-1 identity + DNS + Kerberos + NTP
LAN addressing + gateway + domain membership
native Ubuntu Linux + systemd
```

Accepted foundation values:

| Item | HX baseline |
|---|---|
| LAN | `192.168.50.0/24` |
| Default gateway | `192.168.50.1` |
| HX infrastructure DNS | HX-1 at `192.168.50.200` |
| Active Directory domain | `hx.local.arpa` |
| Kerberos realm | `HX.LOCAL.ARPA` |
| Identity client | SSSD / realmd / adcli |
| Foundation server | HX-1 — Samba AD / DNS / Kerberos / NTP |
| Deployment | Native Ubuntu Linux + systemd |
| Host firewall | No UFW per D-018 |

## 3. Executive finding

**Blocks 1 and 2 are not a complete clean-OS Layer 0/1 bootstrap.**

They combine prerequisite validation, selected host configuration, package installation, domain join, NVIDIA installation, and reboot boundaries. The runbook README explicitly says the scripts must not alter hostname, IP, DNS, gateway, partitions, or mounts without owner approval. Those values are therefore prerequisites to Block 1 rather than outcomes of Block 1.

The current architecture also requires HX-1 NTP as part of the foundation, but neither Block 1 nor Block 2 configures or validates client time synchronization.

The correct clean-build shape is:

```text
PRE-BLOCK FOUNDATION CONFIGURATION
        -> BLOCK 1 VALIDATION / HOST POLICY / OS UPDATE
        -> BLOCK 2 DOMAIN / NVIDIA
        -> POST-BLOCK VALIDATION
```

Treating Blocks 1 and 2 alone as the entire Layer 0/1 rebuild creates an incomplete baseline.

## 4. Pre-Block 1 foundation prerequisites

| Foundation item | Expected state | Block 1 behavior | Coverage |
|---|---|---|---|
| Static hostname | `hx-N` | Displays via `hostnamectl`; host guard uses short hostname | **PREREQUISITE** |
| FQDN resolution | `hx-N.hx.local.arpa` | Not validated | **GAP** |
| Static IPv4 | Fleet map, `/24` | Validates live address | **PREREQUISITE** |
| Default gateway | `192.168.50.1` | Validates live route | **PREREQUISITE** |
| DNS resolver | HX-1 `192.168.50.200` | Validates live resolver | **PREREQUISITE** |
| Persistent network config | Netplan/system network config | Not inspected | **GAP** |
| Fleet NTP client | HX-1 is fleet NTP source | Not configured or validated | **GAP** |
| SSH host service | Active | Validates active and reports port | Validation only |
| Fleet SSH public key | Authorized for `hxsa` | Not installed or validated | **GAP** |
| Storage layout | Approved server-specific layout | Outside Blocks 1-2 | Outside scope |

## 5. Block 1 — actual behavior

Source: `01-base-admin-network-updates.sh`.

### 5.1 Host guard

- Requires one expected HX hostname argument.
- Calls `hx_require_host`.
- Refuses execution if `hostname -s` does not match.
- Resolves expected IP from the fleet map.

### 5.2 Identity/network validation

Displays:

```bash
hostnamectl
ip -br addr
ip route
resolvectl status
```

Validates:

- expected host IPv4 `/24`;
- default route via `192.168.50.1`;
- resolver state contains `192.168.50.200`.

It does **not** configure hostname, IP, gateway, DNS, FQDN, Netplan, or NTP.

### 5.3 Administrative sudo policy

Creates/replaces:

```text
/etc/sudoers.d/90-hx-admin
```

with:

```text
hxsa ALL=(ALL:ALL) NOPASSWD: ALL
```

Then validates with `sudo -n true`.

### 5.4 Firewall posture

Per D-018, Block 1 runs:

```bash
sudo ufw disable || true
sudo systemctl disable --now ufw || true
```

It then reports UFW, nftables, and firewalld state. It does not impose additional firewall rules.

### 5.5 SSH validation

Requires `ssh` to be active and reports the effective port. It does not install the fleet key, enable the service, modify `sshd_config`, or prove reboot persistence.

### 5.6 OS maintenance

Runs:

```bash
sudo apt update
sudo apt upgrade -y
```

Then reports remaining upgrades and failed systemd units.

### 5.7 Reboot

Ends with an unconditional reboot. There is no same-script post-reboot validation.

## 6. Block 1 coverage gaps

Block 1 does not establish or fully prove:

1. hostname configuration;
2. FQDN configuration/resolution;
3. persistent static IP configuration;
4. persistent gateway configuration;
5. persistent DNS configuration;
6. **HX-1 NTP client configuration or validation**;
7. fleet SSH public-key installation or key-only proof;
8. timezone policy;
9. persistent network-file inspection;
10. SSH startup persistence;
11. post-reboot persistence of the Block 1 state.

Items 1, 3, 4, and 5 are intentionally outside the block under the current rule against unapproved network mutation. NTP and fleet-key coverage currently lack an equivalent explicit pre-block implementation authority.

## 7. Block 2 — actual behavior

Source: `02-domain-nvidia.sh`.

### 7.1 Domain-client packages

Installs:

```text
realmd
sssd-ad
sssd-tools
adcli
krb5-user
samba-common-bin
```

### 7.2 Realm discovery and join

Runs `realm discover hx.local.arpa`. If `realm list` already reports `configured: kerberos-member`, it skips the join. Otherwise it runs:

```bash
sudo realm join hx.local.arpa -U Administrator
```

### 7.3 Domain validation

Checks:

```bash
realm list
systemctl is-active sssd
id jarvisr@hx.local.arpa
```

The domain test-user resolution failure is blocking.

### 7.4 NVIDIA installation

Current shared target:

```text
HX_NVIDIA_BRANCH=595
HX_NVIDIA_PKG_VERSION=595.71.05-0ubuntu0.24.04.1
```

Therefore the block targets:

```text
nvidia-driver-595-server-open=595.71.05-0ubuntu0.24.04.1
```

plus current-kernel headers.

### 7.5 Reboot

Ends with an unconditional reboot. It does not perform post-reboot GPU or domain validation itself.

## 8. Block 2 prerequisites and gaps

### 8.1 Time synchronization

Kerberos depends on synchronized clocks. HX architecture assigns HX-1 as the fleet NTP source, but Block 2 does not prove or establish this before domain operations.

**Status: GAP CONFIRMED ON HX-5.**

### 8.2 Host/FQDN handling

Block 2 does not verify intended short hostname plus FQDN before realm join. HX-5's fresh join initially created `dNSHostName: hx-5` rather than `hx-5.hx.local.arpa`.

**Status: GAP CONFIRMED ON HX-5.**

### 8.3 Stale AD computer object handling

No detection/removal of a stale machine object is encoded. HX-5 required deletion of stale `HX-5$` before clean rejoin.

**Status: GAP CONFIRMED ON HX-5.**

### 8.4 Samba DNS registration

The block does not verify the host A record after join. HX-5 required explicit creation of `hx-5.hx.local.arpa -> 192.168.50.205`.

**Status: GAP CONFIRMED ON HX-5.**

### 8.5 AD computer attributes / SPNs

The block does not validate `dNSHostName`, short/FQDN host SPNs, or short/FQDN RestrictedKrbHost SPNs. HX-5 required direct Samba correction.

**Status: GAP CONFIRMED ON HX-5.**

### 8.6 Machine trust proof

The block does not run:

```bash
adcli testjoin -D hx.local.arpa
```

**Status: GAP.**

### 8.7 SSSD failed-unit validation

The block checks only `sssd.service`. HX-4 and HX-5 both show the deferred responder/socket condition in HX4-F02.

### 8.8 NVIDIA post-reboot validation

The block does not prove after reboot:

- `nvidia-smi` health;
- GPU count/models;
- PCI enumeration;
- kernel module version;
- open-kernel module state.

**Status: GAP.**

### 8.9 HX-5 driver divergence

HX-5 currently runs verified NVIDIA `595.99.02` with the open kernel module. Current Block 2 still pins Ubuntu package `595.71.05-0ubuntu0.24.04.1`.

**Block 2 must not be rerun on current HX-5 as written.**

## 9. HX-5 Layer 0/1 runtime audit — 2026-09-15

Evidence captured after the fresh OS rebuild.

### 9.1 Identity and persistent network

| Control | Evidence | State |
|---|---|---|
| Hostname | `hx-5` | **PASS** |
| FQDN | `hx-5.hx.local.arpa` | **PASS** |
| `/etc/hosts` | `127.0.1.1 hx-5.hx.local.arpa hx-5` | **PASS** |
| Persistent IPv4 | Netplan `192.168.50.205/24` | **PASS** |
| Persistent gateway | Netplan default via `192.168.50.1` | **PASS** |
| Persistent DNS | Netplan `192.168.50.200` | **PASS** |
| Live IPv4 | `192.168.50.205/24` on `eno1` | **PASS** |
| Live gateway | `192.168.50.1` | **PASS** |
| Live DNS | current DNS server `192.168.50.200` | **PASS** |

Persistent network authority is `/etc/netplan/50-cloud-init.yaml`.

### 9.2 Time synchronization

Observed:

```text
System clock synchronized: yes
NTP service: active
chrony: not installed
systemd-timesyncd: active/enabled
Current time source: ntp.ubuntu.com (91.189.91.157)
```

The host clock is synchronized, but **not to the HX fleet NTP source**.

Required HX architecture:

```text
HX-1 / 192.168.50.200 = fleet NTP source
```

**NTP FOUNDATION GATE: FAIL / CONFIGURATION MISSING.**

This is a genuine clean-rebuild gap and must be corrected before Layer 0/1 is closed.

### 9.3 Administrative access

| Control | Evidence | State |
|---|---|---|
| NOPASSWD sudo | `sudo -n true` | **PASS** |
| Sudoers file | `/etc/sudoers.d/90-hx-admin` | **PASS** |
| Fleet public key | one ED25519 key, comment `hx-fleet-20260810` | **PASS** |
| Fleet key fingerprint | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk` | **PASS** |
| Key-only remote login | proven from Windows control workstation | **PASS** |

Authoritative Windows private key filename: `hx_fleet_ed25519`.

### 9.4 SSH service

Observed:

```text
ssh.service: active
ssh.service enabled state: disabled
effective port: 22
```

Current remote access works. However, service startup persistence cannot be called PASS from this evidence alone because Ubuntu may be using socket activation.

**SSH runtime: PASS.**  
**SSH reboot/startup persistence: VERIFICATION REQUIRED.**

Required follow-up: inspect `ssh.socket` state and perform/retain reboot persistence proof before Layer 0/1 closure.

### 9.5 Firewall posture

Observed:

```text
ufw status: inactive
ufw.service: enabled
ufw.service: active
nftables ruleset: empty
firewalld: inactive / not found
```

The effective firewall is not filtering traffic, but the service state does not match Block 1/D-018, which calls for UFW to be disabled and stopped.

**Effective no-firewall posture: PASS.**  
**Block 1 UFW service-state compliance: FAIL / DRIFT.**

This is a configuration reconciliation item, not a reason to introduce firewall rules.

### 9.6 Domain / Kerberos

| Control | Evidence | State |
|---|---|---|
| Realm | `HX.LOCAL.ARPA` | **PASS** |
| Domain | `hx.local.arpa` | **PASS** |
| Realm membership | `kerberos-member` | **PASS** |
| Machine trust | `adcli testjoin -D hx.local.arpa` | **PASS** |
| SSSD service | active | **PASS** |
| Domain user resolution | `jarvisr@hx.local.arpa` | **PASS** |
| Samba machine object | recreated | **PASS** |
| Samba `dNSHostName` | `hx-5.hx.local.arpa` | **PASS after correction** |
| Samba FQDN/short SPNs | present | **PASS after correction** |
| Samba DNS A record | `192.168.50.205` | **PASS after explicit add** |

`/etc/krb5.conf` correctly sets `default_realm = HX.LOCAL.ARPA`; the package also carries many distribution/example realm entries that are not HX configuration authority and do not affect the current HX join proof.

### 9.7 SSSD responder sockets

Failed units:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

Core SSSD/domain functions pass. This is the known HX4-F02 fleet-pattern finding.

**State: DEFERRED / NON-BLOCKING.**

### 9.8 NVIDIA

| Control | Evidence | State |
|---|---|---|
| Driver | `595.99.02` | **PASS** |
| CUDA reported | `13.2` | **PASS** |
| Kernel module | `595.99.02` | **PASS** |
| Module license | `Dual MIT/GPL` | **PASS** |
| GPU 0 | RTX 5060, 8151 MiB | **PASS** |
| GPU 1 | RTX 5060 Ti, 16311 MiB | **PASS** |
| PCI enumeration | both GPUs + audio functions | **PASS** |

**GPU gate: PASS.**

### 9.9 OS/package state

Observed:

```text
Ubuntu 24.04.5 LTS
kernel 7.0.0-31-generic
BIOS 1836
```

Four Netplan-related packages remain upgradeable:

```text
libnetplan1
netplan-generator
netplan.io
python3-netplan
```

Therefore the Block 1 update/upgrade closure is **not currently clean**.

**OS package-current gate: FAIL / UPDATE PENDING.**

## 10. HX-5 Layer 0/1 closure matrix

| Foundation control | State |
|---|---|
| Hostname / FQDN | **PASS** |
| Persistent IPv4 / gateway / DNS | **PASS** |
| Live IPv4 / gateway / HX-1 DNS | **PASS** |
| HX-1 NTP client | **FAIL — missing** |
| NOPASSWD sudo | **PASS** |
| Fleet SSH key | **PASS** |
| SSH runtime / port 22 | **PASS** |
| SSH reboot persistence | **VERIFICATION REQUIRED** |
| D-018 effective no-firewall posture | **PASS** |
| UFW service disabled/stopped | **FAIL — drift** |
| Domain membership | **PASS** |
| Machine trust | **PASS** |
| Samba DNS / FQDN / SPNs | **PASS after repair** |
| SSSD functional state | **PASS** |
| SSSD socket cleanliness | **DEFERRED / HX4-F02** |
| NVIDIA runtime / GPUs | **PASS** |
| OS packages current | **FAIL — 4 Netplan updates pending** |
| Post-reboot closure proof | **NOT YET COMPLETE** |

**HX-5 Layer 0/1 overall state: NOT CLOSED.**

Remaining blocking reconciliation items:

1. restore the approved HX-1 NTP client configuration;
2. reconcile UFW service state to D-018 / Block 1 (`disabled` and stopped);
3. apply/resolve the remaining approved OS package updates;
4. prove SSH startup mechanism/persistence;
5. perform a final reboot validation after corrections.

The deferred SSSD socket finding does not block closure under the existing disposition.

## 11. Required corrected Layer 0/1 process shape

### Stage A — Foundation configuration / preflight

Establish and record:

- short hostname;
- FQDN resolution;
- persistent static IP;
- gateway;
- HX-1 DNS;
- **HX-1 NTP client configuration**;
- administrative account target;
- fleet SSH public key;
- approved storage layout where applicable.

### Stage B — Block 1

- validate identity/network/DNS;
- validate HX-1 NTP source;
- enforce NOPASSWD sudo;
- enforce D-018 UFW disabled/stopped posture;
- validate fleet SSH key and SSH startup persistence;
- OS update/upgrade;
- report failed units;
- reboot.

### Stage C — Block 2

- install domain-client packages;
- detect/handle stale clean-rebuild machine object when required;
- discover/join domain;
- validate machine trust;
- validate Samba DNS, FQDN attributes, and SPNs;
- validate SSSD/domain user;
- install the owner-approved NVIDIA baseline;
- reboot.

### Stage D — post-Block 2 closure

Prove after reboot:

- hostname/FQDN;
- persistent and live network/DNS;
- HX-1 NTP synchronization;
- sudo and fleet-key access;
- firewall posture;
- SSH persistence;
- domain trust and identity resolution;
- Samba DNS/FQDN/SPNs;
- NVIDIA module and GPU visibility;
- package-current state;
- failed units classified as blocking or deferred.

## 12. Runbook corrections required

This audit identifies a process defect, not merely an HX-5 exception. Before using Blocks 1-2 as the clean-rebuild authority for later servers, the active runbooks should be updated so the missing foundation stages are explicit and executable.

High-priority corrections:

1. Add explicit pre-Block foundation configuration/validation authority.
2. Add HX-1 NTP client setup and proof.
3. Add persistent Netplan validation.
4. Add fleet SSH key/key-only validation.
5. Add FQDN pre-join validation.
6. Add clean-rebuild stale computer-object handling procedure.
7. Add post-join `adcli testjoin`, Samba DNS, `dNSHostName`, and SPN proof.
8. Add post-reboot GPU proof.
9. Add post-reboot SSH persistence proof.
10. Reconcile the shared NVIDIA pin with the explicitly accepted HX-5 595.99.02 state before reusing Block 2 on HX-5.

Do not silently fold these into unrelated application blocks. Layer 0/1 must be complete and independently auditable before Block 3 or application installation proceeds.
