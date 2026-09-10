---
name: hx-lightrag-advisor
description: Guide LightRAG work inside the HX Eco-System by combining HX architecture and execution authority with current official HKUDS/LightRAG guidance. Use for HX-11 LightRAG planning, native bare-metal installation, configuration, storage/backend selection, model and embedding integration, document pipeline choices, API usage, validation, smoke testing, troubleshooting, performance diagnosis, migration, or upgrades, including the LightRAG MCP companion. Preserve HX owner decisions and server placement; official upstream guidance informs product decisions but cannot override HX architecture, runbooks, smoke-test criteria, network/security/storage boundaries, or model-placement rules.
---

# HX LightRAG Advisor

Use current LightRAG engineering guidance without allowing generic deployment examples or community integrations to redesign HX.

## Authority order

Apply this order before recommending or changing anything:

1. Current infrastructure-owner instruction.
2. Current HX control and architecture Markdown.
3. Current live evidence from the relevant HX server.
4. Current HX server record, runbook, and application/model standards.
5. Current HX smoke-test roadmap and exact smoke-test authority when validating.
6. Current official `HKUDS/LightRAG` repository guidance for LightRAG-specific behavior.
7. Reviewed community LightRAG skills/MCPs as reference only.
8. General model knowledge only when higher authorities do not answer the question.

Do not treat an upstream example as HX architecture.

## Workflow

### 1. Establish HX context first

Read `references/hx-context.md` and `references/authority-map.md`.

Before LightRAG work, be able to state:

- owner server and IP;
- current build state;
- LightRAG's HX role and MCP companion boundary;
- native deployment boundary;
- accepted LLM, embedding, vector-store, and other required storage dependencies;
- current build-roadmap position and smoke-proof prerequisites;
- BASE PASS boundary;
- whether the task is planning, build/configuration, validation, troubleshooting, migration, or upgrade.

If any required implementation choice is not yet owner-pinned, classify it as `OWNER_DECISION_REQUIRED`; do not fill the gap from a generic tutorial.

### 2. Verify current official LightRAG guidance

Read `references/upstream.md`.

For material implementation or troubleshooting work, verify current upstream rather than relying on remembered LightRAG behavior. Prefer:

1. current `HKUDS/LightRAG` release/tag and `main` state;
2. upstream `AGENTS.md` for repository architecture and developer rules;
3. `docs/LightRAG-API-Server.md` for server/API/auth/storage configuration;
4. current `env.example` for supported configuration keys and defaults;
5. storage/parser/role-specific documentation linked by the current repo;
6. source code only when documentation is insufficient or behavior is disputed.

The official LightRAG repository does not currently provide a Qdrant-style official `SKILL.md` library. Do not describe a community skill as vendor-official.

### 3. Reconcile guidance with HX

Classify each material recommendation as:

- `ACCEPT` — compatible with current HX authority.
- `ADAPT` — upstream principle is useful but must be changed to fit HX.
- `REJECT_FOR_HX` — conflicts with an explicit HX decision.
- `OWNER_DECISION_REQUIRED` — would choose or change unresolved HX architecture.

Examples:

- Docker/Compose/Kubernetes deployment -> `REJECT_FOR_HX` unless the owner explicitly changes the native/systemd standard.
- LightRAG Cloud/host replacement -> `REJECT_FOR_HX` unless server placement changes are approved.
- custom hand-written FastAPI `server.py` replacing the official server -> normally `REJECT_FOR_HX`; prefer the official `lightrag-server` runtime.
- `localhost` model/vector endpoints on HX-11 -> `REJECT_FOR_HX` when the assigned HX dependency lives on another server.
- BGE-M3 configured at 1536 dimensions -> `REJECT_FOR_HX`; current HX BGE-M3 authority is 1024 dimensions.
- adding Neo4j, MongoDB, Milvus, OpenSearch, or another unassigned backend -> `OWNER_DECISION_REQUIRED`.
- selecting LightRAG's KV, graph, or document-status backend when HX has not yet pinned it -> `OWNER_DECISION_REQUIRED`.
- LightRAG API/query/parser behavior that does not alter HX architecture -> normally `ACCEPT` or `ADAPT`.
- firewall/TLS/DNS/routing/auth architecture changes -> `OWNER_DECISION_REQUIRED` unless already approved.

### 4. Use the official native runtime

For the HX-11 base build, prefer the current official host-native distribution and server entrypoint:

```text
Python >= upstream supported floor
isolated Python environment
lightrag-hku[api]
lightrag-server
systemd service defined by the HX-11 runbook
```

Verify the stable LightRAG version at build time and pin the accepted version in the HX-11 as-built record/runbook. Do not silently float to `latest` during an implementation or smoke run.

Do not create the HX-11 runbook inside this skill. If it does not yet exist, report that gap and create it through normal repository authority before executing the build.

### 5. Preserve the HX model and storage architecture

LightRAG requires four logical storage roles: KV, vector, graph, and document status. Upstream supports multiple implementations; support does not equal HX approval.

Current HX direction:

- HX-10 Qdrant is the expected vector service when the accepted LightRAG configuration uses Qdrant.
- HX-4 BGE-M3 is the primary/default embedding capability at 1024 dimensions.
- use only already-PASS HX model endpoints required by the accepted configuration;
- do not run duplicate Ollama/embedding/Qdrant services on HX-11 merely for convenience;
- do not infer the KV/graph/document-status backend from a tutorial; use the owner-approved HX-11 configuration when it is pinned.

If a storage change would alter persisted LightRAG data layout, collection identity, graph semantics, or migration requirements, treat it as a material architecture/migration decision.

### 6. Preserve embedding identity

Do not change the embedding model after data is indexed without an explicit migration/re-index plan.

For HX:

- BGE-M3 = 1024 dimensions;
- keep embedding identity and dimension consistent with the accepted LightRAG/Qdrant state;
- never mix vectors from different embedding model identities in the same HX Qdrant collection;
- a model change requires a new collection/re-embedding path under current HX policy.

### 7. Keep parsing choices subordinate to the base boundary

Current LightRAG has native and external parsing paths plus multiple chunking strategies. Consult current upstream before choosing them.

For BASE smoke validation, keep the LightRAG proof narrow: synthetic text ingestion and retrieval/query. Do not force Docling, Crawl4AI, MinerU, VLM, or production document pipelines into LightRAG BASE PASS merely because upstream supports them.

HX-16 Docling and HX-17 Crawl4AI remain separately owned ecosystem components. Their later integration with LightRAG is a separate validation/integration decision.

### 8. Validate through the HX smoke model

When validating HX-11:

1. confirm the deployment roadmap says HX-11 is ready;
2. confirm the smoke roadmap's required prior PASS evidence;
3. execute `smoke-tests/lightrag-smoke-test.md` from HX-5 CentCom after CentCom activation;
4. use the accepted Qdrant/embedding/LLM path only when required by the HX-11 configuration;
5. prove known-answer ingestion, retrieval, RAG response, cleanup, and cleanup verification;
6. execute the LightRAG MCP companion gate separately;
7. capture reboot-persistence and retained evidence before closure.

Do not replace HX acceptance with `/health`, a WebUI render, a vendor quickstart, or a community Claude skill.

### 9. Treat community skills and MCPs as reference only

Read `references/community-candidates.md` when agent-client or MCP integration is in scope.

Community projects can provide useful implementation ideas, but they are not current LightRAG vendor authority. Do not automatically install:

- Claude Code hooks that sync memory on session events;
- Node helpers;
- community MCP servers;
- LobeHub/OpenClaw packages;
- skill packages that assume `localhost` or a different auth/network model.

Any such integration must pass HX skill/MCP governance separately before operational use.

### 10. Produce an auditable result

For material LightRAG decisions, summarize:

```text
HX CONTEXT
  server / role / state / applicable authority

OFFICIAL LIGHTRAG GUIDANCE
  release/commit / docs or source inspected

COMMUNITY INPUT
  source and status, if used

RECONCILIATION
  ACCEPT / ADAPT / REJECT_FOR_HX / OWNER_DECISION_REQUIRED

EXECUTION AUTHORITY
  exact HX runbook/standard, or explicit gap if not yet created

VALIDATION AUTHORITY
  smoke roadmap + exact LightRAG/MCP smoke authority

STOP CONDITIONS
  unresolved owner decision, stale prerequisite, migration risk, or cleanup boundary
```

## Stop conditions

Stop and report rather than improvising when:

- the HX-11 runbook or server record required for execution does not yet exist;
- vendor/community guidance would change HX server placement or native deployment architecture;
- the accepted LightRAG storage mix is not yet pinned and the task requires choosing one;
- a recommendation would add a new database/graph/vector service not already assigned by HX;
- an embedding model/dimension change would invalidate existing indexed data;
- current live behavior contradicts active HX smoke/runbook authority;
- cleanup could affect non-smoke LightRAG/Qdrant data;
- required credentials are unavailable;
- a version-specific behavior cannot be verified against current official LightRAG guidance.

## References

- `references/hx-context.md` — HX-11 placement, dependencies, and boundaries.
- `references/authority-map.md` — HX repository authority and validation sequence.
- `references/upstream.md` — official LightRAG provenance and current-source workflow.
- `references/community-candidates.md` — reviewed community skill/MCP candidates and restrictions.
