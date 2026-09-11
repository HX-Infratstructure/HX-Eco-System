# BGE Reranker Smoke Test

## 1. Title & Purpose

HX-4 will host a shared BGE-family reranker for retrieval workloads. This smoke test defines the minimal known-answer ranking proof required before that reranker can receive BASE PASS.

**Status: EXECUTABLE.** The checkpoint and serving runtime were pinned on 2026-09-10 and now live in `docs/03-runbooks/common/hx-base.env`:

```text
HX_RERANKER_MODEL="BAAI/bge-reranker-v2-m3"
HX_RERANKER_REVISION="953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e"
HX_RERANKER_RUNTIME="infinity-emb"
HX_RERANKER_RUNTIME_VERSION="0.0.77"
HX_RERANKER_PORT="7997"
```

This test consumes those pins. It still does not choose them: a change of checkpoint or runtime is an owner decision recorded in `hx-base.env` and the HX-4 server record.

## 2. Prerequisites

- The pins above are current in `docs/03-runbooks/common/hx-base.env`.
- `docs/03-runbooks/common/04-reranker.sh` has been run on HX-4 and `hx-reranker` is active.
- The resolved checkpoint, revision, runtime and version are recorded in `docs/02-server-records/HX-4.md`.
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

If `hx-base.env` and the HX-4 record disagree on the checkpoint or revision, stop and reconcile them before running. Do not resolve the difference inside a run.

### Request shape

The pinned runtime exposes an OpenAI-style rerank endpoint:

```bash
curl -fsS http://192.168.50.204:7997/rerank   -H 'Content-Type: application/json'   -d '{"model":"hx-reranker","query":"<query>","documents":["<A>","<B>","<C>"]}'
```

Rank 1 is the entry with the highest `relevance_score` in the response.

## 6. Cleanup / Teardown

No persistent data is created. Release temporary model state according to the accepted runtime and remove disposable local test artifacts after evidence capture.

**Do not use this document to select a checkpoint, introduce a new runtime, or create Qdrant data. Those decisions must be explicit before execution.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of both rerank responses with their `relevance_score` values.

Record the pinned checkpoint and revision, the runtime and its version, the
endpoint used, the rank 1 passage from each of the two runs, and
confirmation that `hx-base.env` and the HX-4 record agreed on the checkpoint
before the run.
