# Official LightRAG Upstream

## Primary source

```text
Organization: HKUDS
Repository: HKUDS/LightRAG
Reviewed main commit: d964d92b1018c27983d1dcf6ca19ebbaebeb262e
Reviewed latest release: v1.5.7
Release publication date: 2026-09-02
Review date: 2026-09-09
Classification: official project source
Official LightRAG SKILL.md library: not found at review time
```

## Current official facts relevant to HX

- Package name: `lightrag-hku`.
- Python floor in current `pyproject.toml`: `>=3.10`.
- API/server install path: `lightrag-hku[api]`.
- Official server entrypoint: `lightrag-server`.
- API server default host configuration in current `env.example`: `HOST=0.0.0.0`, `PORT=9621`.
- LightRAG supports API-key authentication through `LIGHTRAG_API_KEY` / `X-API-Key`; HX does not automatically adopt a security change without owner approval.
- LightRAG uses four logical storage roles: KV, vector, graph, and document status.
- `QdrantVectorDBStorage` uses `QDRANT_URL`; `QDRANT_API_KEY` is optional according to current upstream configuration.
- Current LightRAG guidance shows BGE-M3 at `EMBEDDING_DIM=1024`.
- Current file pipeline supports `legacy`, `native`, `mineru`, and `docling` parser routes plus fixed, recursive, vector-semantic, paragraph-semantic, and custom chunking paths.
- Query modes include `local`, `global`, `hybrid`, `mix`, and `naive`; current APIs also expose direct/query-data behavior described by the upstream server docs.

## Upstream workflow

For every material HX-11 implementation, troubleshooting, or upgrade session:

1. confirm the latest stable LightRAG release;
2. inspect current `main` when behavior may have changed after the latest release;
3. read `AGENTS.md` for current repository architecture and developer rules;
4. read `docs/LightRAG-API-Server.md` and current `env.example` for server/storage/auth keys;
5. read specialized storage/parser/role docs only as needed;
6. inspect source/tests when documentation and live behavior disagree;
7. record the accepted release/commit in the HX-11 implementation record.

Do not freeze generic blog/tutorial examples into HX. LightRAG is actively changing and current upstream must be rechecked at build time.
