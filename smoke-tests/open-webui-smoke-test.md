# Open WebUI Smoke Test

## 1. Title & Purpose

Open WebUI on HX-8 is the HX user-facing model interaction interface. This smoke test validates that the UI is reachable, can temporarily connect directly to one already-proven HX Ollama model, allows that model to be selected, sends a known-answer prompt, renders the model response, and then removes the validation-only connection.

**Scope:** Open WebUI core conversation function only. Permanent backend aggregation, OmniRoute integration, RAG, tools, MCP, authentication design, and production user configuration are outside this test.

## 2. Prerequisites

- Open WebUI is installed natively and running on HX-8.
- The Open WebUI LAN interface is reachable from the test workstation.
- One already-proven HX Ollama endpoint is available.
- Preferred initial validation backend:

```text
HX-2 Qwen-X
http://192.168.50.202:11434
qwen-x:qwen3.8-27b-q6_k
```

- The test operator can access the Open WebUI administration/settings interface needed to add and remove a temporary Ollama connection.
- The temporary connection must be clearly treated as validation-only.
- No permanent OmniRoute route, RAG store, cloud provider, production data, Docker, Podman, Kubernetes, or additional model installation is required.

## 3. Test Steps

1. Open the native HX-8 Open WebUI URL in a browser.

2. Confirm the UI loads normally and the application is responsive.

3. Using the native Open WebUI settings/admin interface for the installed version, add one temporary direct Ollama connection:

```text
Endpoint: http://192.168.50.202:11434
Purpose:  HX Open WebUI smoke test only
```

4. Confirm the approved validation model is visible/selectable:

```text
qwen-x:qwen3.8-27b-q6_k
```

5. Start a new disposable conversation and explicitly select that model.

6. Send the following known-answer prompt:

```text
Reply exactly: HX-OPENWEBUI-PASS
```

7. Confirm the assistant response rendered in the conversation contains exactly:

```text
HX-OPENWEBUI-PASS
```

No additional explanation is expected from the model.

8. Capture evidence of:

```text
HX-8 Open WebUI endpoint
Temporary Ollama backend
Selected model
Prompt
Rendered response
Timestamp
PASS/FAIL
```

9. Remove or disable the temporary direct Ollama connection before closing the BASE PASS test unless the infrastructure owner explicitly approves it as permanent.

10. Confirm Open WebUI remains healthy after the validation-only connection is removed.

11. During the normal HX-8 reboot-persistence check, confirm Open WebUI starts normally and its native UI remains reachable. The temporary test backend does not need to survive reboot because it should already have been removed.

## 4. Sample Data

Validation backend:

```text
HX-2 Qwen-X
http://192.168.50.202:11434
qwen-x:qwen3.8-27b-q6_k
```

Known-answer prompt:

```text
Reply exactly: HX-OPENWEBUI-PASS
```

Expected rendered model response:

```text
HX-OPENWEBUI-PASS
```

## 5. Expected Output

A passing test proves:

- the native Open WebUI page loads and is responsive;
- a temporary direct Ollama endpoint can be configured;
- the approved model becomes visible/selectable;
- a conversation can be started with that model;
- the prompt is sent successfully;
- the response `HX-OPENWEBUI-PASS` is rendered inside the Open WebUI conversation;
- evidence is captured;
- the validation-only direct connection is removed or disabled afterward unless explicitly approved to remain;
- Open WebUI remains healthy after cleanup and after the normal reboot-persistence check.

The recorded result should end with an explicit status similar to:

```text
OPEN_WEBUI_SMOKE_PASS
```

A healthy webpage without a successful model prompt/response round trip is **FAIL** for this smoke test.

## 6. Cleanup / Teardown

1. Remove or disable the temporary direct HX-2 Ollama connection.
2. Confirm the validation backend is no longer active/selectable as a temporary connection.
3. Optionally delete the disposable smoke-test conversation after evidence capture.
4. Do not alter the HX-2 Ollama service or model.
5. Do not remove any approved permanent Open WebUI configuration.

No containers, persistent test databases, or production data are created by this test.

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the rendered conversation showing the response.

Record the Open WebUI version, the native URL used, the temporary direct
Ollama endpoint configured, the model selected, the `HX-OPENWEBUI-PASS`
response as rendered, and confirmation that the validation-only connection
was removed and the service stayed healthy after cleanup and after the
reboot check.
