# LightRAG Smoke Test

## 1. Title & Purpose

LightRAG is the HX retrieval-augmented generation service on HX-11. This smoke test validates that the LightRAG API is reachable, can ingest one synthetic text document, index it with the configured LLM/embedding services, retrieve the known content, generate a small RAG answer, and delete the smoke-test document.

**Scope:** LightRAG core ingest/retrieval/query function only. LightRAG MCP remains a separate companion gate.

## 2. Prerequisites

- LightRAG is installed natively and the LightRAG server is running.
- The LightRAG API is reachable from the test runner.
- The LightRAG instance already has a working LLM and embedding model configured.
- For HX, use only model endpoints that have already passed their own BASE PASS.
- The embedding model/dimension used for indexing must match the LightRAG instance's accepted configuration. If the accepted HX configuration uses BGE-M3, the expected dimension is `1024`.
- Python 3 is available on the test runner; the script uses only the Python standard library.
- Set:

```bash
export LIGHTRAG_URL="http://192.168.50.211:9621"
```

- If the accepted LightRAG configuration requires an API key, also set:

```bash
export LIGHTRAG_API_KEY="<authorized-test-key>"
```

### If LightRAG is configured to use Qdrant

No second Qdrant instance is created for this smoke test. The accepted HX Qdrant service must already be running and LightRAG must already be configured with its normal Qdrant settings, for example:

```text
LIGHTRAG_VECTOR_STORAGE=QdrantVectorDBStorage
QDRANT_URL=http://192.168.50.210:6333
QDRANT_API_KEY=<only if required by the accepted Qdrant configuration>
```

The smoke document is deleted through LightRAG after the test so its vector/KG state is removed by the application that created it.

- No Docker, Podman, Kubernetes, or temporary container is required or permitted for this test.

## 3. Test Steps

1. Save the following as `lightrag_smoke.py` in the disposable test workspace.

```python
import json
import os
import time
import urllib.parse
import urllib.request

BASE = os.environ.get("LIGHTRAG_URL", "http://192.168.50.211:9621").rstrip("/")
API_KEY = os.environ.get("LIGHTRAG_API_KEY")
TIMEOUT = int(os.environ.get("LIGHTRAG_SMOKE_TIMEOUT", "180"))
TOKEN = "HX-LIGHTRAG-SMOKE-9271"
SAMPLE = (
    "This is synthetic HX smoke-test data. "
    "Project Cedar has the exact smoke token HX-LIGHTRAG-SMOKE-9271. "
    "Project Cedar is owned by the fictional HX Smoke Team."
)


def request(method, path, payload=None, timeout=30):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    if API_KEY:
        req.add_header("X-API-Key", API_KEY)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body) if body else {}


track_id = None
doc_ids = []
try:
    code, _ = request("GET", "/health")
    assert code == 200, f"health returned {code}"

    code, inserted = request(
        "POST",
        "/documents/text",
        {
            "text": SAMPLE,
            "file_source": "hx-lightrag-smoke.md",
        },
    )
    assert code in (200, 201, 202), f"insert returned {code}"
    track_id = inserted.get("track_id")
    assert track_id, f"insert response did not contain track_id: {inserted}"

    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        code, status = request(
            "GET",
            "/documents/track_status/" + urllib.parse.quote(track_id, safe=""),
        )
        assert code == 200, f"track status returned {code}"
        docs = status.get("documents", [])
        if docs:
            failed = [d for d in docs if str(d.get("status", "")).lower() == "failed"]
            assert not failed, f"LightRAG indexing failed: {failed}"

            if all(str(d.get("status", "")).lower() == "processed" for d in docs):
                doc_ids = [d["id"] for d in docs if d.get("id")]
                break
        time.sleep(2)
    else:
        raise TimeoutError(f"LightRAG indexing did not finish within {TIMEOUT}s")

    assert doc_ids, "no processed document id was returned"

    code, context = request(
        "POST",
        "/query",
        {
            "query": "What is the exact smoke token for Project Cedar?",
            "mode": "hybrid",
            "only_need_context": True,
        },
        timeout=90,
    )
    assert code == 200, f"context query returned {code}"
    assert TOKEN in json.dumps(context), f"smoke token not found in retrieved context: {context}"

    code, answer = request(
        "POST",
        "/query",
        {
            "query": "Return the exact smoke token for Project Cedar.",
            "mode": "hybrid",
        },
        timeout=90,
    )
    assert code == 200, f"RAG query returned {code}"
    assert TOKEN in json.dumps(answer), f"smoke token not found in RAG answer: {answer}"

    print(f"LIGHTRAG_SMOKE_PASS token={TOKEN}")
finally:
    if doc_ids:
        code, _ = request(
            "DELETE",
            "/documents/delete_document",
            {
                "doc_ids": doc_ids,
                "delete_file": False,
                "delete_llm_cache": True,
            },
            timeout=60,
        )
        assert code in (200, 202), f"document cleanup returned {code}"
        print("LIGHTRAG_SMOKE_CLEANUP_REQUESTED")
    elif track_id:
        print(f"CLEANUP_REQUIRED track_id={track_id}")
```

2. Run the test.

```bash
python3 lightrag_smoke.py
```

3. If cleanup reports only `CLEANUP_REQUIRED`, query the recorded `track_id`, obtain the returned document `id`, and delete only that smoke-test document before closing the test.

4. Record the LightRAG version, configured LLM, configured embedding model/dimension, storage backend, target URL, `track_id`, document id, and console output with the normal HX smoke-test evidence.

## 4. Sample Data

The complete synthetic source text is:

```text
This is synthetic HX smoke-test data. Project Cedar has the exact smoke token HX-LIGHTRAG-SMOKE-9271. Project Cedar is owned by the fictional HX Smoke Team.
```

Known-answer query:

```text
What is the exact smoke token for Project Cedar?
```

Expected token:

```text
HX-LIGHTRAG-SMOKE-9271
```

## 5. Expected Output

A passing run includes:

```text
LIGHTRAG_SMOKE_PASS token=HX-LIGHTRAG-SMOKE-9271
LIGHTRAG_SMOKE_CLEANUP_REQUESTED
```

Pass means:

- `GET /health` returns HTTP `200`;
- text ingestion is accepted and returns a `track_id`;
- the tracked document reaches `processed` rather than `failed`;
- a `hybrid` context-only query retrieves the exact smoke token;
- a normal `hybrid` RAG query returns the exact smoke token;
- deletion of the smoke document is accepted.

If Qdrant is the configured vector backend, this same test also proves the minimal LightRAG-to-Qdrant write/retrieval path without creating a parallel database instance.

## 6. Cleanup / Teardown

The script requests deletion of the exact document ids created by the smoke test using:

```text
DELETE /documents/delete_document
```

with:

```json
{
  "doc_ids": ["<smoke-document-id>"],
  "delete_file": false,
  "delete_llm_cache": true
}
```

After deletion:

1. confirm the smoke document is no longer listed in LightRAG;
2. confirm the token `HX-LIGHTRAG-SMOKE-9271` is no longer retrievable from the smoke document;
3. remove the disposable local test script/workspace.

**Never call a global clear operation as part of this smoke test. Do not delete other LightRAG documents, Qdrant data, or persistent workspaces. No containers are created by this test.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the health response, the `track_id`, and the context-only and RAG query responses.

Record the LightRAG version, the endpoint used, the vector backend in
effect, the known-answer token `HX-LIGHTRAG-SMOKE-9271` from both query
paths, the document ids created, and confirmation that deletion of those
exact ids was accepted.
