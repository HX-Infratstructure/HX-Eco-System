# Official Docling MCP - HX Companion Disposition

## Reviewed source

```text
Publisher: docling-project
Repository: docling-project/docling-mcp
Reviewed branch: main
Reviewed main: a8a41e6014ba3a148261702e760421086e9c80e3
Reviewed date: 2026-09-09
Latest non-prerelease release: v3.2.0
Release published: 2026-09-01
Package: docling-mcp 3.2.0 at reviewed main
Python: >=3.10
License: MIT
HX classification: VENDOR_OFFICIAL companion source
```

The project exposes document conversion, generation, manipulation, and optional RAG/tool integrations through MCP.

## Upstream modes

Current upstream supports:

- remote mode, currently documented as the default/recommended lightweight path;
- local mode with `docling-mcp[local]`;
- hybrid remote with local fallback;
- transports including stdio, SSE, and streamable HTTP;
- `uvx` as an easy launch mechanism;
- optional RAG/information-extraction toolsets.

These are product capabilities, not HX defaults.

## HX disposition

- official `docling-project/docling-mcp` source -> `ACCEPT + ADAPT` as the preferred product-specific companion source;
- local conversion capability -> likely compatible, but exact package/mode/process/transport/systemd choices remain `OWNER_DECISION_REQUIRED` until the HX-16 runbook pins them;
- remote mode requiring `docling-serve` -> `REFERENCE_ONLY` for current BASE unless explicitly approved;
- containerized Docling Serve -> `REJECT_FOR_HX`;
- managed Docling/IBM watsonx endpoint -> `REJECT_FOR_HX` as a replacement for HX-16 under current architecture;
- hybrid remote/local fallback -> `OWNER_DECISION_REQUIRED` because it creates a new remote dependency/failure path;
- `uvx` launch -> `REFERENCE_ONLY` as a quickstart, not the accepted persistent service architecture;
- LlamaIndex/Milvus, LlamaStack, smolagents, or other optional toolsets -> `REFERENCE_ONLY` for BASE; review separately for later integration;
- MCP client registrations and permanent bindings to Deep Agents, Open WebUI, n8n, or other consumers -> later integration, not D2 BASE proof.

## Version compatibility

Current `docling-mcp` 3.x uses MCP Python SDK 2.x. Verify actual package compatibility with the accepted Docling version and MCP client before the runbook is finalized.

Do not infer the HX-16 service unit, transport, listener, port, cache, or credentials from upstream examples.

## HX smoke boundary

D2 starts only after accepted D1 Docling core PASS.

Use `smoke-tests/mcp-companion-smoke-test.md` to prove:

- real MCP client negotiation;
- advertised safe tool;
- one safe known-answer tool call;
- expected result;
- cleanup of any smoke-namespaced state.

Tool discovery alone is not PASS. Do not create permanent client/agent registration during D2.
