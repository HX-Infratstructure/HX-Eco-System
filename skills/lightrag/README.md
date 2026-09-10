# HX LightRAG Skills

LightRAG on HX-11 uses a governed HX wrapper around **current official HKUDS/LightRAG repository guidance**.

Unlike Qdrant, the current `HKUDS/LightRAG` repository does not publish a Qdrant-style official `SKILL.md` catalog. Its strongest current upstream authorities are the repository `AGENTS.md`, API/server documentation, `env.example`, release metadata, and implementation source/tests.

## Canonical HX skill

```text
skills/lightrag/hx-lightrag-advisor/
```

Classification:

```text
HX_NATIVE + WRAPPER
```

Status:

```text
APPROVED for HX LightRAG planning, configuration reasoning,
validation preparation, troubleshooting, migration, and upgrade guidance.
Execution remains subordinate to the future HX-11 runbook and live evidence.
```

## HX placement

```text
HX-11  192.168.50.211
LightRAG + LightRAG MCP
Native Ubuntu Linux + systemd
Direct LAN API/UI
```

The current BASE smoke authority expects LightRAG to use already-proven HX dependencies when its accepted configuration requires them, including:

- HX-10 Qdrant for vector storage when selected;
- HX-4 BGE-M3 at 1024 dimensions;
- one already-PASS HX LLM endpoint;
- HX-9 PostgreSQL/Redis only if the owner-approved LightRAG storage design selects them.

The exact HX-11 KV, graph, and document-status storage choices are not yet pinned. The skill must not choose those silently from a generic tutorial.

## Upstream model

Primary official source:

```text
HKUDS/LightRAG
reviewed main: d964d92b1018c27983d1dcf6ca19ebbaebeb262e
latest reviewed release: v1.5.7 (2026-09-02)
```

The wrapper directs agents to verify the current release/repository state at implementation time rather than freezing examples into HX.

## Material corrections to generic setup guidance

For HX:

- Docker/Compose/Kubernetes examples are not execution authority.
- Prefer the official host-native `lightrag-hku[api]` package and `lightrag-server` runtime rather than inventing a custom FastAPI `server.py`.
- Do not point HX-11 at `localhost` for Qdrant, embeddings, or an LLM when those capabilities live on assigned HX servers.
- BGE-M3 uses `1024` dimensions in current LightRAG/HX guidance, not `1536`.
- Do not introduce Neo4j, MongoDB, Milvus, OpenSearch, or another backend without an owner-approved HX architecture decision.
- Do not force Docling or Crawl4AI into LightRAG BASE smoke validation; those integrations remain later proof unless explicitly promoted.

## Community sources

Community Claude Code skills, hooks, and LightRAG MCP implementations exist and can be useful reference material. They are not vendor-official and are not automatically installed by this skill.

See:

```text
skills/lightrag/hx-lightrag-advisor/references/community-candidates.md
```

Any community skill/hook/MCP must pass separate HX governance before operational use.
