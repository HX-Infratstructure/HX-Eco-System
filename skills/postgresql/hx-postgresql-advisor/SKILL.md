---
name: hx-postgresql-advisor
description: Guide PostgreSQL work inside the HX Eco-System using HX architecture and execution authority, current PostgreSQL Global Development Group documentation, and reviewed Agent Skills expertise. Use for HX-9 PostgreSQL planning, native installation, configuration, SQL/schema/index/query work, performance diagnostics, administration, backup/restore planning, migration, upgrades, validation, troubleshooting, and the PostgreSQL MCP companion. Never let external guidance override HX server placement, native/systemd deployment, network/security/storage boundaries, BASE PASS criteria, or shared-host rules.
---

# HX PostgreSQL Advisor

Apply current PostgreSQL expertise without allowing tutorials, managed-service assumptions, or third-party skills to redesign HX-9.

## Authority order

1. Current infrastructure-owner instruction.
2. Current HX control/architecture Markdown.
3. Current live HX-9 evidence.
4. Current HX-9 server record/runbook/standards.
5. HX smoke roadmap and exact PostgreSQL/MCP smoke authority when validating.
6. Current PostgreSQL Global Development Group (PGDG) docs/releases/packaging guidance.
7. Reviewed external Agent Skills, including Neon `postgres-skills`, as subordinate expertise.
8. General model knowledge only where higher authorities do not answer.

Read `references/hx-context.md` and `references/authority-map.md` first.

## Operating workflow

### Establish HX context

Before material PostgreSQL work, state the HX-9 host/IP, current build state, PostgreSQL/MCP role, Redis shared-host boundary, accepted version/package source if pinned, accepted data/listener/auth pattern if pinned, task type, BASE boundary, and prerequisite proof.

If execution depends on an unpinned choice, return `OWNER_DECISION_REQUIRED`; do not inherit a default from a tutorial.

### Verify current PostgreSQL authority

Read `references/upstream.md`. For version-sensitive work, verify the current PostgreSQL support policy, release notes, manual for the accepted major, and Ubuntu/PGDG packaging guidance as applicable.

The latest supported major is not automatically the HX major. Do not select a beta/development major as normal HX BASE.

### Use the reviewed Agent Skill correctly

Read `references/neon-postgres-skill.md` for schema design, indexing, query optimization, diagnostics, replication, transactions, backup/restore, roles, pooling, bulk loading, or upgrades.

`neondatabase/postgres-skills` follows the Agent Skills format and contains strong practitioner guidance, but it is not PGDG authority. Do not install it as a second canonical HX source; HX canonical source is this wrapper under `skills/`.

### Reconcile material recommendations

Use exactly these labels:

- `ACCEPT` — compatible with current HX authority.
- `ADAPT` — PostgreSQL principle is useful but implementation must fit HX.
- `REJECT_FOR_HX` — conflicts with an explicit HX decision.
- `OWNER_DECISION_REQUIRED` — chooses or changes unresolved HX architecture.

Typical classifications:

- Docker/Podman/Kubernetes -> `REJECT_FOR_HX` unless owner changes the native standard.
- Neon Cloud/managed PostgreSQL replacing HX-9 -> `REJECT_FOR_HX` unless placement changes.
- PostgreSQL major version before HX-9 pins it -> `OWNER_DECISION_REQUIRED`.
- Ubuntu snapshot vs PGDG Apt source before HX-9 pins it -> `OWNER_DECISION_REQUIRED`.
- PostgreSQL 19 beta as normal BASE -> `REJECT_FOR_HX` unless explicitly piloted.
- Current minor inside an already accepted supported major -> normally `ACCEPT`, after release-note review.
- `listen_addresses`, `pg_hba.conf`, TLS, GSS/LDAP, firewall, role/RLS topology -> `OWNER_DECISION_REQUIRED` unless already authorized.
- PgBouncer, HA/hot standby, logical replication, PITR/backup topology -> `OWNER_DECISION_REQUIRED`; none is automatically BASE.
- new/moved data disk or mount -> `OWNER_DECISION_REQUIRED` unless already authorized.
- schema/index/query advice without infrastructure impact -> normally `ACCEPT` or `ADAPT`.

## HX-9 deployment boundary

The accepted placement is:

```text
HX-9 / 192.168.50.209
├── PostgreSQL — native Linux service
├── PostgreSQL MCP — assigned companion capability
└── Redis — separately governed service on the same host
```

Use systemd. Do not hardcode Debian/Ubuntu unit or cluster names before the selected package is installed; discover the actual service and cluster layout.

Do not create a second PostgreSQL instance for smoke testing unless the owner authorizes it.

When the HX-9 runbook exists, infrastructure-changing commands come from that runbook, not this skill.

## Version and package-source discipline

At build time record at minimum:

```text
postgresql_major
postgresql_minor
package_source
package_version
cluster_name
service_unit_or_units
data_directory
config_file
hba_file
listen_addresses
port
```

Verify server and client versions independently; `psql --version` alone does not prove the server version.

## Shared-host and tuning discipline

PostgreSQL and Redis share HX-9. Keep ports, persistence, ownership, and resource decisions separate. Do not move/mount storage or tune memory, connections, WAL, checkpoints, autovacuum, huge pages, or kernel parameters by formula alone.

For tuning, capture hardware, workload, current settings, and measurable evidence first.

## Network/authentication discipline

HX BASE requires the accepted PostgreSQL listener to be reachable by the approved remote smoke runner and intended HX clients. The skill does not choose how that exposure is implemented.

Do not add firewall restrictions, TLS/certificates, LDAP/GSS, RLS, password policy, or new role topology merely because a best-practice source recommends them. Never store credentials in the skill, repository, or retained evidence.

For connection failures, distinguish service state, listener state, network reachability, `pg_hba.conf` rejection, authentication, role/database privileges, SQL/schema errors, lock/contention, and resource issues before editing configuration.

## BASE versus application database design

PostgreSQL BASE proves the platform. Production schemas, indexes, RLS, pooling, replication, application data, and backup topology are not automatically BASE requirements.

Use the Neon skill's database-engineering material only when the actual task places those concerns in scope.

## Destructive stop points

Before any destructive/migration action, identify target scope, recovery implications, downtime, and owner authority. Stop before `DROP DATABASE`, broad destructive schema changes, `pg_upgrade`, data-directory replacement, `pg_resetwal`, restore over existing data, replication/failover cutover, non-smoke `TRUNCATE`/bulk delete, or durability-disablement unless current authority explicitly permits it.

## HX validation

PostgreSQL acceptance remains `smoke-tests/postgresql-smoke-test.md`, not a vendor quickstart.

The governed proof is:

```text
HX-5 approved remote runner
  -> HX-9 accepted PostgreSQL listener
  -> TEMP table hx_smoke_postgresql
  -> insert/read HX-POSTGRES-SMOKE-9271
  -> end session
  -> new session proves TEMP table absent
  -> PostgreSQL MCP companion smoke gate
  -> reboot persistence
  -> retained evidence
```

Do not substitute `pg_isready`, a local socket connection, generic SQL exercise, or the Neon Agent Skill for this proof.

## Auditable response pattern

For material work, report:

```text
HX CONTEXT
OFFICIAL POSTGRESQL GUIDANCE
AGENT-SKILL INPUT
RECONCILIATION: ACCEPT | ADAPT | REJECT_FOR_HX | OWNER_DECISION_REQUIRED
EXECUTION AUTHORITY
VALIDATION AUTHORITY
STOP CONDITIONS
```

## Stop conditions

Stop rather than improvise when the HX-9 runbook/server record required for execution is absent; major/package source, data path, listener/auth, or shared-host resource decisions are unresolved; a recommendation introduces unapproved containers/managed service/HA/pooling/security/storage architecture; non-smoke data is at risk; a migration/restore lacks an accepted recovery plan; required credentials are unavailable; the PostgreSQL MCP implementation is not selected for a task that requires it; or version-specific behavior cannot be verified against current PGDG guidance.

## References

- `references/hx-context.md` — HX-9 placement, state, shared-host and BASE boundaries.
- `references/authority-map.md` — HX execution and validation precedence.
- `references/upstream.md` — PGDG and Agent Skills provenance/current-source workflow.
- `references/neon-postgres-skill.md` — reviewed Neon skill provenance, strengths, and HX restrictions.
