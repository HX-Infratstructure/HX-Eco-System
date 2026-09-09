# Mem0 Smoke Test

## 1. Title & Purpose

Mem0 is the HX memory component on HX-13. This smoke test validates a minimal memory lifecycle: store one synthetic memory, retrieve it through semantic search, delete it, and remove the disposable vector-store state.

**Scope:** Mem0 core memory function only. Mem0 MCP is validated separately with `mcp-companion-smoke-test.md`.

## 2. Prerequisites

- Mem0 OSS is installed natively on HX-13.
- Python 3.10+ and the accepted Mem0 environment are available.
- HX-10 Qdrant has already passed BASE PASS.
- An approved HX Ollama embedding endpoint has already passed its embedding smoke test. BGE-M3 on HX-4 is preferred once HX-4 is closed.
- Set the accepted values before execution:

```bash
export QDRANT_HOST="192.168.50.210"
export QDRANT_PORT="6333"
export OLLAMA_URL="http://192.168.50.204:11434"
export MEM0_EMBED_MODEL="<accepted-embedding-model-alias>"
export MEM0_EMBED_DIM="1024"
export MEM0_LLM_MODEL="<accepted-local-llm-alias>"
```

- If Qdrant requires an API key, set `QDRANT_API_KEY` through the accepted HX credential method.
- The dedicated collection `hx_mem0_smoke` is disposable and must not contain permanent data.
- No container or production data is required.

## 3. Test Steps

1. Save as `mem0_smoke.py`:

```python
import os
import time
import urllib.request
from mem0 import Memory

TOKEN = "HX-MEM0-SMOKE-9271"
USER = "hx_mem0_smoke_9271"
COLLECTION = "hx_mem0_smoke"
QHOST = os.environ.get("QDRANT_HOST", "192.168.50.210")
QPORT = int(os.environ.get("QDRANT_PORT", "6333"))
QKEY = os.environ.get("QDRANT_API_KEY")
OLLAMA = os.environ.get("OLLAMA_URL", "http://192.168.50.204:11434")
EMBED_MODEL = os.environ["MEM0_EMBED_MODEL"]
EMBED_DIM = int(os.environ.get("MEM0_EMBED_DIM", "1024"))
LLM_MODEL = os.environ["MEM0_LLM_MODEL"]

qdrant_config = {
    "collection_name": COLLECTION,
    "host": QHOST,
    "port": QPORT,
    "embedding_model_dims": EMBED_DIM,
}
if QKEY:
    qdrant_config["api_key"] = QKEY

memory = Memory.from_config({
    "vector_store": {"provider": "qdrant", "config": qdrant_config},
    "llm": {
        "provider": "ollama",
        "config": {
            "model": LLM_MODEL,
            "temperature": 0,
            "ollama_base_url": OLLAMA,
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": EMBED_MODEL,
            "embedding_dims": EMBED_DIM,
            "ollama_base_url": OLLAMA,
        },
    },
})

try:
    memory.add(
        [{"role": "user", "content": f"The exact HX memory smoke token is {TOKEN}."}],
        user_id=USER,
        infer=False,
    )

    found = False
    results = {}
    for _ in range(10):
        results = memory.search(
            "What is the HX memory smoke token?",
            filters={"user_id": USER},
            top_k=5,
            threshold=0.0,
        )
        if TOKEN in str(results):
            found = True
            break
        time.sleep(1)

    assert found, f"smoke token not returned: {results}"
    print(f"MEM0_SMOKE_PASS token={TOKEN}")

    memory.delete_all(user_id=USER)
    results = memory.search(
        "What is the HX memory smoke token?",
        filters={"user_id": USER},
        top_k=5,
        threshold=0.0,
    )
    assert TOKEN not in str(results), f"memory still present: {results}"
    print("MEM0_MEMORY_CLEANUP_PASS")
finally:
    close = getattr(memory, "close", None)
    if callable(close):
        close()
```

2. Run:

```bash
python3 mem0_smoke.py
```

3. After the Mem0 memory is deleted, remove the dedicated Qdrant smoke collection using the accepted Qdrant API method.

4. Record Mem0 version, embedding model/dimension, Qdrant endpoint/collection, LLM model, execution timestamp, and console output. Do not capture secrets.

## 4. Sample Data

```text
User ID: hx_mem0_smoke_9271
Memory:  The exact HX memory smoke token is HX-MEM0-SMOKE-9271.
Query:   What is the HX memory smoke token?
```

`infer=False` is intentional so the known-answer test stores the synthetic text as supplied rather than depending on LLM memory extraction behavior.

## 5. Expected Output

```text
MEM0_SMOKE_PASS token=HX-MEM0-SMOKE-9271
MEM0_MEMORY_CLEANUP_PASS
```

Pass means Mem0 initializes with the accepted HX providers, stores the synthetic memory, retrieves the exact token, deletes the user's smoke memory, and leaves no retained smoke memory.

## 6. Cleanup / Teardown

1. Run `delete_all(user_id="hx_mem0_smoke_9271")` if the test did not reach cleanup.
2. Delete only the dedicated Qdrant collection `hx_mem0_smoke` after evidence capture.
3. Remove the local smoke-test script/workspace.

**Never reset Mem0 globally or delete non-smoke Qdrant collections. Permanent Mem0-to-Qdrant/model configuration remains an integration/implementation decision beyond this disposable proof.**
