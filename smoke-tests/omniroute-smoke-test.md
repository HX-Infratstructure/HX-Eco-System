# OmniRoute Smoke Test

## 1. Title & Purpose

OmniRoute on HX-6 is the HX local/cloud model-routing component. This smoke test validates that OmniRoute can route one known-answer request to an already-proven HX model and return the same result as a direct call, while preserving the approved provider/model allowlist boundary.

**Scope:** One temporary validation route only. Permanent provider policy, permanent model routing, load balancing, fallback behavior, and cloud-provider integration are outside this test.

## 2. Prerequisites

- OmniRoute is installed natively and its normal service/UI/API entry point is healthy.
- One already-proven HX Ollama endpoint is available as the validation backend.
- Preferred initial backend:

```text
HX-2 Qwen-X
http://192.168.50.202:11434
qwen-x:qwen3.8-27b-q6_k
```

- `curl` is available on the test runner.
- The OmniRoute provider/model catalog rules are active:
  - approved provider allowlist;
  - approved model allowlist;
  - provider approval does not approve the full provider catalog.
- The temporary route/provider created for this test must be clearly marked validation-only.
- Set the direct backend variables:

```bash
export HX_DIRECT_OLLAMA_URL="http://192.168.50.202:11434"
export HX_DIRECT_MODEL="qwen-x:qwen3.8-27b-q6_k"
```

- Set the native OmniRoute endpoint for the installed version:

```bash
export OMNIROUTE_URL="<accepted-OmniRoute-native-endpoint>"
```

- No new model download, cloud provider, production credential, Docker, Podman, Kubernetes, or permanent route is required.

## 3. Test Steps

1. Prove the selected model directly against Ollama using the known-answer prompt:

```bash
curl -sS "${HX_DIRECT_OLLAMA_URL}/api/generate" \
  -H 'Content-Type: application/json' \
  -d "{\"model\":\"${HX_DIRECT_MODEL}\",\"prompt\":\"Reply exactly: HX-OMNIROUTE-PASS\",\"stream\":false}"
```

2. Confirm the direct response contains exactly:

```text
HX-OMNIROUTE-PASS
```

Allow only normal JSON/wrapper fields outside the model response text.

3. Using the native administration interface for the accepted OmniRoute version, create **one temporary validation provider/route** that points to:

```text
Backend: http://192.168.50.202:11434
Model:   qwen-x:qwen3.8-27b-q6_k
Purpose: HX OmniRoute smoke test only
```

4. Confirm the validation provider and model are visible only because they are explicitly allowed for the smoke test. Do not enable unrelated discovered providers or models.

5. Send the same request through OmniRoute using its accepted native request interface:

```text
Reply exactly: HX-OMNIROUTE-PASS
```

6. Confirm OmniRoute selects the temporary HX-2 validation route and returns:

```text
HX-OMNIROUTE-PASS
```

7. Record the following evidence:

```text
Direct backend URL
Direct model
Direct response
OmniRoute endpoint
Temporary provider/route name
Routed model/backend selected
Routed response
Timestamp
PASS/FAIL
```

8. Remove or disable the temporary validation route/provider before declaring the smoke test complete unless the infrastructure owner explicitly approves it as permanent architecture.

9. Confirm unrelated providers/models were not enabled or changed by the test.

10. During the normal HX-6 reboot-persistence check, prove the OmniRoute service itself returns healthy. The temporary validation route does not need to survive reboot if it was already removed as required.

## 4. Sample Data

Known-answer prompt:

```text
Reply exactly: HX-OMNIROUTE-PASS
```

Validation backend:

```text
HX-2 Qwen-X
http://192.168.50.202:11434
qwen-x:qwen3.8-27b-q6_k
```

Expected model answer:

```text
HX-OMNIROUTE-PASS
```

## 5. Expected Output

A passing test proves:

- the HX-2 validation model answers the known-answer prompt directly;
- OmniRoute can use one explicitly approved temporary provider/model route;
- the routed request reaches the intended HX-2 backend/model;
- the routed response contains the same exact token as the direct response;
- direct-versus-routed evidence is captured;
- no unrelated provider/model becomes active;
- the validation route is removed or disabled after the test unless explicitly retained by owner decision.

The recorded result should end with an explicit status similar to:

```text
OMNIROUTE_SMOKE_PASS
```

A healthy OmniRoute process without a successful routed model request is **FAIL** for this smoke test.

## 6. Cleanup / Teardown

1. Remove or disable the temporary validation provider/route.
2. Confirm the temporary route is no longer selectable/active.
3. Do not remove the HX-2 Ollama model or alter its configuration.
4. Do not remove approved permanent OmniRoute providers/models.
5. Remove any disposable local test files after evidence capture.

No containers or persistent test databases are created by this test.

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the direct response and the routed response side by side.

Record the OmniRoute version, the temporary provider and route used, the
HX-2 backend and model reached, the identical token from the direct and
routed responses, and confirmation that the validation route was removed or
disabled and no unrelated provider became active.
