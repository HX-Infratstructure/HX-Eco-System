# Qdrant Smoke Test

## 1. Title & Purpose

Qdrant is the HX vector database on HX-10. This smoke test validates that the Qdrant HTTP API is reachable and can create a temporary collection, write vectors, perform a similarity query, and remove the test collection cleanly.

**Scope:** Qdrant core function only. Qdrant Web UI and Qdrant MCP remain separate companion gates.

## 2. Prerequisites

- Qdrant is installed natively and running on the target server.
- The Qdrant REST API is reachable from the test runner.
- Python 3 is available on the test runner; the script uses only the Python standard library.
- Set:

```bash
export QDRANT_URL="http://192.168.50.210:6333"
```

- If the accepted Qdrant configuration requires an API key, also set:

```bash
export QDRANT_API_KEY="<authorized-test-key>"
```

- The temporary collection name `hx_smoke_qdrant` must not be used for persistent data.
- No Docker, Podman, Kubernetes, or temporary container is required or permitted for this test.

## 3. Test Steps

1. Save the following as `qdrant_smoke.py` in the disposable test workspace.

```python
import json
import os
import urllib.request

BASE = os.environ.get("QDRANT_URL", "http://192.168.50.210:6333").rstrip("/")
API_KEY = os.environ.get("QDRANT_API_KEY")
COLLECTION = "hx_smoke_qdrant"


def request(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    if API_KEY:
        req.add_header("api-key", API_KEY)
    with urllib.request.urlopen(req, timeout=15) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body) if body else {}


created = False
try:
    code, _ = request("GET", "/collections")
    assert code == 200, f"collections endpoint returned {code}"

    code, _ = request(
        "PUT",
        f"/collections/{COLLECTION}",
        {"vectors": {"size": 4, "distance": "Cosine"}},
    )
    assert code == 200, f"collection create returned {code}"
    created = True

    code, _ = request(
        "PUT",
        f"/collections/{COLLECTION}/points?wait=true",
        {
            "points": [
                {"id": 1, "vector": [1.0, 0.0, 0.0, 0.0], "payload": {"label": "alpha"}},
                {"id": 2, "vector": [0.0, 1.0, 0.0, 0.0], "payload": {"label": "beta"}},
                {"id": 3, "vector": [0.0, 0.0, 1.0, 0.0], "payload": {"label": "gamma"}},
            ]
        },
    )
    assert code == 200, f"point upsert returned {code}"

    code, result = request(
        "POST",
        f"/collections/{COLLECTION}/points/query",
        {"query": [1.0, 0.0, 0.0, 0.0], "limit": 1, "with_payload": True},
    )
    assert code == 200, f"query returned {code}"

    top = result["result"]["points"][0]
    assert top["id"] == 1, f"unexpected top point: {top}"
    assert top["payload"]["label"] == "alpha", f"unexpected payload: {top}"

    print("QDRANT_SMOKE_PASS top_id=1 label=alpha")
finally:
    if created:
        request("DELETE", f"/collections/{COLLECTION}")

    code, collections = request("GET", "/collections")
    names = {item["name"] for item in collections["result"]["collections"]}
    assert COLLECTION not in names, "temporary collection still exists"
    print("QDRANT_SMOKE_CLEANUP_PASS")
```

2. Run the test.

```bash
python3 qdrant_smoke.py
```

3. Record the Qdrant server version, target URL, execution time, and console output with the normal HX smoke-test evidence.

## 4. Sample Data

The script creates three 4-dimensional vectors:

| ID | Vector | Payload |
|---:|---|---|
| 1 | `[1, 0, 0, 0]` | `{"label":"alpha"}` |
| 2 | `[0, 1, 0, 0]` | `{"label":"beta"}` |
| 3 | `[0, 0, 1, 0]` | `{"label":"gamma"}` |

The query vector is `[1, 0, 0, 0]`, so point `1` must be the top result.

## 5. Expected Output

A passing run ends with:

```text
QDRANT_SMOKE_PASS top_id=1 label=alpha
QDRANT_SMOKE_CLEANUP_PASS
```

Pass means:

- `GET /collections` returns HTTP `200`;
- collection creation returns HTTP `200`;
- point upsert returns HTTP `200`;
- vector query returns HTTP `200`;
- point `1` with payload label `alpha` is the top result;
- the temporary collection no longer exists after teardown.

## 6. Cleanup / Teardown

The script deletes `hx_smoke_qdrant` in its `finally` block and verifies that the collection is gone.

If the script is interrupted before cleanup, run:

```bash
curl -X DELETE "${QDRANT_URL}/collections/hx_smoke_qdrant" \
  ${QDRANT_API_KEY:+-H "api-key: ${QDRANT_API_KEY}"}
```

Then remove the disposable test script/workspace as appropriate.

**Do not delete or modify any non-smoke-test Qdrant collection. No containers are created by this test.**
