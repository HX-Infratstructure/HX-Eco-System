# HX-1 — Samba Infrastructure Server

**State:** PASS / CLOSED — but see HX5-F13; three Foundation controls are
recorded NOT ESTABLISHED and this state predates them being asked for.
**IP:** `192.168.50.200`
**FQDN:** `hx-1.hx.local.arpa`

> **Not applicable:** Operating System, GPU, Storage, Runtime, Provenance, Final State — HX-1 is the retained clean Samba foundation, not a rebuilt application host. It carries no GPU, no dedicated application storage, and no model or application artifact. A fuller clean-rebuild as-built record is only created if HX-1 is ever rebuilt; see `docs/00-control/REPOSITORY-STATUS.md`. Do not fabricate the missing detail from historical HX-Infrastructure material.

## Foundation

HX-1 is the domain controller, so several foundation controls are about this
host rather than proven against it: it is the KDC, the DNS server and the fleet
time source. Those rows say so. The rows this record cannot fill are marked
NOT ESTABLISHED rather than declared inapplicable, because they are applicable
and simply have not been proven.

| Control | Evidence | State |
|---|---|---|
| FQDN | `hx-1.hx.local.arpa`, and the NS record for `hx.local.arpa` resolves to it | PASS |
| DNS authority | `dig +short NS hx.local.arpa` returns `hx-1.hx.local.arpa.`; every member resolves through `192.168.50.200` | PASS |
| Kerberos / KDC | Machine accounts obtain tickets against `HX.LOCAL.ARPA`; `adcli testjoin` passes on all four members | PASS |
| Domain controller | `dig +short SRV _ldap._tcp.dc._msdcs.hx.local.arpa` advertises one DC, this host | PASS |
| Fleet time source | HX-2 through HX-5 all select `^* 192.168.50.200`, tracking reference `C0A832C8` | PASS |
| HX-1's own upstream time | Not observed | NOT ESTABLISHED |
| SSH host key | Presents ed25519 `SHA256:krYLm3CEhfYoFoElfxieSI8+KBBb1mB1Cs/sTYKuQ58` and rsa `SHA256:FonPshtSPT5/Fi8ianIsBdjCc5DH+PZw9sPxB5Tsm2E`, neither confirmed at the console | NOT ESTABLISHED |
| Fleet key access | Not attempted; the fleet key is for member administration and HX-1 is reached directly by the owner | N/A |
| External key-only login | N/A for the same reason | N/A |
| SPNs in AD | Not read; querying the DC's own object needs directory access this record has not had | NOT ESTABLISHED |

The host-key row is the one worth closing. When HX-2 and HX-3 presented changed
host keys, the absence of a recorded fingerprint cost a trip to each console;
HX-1 has the same exposure and is the host where it would matter most. The two
fingerprints above were read from the network and are recorded as *presented*,
not as *verified* - confirming them at the console is what turns this row PASS.

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
