# Mem0 Skill Upstream Source

## Primary product authority

```text
Project: Mem0
Organization: mem0ai
Repository: mem0ai/mem0
Official docs: https://docs.mem0.ai/
Vibecoding/skills: https://docs.mem0.ai/vibecoding
Reviewed main: 02f7a9b2c4fe38dedb96631e48c85c74ad58b605
Reviewed date: 2026-09-09
License: Apache-2.0
```

## Current source versions at review

```text
Python package: mem0ai
Source version: 2.0.20
Python requirement: >=3.10,<4.0

TypeScript package: mem0ai
Source version: 3.1.6
```

The official pipeline skills declare compatibility with Python `mem0ai >=2.0.0,<3.0.0` and npm `mem0ai >=3.0.0,<4.0.0`. These are compatibility/provenance facts, not an automatic HX-13 version selection.

## Official Agent Skills graph

Reviewed under `mem0ai/mem0/skills/`:

```text
Reference skills
- mem0                    version 3.0.0
- mem0-cli                version 1.1.0
- mem0-vercel-ai-sdk      version 1.1.0

Pipeline skills
- mem0-integrate          version 0.1.0
- mem0-test-integration   version 0.1.0
- mem0-oss-to-platform    migration workflow
```

The repository explicitly distinguishes always-available reference skills from on-demand pipeline skills that can create branches/files, install dependencies, run tests/code, or migrate projects.

## HX classification

```text
Upstream skills classification: VENDOR_OFFICIAL
HX wrapper: skills/mem0/hx-mem0-advisor/
HX runtime stance: native/self-hosted Mem0 OSS on HX-13
```

HX does not direct-install the six-skill upstream graph as a second canonical source. The HX wrapper consumes current vendor expertise while preserving HX execution and validation authority.

## Coding-assistant plugin and MCP provenance

```text
Portable plugin path: integrations/mem0-agent-plugin
Reviewed plugin version: 0.3.1
Plugin purpose: cross-session memory/token savings for coding agents
Plugin MCP transport: stdio via Python mcp_server.py
Hosted MCP: https://mcp.mem0.ai (Platform/API-key oriented)
Standalone repository: mem0ai/mem0-mcp — archived at review
```

These are reference capabilities. They do not establish the exact HX-13 assigned MCP implementation.

## Current HX-relevant OSS API confirmation

At the reviewed main commit, official source/docs continue to support the primitives already used by the HX Mem0 smoke authority:

- `Memory.from_config(...)`;
- Qdrant `collection_name` and `embedding_model_dims`;
- Ollama `model`, `embedding_dims`, and `ollama_base_url`;
- semantic search with `filters`, `top_k`, and `threshold`.

Re-verify against the accepted installed package version during implementation.
