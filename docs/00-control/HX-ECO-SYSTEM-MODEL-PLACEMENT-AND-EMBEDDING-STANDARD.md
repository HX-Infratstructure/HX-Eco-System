---
document: HX Eco-System Model Placement and Embedding Standard
status: owner_approved
version: 1.0
date: 2026-09-09
scope: HX-4 shared retrieval inference and HX-16 Docling model placement
---

# HX Eco-System — Model Placement and Embedding Standard

## Owner-approved decisions
1. Granite-Docling 258M remains with Docling on HX-16.
2. Granite-Docling is an embedded document-understanding VLM, not the HX general embedding model.
3. Base validation on HX-16 is CPU-first. GPU acceleration is considered later only if measured throughput justifies it.
4. HX-4 Meta-X is the shared HX embedding and reranking host.
5. Both BGE-M3 and Nomic Embed Text v1.5 are installed on HX-4.
6. BGE-M3 is the default/authoritative HX embedding model.
7. Nomic Embed Text v1.5 is the alternate benchmark/fallback embedding model.
8. A BGE-family reranker is hosted on HX-4; exact checkpoint is pinned before installation.
9. HX-5 remains reserved for CentCom / DeepSeek Harness / Ornith / development-test headroom even if its GPU pair becomes 2 x 16 GB.

## Granite-Docling placement

```text
HX-16 Docling
    ├── Docling runtime
    ├── Granite-Docling 258M
    └── Docling MCP server
```

Granite-Docling stays inside the Docling capability boundary. Do not route routine Granite-Docling inference through OmniRoute and do not expose it as a general conversational/vision endpoint.

## Shared embedding/reranking plane

```text
HX-4 Meta-X
    ├── GPT-OSS 20B
    ├── HX Embedding Service
    │   ├── BAAI/bge-m3
    │   └── nomic-ai/nomic-embed-text-v1.5
    └── HX Reranking Service
        └── BGE-family reranker
```

### BGE-M3
- Role: primary/default HX embedding model.
- Native vector dimension: 1024.
- Maximum sequence length: 8192 tokens.

### Nomic Embed Text v1.5
- Role: alternate benchmark/fallback and application-specific candidate.
- Default vector dimension: 768.
- Maximum sequence length: 8192 tokens.
- Supports Matryoshka dimensionality reduction.

## Why both are installed
Both models give HX optionality for quality, latency, utilization, and storage benchmarking at low infrastructure cost compared with the main generative models.

Having both installed does not make them interchangeable inside an existing collection.

## Non-negotiable Qdrant collection rule
Embedding models occupy different semantic vector spaces and must never be mixed in the same Qdrant collection.

Required collection metadata:
- embedding_model
- embedding_model_revision
- embedding_dimension
- embedding_normalization
- embedding_service_version
- chunking_profile
- created_utc

Recommended naming examples:
- `<domain>__bge_m3_1024`
- `<domain>__nomic_v15_768`

## Model-switch procedure
1. Create a new collection.
2. Pin the new embedding model/revision/dimension.
3. Re-embed the source corpus.
4. Load the new vectors into the new collection.
5. Run retrieval acceptance tests.
6. Change the consuming application only after PASS.
7. Retain or retire the prior collection by owner decision.

There is no in-place vector-model switch.
