---
run_id: 20260915T054147Z_hx-4_embedding-models
utc_start: 20260915T054147Z
utc_end: 20260915T054230Z
status: PASS
operator: hxsa
runner_host: hx-4
sut_host: hx-4
sut_ip: 192.168.50.204
component: embedding-models
proof_step: A2
component_version_or_revision: ollama 0.34.0; hx-embed-primary:bge-m3 (790764642607) from bge-m3:567m; hx-embed-alt:nomic-v1.5 (0a109f422b47) from nomic-embed-text:v1.5
smoke_test_file: smoke-tests/embedding-models-smoke-test.md
smoke_test_repo_commit: 663ba76ba7e0f3c1a79ba645f289636bbd012b2c
smoke_test_sha256: 0e69df3821af439d233e5b6f7a58d8c385aff1385528744c5ea8a506ca3d903a
transport_or_endpoint: HTTP POST http://192.168.50.204:11434/api/embed
known_answer: SEE_PROCEDURE
prior_pass_evidence: A1 -> docs/05-evidence/hx-4/ollama-inference/20260915T054105Z_hx-4_ollama-inference
limited_integration_plan: NONE
validation_only_dependencies: SEE_PROCEDURE
cleanup_objects_expected: SEE_PROCEDURE
---

# HX Smoke-Test Run Manifest

Use the copied procedure in procedure/ as the acceptance authority for this run.

Before execution, replace, each on one line:

- prior_pass_evidence: one entry for each step this step requires, written as
  `<step-id> -> <evidence path or accepted server record>` and separated by
  `;`. Use NONE when nothing is required. hx-smoke-promote reads the inline
  value only, and refuses a bare list of paths, because a path alone does not
  say which dependency it proves;
- limited_integration_plan: brief temporary integration plan, or NONE.

Example: `prior_pass_evidence: B5 -> docs/05-evidence/hx-10/qdrant/<run-id>; A2 -> docs/02-server-records/HX-4.md`

Use `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` to determine required proof dependencies.
Do not place secrets in this manifest or retained evidence.
