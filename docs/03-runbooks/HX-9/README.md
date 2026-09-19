# HX-9 Current Runbook

**Host:** hx-9  
**Expected IP:** `192.168.50.209`  
**Role:** PostgreSQL + MCP / Redis + MCP  
**Current state:** IN PROGRESS  
**Current gate:** POSTGRESQL MCP NEXT  
**As-built record:** `../../02-server-records/HX-9.md`

## Current as-built position

Foundation, domain membership, storage, PostgreSQL 18.6, pgvector 0.8.6,
Redis 8.10.2, RedisBloom, RedisJSON, RediSearch, and P3X Redis UI are installed
natively and proven on HX-9. PostgreSQL, Redis, and P3X survive host reboot.

The RedisVL/FastMCP Streamable HTTP companion is active and enabled at
`http://192.168.50.209:8000/mcp`; its post-install host-reboot gate remains
open. PostgreSQL MCP has not yet been installed and is the next primary build
gate.

The authoritative live configuration, hashes, paths, units, listeners,
functional proofs, and unresolved evidence items are recorded in
`docs/02-server-records/HX-9.md`.

## Foundation execution

The shared foundation blocks remain the authority for a clean rebuild of this
host:

```bash
./01-base-admin-network-updates.sh # reboots
./02-domain.sh                     # reboots
```

HX-9 is CPU-only and is not in `HX_GPU_HOSTS`.

## Application execution history

The current HX-9 applications were built during the owner-directed manual
implementation session. Do not re-run the generic application blocks against
the live host merely to make the host resemble an older pin.

Current live versions are:

```text
PostgreSQL 18.6
pgvector 0.8.6
Redis 8.10.2
P3X Redis UI 2026.10.100
FastMCP 3.4.7 inside the RedisVL MCP runtime
```

The repository application blocks remain useful rebuild references, but any
version or procedure conflict must be reconciled against the as-built server
record and current owner direction before execution. In particular, the live
Redis runtime is 8.10.2; do not silently downgrade it to an older repository
pin.

## Accepted service layout

| Capability | Unit / process | Native endpoint |
|---|---|---|
| PostgreSQL | `hx-postgresql.service` | `192.168.50.209:5432` |
| Redis | `hx-redis.service` | `192.168.50.209:6379` |
| P3X Redis UI | `hx-redis-webui.service` | `http://192.168.50.209:7843/` |
| RedisVL MCP | `hx-redis-mcp.service` | `http://192.168.50.209:8000/mcp` |

PostgreSQL data is under `/srv/postgresql/data/pgdata`; Redis data is under
`/srv/redis/data`. Do not move, remount, or repurpose storage without explicit
owner approval.

## Remaining closure sequence

1. Select and install the PostgreSQL MCP companion.
2. Prove PostgreSQL MCP discovery plus a bounded known-answer safe tool call.
3. Reboot HX-9 and prove `hx-redis-mcp.service` returns active/enabled and the
   Streamable HTTP endpoint responds.
4. Reconcile the Redis PID-file and `vm.overcommit_memory` warnings
   deliberately; do not convert them into generic hardening work.
5. Close or explicitly accept the two remaining foundation-record evidence
   gaps: SSH host-key fingerprint and four-form AD SPN transcript.
6. Run/promote the repository-defined HX-9 smoke/evidence gates when the
   approved runner layer is available.
7. Update `docs/00-control/hx-fleet.tsv` to `PASS / CLOSED` only after every
   required companion, cleanup, and reboot gate is actually proven.

## Validation references

```text
smoke-tests/postgresql-smoke-test.md
smoke-tests/redis-smoke-test.md
smoke-tests/mcp-companion-smoke-test.md
```

Do not equate service health with companion-tool discovery. Redis MCP client
registration/tool injection belongs to the consuming runtime; the HX-9 server
gate proves the MCP endpoint and bounded tool contract.

Do not mount/wipe unrelated disks. Do not import prior application state. Do
not add firewall/TLS/access restrictions without owner approval.
