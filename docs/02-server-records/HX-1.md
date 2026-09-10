# HX-1 — Samba Infrastructure Server

**State:** PASS / CLOSED
**IP:** `192.168.50.200`
**FQDN:** `hx-1.hx.local.arpa`

> **Not applicable:** Operating System, GPU, Storage, Runtime, Provenance, Final State — HX-1 is the retained clean Samba foundation, not a rebuilt application host. It carries no GPU, no dedicated application storage, and no model or application artifact. A fuller clean-rebuild as-built record is only created if HX-1 is ever rebuilt; see `docs/00-control/REPOSITORY-STATUS.md`. Do not fabricate the missing detail from historical HX-Infrastructure material.

## Role
- Samba Active Directory Domain Controller
- DNS for HX domain
- Kerberos
- Fleet NTP source

## Identity and Network
- Hostname: `hx-1`
- FQDN: `hx-1.hx.local.arpa`
- IP: `192.168.50.200/24`
- Gateway: `192.168.50.1`
- Realm: `HX.LOCAL.ARPA`
- Domain: `hx.local.arpa`
- NetBIOS: `HX`
- DNS forwarder: `192.168.50.1`

HX-1 is itself the fleet DNS server; every other HX host resolves the domain
through `192.168.50.200`.

## Current validation
- Samba database health: PASS
- Samba service active/enabled: PASS
- Domain/DNS/Kerberos foundation retained as clean baseline
- Fleet clients use HX-1 for HX domain DNS

No additional workload is assigned to HX-1 in the current base architecture.
