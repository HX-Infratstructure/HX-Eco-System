# BGE Reranker Smoke Test

## 1. Title & Purpose

HX-4 will host a shared BGE-family reranker for retrieval workloads. This smoke test defines the minimal known-answer ranking proof required before that reranker can receive BASE PASS.

**Important:** the exact BGE-family checkpoint and native serving runtime are still intentionally TBD in the current HX model-placement standard. This smoke test becomes executable only after both are pinned; it does not choose them by implication.

## 2. Prerequisites

- The infrastructure owner has approved the exact BGE-family reranker checkpoint.
- The exact model revision and native serving runtime/interface are pinned in the HX-4 record.
- The reranker is installed on HX-4 and its endpoint/interface is reachable from the test runner.
- No Qdrant collection, production corpus, LLM, or container is required.

## 3. Test Steps

1. Record the exact checkpoint, revision, serving runtime, and endpoint/interface.
2. Submit this query with all three passages in one rerank request:

```text
Which passage describes a critical system outage?
```

3. Candidate passages:

```text
A: The monthly billing invoice was processed successfully.
B: A critical production outage is affecting 50 users and requires immediate operations response.
C: The employee vacation schedule was updated for next month.
```

4. Record the returned score/rank for A, B, and C.
5. Require passage **B** to rank first.
6. Repeat the identical request once more.
7. Require passage **B** to rank first again.
8. Record both result sets and execution timestamp.

Use the accepted runtime's native API/SDK. Do not invent or substitute an interface before the runtime is selected.

## 4. Sample Data

```text
Query: Which passage describes a critical system outage?

A: The monthly billing invoice was processed successfully.
B: A critical production outage is affecting 50 users and requires immediate operations response.
C: The employee vacation schedule was updated for next month.

Expected top passage: B
```

## 5. Expected Output

Both runs must produce passage B as rank 1. Record a result similar to:

```text
RERANKER_SMOKE_PASS checkpoint=<pinned-checkpoint> run1_top=B run2_top=B
```

Exact numeric scores are evidence, not hard-coded acceptance thresholds. The known-answer rank is the KISS functional gate.

If the checkpoint/runtime is not yet pinned, status is **NOT EXECUTABLE — IMPLEMENTATION DECISION REQUIRED**, not PASS or FAIL.

## 6. Cleanup / Teardown

No persistent data is created. Release temporary model state according to the accepted runtime and remove disposable local test artifacts after evidence capture.

**Do not use this document to select a checkpoint, introduce a new runtime, or create Qdrant data. Those decisions must be explicit before execution.**
