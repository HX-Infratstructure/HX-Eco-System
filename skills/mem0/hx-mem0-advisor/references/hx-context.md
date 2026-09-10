# HX Mem0 Context

## Placement

```text
Server: HX-13
IP: 192.168.50.213
Role: Mem0 OSS + assigned MCP capability
Current state: NOT STARTED
Deployment: native Ubuntu Linux; systemd for long-running services where applicable
Containers: not used unless the owner explicitly changes the architecture
```

Mem0 is the HX memory-layer component. It is downstream of the state/retrieval and model planes; it does not own Qdrant, Ollama, PostgreSQL, Redis, or their configuration.

## Current roadmap position

The current base implementation roadmap places Mem0 at priority 13, after LightRAG and after the required state/retrieval/model dependencies are proven.

Current BASE PASS summary:

```text
native Mem0
accepted dependency configuration
disposable store/search/delete memory lifecycle
assigned Mem0 MCP companion smoke test
cleanup
persistent config / reboot validation
```

Authority: `smoke-tests/mem0-smoke-test.md`.

## Current smoke dependency model

The current executable smoke test requires:

- HX-10 Qdrant with accepted PASS evidence;
- an approved HX Ollama embedding endpoint with accepted embedding proof;
- an approved local LLM endpoint;
- a disposable Qdrant collection named `hx_mem0_smoke`;
- a synthetic user ID and token;
- `infer=False` so the known-answer test isolates deterministic memory storage/retrieval from LLM extraction behavior.

The current test uses `Memory.from_config` with a Qdrant vector store, Ollama LLM, and Ollama embedder. Current upstream documentation still supports those configuration primitives at the reviewed commit.

## Current implementation gaps

As of the current clean rebuild state:

- HX-13 is NOT STARTED;
- no active HX-13 server record exists under `docs/02-server-records/`;
- no active HX-13 runbook exists under `docs/03-runbooks/`;
- the exact Mem0 package/runtime version is not owner-pinned by an HX-13 runbook;
- environment/venv layout is not pinned;
- service/API process and systemd unit design are not pinned;
- Mem0 config/data/cache paths are not pinned;
- permanent Qdrant collection naming/ownership is not pinned;
- permanent embedding/LLM model bindings are not pinned;
- network listener/access pattern is not pinned;
- memory retention, cross-agent sharing, graph memory, and production identity scoping are not BASE assumptions;
- exact assigned Mem0 MCP implementation remains to be selected/reviewed.

Do not fill these gaps from a tutorial or hosted Platform default.

## HX invariants

- One server -> validate -> record -> next server.
- Native Linux; no Docker/Podman/Kubernetes.
- Do not impose firewall/TLS/access restrictions without owner approval.
- Do not make unapproved network or permanent cross-service architecture changes.
- Product-specific MCP belongs to the parent application's base build but is independently smoke-tested.
- HX-15 FastMCP is not a prerequisite for a product-specific Mem0 MCP implementation.
- HX-5 CentCom is the standard remote fleet smoke-test runner after its activation gate.
- Validation-only data and collections are disposable and must be removed.
- Documentation or skill approval never changes BUILD-STATE.
