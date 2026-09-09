# OmniRoute Provider and Model Catalog Standard

## Principle
Known by OmniRoute != approved HX provider != approved HX model.

## Required controls
- Explicit provider allowlist.
- Explicit model allowlist.
- Provider approval does not approve all provider models.
- Free/no-auth/discovered providers are not automatically enabled for HX use.
- Only locally proven HX models enter the active local model catalog.
- Cloud providers and cloud models require explicit owner approval.

## Base smoke test
1. Choose one already-proven Ollama endpoint.
2. Prove the model directly.
3. Configure one temporary OmniRoute route/provider.
4. Send the same known-answer request through OmniRoute.
5. Record direct-versus-routed evidence.
6. Remove/disable the temporary route after validation unless explicitly approved to remain.
