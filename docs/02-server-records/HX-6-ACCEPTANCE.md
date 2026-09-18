# HX-6 OmniRoute Acceptance — Phase 10

**Version:** 3.8.50
**Date:** 2026-09-18
**Implementation:** npm global install, `hx-omniroute.service` (D-031)
**Scope:** confirm the integrated HX-6 baseline and record the result. No new
tests were invented, and no finding was fixed during acceptance.

## Result

| Gate | Result |
|---|---|
| Installation / Persistence | PASS |
| API Security | PASS |
| HX Routing | PASS |
| Open WebUI | PASS |
| OpenCode | PASS |
| A2A | PASS |
| MCP | PASS |
| CLI | DEFERRED BY OWNER |
| **Overall** | **ACCEPTED WITH FOLLOW-UP ITEMS** |

## Evidence

### Installation / persistence

```text
systemctl is-active hx-omniroute     active
systemctl is-enabled hx-omniroute    enabled
LISTEN 0 511   0.0.0.0:20128   users:(("omniroute (v16.",pid=4221,fd=21))
LISTEN 0 511 127.0.0.1:20132   users:(("omniroute (v16.",pid=4221,fd=33))
```

20128 is LAN-facing and 20132 is loopback-only, which is the posture the runbook
states. The service had already survived a reboot earlier the same day.

### API security

Run from the workstation, off-host, so the LAN path is proven rather than a
loopback listener:

```text
GET /v1/models  no Authorization    401  AUTH_002 Authentication required
GET /v1/models  Bearer <sk- key>    200
GET :20132      from the LAN        no answer
```

### HX routing

One request per alias. Each resolved to a different inference host:

```text
hx/general    -> meta-x:gpt-oss-20b        HX-4    finish_reason=stop   6429ms
hx/coding     -> Coder-X-GLM-Flash:latest  HX-3    finish_reason=stop  12648ms
hx/reasoning  -> qwen-x:qwen3.8-27b-q6_k   HX-2    finish_reason=stop   5934ms
```

`finish_reason=stop` with a resolved model name is what separates a real
completion from a truncated or substituted one.

### Open WebUI

A prompt answered in the browser through `HX-REASONING`.

### OpenCode

A completion returned in the client through an HX alias.

### A2A

```text
GET /.well-known/agent.json          200, version 1.8.1, six skills advertised
POST /a2a  message/send
  skill    smart-routing
  metadata model = hx/general
  result   task.state = completed, artifact returned
```

### MCP

```text
initialize        PASS   protocolVersion 2025-03-26
server            omniroute 1.8.1
session creation  PASS
tools/list        PASS   110 tools
tools/call        PASS   omniroute_get_health
transport         streamable-http
audit telemetry   PASS   2 calls in 24h, success rate 100%
```

The audit entry corroborates the call independently: the recorded output carries
`uptime 5293.241318082`, matching the value returned to the caller.

### CLI — deferred by owner

Deferred by owner direction on 2026-09-18, not because a gate failed. What was
proven before stopping:

```text
workstation CLI 3.8.50 installed        under a user prefix, no root
@parcel/watcher                         LOADS
koffi                                   LOADS
keytar                                  LOADS
remote context hx-6                     connected
admin token                             authenticated
```

Further CLI acceptance was intentionally deferred.

## Follow-up items

Recorded, not fixed. None blocks acceptance.

| Finding | Status | Summary |
|---|---|---|
| `HX6-A2A-01` | RESOLVED | Configuration. `OMNIROUTE_API_KEY` was absent from the OmniRoute process environment; persisted in `/home/hxsa/.omniroute/.env` and the service restarted. Validated by `message/send` through `hx/general` to Meta-X, `state=completed`, artifact returned. |
| `HX6-A2A-02` | FOLLOW-UP | A2A smart-routing defaults to `model=auto` when none is supplied, and live testing showed `auto` can select non-HX providers. HX aliases work correctly when explicitly supplied. |
| `HX6-A2A-03` | FOLLOW-UP | `routing_explanation` returned `provider="unknown"` while the selected HX model was correctly identified. Observability and metadata, not a routing failure. |
| `HX6-MCP-01` | FOLLOW-UP | The dashboard summary advertises 37 tools; live `tools/list` exposes 110. Scopes enforced: no. |
| `HX6-MCP-02` | FOLLOW-UP | The MCP audit records tool, timestamp, duration, result and output, and leaves the API-key attribution field blank for the observed calls. |
| `HX6-CLI-01` | FOLLOW-UP | The remote CLI applies the active context inconsistently. Client behaviour; unrelated to the deferral above. |
| `HX6-CLI-02` | FOLLOW-UP | The CLI writes `.env` at mode 644 while `config.json` gets 600. |
| `HX6-F04` | LOGGED | The service runs as `hxsa`, by owner decision D-031, with reversal criteria. |
| `HX6-F05` | FOLLOW-UP | `/srv/omniroute` holds 15G of the abandoned source checkout while the live service works from `/home/hxsa`. |

### A2A skills outside this scope

Live discovery advertises six skills. Only `smart-routing` was
acceptance-tested. Five remain present and untested:

```text
quota-management
provider-discovery
cost-analysis
health-report
list-capabilities
```

Phase 10 was deliberately not widened to cover them. The scope was baseline
acceptance, not additional test invention.

## Disposition

**ACCEPTED WITH FOLLOW-UP ITEMS.** The integrated HX-6 baseline is confirmed at
3.8.50: the service persists, the API refuses unauthenticated callers, all three
tested HX aliases route to distinct hosts, and both agent protocols complete a
real task end to end from off-host.
