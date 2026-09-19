# HX Redis Skill

Redis on HX-9 uses the governed HX wrapper:

```text
skills/redis/hx-redis-advisor/
```

## HX placement

```text
HX-9 — 192.168.50.209
PostgreSQL + PostgreSQL MCP
Redis + Redis MCP on the same host
State: IN PROGRESS — Redis core/modules/WebUI proven; Redis MCP daemon active, reboot proof pending
Deployment: native Ubuntu Linux + systemd
```

## Source model

Redis publishes an official Agent Skills repository, so the HX wrapper uses a layered source model:

1. **Redis official documentation, releases, source, and packaging guidance** as primary Redis product authority.
2. **Redis `redis/agent-skills`** as reviewed `VENDOR_OFFICIAL` agent expertise, pinned at the recorded review commit.
3. HX architecture/runbooks/smoke authority above all external guidance for HX placement, execution, security, topology, and acceptance decisions.

## Canonical files

```text
skills/redis/
├── README.md
├── upstream/
│   └── SOURCE.md
└── hx-redis-advisor/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── scripts/
    │   └── redis-readonly-audit.sh
    └── references/
        ├── authority-map.md
        ├── hx-context.md
        ├── upstream.md
        └── redis-agent-skills.md
```

## Upstream curation boundary

The official Redis skill bundle is not installed wholesale as a second HX source of truth. The HX wrapper accepts/adapts Redis core, connections, Search, and observability guidance; treats Cluster/replication, Redis Cloud LangCache, and managed Agent Memory as reference-only for current BASE; and keeps TLS/firewall/bind/global-command hardening owner-controlled.

At the 2026-09-09 skill review, Redis 8.10.1 was the upstream context and the reviewed `redis/agent-skills` main commit was `a84871d065f398fed55e1633f66b66f731eb4e2b`. The later owner-directed HX-9 build installed and hash-verified Redis 8.10.2; the live server record now governs the as-built runtime. Skill-review version context must not be used to downgrade the live host.

## Governed intake verification

The current wrapper was re-audited against `skills/AGENTS.md`, `skills/SKILL-GOVERNANCE.md`, the active base implementation roadmap, and the active smoke-test roadmap on 2026-09-09.

Current proof alignment:

```text
B3  HX-9 Redis core
    prerequisite: CentCom active
    live coupling: none; TTL-protected disposable key only
    authority: smoke-tests/redis-smoke-test.md

B4  HX-9 Redis MCP
    prerequisite: accepted B3 Redis PASS
    live coupling: parent Redis service only
    authority: smoke-tests/mcp-companion-smoke-test.md
```

The canonical `hx-redis-advisor` package passes the current skill validator and packages successfully as `skill.zip`. The included `redis-readonly-audit.sh` also passes shell syntax validation and a representative no-Redis read-only run. The helper discovers Redis-named systemd service units rather than assuming a package-specific unit name.

The skill-package validation remains separate from runtime evidence. HX-9 runtime state now comes from the live build and `docs/02-server-records/HX-9.md`, not from skill approval.

## Important boundary

The wrapper remains advisory. HX-9 now runs Redis 8.10.2 natively with AOF, RedisBloom, RedisJSON, RediSearch, P3X Redis UI, and a RedisVL/FastMCP Streamable HTTP companion. The live as-built record pins the current paths, units, listeners, hashes, and deliberate trusted-LAN posture. Redis MCP host-reboot proof, the PID-file/overcommit warnings, and any future memory/eviction tuning remain open; Cluster/Sentinel/replication and generic security hardening remain outside current BASE unless separately approved.

Validation remains controlled by `smoke-tests/redis-smoke-test.md`, the companion MCP smoke test, reboot persistence, retained evidence, and current HX closure rules.
