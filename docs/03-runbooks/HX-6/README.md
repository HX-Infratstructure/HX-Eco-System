# HX-6 Current Runbook — OmniRoute

> **Superseded for the deployment path.** HX-6 runs the **npm global install of
> `omniroute@3.8.50`**, started by `hx-omniroute.service` from
> `/usr/local/bin/omniroute`. `D-031` ratified that on 2026-09-17 and is the
> authority. Phase 10 acceptance is recorded in
> [`HX-6-ACCEPTANCE.md`](../../02-server-records/HX-6-ACCEPTANCE.md):
> ACCEPTED WITH FOLLOW-UP ITEMS.
>
> The source-build material below describes building `3.8.51` from a pinned
> commit into `/srv/omniroute/app`. **HX-6 does not run that.** It is kept as
> history because the defects it found are real and transfer to any host that
> builds from source under npm 11 — `HX6-F01`, `HX6-F02`, `HX6-F03`.
>
> `../common/10-omniroute.sh` refuses to run and exits 47. Do not execute it.
> Live configuration, findings and the A2A/MCP setup are recorded in
> [`HX-6.md`](../../02-server-records/HX-6.md).

**Host:** `hx-6`  
**Expected IP:** `192.168.50.206`  
**FQDN:** `hx-6.hx.local.arpa`  
**Role:** OmniRoute AI gateway / routing control plane / MCP-A2A interface  
**Deployment:** native Ubuntu Linux + systemd; no Docker, Podman, Kubernetes, or Snap  
**Target OmniRoute release:** `3.8.50`, npm global install (D-031). The `3.8.51` source build described below is historical.
**Upstream:** `https://github.com/diegosouzapw/OmniRoute.git`  
**Persistent application root:** `/srv/omniroute`

This runbook owns the **HX-6-specific OmniRoute build, configuration, validation and BASE PASS boundary**. It does **not** reimplement the fleet foundation.

> **Ownership rule:** common foundation owns fleet controls; HX-6 owns OmniRoute-specific installation, configuration, capability validation and BASE PASS.

The fleet foundation implemented on `main` after the 2026-09-16 Layer 0/1 remediation is authoritative for hostname/FQDN, network validation, HX-1 time authority, the `hxsa` administration account, fleet-key presence, SSH persistence, base patching, domain join and the current NVIDIA package policy. HX-6 consumes those controls rather than duplicating them here.

## 1. HX authority and boundaries

Current HX decisions that apply directly to OmniRoute:

- **D-002:** native Linux + systemd only.
- **D-003:** a product-specific MCP server and native Web UI are part of the parent application's base build where applicable.
- **D-009:** BASE PASS requires one temporary route to one already-proven Ollama endpoint, direct-versus-routed known-answer evidence, and cleanup of the temporary route.
- **D-010:** supported or discovered providers/models are not automatically HX-approved. Maintain an explicit provider allowlist and an explicit model allowlist.
- **D-018:** do not add UFW or unrelated network restrictions. This does not make anonymous OmniRoute API access mandatory.
- **D-019:** HX-6 uses the Diego Souza OmniRoute project, installed from the pinned npm package on Node.js from the official Node binary distribution.
- **D-021:** Snap is never a package source.

The current foundation scripts on `main` also implement newer fleet controls discovered during the Layer 0/1 audit. Those controls are now recorded in `docs/00-control/DECISIONS.md` as D-026 through D-029, documenting the already-implemented common behavior; this runbook inherits them rather than redefining them.

Owner direction for HX-6:

- OmniRoute API-key authentication is required for the LAN-facing API.
- The main Dashboard/API service is LAN-facing on port `20128`.
- The dedicated live-dashboard WebSocket service on `20132` remains loopback-only unless a later owner decision changes that posture.
- `/srv/omniroute` is already provisioned. **Do not format, wipe, repartition, replace or remount it as part of this runbook.** Validate it and use it.
- Advanced OmniRoute capabilities that are not necessary for HX-6 BASE PASS stay deferred until separately adopted.

## 2. Product model — HX-6 scope

OmniRoute is more than a routing daemon. HX-6 BASE covers the product surfaces required to operate it as the ecosystem routing control plane.

| Capability | HX-6 BASE scope |
|---|---|
| Gateway / routing API | Required |
| Dashboard | Required |
| OpenAI-compatible `/v1` API | Required |
| CLI / diagnostics | Required |
| SQLite-backed persistent state | Required |
| Provider management | Required |
| Model management | Required |
| Explicit HX provider allowlist | Required |
| Explicit HX model allowlist | Required |
| Product-native MCP server | Required |
| A2A Agent Card and endpoint | Required |
| D-009 direct-vs-routed Ollama proof | Required |
| API-key authentication | Required |
| Live WS `20132` LAN exposure | Not in BASE; loopback only |
| Memory/Qdrant integration | Deferred |
| Skills marketplace / external skill packs | Deferred |
| Cloud agents | Deferred |
| Tunnels | Deferred |
| MITM / Traffic Inspector | Deferred |
| Free-provider automation / Radar | Deferred |
| Electron desktop app | Out of scope |
| Docker / Kubernetes deployment | Prohibited by HX policy |

HX-15 FastMCP remains the HX shared/custom MCP development host. OmniRoute's own MCP server remains inside the HX-6 application boundary and does not replace HX-15.

## 3. Foundation boundary — inherited, not duplicated

### 3.1 Current common sequence

The current fleet sequence on `main` is:

```text
Step 0  common/00-foundation.sh <host>
Step 1  tools/hx-doc/hx-fleet-access <host>   # from the operator workstation
Step 2  common/01-base-admin-network-updates.sh <host>   # reboots
Step 3  common/02-domain.sh <host>                 # reboots
Step 4  common/03-storage-ollama.sh                       # inference hosts only; SKIP on HX-6
Step 5  application block
```

For HX-6, the application block is `common/10-omniroute.sh hx-6` **only after the OmniRoute-specific pre-read in section 5 passes**.

The common scripts own their implementation. Do not copy their package lists, host-file logic, Chrony logic, fleet-key logic, SSH enablement, patching commands or domain-join commands into this runbook.

### 3.2 Step 0 — establish the foundation

From the repository on HX-6:

```bash
cd ~/src/HX-Eco-System
./docs/03-runbooks/common/00-foundation.sh hx-6
```

The common foundation currently:

- validates the recorded IP, gateway and HX-1 DNS and **does not rewrite network configuration**;
- establishes `hx-6` and local FQDN resolution as `hx-6.hx.local.arpa`;
- installs/configures Chrony when required and requires HX-1 `192.168.50.200` to become the selected `^*` time source;
- establishes the `hxsa` NOPASSWD sudo policy;
- installs the committed HX fleet public key and validates its fingerprint;
- enables SSH persistence using the Ubuntu service/socket model.

A failed common foundation block is a stop. Do not reproduce its corrective logic manually in this runbook.

### 3.3 Step 1 — prove fleet access from off-host

This is the one foundation control HX-6 cannot prove about itself. Run it from the approved operator workstation environment:

```bash
tools/hx-doc/hx-fleet-access hx-6
```

Required output:

```text
hx-6
KEY+SUDO-PASS
```

Retain the output as foundation evidence. A locally active SSH service is not a substitute for this proof.

### 3.4 Steps 2 and 3 — common base/domain blocks

The HX-6 wrappers remain thin dispatchers into common authority:

```bash
cd ~/src/HX-Eco-System/docs/03-runbooks/HX-6
./01-base-admin-network-updates.sh
./02-domain.sh
```

`01-base-admin-network-updates.sh` opens with the foundation gate and refuses to continue unless FQDN, HX-1 NTP selection, the approved fleet key and SSH persistence are present. It also applies the common patch flow and current NVIDIA-package hold policy before reboot.

`02-domain.sh` remains the current shared authority for domain join, SSSD/domain-user resolution and the fleet's pinned NVIDIA package policy. HX-6 does not redefine that block here.

**Important:** if live HX-6 foundation/base work has already been completed under the current common standard, do not replay a destructive or unnecessary block merely because this document lists the canonical sequence. Reconcile live evidence and the HX-6 server record first. Target-state text is not proof that a block still needs to run.

### 3.5 Foundation acceptance before OmniRoute

Before the application phase, the HX-6 server record must carry observed evidence for the current Foundation section, including:

- `hostname -f` = `hx-6.hx.local.arpa`;
- AD DNS A record at the recorded fleet address;
- HX-1 selected as the time source;
- approved fleet-key fingerprint;
- `sudo -k -n true` PASS;
- SSH persistence;
- external `KEY+SUDO-PASS` proof;
- recorded SSH host key;
- AD computer identity with FQDN `dNSHostName` and the required short/FQDN `host/` and `RestrictedKrbHost/` SPNs.

The repository proof chain treats foundation step `F0` as a prerequisite for unbuilt-server proof. Do not close HX-6 application work around an unproven foundation.

### 3.6 Known fleet findings are not HX-6 application work

Do not remediate unrelated fleet findings while installing OmniRoute. In particular, the current fleet still tracks reverse-DNS/GSSAPI canonicalization and SSSD responder/socket behavior separately. If either affects HX-6 execution, stop and reference the existing finding rather than silently changing the shared domain model from this runbook.

## 4. Existing `/srv/omniroute` storage

The owner has already provisioned `/srv/omniroute`. This runbook consumes that storage; it does not create a new filesystem.

Validate before application installation:

```bash
findmnt /srv/omniroute
lsblk -f
sudo ls -ld /srv/omniroute
```

Record the backing device, filesystem, UUID, mount source, mount options, capacity and persistence mechanism. Stop if `/srv/omniroute` is not the intended persistent application storage.

Do not mount, format, wipe, repartition, replace or repurpose storage from this runbook.

## 5. OmniRoute application pre-read — current hard stops

Do not execute `common/10-omniroute.sh hx-6` until all items in this section are reconciled.

### 5.1 Version baseline

HX-6 deploys **OmniRoute 3.8.51**, built from the official upstream release
branch. Owner decision of 2026-09-17.

`3.8.51` is not published to the npm registry. `npm view omniroute@3.8.51`
returns `E404`, `dist-tags.latest` is `3.8.50`, and the newest publish of any
version is 2026-08-28. **npm publication is not required for this deployment**,
and there is no fallback to the published `3.8.50`.

```text
repository  https://github.com/diegosouzapw/OmniRoute
branch      release/v3.8.51
commit      3d5baf13f41bf0e35c8b1e57f1d5119dbdaaaf3f
```

The authority chain is:

```text
hx-base.env -> common/10-omniroute.sh -> built version verification
```

`hx-base.env` pins the version, the repository, the branch and the commit.
`../common/10-omniroute.sh` checks out that commit, refuses a branch tip,
refuses a dirty tree, builds, and verifies the built CLI reports `3.8.51`
before the unit is written or the block can report success. This runbook
documents that state; it does not independently control it.

The branch is how the commit is found. The commit is what is built. A moving
tip would let two runs of the same block produce different servers under one
recorded version, which is why the block checks the resolved SHA back after
checkout and stops on any mismatch.

### 5.2 Current common OmniRoute block is incomplete for the accepted HX-6 contract

The current `../common/10-omniroute.sh` installs Node, installs the pinned npm package, creates `hx-omniroute.service`, sets `HOME`, `PORT` and `HOST=0.0.0.0`, and validates `/v1/models`.

That is not sufficient for the HX-6 contract in this runbook. Before execution, the common application block must be reconciled so that it also establishes or explicitly preserves:

- persistent `DATA_DIR` under `/srv/omniroute`;
- the accepted API-key authentication posture;
- required secret handling outside the repository;
- the accepted `20128` LAN listener posture;
- the accepted `20132` loopback-only posture;
- persistent runtime semantics verified against the pinned package rather than assumptions inherited from another version.

Until that shared block is reconciled, **do not run it** and then manually patch around it. The reviewed common block should produce the intended service state.

### 5.3 Native bind variable must be verified, not guessed

Do not carry `APP_BIND_HOST=0.0.0.0` forward as a native-systemd control. Current upstream uses `APP_BIND_HOST` for Docker/Compose host publishing, while upstream native/runtime material uses other host variables such as `HOSTNAME` and development code also references `HOST`.

The exact bind variable used by the packaged CLI must be confirmed before the shared HX application block is changed. The final runbook/service should document the variable actually proven on the packaged native runtime.

**Resolved 2026-09-17, from `release/v3.8.51` source at the pinned commit.**

`bin/cli/utils/serverHost.mjs`:

```js
export function resolveServerHost(env = process.env, runtimePlatform = platform(), machineHostname = hostname()) {
  if (env.OMNIROUTE_SERVER_HOST) return env.OMNIROUTE_SERVER_HOST;
  if (runtimePlatform === "win32" && env.HOSTNAME && env.HOSTNAME !== machineHostname) {
    return env.HOSTNAME;
  }
  return "0.0.0.0";
}
```

On Linux the only configuration input is `OMNIROUTE_SERVER_HOST`. `HOSTNAME` is
a Windows-only legacy fallback, and the source says why: it is a standard shell
variable on Unix-like systems, so only the dedicated OmniRoute variable is
treated as configuration there. `APP_BIND_HOST` is Docker/Compose host
publishing and is not the native serve control.

The published `3.8.50` did read `HOSTNAME` directly, in `dist/server.js`.
Deploying that pin would have worked and then quietly changed meaning on
upgrade, which is the concern this section was written for.

`HX_OMNIROUTE_BIND_VAR="OMNIROUTE_SERVER_HOST"` in `hx-base.env`. The gate
stays: an empty value still stops the block at exit 36, so a future version
whose variable changes cannot be papered over by a default.

### 5.4 Application pre-read commands

Run these from the repository root so they do not depend on the caller's
working directory:

```bash
cd ~/src/HX-Eco-System
node --version 2>/dev/null || true
npm --version 2>/dev/null || true
findmnt /srv/omniroute
grep '^HX_OMNIROUTE_VERSION=' docs/03-runbooks/common/hx-base.env
sed -n '1,260p' docs/03-runbooks/common/10-omniroute.sh
```

Do not execute if the block would:

- build a commit other than the pin in `hx-base.env`, or install the published `3.8.50`;
- use Docker, Podman, Kubernetes or Snap;
- use `npm run dev` as the permanent service;
- wipe or replace `/srv/omniroute`;
- expose the API anonymously to the LAN;
- expose `20132` to the LAN without a later owner decision;
- omit persistent application state under `/srv/omniroute`;
- omit the required secret/configuration boundary.

## 6. Node.js and package provenance

Node.js comes from the official Node binary tarball through the HX shared helper. It is not installed from Snap, NodeSource or the Ubuntu application archive.

Required proof:

```bash
node --version
npm --version
command -v node
command -v npm
```

Provenance is an artifact identity, not a version string.

**Node.js** keeps artifact provenance: record its source URI and the full
SHA-256 of the tarball actually installed. `hx_node_install` fetches a
checksum-verified binary from nodejs.org. 3.8.51 requires
`>=22.22.2 <23 || >=24.0.0 <27`; `HX_NODE_VERSION` is inside that range.

**OmniRoute does not, because this deployment is source-based.** There is no
published artifact to hash. **The commit is the provenance.** Registry
`dist.tarball` and `dist.integrity` do not apply and are not recorded.

Record in the HX-6 server record, section 6:

```text
Component:        OmniRoute 3.8.51
Source URI:       https://github.com/diegosouzapw/OmniRoute
Branch:           release/v3.8.51
Source commit:    3d5baf13f41bf0e35c8b1e57f1d5119dbdaaaf3f
package.json:     3.8.51
Built CLI:        3.8.51   (node <app>/bin/omniroute.mjs --version)
App directory:    /srv/omniroute/app
Node:             as installed
npm:              as installed
Install method:   source build from the release branch, npm ci + npm run build
```

`../common/10-omniroute.sh` prints exactly that block at install time. If a
value cannot be established, record `UNRESOLVED` for it; do not fabricate one.

The build is `npm ci` against the committed lockfile, then `npm run build`,
which produces the standalone bundle at `dist/server.js`. The block stops if
that file is absent afterwards, because `omniroute serve` would otherwise fall
back to a path that does not exist here.

If the pinned commit does not check out, or the built CLI does not report
`3.8.51`, deployment is blocked. Do not fall back to the published `3.8.50`,
to a branch tip, to `latest`, or to `npm run dev`.

Required package proof:

```bash
command -v omniroute
omniroute --version
npm list -g --depth=0 omniroute
```

Record the npm package identity/version and available integrity/provenance evidence in the HX-6 server record.

## 7. Runtime ownership and persistence

Use a dedicated `omniroute` service identity and the existing `/srv/omniroute` application root.

Persistent application state belongs under:

```text
/srv/omniroute/
└── data/                # OmniRoute DATA_DIR; SQLite, backups and runtime state
```

Do not redirect OmniRoute persistence to HX-9 PostgreSQL. HX-9 remains a separate ecosystem service.

Create application directories only if they do not already exist. Preserve the owner-provisioned storage and record the observed ownership/mode rather than assuming it.

For an existing `/srv/omniroute/data`, do not chown or chmod it to force a result. Prove the `omniroute` service identity can already write it, and stop if it cannot:

```bash
# Record the existing ownership/mode first.
sudo stat -c '%U:%G %a' /srv/omniroute/data
# Write probe as the actual service identity; a failure is a stop. The probe
# path is unique to this run so it cannot overwrite an owner-provisioned file.
PROBE="/srv/omniroute/data/.hx-write-probe.$$"
sudo -u omniroute touch "$PROBE" \
  || { echo 'FAIL: omniroute identity cannot write DATA_DIR'; exit 1; }
sudo -u omniroute rm -f -- "$PROBE" \
  || { echo 'WARN: probe cleanup failed; remove '"$PROBE"' manually'; exit 1; }
```

Only when the write probe fails and the owner directs a change may ownership/mode be adjusted, and then the change and its approval are recorded.

Target application-owned identity:

```text
omniroute:omniroute
```

## 8. Runtime configuration contract

The permanent service must consume a root-owned, non-repository environment file or equivalent systemd environment source. No secret value is committed to the repository or copied into the server record.

When the source is an environment file, it must be least-privilege: owner and group `root:root`, mode `0600`. Record only the path, owner and mode — never a secret value or its hash.

The final reviewed native service configuration must explicitly cover at least:

```text
HOME=/srv/omniroute
DATA_DIR=/srv/omniroute/data
PORT=20128
<verified native bind variable>=0.0.0.0
REQUIRE_API_KEY=true
LIVE_WS_HOST=127.0.0.1
LIVE_WS_PORT=20132
JWT_SECRET=<generated locally; secret>
API_KEY_SECRET=<generated locally; secret>
INITIAL_PASSWORD=<owner/operator supplied; secret>
OMNIROUTE_WS_BRIDGE_SECRET=<generated locally; secret>
```

`10-omniroute.sh` writes all eleven, split by whether the value is a secret.

The seven non-secret entries become `Environment=` lines in
`/etc/systemd/system/hx-omniroute.service`, with the bind variable taken from
`HX_OMNIROUTE_BIND_VAR` and refused while that is empty.

The four secrets do not. `/etc/systemd/system` is world-readable and
`systemctl show` prints `Environment=` values, so they go in
`/srv/omniroute/omniroute.env` at `root:root` `0600`, referenced by a single
`EnvironmentFile=` line.

Root rather than the service identity: systemd reads an `EnvironmentFile` as
PID 1 and then drops to `User=`, so `omniroute` never needs to read it, and
giving it access would widen an application compromise for no gain. The block
prints the result of:

```bash
sudo stat -c '%U:%G %a %n' /srv/omniroute/omniroute.env
```

Expected: `root:root 600 /srv/omniroute/omniroute.env`. Three are generated with
`openssl rand -hex 32` on first run and deliberately not regenerated
afterwards, because rotating them would invalidate every key and token already
issued against them.

`INITIAL_PASSWORD` is the exception. It is owner-supplied, never generated and
never stored in this repository. Export it for the run:

```bash
export HX_OMNIROUTE_INITIAL_PASSWORD='<owner supplied>'
```

The block stops with exit 37 if it is absent.

The exact runtime semantics of the pinned package must be verified against the packaged runtime immediately before implementation. If upstream behavior contradicts this target, stop and reconcile the shared block and this runbook rather than improvising on HX-6.

Preferred authenticated client contract:

```http
Authorization: Bearer <HX-issued OmniRoute endpoint key>
```

Required listener posture:

```text
20128/tcp  Dashboard + canonical API  LAN-facing
20132/tcp  Live dashboard WebSocket   loopback-only
```

Prove actual listeners with `ss`; environment text alone is not evidence.

## 9. systemd service

OmniRoute runs as a native systemd service named:

```text
hx-omniroute.service
```

Required properties:

- dedicated `omniroute` user;
- working/home boundary under `/srv/omniroute`;
- explicit persistent `DATA_DIR`;
- secret values sourced outside the repository;
- boot enablement;
- restart policy consistent with the current HX application-service helper;
- no development-mode runner;
- no container runtime.

Validate without printing secrets:

```bash
sudo systemctl status hx-omniroute --no-pager -l
sudo systemctl is-enabled hx-omniroute
sudo systemctl is-active hx-omniroute
sudo systemctl cat hx-omniroute
```

Listener posture is a pass/fail check, not an observation. The following must exit non-zero on any deviation:

```bash
set -e
# 20128 must be present and reachable on an HX-6 LAN address: wildcard bind
# (0.0.0.0 / [::]) or the recorded HX-6 LAN address itself. A bind to some
# other specific address fails.
sudo ss -lntH | grep -E ':20128\s' \
  | grep -qE '0\.0\.0\.0:20128|\[::\]:20128|192\.168\.50\.206:20128'
# 20132 must be present, and EVERY listening endpoint on 20132 must be
# loopback. Fail if the port is absent or if any bind is non-loopback —
# this is all-endpoints-must-be-loopback, not a denylist.
ss_out="$(sudo ss -lntH | grep -E ':20132\s')"
[ -n "$ss_out" ] || { echo 'FAIL: 20132 not listening'; exit 1; }
! printf '%s\n' "$ss_out" | grep -qvE '127\.0\.0\.1:20132|\[::1\]:20132'
```

A missing `20128` listener, a `20128` bound only to an address other than wildcard or the recorded HX-6 LAN address, a missing `20132` listener, or any single `20132` endpoint bound to a non-loopback address each fail this gate.

## 10. First-party CLI diagnostics

A running process is not an OmniRoute BASE PASS. Use the installed product's own control plane as evidence.

At minimum establish the current equivalents of, in the pinned package:

```bash
omniroute --version
omniroute doctor --json
omniroute status
omniroute providers validate
omniroute mcp status
omniroute a2a status
```

If the command surface differs in the pinned package, use `omniroute --help`, record the exact supported command and update the runbook/shared implementation if required. Do not bypass a failed diagnostic because the HTTP port is open.

## 11. Dashboard and HTTP/API proof

Prove localhost first, then the LAN surface using the approved API-key contract.

Required surfaces:

```text
Dashboard:  http://192.168.50.206:20128
API base:   http://192.168.50.206:20128/v1
Models:     /v1/models
Health:     current health surface identified by product diagnostics/docs
```

At minimum prove:

- unauthenticated protected API behavior matches the configured policy;
- authenticated `/v1/models` succeeds;
- an unauthenticated dashboard request is challenged semantically: PASS is a redirect to login, an authentication challenge, or a login page (which may legitimately return HTTP 200 with a login body); FAIL is an unauthenticated request exposing the usable authenticated dashboard/application state;
- an authenticated session loads the dashboard successfully;
- the expected OmniRoute version is observed where the product exposes it;
- service remains stable while accessed over the LAN.

Dashboard and API auth behavior are proved per surface as configured; do not assume one result implies the other beyond what is observed. A single HTTP 200 does not close the application.

## 12. Provider and model governance — D-010

Before HX-6 closes:

1. Build an explicit HX-approved provider allowlist.
2. Build an explicit HX-approved model allowlist.
3. Confirm free/no-auth/discovered providers are not automatically approved.
4. Confirm provider approval does not implicitly approve its entire model catalog.
5. Confirm cloud providers/cloud models are inactive unless explicitly approved.
6. Retain evidence showing the effective approved provider/model set.

Discovery is not approval.

## 13. Product-native MCP proof — D-003

OmniRoute's product-native MCP capability is part of HX-6 BASE PASS. HX-15 FastMCP does not substitute for it.

Use the MCP transport supported by the pinned package and retain the exact endpoint/transport actually used. Expected product surfaces include network MCP endpoints such as `/api/mcp/stream` and `/api/mcp/sse`, subject to confirmation against the pinned package.

Required proof:

1. product MCP status reports healthy/ready state;
2. establish an authenticated MCP client connection;
3. execute at least one read-only known-answer tool, preferably health/status;
4. confirm the result describes the HX-6 OmniRoute instance;
5. retain evidence without exposing credentials.

Do not install a separate generic MCP server on HX-6 to satisfy this gate.

### 13.1 Authentication coverage per surface

Each surface is proved against its own configured policy — API, dashboard, MCP and A2A are not assumed to share one mechanism:

| Surface | Required acceptance |
|---|---|
| API (`/v1`) | unauthenticated request behaves per configured policy; authenticated key succeeds |
| Dashboard | unauthenticated request challenged (redirect, auth challenge, or login page) and authenticated state not exposed; authenticated session loads |
| MCP | connection per the configured MCP auth policy; unauthenticated behavior recorded |
| A2A | Agent Card and task endpoint per the configured A2A auth policy; behavior recorded |

For each surface, record the observed unauthenticated and authenticated behavior. Where a surface is configured unauthenticated, that is the recorded policy — do not invent a requirement it does not have.

## 14. A2A proof

A2A is a native OmniRoute product surface included in the HX-6 contract.

Confirm the pinned package exposes and successfully serves the current equivalents of:

```text
GET  /.well-known/agent.json
POST /a2a
```

Required evidence:

1. Agent Card is reachable and valid;
2. A2A service reports healthy/ready state through the product CLI or API;
3. one bounded known-answer A2A task succeeds through the supported JSON-RPC contract;
4. retain task/result status.

Do not use this BASE proof to create permanent multi-agent architecture that HX has not approved.

## 15. D-009 routing proof

After service health, authentication, CLI diagnostics, catalog governance, MCP and A2A are healthy, prove the primary routing contract.

Use one already-proven HX Ollama endpoint. The route exists only for this test unless separately approved as permanent architecture.

### 15.1 Direct request

Send a deterministic/known-answer request directly to the chosen Ollama endpoint and retain the target, model, request, response and timestamp.

### 15.2 Routed request

Create one explicitly approved temporary OmniRoute connection/route to that same endpoint and send the equivalent request through HX-6.

Retain the OmniRoute endpoint, connection/provider identity, model mapping, response and routing decision/trace metadata where exposed.

### 15.3 Compare and clean up

Establish that the routed path reached the intended backend and returned the expected answer/behavior.

Cleanup of the temporary route is **unconditional**. It must happen whether the routed request, the comparison or any verification step succeeded or failed — a failed test is never a reason to leave a temporary route active. Structure the execution so the removal step runs on both the success and the failure path, and record which path it ran on.

Where the execution is shell, use a `trap` so cleanup runs even on a mid-script failure or interrupt:

```bash
ROUTE_ID=<temporary-route-id>
route_absent() {
  # route-not-active check; non-zero while the route is still resolvable
  ! omniroute <route-list-command> | grep -q "$ROUTE_ID"
}
cleanup_route() {
  omniroute <route-remove-command> "$ROUTE_ID" || return 1
  route_absent || { echo 'FAIL: temporary route still active after removal'; return 1; }
}
trap cleanup_route EXIT
# ... routed request and comparison; any failure path still exits through the trap ...
# On the success path: run cleanup explicitly (removal + absence verification),
# and only release the trap when both pass.
if cleanup_route; then
  trap - EXIT
else
  echo 'FAIL: D-009 cleanup did not verify; gate fails' >&2
  exit 1   # EXIT trap remains active as the fallback
fi
```

The EXIT trap remains in place as the failure-path fallback until cleanup (removal **and** route-absent verification) has passed; a removal or verification failure is a non-zero result that fails the D-009 cleanup gate, not a warning. The equivalent requirement for any other execution style is a `finally`-style or explicitly sequenced cleanup block that executes after a failed request/comparison exactly as it does after a successful one.

After removal, prove the temporary route is no longer active. That verification runs regardless of how the request or comparison ended; if it cannot confirm removal, the D-009 cleanup gate fails and HX-6 does not close.

## 16. Reboot-persistence gate

Before reboot capture:

```bash
sudo systemctl is-enabled hx-omniroute
sudo systemctl is-active hx-omniroute
findmnt /srv/omniroute
```

Apply the same listener pass/fail checks as section 9 (20128 present and reachable on an HX-6 LAN address; 20132 present and loopback-only; any non-loopback 20132 bind fails) before rebooting.

Reboot once. After HX-6 returns, re-prove:

- applicable common foundation controls remain valid;
- external fleet-key access still returns `KEY+SUDO-PASS`;
- domain identity remains healthy;
- `/srv/omniroute` mount persists;
- `hx-omniroute.service` is active/enabled;
- exact OmniRoute version;
- `20128` LAN listener;
- `20132` loopback-only listener;
- persistent application state survived;
- dashboard/API authentication still works;
- provider/model allowlists survived;
- MCP status and one read-only MCP call;
- A2A Agent Card and service status;
- no temporary D-009 route was resurrected.

Do not rerun `00-foundation.sh` after reboot merely as a substitute for proof. Re-run a common remediation block only when an observed foundation control actually fails and the current common authority says that block is the remedy.

## 17. HX-6 BASE PASS definition

HX-6 is not BASE PASS because `systemctl` is green or `/v1/models` returns 200.

| Gate | Required result |
|---|---|
| Common Foundation / F0 | PASS with recorded evidence |
| External fleet-key proof | `hx-6` + `KEY+SUDO-PASS` |
| Domain join / SSSD core function | PASS, or `HX4-F02` (SSSD responder/socket conflict, OPEN/DEFERRED) documented as non-impacting HX-6 with recorded evidence; no other finding satisfies this gate |
| Existing `/srv/omniroute` storage | PASS; no destructive storage change |
| Node.js exact supported version | PASS |
| Node.js provenance (source URI + SHA-256) | PASS; UNRESOLVED blocks closure |
| OmniRoute built from the pinned commit, CLI reports `3.8.51` | PASS |
| OmniRoute provenance (source URI + SHA-256) | PASS; UNRESOLVED blocks closure |
| Native `hx-omniroute.service` | PASS |
| Persistent `DATA_DIR` under `/srv/omniroute` | PASS |
| API-key authentication | PASS |
| Dashboard/API `20128` | PASS |
| Live WS `20132` loopback-only posture | PASS |
| First-party CLI diagnostics | PASS |
| Explicit provider allowlist | PASS |
| Explicit model allowlist | PASS |
| Product-native MCP | PASS |
| A2A | PASS |
| D-009 direct-vs-routed functional proof | PASS |
| D-009 cleanup verification | PASS |
| Reboot persistence | PASS |
| Server record/evidence | COMPLETE |

Only after every required gate passes should HX-6 be promoted to `PASS / CLOSED`.

## 18. Evidence and record closure

Update `docs/02-server-records/HX-6.md` from observed evidence only. Do not copy target-state text from this runbook into the record as though it were runtime proof.

The current server record still represents an unproven/not-started host until observed evidence is entered. The owner's statement that `/srv/omniroute` has been provisioned is an execution input, not permission to mark unrelated foundation rows PASS without their evidence.

The final record/evidence must include at least:

- Foundation/F0 evidence from the current common standard;
- external `hx-fleet-access` proof;
- domain identity and SPN evidence;
- `/srv/omniroute` filesystem/UUID/mount evidence;
- Node version/source;
- Node.js provenance: source URI and full SHA-256, or `UNRESOLVED`;
- OmniRoute version, package source and provenance: source URI and full SHA-256, or `UNRESOLVED`;
- systemd unit and effective runtime configuration with secrets redacted;
- persistent data path;
- actual listeners;
- authentication posture;
- CLI diagnostic results;
- approved provider allowlist;
- approved model allowlist;
- MCP proof;
- A2A proof;
- D-009 direct/routed comparison;
- D-009 cleanup proof;
- reboot-persistence proof.

Then set HX-6 state/gate in `docs/00-control/hx-fleet.tsv` only when the actual closure evidence supports it, regenerate repository-derived artifacts and run the repository checks required by `AGENTS.md`.

## 19. Explicit non-goals

Do not add these merely because OmniRoute supports them:

- Docker, Compose, Podman or Kubernetes;
- Electron desktop deployment;
- NGINX as a mandatory common gateway in front of HX-6;
- external PostgreSQL for OmniRoute state;
- Qdrant-backed OmniRoute memory;
- cloud agents;
- tunnels;
- MITM/traffic-inspection features;
- external skill marketplaces;
- automatic activation of free/no-auth providers;
- LAN exposure of `20132`;
- unrelated firewall/TLS/segmentation changes.

Each can be evaluated later under its own HX decision if a real requirement appears.
