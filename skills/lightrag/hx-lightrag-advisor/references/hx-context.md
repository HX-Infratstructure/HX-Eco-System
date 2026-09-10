# HX LightRAG Context

## Placement

- Component: LightRAG
- Owner server: HX-11
- IP: `192.168.50.211`
- Current state: `NOT STARTED`
- Companion capability: LightRAG MCP
- Architecture layer: knowledge / RAG
- Native API port expected by current smoke authority: `9621`

## HX deployment boundary

- Native Ubuntu Linux + systemd.
- No Docker, Podman, Kubernetes, or temporary container deployment.
- Normal service access is direct LAN host/port; HX-7 NGINX is not inserted as a common reverse proxy.
- Do not duplicate already-assigned ecosystem services on HX-11 merely to simplify LightRAG configuration.
- Do not impose firewall, TLS, DNS, routing, or access-policy changes without explicit owner approval.

## Dependency direction

Current smoke-roadmap proof for LightRAG expects the accepted HX-11 configuration to consume already-proven capabilities rather than instantiate substitutes locally.

Expected/conditional dependencies:

- HX-10 Qdrant (`192.168.50.210`) when `QdrantVectorDBStorage` is the accepted vector backend.
- HX-4 BGE-M3 embedding capability, primary/default, `1024` dimensions.
- One already-PASS approved HX LLM endpoint.
- HX-9 PostgreSQL/Redis only if the owner-approved LightRAG configuration actually selects those backends.

The exact KV, graph, and document-status storage choices are **not yet owner-pinned by the current HX-11 runbook**, because the HX-11 runbook has not yet been created. Do not infer these choices from upstream examples.

## Model/vector integrity

- BGE-M3 is the HX primary/default embedding model at 1024 dimensions.
- Nomic Embed Text v1.5 is an alternate/benchmark capability with its separately accepted dimension.
- Never mix different embedding model identities in one Qdrant collection.
- Changing the embedding model requires a new collection and re-embedding under current HX policy.

## Validation boundary

LightRAG BASE validation is intentionally small:

1. LightRAG service/API reachable from HX-5 CentCom.
2. Ingest one synthetic known-answer text.
3. Wait for the exact document to reach processed state.
4. Retrieve the known token through LightRAG.
5. Generate a small RAG answer containing the known token.
6. Delete the exact smoke document.
7. Verify the smoke state is gone.
8. Validate the LightRAG MCP companion separately.
9. Prove reboot persistence and retain evidence before closure.

Do not force Docling or Crawl4AI into this BASE test. They are separately owned HX components and become later integration inputs unless explicitly promoted into the LightRAG BASE boundary.
