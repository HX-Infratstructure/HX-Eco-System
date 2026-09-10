# Mem0 Upstream Reference

## Reviewed official source

```text
Organization: mem0ai
Repository: mem0ai/mem0
Reviewed main: 02f7a9b2c4fe38dedb96631e48c85c74ad58b605
Reviewed date: 2026-09-09
License: Apache-2.0
Official docs: https://docs.mem0.ai/
Vibecoding/skills landing page: https://docs.mem0.ai/vibecoding
```

The reviewed main commit is dated 2026-09-08 and includes the current official skills graph and coding-agent integration work.

## Current source versions at the review point

```text
Python project: mem0ai
pyproject.toml version: 2.0.20
Python requirement: >=3.10,<4.0

TypeScript project: mem0ai
mem0-ts/package.json version: 3.1.6
```

Official pipeline skill metadata declares tested SDK ranges:

```text
mem0ai (PyPI) >=2.0.0,<3.0.0
mem0ai (npm)  >=3.0.0,<4.0.0
```

These facts constrain compatibility checks. They do not select the HX-13 package version.

## Current OSS primitives relevant to HX

At the reviewed commit, official source/docs support:

- `Memory.from_config(...)` for OSS configuration;
- Qdrant vector-store configuration using `collection_name` and `embedding_model_dims`;
- Ollama embedding configuration using `model`, `embedding_dims`, and `ollama_base_url`;
- OSS semantic search using `filters`, `top_k`, and `threshold`;
- Python and TypeScript SDKs plus framework integrations.

This aligns with the current HX Mem0 smoke-test shape. Re-verify against the accepted installed version before execution.

## Release-tag caution

The repository's latest GitHub release tag at the review point is a component/plugin release (`pi-agent-v0.3.0`), not a reliable canonical version marker for the Python Mem0 OSS runtime. For HX runtime version decisions, use the accepted package source, package metadata, changelog/release notes, and runbook decision together rather than blindly using `releases/latest`.

## MCP/plugin landscape

- The official repo advertises hosted MCP at `https://mcp.mem0.ai`; this requires the Platform and must not be assumed to be the HX-13 assigned MCP.
- The official portable `integrations/mem0-agent-plugin` is an agent-plugin package for coding assistants; reviewed plugin metadata version is 0.3.1 and it includes a stdio MCP server.
- The separate `mem0ai/mem0-mcp` repository is archived. Do not select it as the HX companion by default.

Exact HX-13 MCP implementation remains `OWNER_DECISION_REQUIRED` until a current runbook/admission decision pins it.
