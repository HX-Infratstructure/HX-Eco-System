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
State: NOT STARTED
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

At the 2026-09-09 review, the latest non-prerelease Redis release is 8.10.1 and the reviewed `redis/agent-skills` main commit is `a84871d065f398fed55e1633f66b66f731eb4e2b`. These record upstream context; they do not by themselves select the HX-9 runtime version or package source.

## Important boundary

The wrapper is approved guidance; HX-9 itself remains NOT STARTED. It does not advance BUILD-STATE or independently select Redis runtime version/package source, service/config/data path, persistence/memory/eviction policy, network/auth/TLS/firewall policy, Cluster/Sentinel/replication topology, application integration, or exact Redis MCP implementation before current HX authority pins those choices.

Validation remains controlled by `smoke-tests/redis-smoke-test.md`, the companion MCP smoke test, reboot persistence, retained evidence, and current HX closure rules.
