# HX PostgreSQL Context

## Placement

```text
Server: HX-9
IP: 192.168.50.209
Role: PostgreSQL + PostgreSQL MCP / Redis + assigned Redis MCP
Current state: IN PROGRESS — PostgreSQL core/pgvector proven; PostgreSQL MCP pending
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

## Current as-built state and remaining gaps

As of the 2026-09-19 clean-rebuild record:

- PostgreSQL 18.6 is installed from the official source tarball and hash-verified.
- Prefix: `/srv/postgresql`.
- PGDATA: `/srv/postgresql/data/pgdata`.
- Unit: `hx-postgresql.service`; active/enabled and reboot-proven.
- Listener: LAN-capable port 5432 with `192.168.50.0/24` SCRAM HBA access.
- Data checksums are enabled.
- pgvector 0.8.6 is installed and functionally proven.
- LAN create/write/read/temporary-object cleanup proof passed.
- remote pgAdmin administration over SCRAM is proven.
- PostgreSQL MCP is not yet implemented and is the next PostgreSQL companion gate.

Still outside current BASE unless separately approved: HA/replication, PgBouncer,
backup/PITR topology, production application role/database/schema design, and
formula-driven tuning.

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
