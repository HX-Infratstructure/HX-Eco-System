# LightRAG Upstream Source Record

```text
Component: LightRAG
Official organization: HKUDS
Official repository: https://github.com/HKUDS/LightRAG
Reviewed main commit: d964d92b1018c27983d1dcf6ca19ebbaebeb262e
Reviewed latest release: v1.5.7
Release publication: 2026-09-02
Review date: 2026-09-09
Official SKILL.md catalog found: NO
HX wrapper: skills/lightrag/hx-lightrag-advisor/
```

## Primary official authorities

Use current versions of:

- `AGENTS.md`
- `README.md`
- `docs/LightRAG-API-Server.md`
- `env.example`
- storage/parser/role-specific docs linked from the repository
- current source/tests when documentation and runtime behavior disagree

## Current HX-relevant facts at review

- package: `lightrag-hku`
- current Python requirement floor: `>=3.10`
- native API install: `lightrag-hku[api]`
- server entrypoint: `lightrag-server`
- default server configuration exposes `HOST=0.0.0.0`, `PORT=9621`
- API key uses `LIGHTRAG_API_KEY` / `X-API-Key`
- four logical storage roles: KV, vector, graph, document status
- Qdrant vector backend uses `QDRANT_URL`; API key is optional in current upstream configuration
- BGE-M3 example/current Ollama binding dimension: `1024`
- current parsing framework includes legacy/native/mineru/docling routes and multiple chunking strategies

These facts are a reviewed snapshot, not a permanent pin. Reverify current upstream before the HX-11 build or upgrade.

## Community references reviewed separately

- `zwovadis/lightrag-claude-skill` — query-only Claude Code skill; COMMUNITY / REFERENCE_ONLY.
- `butchokoy25/lightrag-claude-skills` — persistent-memory skills/hooks; COMMUNITY / LATER_INTEGRATION.
- `desimpkins/daniel-lightrag-mcp` — community MCP candidate; DISCOVERY / REFERENCE_ONLY.

Do not promote a community source to vendor authority.
