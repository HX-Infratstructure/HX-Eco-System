# HX-6 — OmniRoute Server Configuration

**Build state:** PASS
**Gate:** ACCEPTED WITH FOLLOW-UP ITEMS
**IP:** `192.168.50.206`
**FQDN:** `hx-6.hx.local.arpa`
**Record updated:** 2026-09-18

> **Deployment method: npm global install.** HX-6 runs `omniroute@3.8.50`
> installed globally from the npm registry, started by `hx-omniroute.service`
> from `/usr/local/bin/omniroute`. `D-031` ratified this on 2026-09-17.
>
> The source build of `3.8.51` described in
> [`../03-runbooks/HX-6/README.md`](../03-runbooks/HX-6/README.md) is **not** the
> deployment path. Its checkout remains on disk and nothing runs it;
> `../03-runbooks/common/10-omniroute.sh` refuses to execute and exits 47.

## Foundation

**Not captured in this record.** HX-6 was built before the Phase 10 acceptance
run, and the foundation controls were not re-measured during it. This section
states that rather than reproducing rows nobody took.

What is known from the acceptance run: the host answers on `192.168.50.206`, it
is reachable by name as `hx-6` from the workstation, and its services survive
reboot.

To close this section, capture the same nine controls HX-8 carries:

```bash
hostname -f
chronyc sources
sudo -k -n true && echo NOPASSWD-OK
tools/hx-doc/hx-fleet-access hx-6          # from the workstation, not the host
ssh-keyscan -t ed25519 192.168.50.206 | ssh-keygen -lf -
samba-tool computer show hx-6 -U 'HX\Administrator'   # on HX-1, for the SPNs
```

## 1. Identity and Network

| Item | Value |
|---|---|
| Hostname | `hx-6` |
| IP | `192.168.50.206` |
| Dashboard / API | `http://192.168.50.206:20128` |
| Live WebSocket | `127.0.0.1:20132`, loopback only |

**Domain join gate: NOT RECORDED** in this pass. See Foundation above.

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | NOT RECORDED in this pass |
| Kernel | NOT RECORDED in this pass |
| Firmware version | NOT RECORDED in this pass |
| Node.js | v16-series reported by the process name in `ss` output; the exact version was not read |
| npm | `11.19.0` observed during the install, which is what `HX6-F02` turns on |

## 3. GPU Configuration

HX-6 carries no GPU. `HX_GPU_HOSTS` is `hx-2 hx-3 hx-4 hx-5`, and
`hx_require_gpu_expectation` refuses a driver install on any host outside it.

**GPU gate: PASS — no GPU expected, none installed**

## 4. Storage Layout

`/srv/omniroute` is a dedicated filesystem. Measured 2026-09-17:

```text
/dev/nvme0n1p3  116G   17G   94G  15%  /srv/omniroute

15G     /srv/omniroute/app          the abandoned source checkout
2.5M    /srv/omniroute/data         written by that build
4.0K    /srv/omniroute/omniroute.env
16K     /srv/omniroute/lost+found
```

**The running service does not use it.** `WorkingDirectory` is `/home/hxsa`, on
the 120G root filesystem, and the CLI's data directory is
`/home/hxsa/.omniroute/`. So the dedicated volume carries 15G of a checkout
nothing runs while the live service writes to the root disk. Recorded as
`HX6-F05`; where the live store sits was not established.

**Storage gate: PASS with an exception** — the volume exists, is mounted and is
persistent. It is not where the application writes.

## 5. Runtime

| Item | Value |
|---|---|
| Package source | npm registry, global install |
| Installed version | `3.8.50` |
| Install path | `/usr/local/lib/node_modules/omniroute` |
| Executable | `/usr/local/bin/omniroute` |
| Service unit | `hx-omniroute.service` |
| Service identity | `User=hxsa` — see D-031 and `HX6-F04` |
| Working directory | `/home/hxsa` |
| LAN listener | `0.0.0.0:20128` |
| Loopback listener | `127.0.0.1:20132` |

```text
ExecStart={ path=/usr/local/bin/omniroute ; argv[]=/usr/local/bin/omniroute ; ... }
WorkingDirectory=/home/hxsa
User=hxsa
EnvironmentFiles=          (empty)

systemctl is-active   active
systemctl is-enabled  enabled

LISTEN 0 511   0.0.0.0:20128   users:(("omniroute (v16.",pid=4221,fd=21))
LISTEN 0 511 127.0.0.1:20132   users:(("omniroute (v16.",pid=4221,fd=33))
```

### Configuration and secrets

The unit supplies no environment. OmniRoute loads its own, at startup, before
the server begins, from `bin/omniroute.mjs` `loadEnvFile()`:

```text
1  $DATA_DIR/.env                          when DATA_DIR is set
2  /home/hxsa/.omniroute/.env               the default data dir — authoritative
3  $PWD/.env
4  /usr/local/lib/node_modules/omniroute/.env   inside the npm tree
```

First writer wins, and a shadowed key is reported rather than dropped:

```text
⚠ REQUIRE_API_KEY in /usr/local/lib/node_modules/omniroute/.env is ignored,
  /home/hxsa/.omniroute/.env set it first
```

`/home/hxsa/.omniroute/.env` is the authoritative file and holds
`STORAGE_ENCRYPTION_KEY`, `OMNIROUTE_API_KEY` and `REQUIRE_API_KEY`. It was set
to mode `600` on 2026-09-17; the CLI creates it at `644`, which is `HX6-CLI-02`.

Two consequences worth knowing. `systemctl show hx-omniroute` does not report
the service's configuration, so the unit is not a truthful record of how it
runs — `HX6-F06`. And the fourth file lives inside the npm package tree, so
`npm install -g omniroute` replaces it.

**A restart, not a reload, is required after changing that file.** The A2A
skill reads its credential into a module-level `const` at import time, so the
value is fixed for the life of the process.

### API-key enforcement

`REQUIRE_API_KEY=true`. Proven from the workstation, off-host, on 2026-09-18:

```text
GET /v1/models  no Authorization    401  AUTH_002 Authentication required
GET /v1/models  Bearer <sk- key>    200
GET :20132      from the LAN        no answer
```

Two credential classes, not interchangeable:

| Form | Plane | Used for |
|---|---|---|
| `sk-…` | `CLIENT_API` | `/v1/*` inference, and the A2A internal call |
| `oma_live_…` | `MANAGEMENT` | remote CLI access tokens, scoped read/write/admin |

## 6. Model / Application Provenance

```text
HX alias:              hx-omniroute
Upstream identity:     OmniRoute 3.8.50
Source URI:            https://registry.npmjs.org/omniroute  (dist-tag latest)
Artifact SHA-256:      UNRESOLVED — not captured at install time
Import method:         package install (npm install -g omniroute)
```

`3.8.50` was the npm `latest` when installed, published 2026-08-28, and the
newest GitHub release tag was `v3.8.50` from 2026-08-26. `3.8.51` has never been
published to the registry; upstream's default branch is `release/v3.8.51` and
was still being pushed to on 2026-09-17.

The artifact hash is `UNRESOLVED` rather than omitted: the install predates this
record and no digest was captured. It can be closed by reading the integrity
field npm recorded, or by re-resolving the published tarball digest.

### Providers, aliases and combos

Four local Ollama providers, all reachable and answering `{"version":"0.34.0"}`:

| Provider | Host | Model |
|---|---|---|
| Orion-X | HX-5 `192.168.50.205` | `ornith-1.5:35b` |
| Coder-X | HX-3 `192.168.50.203` | `Coder-X-GLM-Flash:latest` |
| Qwen-X | HX-2 `192.168.50.202` | `qwen-x:qwen3.8-27b-q6_k` |
| Meta-X | HX-4 `192.168.50.204` | `meta-x:gpt-oss-20b` |

`GET /v1/models` returns **516** model ids. Five are HX aliases:

```text
HX-CODING   HX-REASONING   HX-GENERAL   HX-TOOLS   HX-FAST
```

Eight are the local Ollama models behind them:

```text
ollama/ornith-1.5:35b
ollama/Coder-X-GLM-Flash:latest
ollama/coder-x-glm:glm47flash-q5km
ollama/hf.co/bartowski/zai-org_GLM-4.7-Flash-GGUF:Q5_K_M
ollama/coder-x:qwen3-coder-30b-q6_k
ollama/qwen-x:qwen3.8-27b-q6_k
ollama/gpt-oss:20b
ollama/meta-x:gpt-oss-20b
```

An `omniroute_test_combo` run against the tools combo returned, per provider:

```text
Meta-X   1381ms   ok
Orion-X  8668ms   ok
Qwen-X  15064ms   ok
```

Cold model loading on the larger local models is visible in those figures and is
carried as a performance item, not a defect.

## 7. Functional Validation

### HX routing

One request per alias, from the workstation, 2026-09-18. Each resolved to a
different inference host:

```text
hx/general    -> meta-x:gpt-oss-20b        HX-4   finish_reason=stop   6429ms
hx/coding     -> Coder-X-GLM-Flash:latest  HX-3   finish_reason=stop  12648ms
hx/reasoning  -> qwen-x:qwen3.8-27b-q6_k   HX-2   finish_reason=stop   5934ms
```

### A2A — enabled and validated

```text
GET /.well-known/agent.json      200, agent version 1.8.1
skills advertised                six
POST /a2a  message/send
  skill                          smart-routing
  metadata.model                 hx/general
  result                         task.state = completed, artifact returned
```

The six advertised skills are `smart-routing`, `quota-management`,
`provider-discovery`, `cost-analysis`, `health-report` and `list-capabilities`.
**Only `smart-routing` has been tested.** Upstream's own `A2A-SERVER.md`
documents two skills, not six.

The agent card is served unauthenticated, which is correct for discovery. Two
observations on its content: `url` advertises `http://0.0.0.0:20128/a2a`, which
is a bind address rather than a destination a client can use, and the card is
served in Chinese.

`/a2a` itself refuses an unauthenticated request with
`-32600 Unauthorized: missing or invalid API key`.

### MCP — enabled, streamable-http

```text
initialize        PASS    protocolVersion 2025-03-26
server            omniroute 1.8.1
session creation  PASS
tools/list        PASS    110 tools
tools/call        PASS    omniroute_get_health
transport         streamable-http
audit telemetry   PASS    2 calls in 24h, success rate 100%
```

The audit entry corroborates the call independently: its recorded output carries
`uptime 5293.241318082`, matching the value returned to the caller.

`/api/mcp/*` is `LOCAL_ONLY` by default. It was reached from a non-loopback
address because the key carries the `manage` scope, which upstream's route guard
admits as a carve-out. A narrower `mcp:connect` scope exists for exactly this
purpose and is not in use.

### Client integration

| Client | Result |
|---|---|
| Open WebUI | PASS — a prompt answered through `HX-REASONING` |
| OpenCode | PASS — a completion returned through an HX alias |

### Health baseline

Taken 2026-09-18 through `omniroute_get_health`, for later comparison:

```text
version          3.8.50
cryptography     aes-256-gcm, healthy
circuitBreakers  []
rateLimits       []
admission        normal
```

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | NOT RECORDED in this pass |
| Domain join / SSSD | NOT RECORDED in this pass |
| GPU driver and visibility | PASS — no GPU expected, none installed |
| Dedicated storage | PASS with an exception — mounted, not where the app writes |
| Runtime version | PASS — `3.8.50` |
| Service active / enabled | PASS |
| Model / application loaded | PASS — four providers, five aliases, 516 model ids |
| Known-answer functional proof | PASS — three aliases to three hosts |
| Reboot persistence | PASS |

**Phase 10 acceptance: ACCEPTED WITH FOLLOW-UP ITEMS.** Full record in
[`phase-10-acceptance.md`](../05-evidence/hx-6/omniroute/phase-10-acceptance.md).

### Resolved findings

| Finding | Resolution |
|---|---|
| `HX6-A2A-01` | Configuration, not an upstream defect. The A2A skill reads `OMNIROUTE_API_KEY` from the process environment at module load and sends no `Authorization` header when it is empty, so `AUTH_002` was the authorization policy answering correctly. Persisting the key in `/home/hxsa/.omniroute/.env` and restarting the service resolved it. Validated by `message/send` through `hx/general` to Meta-X, `state=completed`. The file is byte-identical between `v3.8.50` and `release/v3.8.51`, so waiting for a release would not have helped. |
| `HX6-F01` | npm dropped `better-sqlite3`, an `optionalDependency` whose install script it would not run, and exited 0. Class recorded; the repair lives in the now-obsolete source block. |
| `HX6-F02` | npm 11.19 declines install scripts it has not been told to allow, names them, and exits 0 — the package stays and the binary does not. Hit three times: the source build, this npm-global install, and the workstation CLI. Repaired here with `--allow-scripts`. |
| `HX6-F03` | `keytar` links against libsecret at load time, so a correctly built binding still failed to import until `libsecret-1-0` was installed. Distinct from `HX6-F02`: npm was not what was missing. |
| `HX6-F06` | Reclassified. OmniRoute has a supported persistent environment mechanism; the key was simply absent from it. |

### Open follow-ups

| Finding | Summary |
|---|---|
| `HX6-A2A-02` | Smart-routing defaults to `model=auto` when none is supplied, and `auto` can select non-HX providers. HX aliases work correctly when explicitly supplied. Upstream documents `auto` filtering as fail-open, so a category suffix is not a boundary. |
| `HX6-A2A-03` | `routing_explanation` returns `provider="unknown"` while the selected HX model is correctly identified. The skill reads provider and cost from the response body; OmniRoute publishes both as `X-OmniRoute-*` headers and leaves the body intact. Observability, not a routing failure. |
| `HX6-MCP-01` | The dashboard advertises 37 tools; live `tools/list` exposes 110. Scopes enforced: no. The 73 tools the dashboard omits are the same 73 that carry no scope. |
| `HX6-MCP-02` | The MCP audit records tool, timestamp, duration, result and output, and leaves the API-key attribution blank. |
| `HX6-CLI-01` | The remote CLI applies the active context inconsistently. Client behaviour, unrelated to the acceptance deferral. |
| `HX6-CLI-02` | The CLI writes `.env` at mode `644` while `config.json` gets `600`. |
| `HX6-F04` | The service runs as `hxsa`, which holds NOPASSWD sudo. Logged by owner decision `D-031` with reversal criteria, not open for fix. |
| `HX6-F05` | `/srv/omniroute` holds 15G of the abandoned checkout while the live service works from `/home/hxsa`. |
| CLI acceptance | Deferred by owner on 2026-09-18. The install was proven first: 3.8.50 under a user prefix, `@parcel/watcher`, `koffi` and `keytar` all loading, the remote context connected and the token authenticated. |
| A2A skills | Five advertised skills untested: `quota-management`, `provider-discovery`, `cost-analysis`, `health-report`, `list-capabilities`. |
| Performance | Cold model loading is visible on the larger local models, up to 15s. Keeping selected Ollama models resident is a separate tuning activity. |

## 9. Evidence References

The proof is recorded inline in section 7 of this record and in
[`phase-10-acceptance.md`](../05-evidence/hx-6/omniroute/phase-10-acceptance.md). Every figure is a command and its
output, captured 2026-09-17 and 2026-09-18. The security, routing, A2A and MCP
gates were run from the workstation rather than on the host, so they prove the
LAN path and not a loopback listener.

Foundation controls and the OS rows are marked NOT RECORDED rather than filled
from memory. The commands that would close them are listed under Foundation.
