# HX Redis Context

## Placement

```text
Server: HX-9
IP: 192.168.50.209
Role: PostgreSQL + PostgreSQL MCP / Redis + Redis MCP
Current state: NOT STARTED
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

## Current implementation gaps

As of the current clean rebuild state:

- HX-9 is NOT STARTED;
- no active HX-9 server record exists under `docs/02-server-records/`;
- no active HX-9 runbook exists under `docs/03-runbooks/`;
- Redis runtime version/package source is not selected by this skill;
- actual Redis unit/config/data path must be established by package/runbook/runtime evidence;
- persistence and memory/eviction policy must be reconciled with PostgreSQL shared-host requirements;
- network/authentication/TLS/firewall policy is owner/runbook controlled;
- Cluster, Sentinel, replication/failover are not current BASE assumptions;
- exact Redis MCP implementation still requires current runbook/selection authority.

Do not turn these gaps into guessed defaults.

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
