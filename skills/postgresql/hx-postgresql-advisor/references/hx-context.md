# HX PostgreSQL Context

## Placement

```text
Server: HX-9
IP: 192.168.50.209
Role: PostgreSQL + PostgreSQL MCP / Redis + assigned Redis MCP
Current state: NOT STARTED
Deployment: native Ubuntu Linux + systemd
Containers: not used unless the owner explicitly changes the architecture
```

PostgreSQL is the HX relational state service. Redis is a separate state service that shares HX-9; neither component owns the other's configuration or persistence.

## Current roadmap position

The current base implementation roadmap places PostgreSQL at priority 3, after:

1. HX-4 Meta-X; and
2. HX-5 CentCom / Ornith.

Redis on the same HX-9 server is priority 4 and Qdrant is priority 5.

PostgreSQL BASE PASS currently requires:

```text
native database
persistent service/data path
create/write/read disposable database proof
PostgreSQL MCP companion smoke test
reboot persistence
```

The exact executable PostgreSQL proof is narrower than that summary and uses a temporary table in the accepted test database.

## Exact PostgreSQL smoke boundary

Authority:

```text
smoke-tests/postgresql-smoke-test.md
```

Current known-answer contract:

```text
runner reaches HX-9 accepted listener
psql session creates TEMP table hx_smoke_postgresql
insert HX-POSTGRES-SMOKE-9271
read exact token
close session
new psql session proves pg_temp.hx_smoke_postgresql is absent
```

No permanent schema/table or production data is required. PostgreSQL MCP is proven separately with `smoke-tests/mcp-companion-smoke-test.md`.

## Current implementation gaps

As of the current clean rebuild state:

- HX-9 is NOT STARTED;
- no active HX-9 server record exists yet under `docs/02-server-records/`;
- no active HX-9 runbook exists yet under `docs/03-runbooks/`;
- PostgreSQL major version is not owner-pinned in current authority;
- Ubuntu distribution package versus PostgreSQL Apt Repository source is not pinned;
- PostgreSQL data directory/storage placement is not pinned;
- listener address and `pg_hba.conf` pattern are not pinned;
- application role/database topology is not pinned;
- HA/replication, PgBouncer, backup/PITR architecture, and production schema design are not BASE assumptions;
- exact PostgreSQL MCP implementation still requires separate review/selection.

These are not reasons to invent defaults. They are implementation-time owner decisions or runbook work.

## HX invariants

- One server -> validate -> record -> next server.
- Native Linux + systemd; no Docker/Podman/Kubernetes.
- Do not impose firewall/TLS/access restrictions without owner approval.
- Do not make unapproved network architecture changes.
- Do not touch/repartition/mount storage without explicit current authority.
- Product-specific MCP belongs to the parent application's base build but is independently smoke-tested.
- HX-15 FastMCP is not a prerequisite for PostgreSQL MCP.
- HX-5 CentCom is the standard remote fleet smoke-test runner after its activation gate.
- Test tooling/artifacts remain on HX-5; the system under test receives only the application/configuration plus smoke-namespaced temporary application state.
- Documentation alone never changes BUILD-STATE.
