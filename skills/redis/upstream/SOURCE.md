# Redis Skill Upstream Source

## Primary product authority

```text
Project: Redis
Authority: Redis official documentation, source, and releases
Official site: https://redis.io/
Documentation: https://redis.io/docs/latest/
Source repository: https://github.com/redis/redis
Releases: https://github.com/redis/redis/releases
Review date: 2026-09-09
Latest non-prerelease release at review: 8.10.1 (published 2026-08-17)
```

Redis 8.10.1 is current upstream release context at review time. This does not independently select or upgrade the HX-9 Redis runtime; the current owner/runbook remains execution authority.

## Official Redis Agent Skills

```text
Publisher: Redis
Repository: redis/agent-skills
Reviewed branch: main
Reviewed main: a84871d065f398fed55e1633f66b66f731eb4e2b
Plugin: redis-development
Plugin version: 1.4.0
License: MIT
HX classification: VENDOR_OFFICIAL external source
```

The reviewed repository contains eight source skills under `skills/`: `redis-core`, `redis-connections`, `redis-search`, `redis-semantic-cache`, `redis-clustering`, `redis-security`, `redis-observability`, and `iris-development`. Its distribution layer vendors real copies into plugin packages and validates plugin/source drift and eval baselines.

## HX disposition

The official Redis bundle is reviewed product expertise, not a second canonical HX library. HX uses a local wrapper because some upstream guidance assumes architectures outside current HX BASE:

- core/connections/search/observability — accept and adapt;
- security — adapt; owner approval remains required for TLS/firewall/bind/protected-mode/global command hardening changes;
- clustering/replicas — reference-only unless HX topology is separately changed;
- Redis Cloud LangCache and managed Agent Memory — reference-only for current native HX-9.

The upstream skill tree is not vendored wholesale. Re-fetch/review current upstream material when behavior, versions, or HX-relevant scope materially changes.

## HX wrapper

```text
skills/redis/hx-redis-advisor/
```

The wrapper combines current Redis truth, selected official Agent Skills expertise, and HX-specific architecture/validation constraints.
