# Redis Agent Skills Review for HX

## Reviewed source

```text
Publisher: Redis
Repository: redis/agent-skills
Commit: a84871d065f398fed55e1633f66b66f731eb4e2b
Plugin: redis-development 1.4.0
License: MIT
HX classification: VENDOR_OFFICIAL external source behind HX_NATIVE + WRAPPER
```

Do not vendor or direct-install the full upstream bundle as a second HX authority. The canonical HX source remains `skills/redis/hx-redis-advisor/`.

## Skill-by-skill disposition

| Upstream skill | HX disposition | Reason |
|---|---|---|
| `redis-core` | `ACCEPT + ADAPT` | Strong data-type/key guidance; add HX ownership, TTL, persistence and Redis 8.x awareness. |
| `redis-connections` | `ACCEPT + ADAPT` | Useful pooling/SCAN/timeouts; keep pipeline vs transaction semantics explicit. |
| `redis-search` | `ACCEPT + ADAPT` | High-value Search/vector/RAG guidance; verify current 8.x command/version gates. |
| `redis-observability` | `ACCEPT + ADAPT` | Good triage baseline; integrate HX shared-host and evidence rules. |
| `redis-security` | `ADAPT / OWNER_DECISION_REQUIRED` | Technical guidance is valid, but TLS/firewall/bind/protected-mode/global command changes cannot become autonomous HX defaults. |
| `redis-clustering` | `REFERENCE_ONLY` | Cluster, replicas and related topology are outside current HX BASE unless separately authorized. |
| `redis-semantic-cache` | `REFERENCE_ONLY` | Upstream skill targets Redis Cloud LangCache; HX-9 is native/self-managed. |
| `iris-development` | `REFERENCE_ONLY` | Upstream skill targets managed Redis Agent Memory; not current HX-9 BASE. |

## Evaluation signal

Upstream includes `with_skill` versus `without_skill` eval baselines. At the reviewed commit, Redis Search and cloud-specific AI skills show the clearest gains; core is largely neutral on stronger models, and the connections suite contains a pipeline-atomicity regression case. Treat this as evidence supporting selective curation rather than blind bundle adoption.

## HX-specific eval expectations

Any future HX Redis skill evaluation should penalize:

- container recommendations;
- Redis Cloud substitution for HX-9;
- Cluster/Sentinel/replication introduced as default;
- unauthorized firewall/TLS/bind restriction;
- pipeline described as inherently atomic;
- localhost used for remote HX consumers;
- unbounded keyspace operations as production defaults;
- false PASS without smoke/evidence execution.
