# Open WebUI Base Smoke-Test Standard

A healthy webpage is not sufficient for BASE PASS.

## Test
1. Start Open WebUI and validate its direct LAN UI.
2. Temporarily configure one direct Ollama endpoint from an already-proven HX inference server.
3. Expose/select one intended model.
4. Send a known-answer prompt.
5. Confirm a model response renders inside Open WebUI.
6. Record the server, model, endpoint, prompt, response, and result.
7. Remove/disable the temporary direct Ollama connection before base-build closure unless explicitly approved to remain.

Permanent backend aggregation/routing is integration-phase work.
