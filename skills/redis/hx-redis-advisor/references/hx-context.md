# HX Redis Context

## Placement

```text
Server: HX-9
IP: 192.168.50.209
Role: PostgreSQL + PostgreSQL MCP / Redis + Redis MCP
Current state: IN PROGRESS — Redis core/modules/WebUI proven; Redis MCP daemon active, reboot proof pending
Deployment: native Ubuntu Linux + systemd
Containers: not used unless the owner explicitly changes the architecture
```

Redis is the HX in-memory/state service. PostgreSQL is a separate relational state service sharing HX-9; neither owns the other's configuration or persistence.

## Current roadmap position

The current base implementation roadmap places Redis at priority 4, after PostgreSQL on HX-9. Qdrant follows at priority 5.

Redis BASE proof currently requires the accepted native Redis service and deterministic application-level proof. Exact authority: `smoke-tests/redis-smoke-test.md`.

Current known-answer contract:

```text
runner reaches the accepted HX-9 Redis endpoint
PING -> PONG
SET hx:smoke:redis:9271 HX-REDIS-SMOKE-9271 EX 120
GET returns exact token
DEL returns 1
EXISTS returns 0
cleanup is therefore proven
```

Redis MCP is proven separately by `smoke-tests/mcp-companion-smoke-test.md`. Reboot persistence and retained evidence follow current closure rules.

## Current as-built state and remaining gaps

As of the 2026-09-19 clean-rebuild record:

- Redis 8.10.2 is installed natively from the official release tarball and hash-verified.
- Unit: `hx-redis.service`; active/enabled and reboot-proven.
- Config: `/etc/redis/redis.conf`; data: `/srv/redis/data`; AOF enabled.
- LAN listeners: port 6379 on IPv4/IPv6; current trusted-LAN no-auth posture is deliberate owner policy.
- RedisBloom, RedisJSON, and RediSearch are loaded from absolute module paths and functionally proven.
- RedisTimeSeries remains deferred.
- P3X Redis UI 2026.10.100 is active/enabled on port 7843 and reboot-proven.
- RedisVL/FastMCP Streamable HTTP companion is active/enabled on port 8000 at `/mcp`.
- Redis MCP post-install host-reboot proof remains open.
- PID-file permission and `vm.overcommit_memory` warnings remain deliberate follow-up items, not automatic hardening triggers.
- memory/eviction tuning remains evidence-driven because PostgreSQL shares HX-9.
- Cluster, Sentinel, replication/failover remain outside current BASE unless separately approved.

## HX invariants

- One server -> validate -> record -> next server.
- Native Linux + systemd; no Docker/Podman/Kubernetes.
- Do not impose firewall/TLS/access restrictions without owner approval.
- Do not make unapproved network architecture changes.
- Do not touch/repartition/mount storage without explicit current authority.
- Product-specific MCP belongs to the parent application's base build but is independently smoke-tested.
- HX-15 FastMCP is not a prerequisite for Redis MCP.
- HX-5 CentCom is the standard remote smoke-test runner after its activation gate.
- Test tooling/artifacts remain on HX-5; the system under test receives only application/configuration plus bounded smoke state.
- Documentation alone never changes BUILD-STATE.
