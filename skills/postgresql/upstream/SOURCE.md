# PostgreSQL Skill Upstream Source

## Primary product authority

```text
Project: PostgreSQL
Authority: PostgreSQL Global Development Group (PGDG)
Official site: https://www.postgresql.org/
Documentation: https://www.postgresql.org/docs/
Version policy: https://www.postgresql.org/support/versioning/
Ubuntu packaging: https://www.postgresql.org/download/linux/ubuntu/
Review date: 2026-09-09
```

At review time PostgreSQL 18 is the current stable major and 18.6 is the current minor release. PostgreSQL 19 is still beta. This records upstream context only; the HX-9 major/package source remains an owner/runbook decision.

## Agent Skills format

```text
Source: https://agentskills.io/
Role: open Agent Skills format/specification
Classification: STANDARD / FORMAT, not PostgreSQL product authority
```

## Reviewed practitioner skill

```text
Publisher: Neon
Repository: neondatabase/postgres-skills
Reviewed main: 27fe45e0f71ea89a6eaf9ea4d2e4068957c81c26
Skill: skills/postgres-best-practices/SKILL.md
Skill blob: 1720cf9fb7e7c31795433756d4bea154b5512d0f
License: Apache-2.0
HX classification: COMMUNITY / reviewed expert reference
```

The Neon skill is vendor-agnostic and covers PostgreSQL 14-18 best practices. It is not PostgreSQL Global Development Group authority and is not vendored or installed as a second HX source of truth.

## HX wrapper

```text
skills/postgresql/hx-postgresql-advisor/
```

The wrapper combines current PGDG truth, selected Neon practitioner guidance, and HX-specific architecture/validation constraints.
