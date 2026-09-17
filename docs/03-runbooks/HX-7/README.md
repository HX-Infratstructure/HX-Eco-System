# HX-7 Current Runbook

**Host:** hx-7
**Expected IP:** `192.168.50.207`
**FQDN:** `hx-7.hx.local.arpa`
**Role:** NGINX, development and test rendering only

## 1. HX authority and boundaries

This runbook executes the shared blocks. It does not redefine them. Where this
file and a control document disagree, the control document wins.

- Role boundary: [`NGINX-ROLE-STANDARD.md`](../../04-application-standards/NGINX-ROLE-STANDARD.md), ratified as D-004.
- Proof obligation: step `C4` in [`hx-proof.tsv`](../../00-control/hx-proof.tsv).
- Proof procedure: [`nginx-smoke-test.md`](../../../smoke-tests/nginx-smoke-test.md).
- As-built record: [`HX-7.md`](../../02-server-records/HX-7.md).
- Implementation and pins: `../common/`, with pins in `../common/hx-base.env`.

D-004 is the point of this server and it is a limit, not a feature:

> HX-7 NGINX is limited to dev/test application rendering. It is not the common
> reverse proxy for HX ecosystem services.

## 2. Foundation — inherited, not duplicated

Layer 0/1 is established once, by the shared foundation block, and this runbook
does not restate it. Run it first:

```bash
../common/00-foundation.sh hx-7
```

That establishes network validation, identity, time authority, the admin
account and sudo, the fleet key, and SSH persistence.

`01-base-admin-network-updates.sh` opens with a gate that refuses to continue
without that state. If you skip step 0 the build stops, and the exit code names
what is missing:

| Exit | Meaning |
|---|---|
| 41 | the host cannot resolve its own FQDN |
| 42 | HX-1 is not the selected time source |
| 43 | the fleet key is absent |
| 44 | the fleet key is present with the wrong fingerprint |
| 45 | neither `ssh.service` nor `ssh.socket` is enabled |

Do not work around a foundation exit. Run `00-foundation.sh` and read what it
reports.

Proof step `F0` must be satisfied before HX-7's own phase can close.

## 3. Execution

Run from this directory. Each block refuses to run on any host other than
`hx-7`.

```bash
../common/00-foundation.sh hx-7     # foundation; no reboot
./01-base-admin-network-updates.sh # reboots
./02-domain.sh              # reboots
../common/10-nginx.sh hx-7
```

## 4. Sequence

1. **Foundation.** Network validated and never written (D-026), identity, time
   authority against HX-1, admin account and NOPASSWD sudo, fleet key, SSH
   persistence.

2. **Base, admin, network, updates.** Foundation gate, then `apt update` and
   `apt upgrade`, then reboot.

3. **Domain join.** Join `hx.local.arpa`, validate SSSD and domain user
   resolution, then reboot. The block is shared and installs a driver only on
   the hosts that carry one. It installs nothing here.

4. **NGINX.** `../common/10-nginx.sh hx-7` builds NGINX from the upstream
   nginx.org source tarball, verified against its recorded SHA-256, and
   installs `hx-nginx.service`. Source is pinned in `../common/hx-base.env`.
   Not Snap. Not the Ubuntu archive (D-021).

5. **Provenance.** The block prints a provenance summary. Copy it into
   [`HX-7.md`](../../02-server-records/HX-7.md) section 6. A version string is
   not an artifact identity; the tarball and binary digests are.

6. **Proof.** Run [`nginx-smoke-test.md`](../../../smoke-tests/nginx-smoke-test.md)
   for proof step `C4`. It needs one temporary private-IP HTTP upstream on
   HX-5. Remove the upstream afterwards.

7. **Closure.** Section 9 below.

## 5. Provenance to record

Record all of these in section 6 of the server record. An unknown value is
written `UNRESOLVED`, never omitted.

```text
Component         NGINX <pinned version>
Source URI        https://nginx.org/download/nginx-<version>.tar.gz
Tarball SHA-256   the value the block verified against HX_NGINX_SHA256
Binary path       /usr/local/sbin/nginx
Binary SHA-256    the digest of the binary this build produced
Build arguments   the configure arguments reported by `nginx -V`
```

## 6. D-004 governance

HX-7 renders the UI of an application under active development. Put
development server blocks in `/srv/nginx/conf.d/` and reload.

Do **not** front any of the following from HX-7:

- Qdrant Web UI
- LightRAG
- n8n
- Open WebUI
- PostgreSQL or Redis consoles
- MCP servers
- any other normal HX ecosystem service

Remove a temporary development proxy when the work that needed it is finished.

This boundary is enforced by review, not by the block. Nothing inspects
`/srv/nginx/conf.d/`, so a server block that violates D-004 will start. Treat
the contents of that directory as reviewable configuration.

## 7. Reboot persistence

Layer 0/1 is not closed until the host returns to the same state unattended.
After the final reboot, confirm:

```bash
systemctl is-active hx-nginx
systemctl is-enabled hx-nginx
curl -fsS -o /dev/null -w '%{http_code}\n' http://192.168.50.207/
```

`systemctl is-active` on its own is not proof. A service that crashes and
restarts reports `active` in the gaps between restarts, which is how HX4-F06
went unseen. The HTTP response is what shows it is serving.

## 8. HX-7 BASE PASS definition

All of the following, or the server does not close:

| Requirement | Evidence |
|---|---|
| Foundation established | proof step `F0` satisfied |
| Every Foundation row filled | `tools/hx-doc/hx-record-check` passes for HX-7 |
| External key-only administration | `tools/hx-doc/hx-fleet-access hx-7` returns `hx-7` and `KEY+SUDO-PASS` |
| Domain join | `realm list` reports `configured: kerberos-member`; domain user resolves |
| NGINX serving | `hx-nginx` active and enabled, HTTP answering on the LAN address |
| Provenance recorded | section 6 of the record carries the tarball and binary digests |
| Reboot persistence | section 7 above, after an unattended reboot |
| Routing proof | step `C4` run, evidence retained, temporary upstream removed |

## 9. Record and fleet closure

1. Fill [`HX-7.md`](../../02-server-records/HX-7.md), including every Foundation
   row and section 6 provenance.
2. Set `state` and `gate` for `HX-7` in [`hx-fleet.tsv`](../../00-control/hx-fleet.tsv).
3. Set `C4` status in [`hx-proof.tsv`](../../00-control/hx-proof.tsv).
4. Run `tools/hx-doc/hx-fleet`, `tools/hx-doc/hx-record-check` and
   `tools/hx-doc/hx-render-html`.

## 10. Non-goals

- HX-7 is not the ecosystem reverse proxy. That is D-004 and it is not
  negotiable in this runbook.
- Do not mount or wipe unrelated disks.
- Do not import prior application state.
- Do not add TLS termination for an ecosystem service here. A development
  certificate for a development app is in scope; a production front door is
  not.
