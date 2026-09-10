# PostgreSQL and Agent Skills Upstream Provenance

## Primary PostgreSQL authority

Project:

```text
PostgreSQL Global Development Group (PGDG)
Official site: https://www.postgresql.org/
Documentation: https://www.postgresql.org/docs/
Version policy: https://www.postgresql.org/support/versioning/
Ubuntu packages: https://www.postgresql.org/download/linux/ubuntu/
```

At review time (2026-09-09):

```text
Current stable major: PostgreSQL 18
Current stable minor: 18.6
18.6 release date: 2026-08-13
Supported majors: 18, 17, 16, 15, 14
PostgreSQL 14 EOL: 2026-11-12
Development line: PostgreSQL 19 beta
```

Always re-check these facts before a build, migration, upgrade, or version-sensitive recommendation.

The PostgreSQL versioning policy recommends running the current minor release within the chosen supported major. That principle does not choose the HX major version.

## Ubuntu packaging

Official PostgreSQL guidance recognizes two relevant native Ubuntu paths:

1. Ubuntu's distribution-provided PostgreSQL package; and
2. the PostgreSQL Apt Repository (PGDG), which exposes supported major versions explicitly.

Do not choose between them inside the skill. The HX-9 runbook must pin package source and major version.

## Core configuration facts to verify from the accepted major

The PostgreSQL manual documents that:

- `listen_addresses` defaults to `localhost`;
- `*` listens on all available interfaces;
- `0.0.0.0` listens on all IPv4 interfaces;
- default PostgreSQL port is `5432`;
- `pg_hba.conf` controls client authentication after the server is listening;
- server/client versions and effective runtime settings should be inspected rather than assumed.

Use the manual for the accepted HX major; do not carry a remembered setting across major versions without verification.

## Agent Skills standard

Source:

```text
https://agentskills.io/
```

Agent Skills is an open skill format, not a PostgreSQL vendor catalog. The specification defines:

```text
<skill>/SKILL.md                    required
scripts/ references/ assets/       optional
name + description frontmatter     required
progressive disclosure             expected
SKILL.md under 500 lines           recommended
relative references                recommended
```

At review time no PostgreSQL-specific skill was published by agentskills.io itself; the site defines the standard and creation/validation guidance.

## Current-source workflow

For any version-sensitive PostgreSQL task:

1. identify the accepted HX major/version if already pinned;
2. check `postgresql.org/support/versioning/`;
3. inspect release notes for the current minor in that major;
4. use the matching major-version manual;
5. inspect official Ubuntu/PGDG packaging guidance when package source is relevant;
6. consult the reviewed Neon Agent Skill only as subordinate expert guidance;
7. reconcile with HX architecture before recommending a change.
