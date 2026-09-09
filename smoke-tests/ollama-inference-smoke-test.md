# Ollama Inference Smoke Test

## 1. Title & Purpose

Ollama provides the HX local generative-model serving pattern used on inference hosts. This smoke test validates that an accepted Ollama endpoint can load the assigned model, accept a non-streaming API request, and return an exact known-answer token.

**Scope:** Generic Ollama generative inference proof. Use for newly built inference workloads such as HX-4 GPT-OSS and HX-5 Ornith; it does not reopen already-closed HX-2/HX-3 unless explicitly requested.

## 2. Prerequisites

- Ollama is installed natively and running on the target HX server.
- The exact assigned model/alias is already installed.
- The test runner can reach port `11434` on the accepted endpoint.
- Set:

```bash
export OLLAMA_URL="http://<target-private-ip>:11434"
export OLLAMA_MODEL="<exact-accepted-model-alias>"
```

- Python 3 is available on the test runner.
- No cloud model, router, UI, database, or container is required.

## 3. Test Steps

1. Save as `ollama_inference_smoke.py`:

```python
import json
import os
import urllib.request

BASE = os.environ["OLLAMA_URL"].rstrip("/")
MODEL = os.environ["OLLAMA_MODEL"]
TOKEN = "HX-OLLAMA-SMOKE-9271"

payload = {
    "model": MODEL,
    "prompt": f"Reply exactly: {TOKEN}",
    "stream": False,
    "think": False,
    "keep_alive": "0",
    "options": {"temperature": 0},
}

req = urllib.request.Request(
    BASE + "/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req, timeout=180) as response:
    assert response.status == 200, response.status
    result = json.loads(response.read().decode("utf-8"))

assert result.get("done") is True, result
assert TOKEN in result.get("response", ""), result
assert result.get("model"), result

print(
    f"OLLAMA_SMOKE_PASS model={result['model']} token={TOKEN}"
)
```

2. Run:

```bash
python3 ollama_inference_smoke.py
```

3. Record Ollama version, endpoint, exact model alias/ID where available, execution timestamp, response, and basic resource observation.

## 4. Sample Data

```text
Prompt: Reply exactly: HX-OLLAMA-SMOKE-9271
Expected token: HX-OLLAMA-SMOKE-9271
```

## 5. Expected Output

```text
OLLAMA_SMOKE_PASS model=<actual-model> token=HX-OLLAMA-SMOKE-9271
```

Pass means HTTP `200`, `done=true`, the response contains the exact known-answer token, and the actual model identity is returned.

## 6. Cleanup / Teardown

The request uses `keep_alive: "0"` so the test does not intentionally leave the model loaded after completion.

Remove the disposable test script/workspace after evidence capture. Do not delete the accepted model or change persistent Ollama configuration.

**No temporary router, cloud provider, or container is created by this test.**
