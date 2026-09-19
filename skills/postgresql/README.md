# HX PostgreSQL Skill

PostgreSQL on HX-9 uses the governed HX wrapper:

```text
skills/postgresql/hx-postgresql-advisor/
```

## HX placement

```text
HX-9 — 192.168.50.209
PostgreSQL + PostgreSQL MCP
Redis + assigned Redis MCP on the same host
State: IN PROGRESS — PostgreSQL core/pgvector proven; PostgreSQL MCP pending
Deployment: native Ubuntu Linux + systemd
```

## Source model

PostgreSQL has no PGDG-published Agent Skill identified in this review. The HX wrapper therefore uses a layered source model:

1. **PostgreSQL Global Development Group** documentation, release notes, and packaging guidance as primary PostgreSQL product authority.
2. **Agent Skills specification** at `agentskills.io` as the portable skill format.
3. **Neon `neondatabase/postgres-skills`** as reviewed third-party practitioner expertise, classified `COMMUNITY`, not PGDG official.
4. HX architecture/runbooks/smoke authority above all external guidance for HX decisions and execution.

## Canonical files

```text
skills/postgresql/
├── README.md
├── upstream/
│   └── SOURCE.md
└── hx-postgresql-advisor/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── authority-map.md
        ├── hx-context.md
        ├── upstream.md
        └── neon-postgres-skill.md
```

## Important boundary

The wrapper remains advisory. HX-9 now runs PostgreSQL 18.6 built from the official source tarball under `/srv/postgresql`, with PGDATA at `/srv/postgresql/data/pgdata`, LAN SCRAM access, pgvector 0.8.6, functional LAN proof, pgAdmin access, and reboot persistence. The PostgreSQL MCP companion remains unimplemented and is the next HX-9 application gate. HA/replication, PgBouncer, backup/PITR topology, production schema design, and unrelated tuning remain outside the current BASE unless separately approved.

Validation remains controlled by `smoke-tests/postgresql-smoke-test.md`, the companion MCP smoke test, reboot persistence, retained evidence, and current HX closure rules.
