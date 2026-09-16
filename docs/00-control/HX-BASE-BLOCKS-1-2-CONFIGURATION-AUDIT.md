---
document: HX Base Blocks 1-2 Configuration Audit
status: current
date: 2026-09-15
scope: Layer 0/1 foundation prerequisites, Block 1-2 implementation coverage, HX-5 reconciliation, and retrospective audit requirement
---

# HX Base Blocks 1-2 Configuration Audit

## 1. Purpose

This document reconciles the accepted HX foundation architecture with the actual implementation in:

- `docs/03-runbooks/common/01-base-admin-network-updates.sh`
- `docs/03-runbooks/common/02-domain-nvidia.sh`
- `docs/03-runbooks/common/hx-base.env`

HX-5's 2026-09-15 clean OS rebuild proved that Blocks 1 and 2 alone are not a complete clean-OS Layer 0/1 bootstrap. They validate and configure important portions of the foundation, but several required conditions live outside those scripts and must still be proven before Layer 0/1 may be closed.

## 2. Authority hierarchy

1. Current owner-approved architecture and decisions.
2. Current repository source-of-truth files and runbooks.
3. Current as-built/runtime evidence.
4. Current server records and findings.
5. Historical material only when explicitly identified as historical evidence.

Accepted foundation values:

| Item | HX baseline |
|---|---|
| LAN | `192.168.50.0/24` |
| Gateway | `192.168.50.1` |
| HX infrastructure DNS | HX-1 `192.168.50.200` |
| Fleet NTP source | HX-1 `192.168.50.200` |
| AD domain | `hx.local.arpa` |
| Kerberos realm | `HX.LOCAL.ARPA` |
| Identity client | SSSD / realmd / adcli |
| Deployment | Native Ubuntu Linux + systemd |
| Host firewall | UFW disabled per D-018 |

## 3. Executive finding

**Blocks 1 and 2 are shared implementation blocks, not the full clean-OS Layer 0/1 acceptance standard.**

The accepted clean-build shape is:

```text
PRE-BLOCK FOUNDATION CONFIGURATION
        -> BLOCK 1 VALIDATION / ADMIN POLICY / OS UPDATE
        -> BLOCK 2 DOMAIN / NVIDIA
        -> POST-BLOCK RECONCILIATION
        -> FINAL REBOOT / PERSISTENCE PROOF
```

A host is not Layer 0/1 CLOSED merely because Blocks 1 and 2 complete without a fatal exit.

## 4. Block 1 — actual coverage

Block 1:

- enforces the intended host/IP association through `hx_require_host`;
- validates live IPv4, gateway, and HX-1 DNS;
- creates `hxsa` NOPASSWD sudo policy;
- disables/stops UFW per D-018;
- requires active SSH and reports its port;
- runs `apt update` and `apt upgrade -y`;
- reports remaining updates and failed units;
- reboots.

Block 1 does **not** establish or fully prove:

- FQDN configuration/resolution;
- persistent Netplan address/gateway/DNS state;
- HX-1 NTP client configuration;
- fleet SSH public-key installation;
- SSH reboot/startup mechanism;
- post-reboot persistence.

Those items are therefore prerequisites or reconciliation controls, not implicit PASS conditions.

## 5. Block 2 — actual coverage

Block 2:

- installs `realmd`, SSSD/adcli/Kerberos/Samba client packages;
- discovers and joins `hx.local.arpa` when needed;
- validates realm membership, SSSD active state, and domain-user resolution;
- installs the shared pinned NVIDIA package;
- reboots.

Block 2 does **not** fully prove:

- HX-1 NTP before Kerberos operations;
- intended FQDN before join;
- stale AD computer-object handling;
- Samba DNS A record after join;
- `dNSHostName` and required short/FQDN SPNs;
- `adcli testjoin` machine trust;
- SSSD failed responder/socket state;
- post-reboot `nvidia-smi`, GPU count/model, or module state.

## 6. HX-5 reconciliation — final accepted state

### 6.1 Identity and persistent network

```text
hostname: hx-5
FQDN: hx-5.hx.local.arpa
IPv4: 192.168.50.205/24
Gateway: 192.168.50.1
DNS: 192.168.50.200
Persistent network file: /etc/netplan/50-cloud-init.yaml
```

**PASS**

### 6.2 HX-1 NTP

The initial clean rebuild synchronized to a public Ubuntu time source, which was not the HX architecture baseline.

Corrected final state:

```text
chrony: active / enabled
selected source: ^* 192.168.50.200
Reference ID: C0A832C8
HX-5 local stratum: 4
Leap status: Normal
```

Post-reboot proof confirmed HX-1 remained selected.

**PASS**

### 6.3 Administrative access and SSH

```text
NOPASSWD sudo: PASS
fleet key: C:\Users\JarvisRichardson\.ssh\hx_fleet_ed25519
key-only remote login: PASS
ssh.service: active
ssh.socket: active / enabled
port: 22
post-reboot remote access: PASS
```

Ubuntu socket activation explains why `ssh.service` itself may report disabled while SSH persistence is healthy.

**PASS**

### 6.4 D-018 UFW posture

Initial post-rebuild state had UFW inactive at the rules level but its service enabled/active. This was corrected.

Final state:

```text
ufw status: inactive
ufw.service: disabled
ufw.service: inactive
```

**PASS**

### 6.5 OS maintenance

Four Netplan packages remained listed as upgradeable after normal maintenance. Read-only simulation showed both normal and dist-upgrade paths deferred the same four packages solely due to Ubuntu phased updates. `apt-mark showhold` returned no held packages.

```text
libnetplan1
netplan-generator
netplan.io
python3-netplan
```

This is normal phased-update behavior, not an HX maintenance failure.

**PASS WITH NORMAL PHASED-UPDATES EXCEPTION**

### 6.6 Domain, machine trust, DNS, and SPNs

Final HX-5 state:

```text
realm membership: PASS
sssd.service: active
jarvisr@hx.local.arpa resolution: PASS
adcli testjoin -D hx.local.arpa: PASS
Samba computer object HX-5$: PASS
dNSHostName hx-5.hx.local.arpa: PASS
Samba A record hx-5 -> 192.168.50.205: PASS
host/HX-5: PASS
host/hx-5.hx.local.arpa: PASS
RestrictedKrbHost/HX-5: PASS
RestrictedKrbHost/hx-5.hx.local.arpa: PASS
```

**PASS**

### 6.7 SSSD deferred condition

Initial validation showed three failed responder sockets. After the final reconciliation reboot, two remained:

```text
sssd-nss.socket
sssd-pam-priv.socket
```

Core domain function remains healthy. This is tracked as HX4-F02.

**DEFERRED / NON-BLOCKING**

### 6.8 NVIDIA

Accepted HX-5 state:

```text
NVIDIA driver: 595.99.02
CUDA reported: 13.2
GPU 0: RTX 5060, 8151 MiB
GPU 1: RTX 5060 Ti, 16311 MiB
nvidia-smi: PASS before and after reboot
```

The shared Block 2 pin targets `595.91.07-0ubuntu0.24.04.1` as of 2026-09-16. HX-5 runs 595.99.02, so **Block 2 must not be rerun on HX-5 merely for confirmation**.

**PASS**

### 6.9 Dedicated storage

Authoritative filesystem UUID for `/srv/ollama`:

```text
68d0e365-212c-456f-b42e-d908b445ae77
```

The same filesystem appeared as `/dev/nvme0n1p3` before one reboot and `/dev/nvme1n1p3` afterward. The UUID-backed mount remained correct.

**PASS**

## 7. Final HX-5 Layer 0/1 acceptance matrix

| Gate | Result |
|---|---|
| Hostname / FQDN | PASS |
| Persistent IPv4 / gateway / DNS | PASS |
| Live network / HX-1 DNS | PASS |
| HX-1 NTP | PASS |
| NOPASSWD sudo | PASS |
| Fleet SSH key | PASS |
| SSH runtime / port 22 | PASS |
| SSH reboot persistence | PASS |
| UFW disabled/stopped | PASS |
| Domain membership / SSSD core | PASS |
| Machine trust | PASS |
| Samba DNS / dNSHostName / SPNs | PASS |
| SSSD socket cleanliness | DEFERRED / HX4-F02 |
| GPU runtime | PASS |
| Dedicated storage | PASS |
| OS maintenance | PASS; phased Netplan updates non-blocking |
| Final post-reboot proof | PASS |

# HX-5 LAYER 0/1 STATUS: PASS / CLOSED

## 8. Evidence-standard implication for HX-2 / HX-3 / HX-4

HX-5 established a stronger and more explicit Layer 0/1 acceptance standard than the records currently retained for HX-2, HX-3, and HX-4.

This does **not** mean those servers are known-bad. It means their retained evidence does not yet prove every control now required for a reconciled Layer 0/1 closure, including some combination of:

- HX-1 NTP selection;
- persistent network-file proof;
- fleet-key proof;
- SSH persistence mechanism;
- machine-trust proof;
- Samba DNS / `dNSHostName` / SPN proof;
- failed-unit classification.

Owner direction: **after HX-5 current closeout, perform a read-only retrospective Layer 0/1 audit of HX-2, HX-3, and HX-4 against this reconciled standard.** Do not rebuild or change working configuration merely to satisfy documentation symmetry.

## 9. Required process correction

Before treating future hosts as Layer 0/1 CLOSED, the build process must explicitly prove:

1. intended hostname/FQDN;
2. persistent IPv4/gateway/HX-1 DNS;
3. HX-1 NTP selection;
4. NOPASSWD sudo;
5. fleet-key access;
6. SSH persistence;
7. D-018 UFW state;
8. realm membership and SSSD core function;
9. machine trust;
10. Samba DNS / FQDN / SPNs where applicable;
11. failed units and accepted/deferred disposition;
12. GPU runtime where applicable;
13. approved storage mounts;
14. OS maintenance state;
15. final reboot persistence.

## 10. Evidence references

```text
docs/02-server-records/HX-5.md
docs/05-evidence/hx-5/layer0-1/2026-09-15-closure.md
docs/00-control/FINDINGS.md
```

This audit is the authority for the reconciled Layer 0/1 proof standard discovered during the HX-5 clean rebuild.
