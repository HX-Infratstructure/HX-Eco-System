# HX-1 — Samba Infrastructure Server

**State:** PASS / CLOSED  
**IP:** `192.168.50.200`  
**FQDN:** `hx-1.hx.local.arpa`

## Role
- Samba Active Directory Domain Controller
- DNS for HX domain
- Kerberos
- Fleet NTP source

## Domain
- Realm: `HX.LOCAL.ARPA`
- Domain: `hx.local.arpa`
- NetBIOS: `HX`
- DNS forwarder: `192.168.50.1`

## Current validation
- Samba database health: PASS
- Samba service active/enabled: PASS
- Domain/DNS/Kerberos foundation retained as clean baseline
- Fleet clients use HX-1 for HX domain DNS

No additional workload is assigned to HX-1 in the current base architecture.
