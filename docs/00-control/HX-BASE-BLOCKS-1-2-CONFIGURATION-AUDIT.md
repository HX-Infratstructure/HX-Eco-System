---
document: HX Base Blocks 1-2 Configuration Audit
status: current
date: 2026-09-15
scope: Layer 0/1 foundation prerequisites and current Block 1-2 implementation coverage
---

# HX Base Blocks 1-2 Configuration Audit

## 1. Purpose

This document reconciles the accepted HX foundation architecture with the actual implementation in:

- `docs/03-runbooks/common/01-base-admin-network-updates.sh`
- `docs/03-runbooks/common/02-domain-nvidia.sh`
- `docs/03-runbooks/common/hx-base.env`

It exists because the common scripts are currently described as the shared base blocks, but they do **not** establish the entire Layer 0/1 baseline from a clean OS. Some foundation state is assumed to exist before Block 1 starts, and some required foundation state is not currently configured or validated by either block.

This distinction is operationally significant for HX-5 because its 2026-09-15 clean OS reinstall removed prior host state and exposed several of these assumptions.

## 2. Authority hierarchy used by this audit

1. Current owner-approved decisions and architecture.
2. Current repository runbooks and shared configuration.
3. Current as-built/runtime evidence.
4. Current server records and findings.
5. Historical material only where explicitly identified as historical evidence.

The architecture authority states that the HX foundation includes:

```text
HX-1 identity + DNS + Kerberos + NTP
LAN addressing + gateway + domain membership
native Ubuntu Linux + systemd
```

The accepted foundation values are:

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

They are a mixture of:

- prerequisite validation;
- selected host configuration;
- package installation;
- domain join;
- NVIDIA installation;
- reboot boundaries.

The current runbook README explicitly says the scripts must not alter hostname, IP, DNS, gateway, partitions, or mounts without owner approval. Therefore those values are prerequisites to Block 1, not outcomes of Block 1.

The current architecture also requires HX-1 NTP as part of the foundation, but neither Block 1 nor Block 2 configures or validates client time synchronization.

A clean rebuild must therefore distinguish:

```text
PRE-BLOCK FOUNDATION CONFIGURATION
        -> BLOCK 1 VALIDATION / HOST POLICY / OS UPDATE
        -> BLOCK 2 DOMAIN / NVIDIA
        -> POST-BLOCK VALIDATION
```

Treating Blocks 1 and 2 alone as the entire Layer 0/1 rebuild creates an incomplete baseline.

## 4. Pre-Block 1 foundation prerequisites

These values must already exist before Block 1 can pass because Block 1 validates them but does not configure them.

| Foundation item | Expected state | Block 1 behavior | Coverage |
|---|---|---|---|
| Static hostname | `hx-N` | Displays via `hostnamectl`; host guard uses short hostname | **PREREQUISITE** |
| FQDN resolution | `hx-N.hx.local.arpa` | Not validated | **GAP** |
| Static IPv4 | Fleet map, `/24` | Validates live address | **PREREQUISITE** |
| Default gateway | `192.168.50.1` | Validates live default route | **PREREQUISITE** |
| DNS resolver | HX-1 `192.168.50.200` | Validates resolver output contains HX-1 | **PREREQUISITE** |
| Persistent network config | Netplan/system network configuration | Not inspected | **GAP** |
| Fleet NTP client | HX-1 is fleet NTP source | Not configured or validated | **GAP** |
| SSH host service | Active | Validates `ssh` active and reports port | Validation only |
| Fleet SSH public key | Authorized for `hxsa` | Not installed or validated | **GAP** |
| Storage layout | Server-specific approved partitions/mounts | Not handled until Block 3 validation | Outside Block 1-2 |

## 5. Block 1 — actual configuration and validation

Source: `01-base-admin-network-updates.sh`.

### 5.1 Host guard

- Requires one expected HX hostname argument.
- Calls `hx_require_host` from `hx-base.env`.
- Refuses execution if `hostname -s` does not match the expected server.
- Resolves the expected IP from the fleet IP map.

### 5.2 Identity/network inspection

Commands:

```bash
hostnamectl
ip -br addr
ip route
resolvectl status
```

Validations:

- expected host IPv4 `/24` is present;
- default route uses `192.168.50.1`;
- resolver state contains HX-1 `192.168.50.200`.

**Important:** the block does not configure hostname, IP, gateway, or DNS.

### 5.3 Administrative sudo policy

Creates/replaces:

```text
/etc/sudoers.d/90-hx-admin
```

with:

```text
hxsa ALL=(ALL:ALL) NOPASSWD: ALL
```

The temporary file is ownership/mode checked with `visudo` before being moved into place.

Validation:

```bash
sudo -n true
```

must pass.

### 5.4 Firewall posture

Per owner decision D-018, Block 1 intentionally disables UFW:

```bash
sudo ufw disable || true
sudo systemctl disable --now ufw || true
```

It then reports:

- UFW status;
- UFW enabled/active state;
- current nftables ruleset;
- firewalld active state if present.

The block does **not** flush arbitrary nftables rules and does **not** disable firewalld. Those commands are observational only.

### 5.5 SSH validation

The block requires:

```bash
systemctl is-active ssh
```

and reports the effective SSH daemon port using:

```bash
sudo sshd -T | grep '^port '
```

It does not install the fleet SSH key and does not modify `sshd_config`.

### 5.6 OS maintenance

Runs:

```bash
sudo apt update
sudo apt upgrade -y
```

Then reports:

- remaining upgradable packages;
- failed systemd units.

### 5.7 Reboot

Block 1 ends with an unconditional:

```bash
sudo reboot
```

There is no same-script post-reboot validation. Subsequent execution assumes the reboot succeeded and the expected baseline persisted.

## 6. Block 1 gaps / unencoded foundation configuration

The following are not currently established by Block 1:

1. Hostname configuration.
2. FQDN configuration/resolution validation.
3. Persistent static IP configuration.
4. Persistent gateway configuration.
5. Persistent DNS configuration.
6. **Fleet NTP client configuration or validation against HX-1.**
7. Fleet SSH public-key installation or key-only proof.
8. Timezone policy/validation.
9. Persistent network-file inspection, e.g. Netplan.
10. Post-reboot validation that the Block 1 state survived.

The first five are intentionally outside the script according to the current runbook rule prohibiting unapproved hostname/network changes. NTP and fleet-key coverage are not currently represented by an equivalent explicit pre-block configuration authority in the active runbook set.

## 7. Block 2 — actual configuration and validation

Source: `02-domain-nvidia.sh`.

### 7.1 Domain-client packages

Installs from the Ubuntu archive:

```text
realmd
sssd-ad
sssd-tools
adcli
krb5-user
samba-common-bin
```

### 7.2 Realm discovery and join

Runs:

```bash
realm discover hx.local.arpa
```

If `realm list` reports `configured: kerberos-member`, the block treats the server as already joined.

Otherwise it runs interactively:

```bash
sudo realm join hx.local.arpa -U Administrator
```

### 7.3 Domain validation

After join/skip, Block 2 checks:

```bash
realm list
systemctl is-active sssd
id jarvisr@hx.local.arpa
```

The domain test-user resolution failure is blocking.

### 7.4 NVIDIA installation

The current shared pin is:

```text
HX_NVIDIA_BRANCH=595
HX_NVIDIA_PKG_VERSION=595.71.05-0ubuntu0.24.04.1
```

Therefore the block targets:

```text
nvidia-driver-595-server-open=595.71.05-0ubuntu0.24.04.1
```

and installs current-kernel headers plus that exact package.

It records the `dpkg -l` line, then reboots.

### 7.5 Reboot

Block 2 ends with an unconditional reboot. It does not perform post-reboot GPU or domain validation itself.

## 8. Block 2 prerequisites and gaps

### 8.1 Time synchronization prerequisite

Kerberos depends on acceptable clock synchronization. The HX architecture assigns HX-1 as fleet NTP source, but Block 2 does not prove time synchronization before domain operations.

**Status: GAP.**

### 8.2 Host/FQDN handling

Block 2 does not verify that the host has the intended short hostname plus resolvable FQDN before realm join.

HX-5 demonstrated the consequence after its clean OS reinstall: the new Samba computer object was initially created with:

```text
dNSHostName: hx-5
```

instead of:

```text
dNSHostName: hx-5.hx.local.arpa
```

and the FQDN SPNs were absent until corrected directly in Samba AD.

**Status: GAP CONFIRMED BY HX-5.**

### 8.3 Stale AD computer object handling

The block does not detect or remove a stale Samba/AD machine object before a clean-OS rejoin.

HX-5 required deletion of the stale `HX-5$` object on HX-1 before the new join.

**Status: GAP CONFIRMED BY HX-5.**

### 8.4 Samba DNS registration

The block does not verify the host A record in the Samba DNS zone after join.

HX-5 required explicit creation of:

```text
hx-5.hx.local.arpa -> 192.168.50.205
```

**Status: GAP CONFIRMED BY HX-5.**

### 8.5 AD computer attributes / SPNs

The block does not validate:

- `dNSHostName`;
- `host/<short>`;
- `host/<fqdn>`;
- `RestrictedKrbHost/<short>`;
- `RestrictedKrbHost/<fqdn>`.

HX-5 required direct Samba computer-object correction.

**Status: GAP CONFIRMED BY HX-5.**

### 8.6 Machine trust validation

The block does not run:

```bash
adcli testjoin -D hx.local.arpa
```

HX-5 used this successfully as explicit machine-trust proof.

**Status: GAP.**

### 8.7 SSSD failed-unit validation

Block 2 checks only that `sssd.service` is active. It does not run `systemctl --failed` after domain configuration or after reboot.

HX-4 and HX-5 both show the known deferred responder/socket condition:

```text
sssd-nss.socket
sssd-pam-priv.socket
sssd-pam.socket
```

while domain identity resolution remains functional.

This is already tracked as HX4-F02 and should remain a non-blocking/deferred finding unless owner direction changes.

### 8.8 NVIDIA post-reboot validation

Block 2 proves package installation before reboot but does not prove after reboot:

- `nvidia-smi` works;
- expected GPU count/models are visible;
- PCI devices enumerate;
- kernel module version matches intended driver;
- open-kernel module is loaded where required.

**Status: GAP.**

### 8.9 Driver baseline conflict exposed by HX-5

HX-5 currently runs a verified NVIDIA `595.99.02` open kernel module installed from the official NVIDIA `.run` distribution during hardware troubleshooting. Current Block 2 still pins the Ubuntu package `595.71.05-0ubuntu0.24.04.1`.

Therefore Block 2 must **not** be rerun on the current HX-5 as written. Doing so would attempt to impose a different driver baseline.

This is a current runbook/as-built divergence that requires an explicit owner decision before the common NVIDIA block is changed fleet-wide.

## 9. Current HX-5 Layer 0/1 evidence — 2026-09-15

Already proven in the current rebuild session:

| Control | HX-5 evidence | State |
|---|---|---|
| Short hostname | `hx-5` | PASS |
| FQDN | `hx-5.hx.local.arpa` | PASS |
| IPv4 | `192.168.50.205/24` | PASS |
| Gateway | `192.168.50.1` | PASS |
| AD trust | `adcli testjoin -D hx.local.arpa` | PASS |
| SSSD service | active | PASS |
| Domain user | `jarvisr@hx.local.arpa` resolves | PASS |
| Samba computer object | `HX-5$` recreated after stale-object deletion | PASS |
| Samba `dNSHostName` | `hx-5.hx.local.arpa` | PASS after correction |
| Samba SPNs | short and FQDN host/RestrictedKrbHost present | PASS after correction |
| Samba A record | `192.168.50.205` | PASS after explicit add |
| NOPASSWD sudo | `sudo -n true` | PASS |
| Fleet SSH identity | Windows `hx_fleet_ed25519` | PASS |
| Key-only fleet SSH | `PasswordAuthentication=no` test | PASS |
| NVIDIA runtime | `595.99.02`, CUDA reported 13.2 | PASS |
| GPU 0 | RTX 5060, 8151 MiB | PASS |
| GPU 1 | RTX 5060 Ti, 16311 MiB | PASS |
| PCI enumeration | both NVIDIA VGA/audio functions visible | PASS |
| NVIDIA module | `595.99.02`, `Dual MIT/GPL` | PASS |
| SSSD socket cleanliness | three failed socket units | DEFERRED / HX4-F02 pattern |

Still requiring current runtime proof before Layer 0/1 can be declared fully reconciled:

1. Resolver state explicitly proving HX-1 `192.168.50.200` on HX-5 after the clean OS reinstall.
2. NTP/time-sync implementation and source proof.
3. UFW disabled/inactive proof after reinstall.
4. nftables/firewalld observation.
5. SSH service active and effective port.
6. Persistent network configuration source, including how IP/gateway/DNS survive reboot.
7. Remaining OS updates / package state.
8. Full failed-unit state already partially captured; SSSD sockets remain the known deferred condition.

## 10. Required corrected Layer 0/1 shape

The clean-build process should be represented as four explicit stages rather than implying Blocks 1 and 2 create everything:

### Stage A — Foundation configuration / preflight

Establish and record, with owner-approved values:

- short hostname;
- FQDN resolution;
- persistent static IP;
- gateway;
- HX-1 DNS;
- HX-1 NTP client configuration;
- administrative account / NOPASSWD policy target;
- fleet SSH public key;
- approved storage layout where applicable.

### Stage B — Block 1

- validate identity/network/DNS;
- enforce NOPASSWD sudo;
- enforce D-018 UFW posture;
- validate SSH service;
- OS update/upgrade;
- report failed units;
- reboot.

### Stage C — Block 2

- install domain-client packages;
- handle clean-rebuild stale computer object when required;
- discover/join domain;
- validate machine trust, Samba DNS, FQDN attributes and SPNs;
- validate SSSD/domain-user resolution;
- install approved NVIDIA baseline;
- reboot.

### Stage D — post-Block 2 closure

- verify hostname/FQDN/network/DNS persisted;
- verify NTP source and synchronization;
- verify `adcli testjoin`;
- verify Samba A record/computer attributes/SPNs;
- verify SSSD and failed units;
- verify NVIDIA module, `nvidia-smi`, GPU count/models and PCI enumeration;
- record evidence before moving to Block 3.

## 11. Immediate HX-5 disposition

Do **not** run Block 1 or Block 2 again on HX-5 merely to make the scripts appear complete.

HX-5 already has manually repaired and verified domain/GPU state that Block 2 as currently written cannot reproduce correctly, and rerunning it would attempt to install the older `595.71.05` NVIDIA package baseline.

Instead:

1. finish the read-only Layer 0/1 reconciliation checks listed in section 9;
2. restore only genuinely missing foundation configuration;
3. record any changes and re-run closure validation;
4. update the common base process separately so future clean rebuilds do not depend on undocumented prerequisites.

## 12. Audit conclusion

The correct finding is not that Block 1 or Block 2 individually failed. The defect is that the repository currently presents Blocks 1-3 as the common base sequence while key Layer 0/1 foundation state is established outside those blocks without one complete active pre-block/bootstrap authority.

NTP is the clearest omission, but HX-5 proves the issue is broader: FQDN/AD computer-object correctness, Samba DNS registration, fleet SSH authorization, and post-reboot GPU/domain closure are also outside the current Block 1-2 implementation.

The next correction should preserve the existing KISS sequence while making prerequisites and closure proof explicit. Do not silently fold unapproved hostname/network mutations into Block 1; create a controlled preflight/bootstrap stage or equivalent authority instead.
