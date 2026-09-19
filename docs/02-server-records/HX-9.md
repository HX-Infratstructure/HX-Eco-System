# HX-9 — PostgreSQL + MCP / Redis + MCP Server Configuration

**Build state:** IN PROGRESS  
**Gate:** POSTGRESQL MCP NEXT  
**IP:** `192.168.50.209`  
**FQDN:** `hx-9.hx.local.arpa`  
**Record updated:** 2026-09-19

HX-9 is the shared HX state-services host. PostgreSQL and Redis are separate
applications with separate service identities, storage, configuration, and
companion gates. This record reflects the live clean-rebuild configuration
observed during the 2026-09-18/19 build session. It does not import prototype
state.

## Foundation

| Control | Current as-built evidence | State |
|---|---|---|
| `hostname -f` | `hx-9.hx.local.arpa` | PASS |
| Address | `192.168.50.209/24` | PASS |
| HX-1 time authority | `chronyc sources` selected `^* 192.168.50.200` | PASS |
| Fleet key | `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk` | PASS |
| NOPASSWD sudo | externally proven with fleet-key administration | PASS |
| SSH persistence | survives reboot; key-only administration proven | PASS |
| External key-only login | fleet-key login + passwordless sudo proven | PASS |
| SSH host-key fingerprint | not captured in this session | UNRESOLVED |
| AD SPN four-form check | domain membership is proven; exact four-form SPN transcript was not retained here | UNRESOLVED |

Foundation, domain, and storage survived reboot. The two unresolved record
fields above are documentation/evidence gaps only; they are not replaced with
guessed values.

## 1. Identity and Network

| Item | Value |
|---|---|
| Hostname | `hx-9` |
| FQDN | `hx-9.hx.local.arpa` |
| IPv4 | `192.168.50.209` |
| Gateway | `192.168.50.1` |
| HX DNS / AD / NTP authority | HX-1, `192.168.50.200` |
| Realm | `HX.LOCAL.ARPA` |
| Domain client | realmd / SSSD / Kerberos member |
| Domain user resolution | PASS |
| Deployment posture | native Ubuntu Linux + systemd; no containers |

**Domain join gate: PASS.**

The trusted HX LAN posture remains owner-controlled. No firewall, TLS,
segmentation, or access-hardening changes were introduced during this build.

## 2. Operating System

| Item | Value |
|---|---|
| Distribution / release | Ubuntu 24.04.5 LTS |
| Kernel | `7.0.0-31-generic` |
| Firmware version | UNRESOLVED |
| sudo policy | HX fleet admin account `hxsa`; passwordless sudo proven |
| Admin account | `hxsa` |
| GPU expectation | CPU-only host |

## 3. GPU Configuration

**Not applicable:** HX-9 is a CPU-only fleet host and is not listed in
`HX_GPU_HOSTS`. No NVIDIA driver is required for its assigned PostgreSQL/Redis
workloads.

**GPU gate: NOT APPLICABLE.**

## 4. Storage Layout

Live persistent layout after reboot:

| Device | Size | Filesystem | Mount | Use |
|---|---:|---|---|---|
| `/dev/sda1` | 1G | vfat | `/boot/efi` | EFI |
| `/dev/sda2` | 120G | ext4 | `/` | OS |
| `/dev/sda3` | 50G | ext4 | `/srv/redis` | Redis service/data/WebUI/MCP |
| `/dev/sda4` | 65G | ext4 | `/srv/postgresql` | PostgreSQL software prefix |
| `/dev/sda5` | 1.6T | ext4 | `/srv/postgresql/data` | PostgreSQL data |
| `/dev/nvme0n1` | present | — | unmounted | intentionally untouched |

PostgreSQL cannot use the ext4 mount root as PGDATA because of `lost+found`.
The accepted child data directory is:

```text
/srv/postgresql/data/pgdata
```

Redis paths:

```text
/srv/redis                 root:root 0755
/srv/redis/data            redis:redis 0700
/srv/redis/webui           HX P3X WebUI working/config directory
/srv/redis/mcp             RedisVL MCP configuration
```

**Storage gate: PASS.**

## 5. Runtime

### 5.1 PostgreSQL

| Item | As-built value |
|---|---|
| Product | PostgreSQL 18.6 |
| Source | official `postgresql.org` source tarball |
| Tarball SHA-256 | `555610c24d53e4316da5b7d3fc25c279d96856d5e0e23ee308c328c5fa881d9f` |
| Prefix | `/srv/postgresql` |
| PGDATA | `/srv/postgresql/data/pgdata` |
| Service identity | `postgres` |
| Unit | `hx-postgresql.service` |
| Listener | `0.0.0.0:5432` and IPv6 equivalent |
| Checksums | PostgreSQL data-checksum version 1 |
| Reboot persistence | PASS |

Build dependencies observed/required:

```text
build-essential
pkg-config
libreadline-dev
zlib1g-dev
libicu-dev
libssl-dev
libsystemd-dev
bison
flex
```

Configure line:

```bash
./configure --prefix=/srv/postgresql --with-openssl --with-icu --with-systemd
```

Accepted network configuration:

```text
listen_addresses = '*'
host all all 192.168.50.0/24 scram-sha-256
```

Local trust defaults remain in place. The `postgres` database role has a LAN
password configured for pgAdmin/SCRAM use; the password is intentionally not
stored in this repository.

### 5.2 pgvector

| Item | Value |
|---|---|
| Extension | pgvector 0.8.6 |
| Reviewed tag/commit | `8ee86c96f0fd72390f890aa8a336fda6d3ab4c6c` |
| Install target | PostgreSQL 18.6 tree under `/srv/postgresql` |
| Extension create | PASS |
| Functional distance query | PASS |
| Reboot persistence | PASS |

pgvector is relational-adjacent capability only. HX-10 Qdrant remains the
authoritative/default HX vector database.

### 5.3 Redis core

| Item | As-built value |
|---|---|
| Product | Redis 8.10.2 |
| Source | official `download.redis.io` release tarball |
| Tarball SHA-256 | `b9ffee226b5eecdba98a679260dad764b2a4ebd90dce4ad5ac9e9f3eef9c02b3` |
| Core build | `make build redis USE_SYSTEMD=yes -j"$(nproc)"` |
| Installed server | `/usr/local/bin/redis-server` |
| Installed CLI | `/usr/local/bin/redis-cli` |
| Config | `/etc/redis/redis.conf` |
| Config ownership | `root:redis 0640` |
| Data path | `/srv/redis/data` |
| Unit | `hx-redis.service` |
| Listener | `0.0.0.0:6379` and `[::]:6379` |
| Persistence | AOF enabled |
| Reboot persistence | PASS |

Accepted active Redis settings:

```text
bind 0.0.0.0 ::
protected-mode no
supervised systemd
dir /srv/redis/data
appendonly yes
```

This unauthenticated LAN posture is deliberate for the current trusted HX LAN
under owner policy. It is not permission to add TLS, firewall, or authentication
hardening without a separate owner decision.

Open Redis runtime follow-ups recorded during build:

- Redis warned that the configured PID-file path was not writable. The service
  itself is systemd-managed and functional; the warning has not yet been
  reconciled in `redis.conf`.
- Redis warned that `vm.overcommit_memory` should be enabled. No kernel tuning
  was applied during this session; measure/reconcile shared-host impact first.

### 5.4 Redis modules

Permanent absolute module load lines:

```text
loadmodule /usr/local/lib/redis/modules/redisbloom.so
loadmodule /usr/local/lib/redis/modules/rejson.so
loadmodule /usr/local/lib/redis/modules/redisearch.so
```

The stock relative module lines under the temporary source tree are disabled.

| Capability | Runtime identity | State |
|---|---|---|
| RedisBloom | module `bf`, version integer `81001` | PROVEN |
| RedisJSON | module `ReJSON`, version integer `81000` | PROVEN |
| RediSearch | module `search`, version integer `81001` | PROVEN |
| VectorSet | Redis 8 built-in `vectorset`, version `1` | PRESENT |
| RedisTimeSeries | not loaded | DEFERRED |

### 5.5 P3X Redis WebUI

| Item | Value |
|---|---|
| Product | P3X Redis UI 2026.10.100 |
| Node.js | 24.21.0 |
| npm | 11.19.0 |
| CLI | `/usr/bin/p3x-redis` |
| Working/config path | `/srv/redis/webui` |
| Config | `/srv/redis/webui/p3xrs.json` |
| Connection target | local Redis `127.0.0.1:6379` |
| Unit | `hx-redis-webui.service` |
| Listener | `0.0.0.0:7843` |
| LAN URL | `http://192.168.50.209:7843/` |
| Health | `/health` returns `{"status":"ok","version":"2026.10.100",...}` |
| Reboot persistence | PASS |

The UI successfully tested the HX-9 Redis connection, console `PING -> PONG`,
and the built-in AI console path.

### 5.6 Redis MCP

Two MCP forms were evaluated:

1. The official `redis-mcp-server` was proven as a local stdio process via
   `uvx` against `redis://127.0.0.1:6379/0`.
2. The permanent remote-capable HX endpoint uses RedisVL MCP over FastMCP with
   Streamable HTTP.

Permanent service:

| Item | Value |
|---|---|
| Unit | `hx-redis-mcp.service` |
| Working path | `/srv/redis/mcp` |
| Config | `/srv/redis/mcp/redisvl-mcp.yaml` |
| Transport | `streamable-http` |
| Bind | `0.0.0.0:8000` |
| MCP URL | `http://192.168.50.209:8000/mcp` |
| FastMCP observed | 3.4.7 |
| RedisVL package version | UNRESOLVED — CLI version was not captured |
| Auth | none; explicit `--allow-unauthenticated` on trusted HX LAN |
| systemd active/enabled | PASS |
| host reboot persistence after MCP installation | NOT YET PROVEN |

RedisVL currently constrains FastMCP to `>=2,<4`; the runtime-advertised
FastMCP 4.x update was deliberately not applied underneath RedisVL.

MCP test index:

```text
Redis index: hx:idx:mcp
RedisVL label: hx-catalog
Seed key: hx:mcp:001
Category: infrastructure
```

The index returned the seeded record through direct RediSearch. A later
Open WebUI client test did not surface/invoke the Redis MCP tools; Open WebUI
itself labels native MCP support experimental. That client-side limitation is
not recorded as an HX-9 server failure. Runtime-level MCP tool registration is
integration/client work.

### 5.7 PostgreSQL MCP

**Not yet implemented.** PostgreSQL core is complete and remote administration
is proven, but the assigned PostgreSQL MCP companion remains the primary open
HX-9 base gate.

## 6. Model / Application Provenance

HX-9 hosts no Ollama model. Application provenance is recorded below.

### PostgreSQL 18.6

```text
HX alias/service:       hx-postgresql
Upstream identity:     PostgreSQL 18.6
Source URI:            https://ftp.postgresql.org/pub/source/v18.6/postgresql-18.6.tar.gz
Artifact SHA-256:      555610c24d53e4316da5b7d3fc25c279d96856d5e0e23ee308c328c5fa881d9f
Import method:         build from source
```

### Redis 8.10.2

```text
HX alias/service:       hx-redis
Upstream identity:     Redis 8.10.2
Source URI:            https://download.redis.io/releases/redis-8.10.2.tar.gz
Artifact SHA-256:      b9ffee226b5eecdba98a679260dad764b2a4ebd90dce4ad5ac9e9f3eef9c02b3
Import method:         build from source
```

### pgvector 0.8.6

```text
HX alias/service:       PostgreSQL extension vector
Upstream identity:     pgvector 0.8.6
Source identity:       tag/commit 8ee86c96f0fd72390f890aa8a336fda6d3ab4c6c
Artifact SHA-256:      UNRESOLVED — source-tree archive hash not retained
Import method:         build from source against PostgreSQL 18.6
```

### P3X Redis UI

```text
HX alias/service:       hx-redis-webui
Upstream identity:     p3x-redis-ui 2026.10.100
Source URI:            npm package p3x-redis-ui@2026.10.100
Artifact SHA-256:      UNRESOLVED — npm package integrity was not retained in this record
Import method:         npm global install
```

### RedisVL MCP

```text
HX alias/service:       hx-redis-mcp
Upstream identity:     RedisVL MCP + FastMCP 3.4.7 runtime
Source URI:            uvx package extra redisvl[mcp]
Artifact SHA-256:      UNRESOLVED
Import method:         uvx-managed Python environment
```

## 7. Functional Validation

### PostgreSQL core

Proven during the build:

- service active/enabled;
- listener on port 5432;
- data checksums enabled;
- pgvector extension version 0.8.6;
- vector distance query returned the expected result;
- LAN smoke from a separate workstation created a temporary database/role,
  created/inserted/read `HX-POSTGRES-SMOKE-9271`, opened a new session and
  proved the temporary relation absent, then cleaned up the disposable
  database/role;
- remote pgAdmin connection from the operator workstation succeeded using
  SCRAM authentication;
- PostgreSQL + pgvector survived host reboot.

### Redis core and modules

Proven during the build:

```text
redis-cli PING -> PONG
```

RedisBloom:

```text
BF.ADD hx:smoke:bloom HX-DOC-001      -> 1
BF.EXISTS ... HX-DOC-001              -> 1
BF.EXISTS ... HX-DOC-999              -> 0
cleanup DEL                            -> 1
```

RedisJSON:

```text
JSON.SET hx:smoke:json '$' {...}       -> OK
JSON.GET hx:smoke:json '$.document'    -> ["HX-DOC-001"]
cleanup DEL                            -> 1
```

RedisJSON + RediSearch combined catalog proof:

```text
FT.CREATE hx:idx:docs ON JSON ...      -> OK
FT.SEARCH hx:idx:docs '@project:{HX\-Infrastructure} @ingested:{false}'
                                      -> 1 hit: hx:doc:001
```

The temporary index/document were intended for cleanup after the proof; the
cleanup transcript was not retained in this session and is therefore
`UNRESOLVED` rather than assumed.

### Redis WebUI

After host reboot:

```text
systemctl is-active hx-redis           -> active
systemctl is-active hx-redis-webui     -> active
systemctl is-enabled hx-redis          -> enabled
systemctl is-enabled hx-redis-webui    -> enabled
0.0.0.0:6379                           -> listening
0.0.0.0:7843                           -> listening
redis-cli PING                          -> PONG
GET /health                             -> status=ok, version=2026.10.100
UI console PING                         -> PONG
```

### Redis MCP

Current daemon proof:

```text
systemctl is-active hx-redis-mcp        -> active
systemctl is-enabled hx-redis-mcp       -> enabled
0.0.0.0:8000                            -> listening
GET /mcp without MCP Accept header      -> HTTP 406 with MCP session id and
                                           "Client must accept text/event-stream"
```

The earlier systemd restart counter was explained by the still-running manual
test process occupying port 8000; once that process was stopped, the systemd
instance bound successfully.

**Redis MCP host-reboot proof after service installation: NOT YET PROVEN.**

## 8. Final State

| Gate | Result |
|---|---|
| Clean base build | PASS |
| Domain join / SSSD | PASS |
| GPU driver and visibility | NOT APPLICABLE |
| Dedicated storage | PASS |
| PostgreSQL 18.6 runtime | PASS |
| PostgreSQL pgvector 0.8.6 | PASS |
| PostgreSQL LAN + pgAdmin access | PASS |
| PostgreSQL reboot persistence | PASS |
| PostgreSQL MCP companion | NOT IMPLEMENTED |
| Redis 8.10.2 runtime | PASS |
| RedisBloom / RedisJSON / RediSearch | PASS |
| Redis P3X WebUI | PASS |
| Redis/WebUI reboot persistence | PASS |
| RedisVL/FastMCP daemon | PASS — current runtime |
| Redis MCP reboot persistence | NOT YET PROVEN |
| SSH host-key record | UNRESOLVED |
| Exact AD four-form SPN transcript | UNRESOLVED |
| Overall HX-9 BASE | IN PROGRESS |

### Next closure sequence

1. Select/install/configure the PostgreSQL MCP companion.
2. Prove PostgreSQL MCP discovery + known-answer safe tool call.
3. Reboot HX-9 and re-prove `hx-redis-mcp.service` plus MCP endpoint.
4. Reconcile Redis PID-file and `vm.overcommit_memory` warnings deliberately,
   without generic security hardening.
5. Close remaining foundation record evidence gaps or explicitly accept them.
6. Run/promote the repository-defined HX-9 smoke/evidence gates from the
   approved runner when that validation layer is available.
7. Only then promote HX-9 to `PASS / CLOSED`.

## 9. Evidence References

This record currently uses **inline evidence** from the live HX-9 build session
rather than a promoted bundle under `docs/05-evidence/`.

Important evidence identities:

- PostgreSQL 18.6 source SHA-256:
  `555610c24d53e4316da5b7d3fc25c279d96856d5e0e23ee308c328c5fa881d9f`
- Redis 8.10.2 source SHA-256:
  `b9ffee226b5eecdba98a679260dad764b2a4ebd90dce4ad5ac9e9f3eef9c02b3`
- pgvector 0.8.6 commit:
  `8ee86c96f0fd72390f890aa8a336fda6d3ab4c6c`
- P3X Redis UI:
  `2026.10.100`
- FastMCP observed in RedisVL MCP runtime:
  `3.4.7`

Secrets are intentionally excluded. In particular, the PostgreSQL role
password used for remote pgAdmin/SCRAM access is not recorded in this
repository.
