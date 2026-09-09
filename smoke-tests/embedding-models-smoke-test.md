# HX Embedding Models Smoke Test

## 1. Title & Purpose

HX-4 hosts the shared HX embedding plane: BGE-M3 as the primary model and Nomic Embed Text v1.5 as the alternate. This smoke test validates that each accepted embedding model can produce stable, non-empty vectors at the approved native dimension.

**Scope:** Embedding generation only. Qdrant storage/retrieval is tested separately. This document does not choose the serving runtime; the runtime/interface must be pinned during HX-4 implementation.

## 2. Prerequisites

- HX-4 base inference state is accepted far enough to run the shared embedding service.
- The serving runtime is explicitly selected and recorded before execution.
- Exact model/revision identifiers are pinned.
- BGE-M3 expected native dimension: `1024`.
- Nomic Embed Text v1.5 expected default dimension: `768`.
- The test runner can call the accepted embedding interface.
- No Qdrant collection, production corpus, or container is required.

## 3. Test Steps

Run the following sequence once for **BGE-M3** and once for **Nomic Embed Text v1.5**:

1. Record the serving runtime, endpoint/interface, exact model identifier/revision, and expected dimension.
2. Submit the same input twice:

```text
HX embedding deterministic smoke sentence 9271.
```

3. Capture both returned vectors.
4. Confirm both vectors contain numeric values and are not all zero.
5. Confirm both vectors have the expected dimension:
   - BGE-M3: `1024`
   - Nomic v1.5: `768`
6. Compute cosine similarity between the two repeated vectors using this helper:

```python
import math

def cosine(a, b):
    assert len(a) == len(b)
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)
```

7. Require repeated-input cosine similarity of at least `0.999`.
8. Record model, revision, dimension, cosine result, runtime, endpoint, timestamp, and execution evidence.

If the selected runtime supports batching, both identical strings may be sent in one request; otherwise make two calls.

## 4. Sample Data

```text
Input A: HX embedding deterministic smoke sentence 9271.
Input B: HX embedding deterministic smoke sentence 9271.

BGE-M3 expected dimension: 1024
Nomic v1.5 expected dimension: 768
Minimum repeat cosine: 0.999
```

## 5. Expected Output

Record one result per model in this form:

```text
EMBEDDING_SMOKE_PASS model=BAAI/bge-m3 dim=1024 cosine=<>=0.999
EMBEDDING_SMOKE_PASS model=nomic-ai/nomic-embed-text-v1.5 dim=768 cosine=<>=0.999
```

Pass means both models return usable numeric vectors at their approved dimensions and repeated identical input produces effectively identical semantic output.

## 6. Cleanup / Teardown

No database objects or permanent test data are created.

Release/unload temporary model state according to the accepted serving runtime, remove disposable test files, and retain only evidence.

**Do not force Nomic to 1024 dimensions merely to match BGE-M3. Do not write vectors from the two models into the same Qdrant collection.**
