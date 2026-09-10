# Reviewed Neon Postgres Agent Skill

## Provenance

```text
Repository: neondatabase/postgres-skills
Reviewed branch: main
Reviewed commit: 27fe45e0f71ea89a6eaf9ea4d2e4068957c81c26
Skill: skills/postgres-best-practices/SKILL.md
Reviewed skill blob: 1720cf9fb7e7c31795433756d4bea154b5512d0f
License: Apache-2.0
Format: Agent Skills / SKILL.md
Review date: 2026-09-09
Classification for HX: COMMUNITY / expert external source; not PGDG official
```

The repository describes the skill as vendor-agnostic and says it is curated from experienced PostgreSQL practitioners. It lists Stas Kelvich as a reviewer and Jonathan Katz, a PostgreSQL Core Team member, as a reviewer.

Those credentials strengthen the source but do not turn Neon into PostgreSQL Global Development Group authority.

## Scope

The skill covers PostgreSQL 14 through 18 and links focused references for:

- schema design;
- indexing;
- query optimization;
- query patterns;
- performance diagnostics;
- logical replication;
- hot standby;
- transaction isolation;
- backup and restore;
- security and roles;
- bulk data loading;
- connection pooling;
- major-version upgrades.

It recommends the current minor release within a supported major. Verify the current minor independently against PostgreSQL.org before acting.

## Strengths for HX

Use this source for practitioner judgment around:

- choosing data types and schema patterns;
- index selection and anti-patterns;
- interpreting `EXPLAIN (ANALYZE, BUFFERS)` and planner behavior;
- diagnosing locks, vacuum/autovacuum behavior, connection pressure, and PostgreSQL statistics;
- transaction-isolation semantics;
- safe backup/restore and major-upgrade planning concepts;
- replication/pooling concepts when the owner has actually placed them in scope.

## Required HX adaptations

Do not automatically adopt examples that:

- create roles/passwords or change privileges;
- revoke `PUBLIC` access;
- change `pg_hba.conf`;
- require SSL/TLS;
- restrict source networks;
- add RLS;
- introduce PgBouncer;
- add hot standby or logical replication;
- establish backup/PITR infrastructure;
- alter data paths;
- tune persistent server settings;
- assume a dedicated PostgreSQL host;
- assume a managed/cloud PostgreSQL service.

Each is useful PostgreSQL expertise only when the current HX task and authority place it in scope.

## Direct-install rule

The upstream README offers an `npx skills add neondatabase/postgres-skills` installation path.

Do not use that command to create a second canonical HX skill source. HX canonical source remains:

```text
skills/postgresql/hx-postgresql-advisor/
```

If agent-specific skill deployment is later automated, deploy the HX wrapper from the canonical HX library. The Neon source can be re-fetched/reviewed as external reference material.

## Update/review trigger

Re-review this source when:

- its main commit changes materially;
- its supported PostgreSQL major range changes;
- PostgreSQL releases a new stable major;
- a security/authentication recommendation becomes material to HX;
- a schema/performance/upgrade recommendation conflicts with current PGDG docs;
- HX decides to vendor or deploy any third-party skill content directly.
