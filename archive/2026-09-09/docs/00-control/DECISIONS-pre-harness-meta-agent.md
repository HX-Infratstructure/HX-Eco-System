---
document: HX Eco-System Owner-Approved Decisions
status: current
date: 2026-09-09
---

# HX Eco-System — Owner-Approved Decisions

## D-001 — Clean-room rebuild
HX-1 clean Samba foundation is retained. HX-2 through HX-17 are rebuilt from scratch. Old HX-Infrastructure configuration and closure claims are reference-only.

## D-002 — Native deployment
Native Linux + systemd. No Docker, Podman, or Kubernetes unless explicitly changed by the owner.

## D-003 — Application companion services
Product-specific MCP servers and native Web UIs are part of the parent application's base build where applicable.

## D-004 — NGINX
HX-7 NGINX is limited to dev/test application rendering. It is not the common reverse proxy for HX ecosystem services.

## D-005 — Embedding/reranking placement
HX-4 Meta-X hosts BGE-M3 as primary/default embedding model, Nomic Embed Text v1.5 as alternate benchmark/fallback, and a BGE-family reranker. Never mix embedding-model vector spaces in one Qdrant collection.

## D-006 — Granite-Docling placement
Granite-Docling 258M stays with Docling on HX-16. Base validation is CPU-first. GPU acceleration is considered only if measured need later justifies it.

## D-007 — HX-5 headroom
Even if HX-5 is upgraded to 2 x 16 GB GPUs, shared embedding/reranking remains on HX-4. HX-5 headroom is reserved for CentCom, Ornith, DeepSeek Harness, and dev/test work.

## D-008 — Open WebUI base functional test
HX-8 Open WebUI BASE PASS includes a temporary direct connection to one already-proven Ollama endpoint, one prompt, one model response in the UI, evidence capture, and cleanup/removal of the temporary connection.

## D-009 — OmniRoute base functional test
HX-6 OmniRoute BASE PASS includes one temporary route to one already-proven Ollama endpoint, direct-versus-routed known-answer validation, evidence capture, and cleanup/removal of the temporary test route.

## D-010 — OmniRoute provider/model catalog
OmniRoute maintains an explicit approved-provider allowlist and an explicit approved-model allowlist. Discovery/support does not equal approval. Approving a provider does not approve its entire model catalog.

## D-011 — Active document rule
Only the latest version of a document remains active. Superseded versions go under `archive/`. Active Markdown is agent authority; HTML is a human mirror.
