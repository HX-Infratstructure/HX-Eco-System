# Current Redis Upstream Guidance

## Primary product authority

Use current official Redis sources for version-sensitive claims:

- Redis documentation: `https://redis.io/docs/latest/`
- Redis source repository: `https://github.com/redis/redis`
- Redis releases: `https://github.com/redis/redis/releases`
- Redis installation guidance: `https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/`
- Redis persistence: `https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/`
- Redis clients: `https://redis.io/docs/latest/develop/clients/`
- Search/query: `https://redis.io/docs/latest/develop/interact/search-and-query/`

At the 2026-09-09 review, the latest non-prerelease GitHub release is Redis 8.10.1, published 2026-08-17. Treat that as current upstream context. The HX-9 runtime version is selected only by current owner/runbook authority.

## Official Redis Agent Skills

```text
Repository: redis/agent-skills
Reviewed branch: main
Reviewed commit: a84871d065f398fed55e1633f66b66f731eb4e2b
Reviewed date: 2026-09-09
Plugin: redis-development
Plugin version: 1.4.0
License: MIT
```

The repository is published by the Redis GitHub organization and contains eight Agent Skills. It uses `skills/` as source of truth, vendored plugin copies for distribution, validation, and eval baselines.

Read `redis-agent-skills.md` for HX dispositions.

## Version discipline

Before a material Redis build/upgrade recommendation:

1. identify current accepted HX version/package source if any;
2. verify current Redis stable release and release notes;
3. verify command behavior against docs for the installed version;
4. reconcile client/framework compatibility;
5. classify any architecture-impacting recommendation against HX authority.

Do not silently turn “latest stable” into “approved HX version.”
