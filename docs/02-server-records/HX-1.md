# HX-1 — Samba Infrastructure Server

**State:** PASS / CLOSED
**IP:** `192.168.50.200`
**FQDN:** `hx-1.hx.local.arpa`

> **Not applicable:** Operating System, GPU, Storage, Runtime, Provenance, Final State — HX-1 is the retained clean Samba foundation, not a rebuilt application host. It carries no GPU, no dedicated application storage, and no model or application artifact. A fuller clean-rebuild as-built record is only created if HX-1 is ever rebuilt; see `docs/00-control/REPOSITORY-STATUS.md`. Do not fabricate the missing detail from historical HX-Infrastructure material.

## Foundation

HX-1 is the domain controller, so several foundation controls are about this
host rather than proven against it: it is the KDC, the DNS server and the fleet
time source. Those rows say so.

Three rows were first recorded NOT ESTABLISHED rather than declared
inapplicable, because they were applicable and simply had not been proven. All
three were read at the HX-1 console on 2026-09-16 and now carry their evidence.
That read closed HX5-F13.

| Control | Evidence | State |
|---|---|---|
| FQDN | `hx-1.hx.local.arpa`, and the NS record for `hx.local.arpa` resolves to it | PASS |
| DNS authority | `dig +short NS hx.local.arpa` returns `hx-1.hx.local.arpa.`; every member resolves through `192.168.50.200` | PASS |
| Kerberos / KDC | Machine accounts obtain tickets against `HX.LOCAL.ARPA`; `adcli testjoin` passes on all four members | PASS |
| Domain controller | `dig +short SRV _ldap._tcp.dc._msdcs.hx.local.arpa` advertises one DC, this host | PASS |
| Fleet time source | HX-2 through HX-5 all select `^* 192.168.50.200`, tracking reference `C0A832C8` | PASS |
| HX-1's own upstream time | 2026-09-16 console read, below: configured `pool ntp.ubuntu.com iburst maxsources 4`; four stratum-2 sources, selected `91.189.91.157`, reach `267`, offset -162us | PASS |
| SSH host key | 2026-09-16 console read, below: the key file and a scan of `192.168.50.200` both return `SHA256:krYLm3CEhfYoFoElfxieSI8+KBBb1mB1Cs/sTYKuQ58`. rsa key not read | PASS |
| Fleet key access | Not attempted; the fleet key is for member administration and HX-1 is reached directly by the owner | N/A |
| External key-only login | N/A for the same reason | N/A |
| SPNs in AD | `HOST/HX-1`, `HOST/hx-1.hx.local.arpa`, `RestrictedKrbHost/HX-1`, `RestrictedKrbHost/hx-1.hx.local.arpa`, plus the `ldap/`, `GC/` and NTDS-replication principals a domain controller carries; `dNSHostName` is `hx-1.hx.local.arpa` | PASS |

The host-key row was the one worth closing. When HX-2 and HX-3 presented
changed host keys, the absence of a recorded fingerprint cost a trip to each
console; HX-1 had the same exposure and is the host where it would matter most.
Console read, 2026-09-16, by the owner. Verbatim.

```text
$ grep -rh '^pool\|^server' /etc/chrony/chrony.conf /etc/chrony/conf.d/
pool ntp.ubuntu.com iburst maxsources 4

$ chronyc sources -v
^+ 185.125.190.57   2  10  377  525  -1192us
^+ 185.125.190.56   2  10  377  454  -3543us
^* 91.189.91.157    2  10  267  271   -162us
^+ 185.125.190.58   2  10  377  363   +571us

$ ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
256 SHA256:krYLm3CEhfYoFoElfxieSI8+KBBb1mB1Cs/sTYKuQ58 root@hx-1 (ED25519)

$ ssh-keyscan -t ed25519 192.168.50.200 | ssh-keygen -lf -
256 SHA256:krYLm3CEhfYoFoElfxieSI8+KBBb1mB1Cs/sTYKuQ58 192.168.50.200 (ED25519)
```

Both reads return the same fingerprint, so the key recorded here is the key
`sshd` serves, not only the key on disk.

One limit: the scan was run from HX-1 against its own LAN address. It proves
what `sshd` presents on `192.168.50.200:22`. It does not prove the path from a
member host to that address is clean.

Two observations came out of the same read, neither of them defects.

HX-1's upstream is the `ntp.ubuntu.com` pool, and `maxsources 4` is why chrony
shows four. Those are public internet addresses, not LAN hosts, so the fleet's
time chain ends outside the LAN. Time keeps working if that link drops - chrony
holds the local clock and every member still agrees with HX-1 - but the chain
is worth knowing when the fleet's time is questioned.

HX-1's upstream is stratum 2, which makes HX-1 stratum 3 and the members
stratum 4.

HX-1 spells its host principals `HOST/`, where the members spell theirs
`host/`. Service principal names compare case-insensitively, so the two forms
are the same principal. No action.

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
