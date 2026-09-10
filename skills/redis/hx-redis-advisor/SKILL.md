---
name: hx-redis-advisor
description: Guide Redis work inside the HX Eco-System using HX architecture and execution authority, current official Redis documentation/releases, and reviewed Redis Agent Skills. Use for HX-9 Redis planning, native standalone installation/configuration, persistence/recovery, memory and eviction, key/TTL/data modeling, client connections/pipelining, Search/JSON/vector/RAG, Streams/coordination, agent-memory patterns, observability, validation, troubleshooting, upgrades, and the Redis MCP companion. Never let upstream guidance override HX server placement, native/systemd deployment, shared-host rules, network/security boundaries, topology decisions, or BASE PASS criteria.
---

# HX Redis Advisor

Apply current Redis expertise without allowing vendor quickstarts, cloud products, cluster patterns, or generic hardening advice to redesign HX-9.

## Authority order

1. Current infrastructure-owner instruction.
2. Current HX control/architecture Markdown.
3. Current live HX-9 evidence.
4. Current HX-9 server record/runbook/standards.
5. HX smoke roadmap and exact Redis/MCP smoke authority when validating.
6. Current official Redis product documentation, releases, and packaging guidance.
7. Reviewed official `redis/agent-skills` guidance as subordinate product expertise.
8. Historical reference and general model knowledge only where higher authorities do not answer.

Before material work, follow the scoped preflight in `skills/AGENTS.md`: read root `AGENTS.md` and `README.md`, establish current component state, read `skills/SKILL-GOVERNANCE.md`, `skills/SKILL-REGISTRY.md`, and `skills/redis/README.md`, then load this wrapper and only the references required for the task. Do not use `human-html/` or `archive/` as execution authority.

Read `references/hx-context.md` and `references/authority-map.md` first.

## Operating workflow

### Establish HX context

Before material Redis work, state the HX-9 host/IP, current build state, Redis/MCP role, PostgreSQL shared-host boundary, accepted runtime version/package source if pinned, accepted data/persistence/memory/access pattern if pinned, task type, BASE boundary, and prerequisite proof.

If execution depends on an unpinned choice, return `OWNER_DECISION_REQUIRED`; do not inherit a default from upstream skills or a tutorial.

### Verify current Redis authority

Read `references/upstream.md`. For version-sensitive work, verify the current stable Redis release, release notes, command documentation, and Ubuntu packaging guidance applicable to the accepted HX runtime.

At the 2026-09-09 review, official upstream latest stable is Redis 8.10.1. This is upstream context, not automatic authority to select or upgrade HX-9.

### Use Redis Agent Skills correctly

Read `references/redis-agent-skills.md` when the task overlaps data modeling, clients, Search, clustering, security, observability, semantic caching, or agent memory.

The official Redis Agent Skills repository is valuable vendor expertise, but HX does not install its full bundle as a second canonical source. Redis Cloud-only, cluster/replication, and generic security-hardening assumptions remain subordinate to HX architecture.

### Reconcile material recommendations

Use exactly these labels:

- `ACCEPT` — compatible with current HX authority.
- `ADAPT` — Redis principle is useful but implementation must fit HX.
- `REFERENCE_ONLY` — useful knowledge outside current HX runtime/base scope.
- `REJECT_FOR_HX` — conflicts with an explicit HX decision.
- `OWNER_DECISION_REQUIRED` — chooses or changes unresolved HX architecture.

Typical classifications:

- Docker/Podman/Kubernetes -> `REJECT_FOR_HX` unless the owner changes the native standard.
- Redis Cloud replacing HX-9 -> `REJECT_FOR_HX` unless placement changes.
- Cluster/Sentinel/replication/failover -> `OWNER_DECISION_REQUIRED`; not current BASE.
- LangCache or Redis Agent Memory managed service -> `REFERENCE_ONLY` unless separately adopted.
- TLS, firewall, bind/protected-mode restriction, global command disabling -> `OWNER_DECISION_REQUIRED` unless already authorized.
- Redis ACL users required by a current HX identity/work order -> normally `ACCEPT` or `ADAPT` within that scope.
- key/type/TTL/client/query advice without infrastructure impact -> normally `ACCEPT` or `ADAPT`.

## HX-9 deployment boundary

```text
HX-9 / 192.168.50.209
├── PostgreSQL + PostgreSQL MCP — separately governed
└── Redis + Redis MCP — this skill's scope
```

Use native Linux + systemd. Do not hardcode a systemd unit/config/data path until the selected package and current runbook establish them. Discover runtime state first.

Do not create a second Redis instance for smoke testing unless the owner authorizes it. Do not install runtime binaries from historical or `redis-unstable` reference material.

When the HX-9 runbook exists, infrastructure-changing commands come from that runbook, not this skill.

## Task references

Use current official Redis documentation for feature-specific details after reading `references/upstream.md` and `references/redis-agent-skills.md`. For HX-specific placement, authority, topology, security boundaries, and acceptance rules, use `references/hx-context.md` and `references/authority-map.md`.

Use `scripts/redis-readonly-audit.sh` only for read-only baseline collection when its endpoint/credential handling matches the current environment.

## Redis correctness rules

- A pipeline reduces round trips; it is not inherently atomic. Distinguish non-transactional pipelining, `MULTI`/`EXEC`, and Lua/Functions.
- Prefer bounded/cursor operations over whole-keyspace or unbounded reads on production-sized data.
- For every application namespace, define owner, consumers, type/serialization, TTL, eviction tolerance, persistence class, source of truth, and rebuild method.
- Redis must not silently become the system of record for PostgreSQL-owned relational data.
- Shared HX-9 memory sizing must account for PostgreSQL, OS headroom, fork/copy-on-write, persistence rewrites, client buffers, Search/vector indexes, and page cache.
- Probe the installed version/command surface before relying on Redis 8.x capabilities.

## Validation boundary

Redis BASE validation remains controlled by the current smoke roadmap and exact authorities. The current proof chain is `B3` HX-9 Redis core -> `B4` HX-9 Redis MCP. `B3` requires CentCom active and proves PING, bounded SET/GET of the exact smoke token, DELETE, and cleanup verification through `smoke-tests/redis-smoke-test.md`. `B4` requires accepted `B3` PASS and proves only the parent Redis MCP companion through `smoke-tests/mcp-companion-smoke-test.md`. Reboot/evidence closure follows current HX roadmap rules.

Do not substitute `systemctl active`, `PING`, a vendor quickstart, or this skill for the current smoke authority.

Never report `PASS` for unexecuted checks. Use `FAIL`, `BLOCKED`, `NOT TESTED`, or `OWNER_DECISION_REQUIRED` where evidence or authority is incomplete.
