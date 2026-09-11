---
document: HX Eco-System Model Placement and Embedding Standard
status: owner_approved
version: 1.1
date: 2026-09-11
scope: HX-4 shared retrieval inference and HX-16 Docling model placement
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Model Placement and Embedding Standard

**Status:** OWNER APPROVED  
**Date:** September 11, 2026 (v1.1; v1.0 approved September 8, 2026)  
**Purpose:** Establish the standard placement, ownership, and usage rules for Granite-Docling, shared embedding models, reranking models, and Qdrant collection compatibility.

## 1. Owner-approved decisions

1. **Granite-Docling 258M remains with Docling on HX-16.**
2. **Granite-Docling is an embedded document-understanding VLM, not the HX general embedding model.**
3. **HX-16 is the authoritative execution location for Granite-Docling during the base-build phase.**
4. **GPU hardware is not a prerequisite for placing Granite-Docling on HX-16.** Base validation begins CPU-first. Performance is measured rather than assumed.
5. **If CPU throughput proves inadequate, acceleration is a later measured architecture decision.** Do not automatically move Granite-Docling to Meta-X or expose it as a general model service.
6. **HX-4 Meta-X is the shared HX embedding and reranking host.**
7. **Both BGE-M3 and Nomic Embed Text v1.5 will be installed on HX-4.**
8. **BGE-M3 is the default/authoritative HX embedding model.**
9. **Nomic Embed Text v1.5 is the alternate benchmark/fallback embedding model.**
10. **A BGE-family reranker is hosted on HX-4.** D-005 placed a BGE-family
   reranker on HX-4; the exact checkpoint and runtime were open until the
   owner directed them on 2026-09-10, recorded as D-022. This entry was
   added in v1.1 rather than at v1.0 approval. Pinned 2026-09-10 to `BAAI/bge-reranker-v2-m3` at revision `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`, served by `infinity-emb` 0.0.77 from PyPI under systemd on port 7997. It is the M3-family cross-encoder that pairs with BGE-M3. The revision is an immutable commit, so a later upstream edit cannot change the model under a stable name. Authoritative pins: `docs/03-runbooks/common/hx-base.env`.
11. **HX-5 remains CentCom / DeepSeek Harness / development-test capacity.** Shared embedding infrastructure will not be placed there merely because a second 16 GB GPU may become available.

## 2. Why Granite-Docling stays on HX-16

Granite-Docling 258M belongs inside the Docling capability boundary.

```text
HX-16 Docling
    ├── Docling runtime
    ├── Granite-Docling 258M
    └── Docling MCP server
```

Granite-Docling performs visual document understanding and structured document conversion. It is not a general text-vector embedding model and is not part of the shared Qdrant embedding plane.

The HX rule is therefore:

> Docling owns document conversion. Granite-Docling is an implementation detail of Docling.

Do not route routine Granite-Docling inference through OmniRoute. Do not expose it as a general conversational or vision endpoint.

### CPU-first execution rule

The 258M model is compact enough that HX will first prove the Docling + Granite path directly on HX-16 without requiring a dedicated GPU.

Base acceptance must measure:

- successful model load;
- representative PDF/scan conversion;
- page latency;
- RAM use;
- CPU utilization;
- output fidelity;
- service stability;
- reboot persistence.

If the measured throughput is unacceptable for HX development/test use, hardware acceleration is reconsidered based on evidence. The model is not preemptively relocated simply because another server has GPU capacity.

## 3. Shared embedding and reranking plane — HX-4

HX-4 Meta-X becomes the shared retrieval-inference host in addition to its primary GPT-OSS workload.

```text
HX-4 Meta-X
    ├── GPT-OSS 20B
    ├── HX Embedding Service
    │   ├── BAAI/bge-m3
    │   └── nomic-ai/nomic-embed-text-v1.5
    └── HX Reranking Service
        └── BGE-family reranker
```

This centralizes small retrieval models on a GPU-rich inference host while preserving HX-5 for control-plane and development workloads.

## 4. Embedding model standard

### Primary: BGE-M3

**Model:** `BAAI/bge-m3`  
**Role:** default HX embedding model  
**Native vector dimension:** 1024  
**Maximum sequence length:** 8192 tokens  
**Strengths:** multilingual retrieval; dense, sparse, and multi-vector/ColBERT-style capability.

Unless a workload-specific acceptance test establishes a better choice, new HX knowledge collections use BGE-M3.

### Secondary: Nomic Embed Text v1.5

**Model:** `nomic-ai/nomic-embed-text-v1.5`  
**Role:** alternate benchmark, fallback, and application-specific candidate  
**Default vector dimension:** 768  
**Maximum sequence length:** 8192 tokens  
**Additional capability:** Matryoshka dimensionality reduction to smaller supported dimensions.

Nomic is intentionally installed and available. It is not mixed with BGE-M3 inside a collection.

## 5. Why both models are installed

Installing both models gives HX useful optionality at low infrastructure cost:

- benchmark retrieval quality on real HX corpora;
- compare latency and GPU utilization;
- evaluate storage tradeoffs from vector dimensions;
- support an application that performs materially better on Nomic;
- retain a tested fallback if one model/runtime has a regression;
- experiment without rebuilding the embedding host.

The cost is manageable because these embedding models are far smaller than the main generative models.

However, **having both installed does not mean model switching is transparent.**

## 6. Non-negotiable Qdrant collection rule

Embedding models produce different semantic spaces. Their vectors must never be mixed in the same Qdrant collection.

BGE-M3 and Nomic also use different default dimensions:

```text
BGE-M3                 1024 dimensions
Nomic Embed v1.5        768 dimensions default
```

Therefore every Qdrant collection must be pinned to one embedding identity.

Required collection metadata:

```text
embedding_model
embedding_model_revision
embedding_dimension
embedding_normalization
embedding_service_version
chunking_profile
created_utc
```

Recommended collection naming pattern:

```text
<domain>__bge_m3_1024
<domain>__nomic_v15_768
```

A production collection must never be repointed from one embedding model to another.

## 7. Model-switch procedure

If HX decides to move a corpus from BGE-M3 to Nomic, or vice versa:

```text
1. Create a new collection.
2. Pin the new embedding model/revision/dimension.
3. Re-embed the source corpus.
4. Load the new vectors into the new collection.
5. Run retrieval acceptance tests.
6. Change the consuming application only after PASS.
7. Retain or retire the prior collection by owner decision.
```

There is no in-place vector-model switch.

## 8. Consumer architecture

The intended shared pattern is:

```text
                  HX-4 Meta-X
             ┌───────────────────┐
             │ Embedding Service │
             │ BGE-M3 / Nomic    │
             │                   │
             │ Reranker          │
             └─────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
       LightRAG       Mem0      RAG/Agents
          │            │            │
          └────────────┼────────────┘
                       ↓
                  HX-10 Qdrant
```

Qdrant stores vectors; it does not own the embedding models.

LightRAG and Mem0 consume the shared embedding capability unless a documented workload-specific exception is approved.

## 9. HX-5 placement decision

Even if HX-5 is upgraded to two RTX 5060 Ti 16 GB GPUs, shared embedding/reranking remains on HX-4.

HX-5 capacity is reserved for:

- CentCom;
- Ornith;
- DeepSeek Harness;
- development/test workloads;
- future control-plane experimentation.

This avoids making a control/development host a shared retrieval-infrastructure dependency.

A future move from HX-4 to HX-5 requires an explicit architecture decision based on measured contention or capacity, not simply available VRAM.

## 10. HX-4 base-build impact

HX-4 is not BASE PASS after GPT-OSS alone. Its base responsibility becomes:

```text
1. Clean OS / domain / NVIDIA baseline
2. Ollama
3. Meta-X / GPT-OSS 20B
4. Shared embedding serving runtime
5. BGE-M3
6. Nomic Embed Text v1.5
7. BGE-family reranker
8. API smoke tests for each model
9. resource/VRAM observation
10. reboot persistence
11. record PASS
```

The serving runtime (TEI, Infinity, or another approved native runtime) is selected before execution. The placement and model identities are already decided by this standard.

## 11. HX-16 base-build impact

HX-16 base responsibility becomes:

```text
1. Clean OS / domain baseline
2. Docling
3. Granite-Docling 258M
4. conventional Docling pipeline retained as fallback/control
5. Docling MCP server
6. representative document conversion tests
7. direct service/API test if deployed as service
8. Granite CPU performance observation
9. reboot persistence where applicable
10. record PASS
```

Granite-Docling is not routed through HX-4 merely to obtain GPU access.

## 12. Standard summary

```text
Granite-Docling 258M
    → HX-16
    → embedded inside Docling
    → CPU-first base validation
    → GPU only if measurement later justifies it

BGE-M3
    → HX-4
    → PRIMARY shared embedding model
    → 1024-dimensional collections

Nomic Embed Text v1.5
    → HX-4
    → SECONDARY benchmark/fallback
    → 768-dimensional default collections

BGE reranker
    → HX-4
    → shared retrieval reranking

Qdrant
    → HX-10
    → vector store only
    → every collection pinned to one model/revision/dimension

HX-5
    → retain headroom for CentCom / Harness / dev-test
```

This standard remains authoritative until the infrastructure owner explicitly changes it.
