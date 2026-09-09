# AGENTS.md — HX Eco-System Agent Operating Contract

This repository is designed to be immediately understandable by agentic coding and infrastructure agents.

## 1. Required reading order

Before changing anything:

1. `README.md`
2. `docs/00-control/CURRENT-STATE.md`
3. `docs/00-control/BUILD-STATE.md`
4. `docs/00-control/DECISIONS.md`
5. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
6. Relevant current server record under `docs/02-server-records/`
7. Relevant runbook under `docs/03-runbooks/`
8. Relevant standard under `docs/04-application-standards/`
9. If executing a component smoke test, the exact authority under `smoke-tests/`.
10. If using the HX-5 runner, `tools/hx-smoke-runner/AGENTS.md`.

Do not read `archive/` or `human-html/` as current authority unless explicitly asked.

## 2. Truth order

1. Explicit current instruction from the infrastructure owner.
2. Current active control/architecture Markdown in `docs/` and the exact current component acceptance authority in `smoke-tests/` when testing.
3. Current live evidence from the server being worked on.
4. Current approved runbook/execution artifact.
5. Historical/archive material, only as reference.
6. General model knowledge.

If current live evidence contradicts an active document, stop treating the document as proof and report the contradiction.

## 3. Non-negotiable operating rules

- KISS: build one server, validate it, record it, then move on.
- Native Linux + systemd.
- No Docker, Podman, Kubernetes, or containerized workload deployment unless explicitly approved.
- Do not impose firewall rules, access restrictions, TLS requirements, segmentation, or security-hardening changes without explicit approval.
- Do not change network architecture unless explicitly approved.
- Do not mount, wipe, repartition, format, or repurpose an old/unmounted disk without explicit approval.
- Do not import old HX-Infrastructure configuration or closure claims into this clean rebuild.
- Historical hardware facts may inform planning but must be reverified before becoming current authority.
- A server is not PASS/CLOSED until workload, functional, cleanup where applicable, and reboot-persistence gates are satisfied and its server record is updated.
- Batch obvious repetitive commands where practical; avoid unnecessary ping-pong and redundant prechecks.
- Do not diagnose or remediate HX-3's longer boot time unless explicitly asked. It is a recorded observation only.

## 4. Base-build rule

The current program is base stand-up, not full integration.

A base build may include small, reversible functional smoke tests against already-proven dependencies when they prove the application actually works.

Examples:
- Open WebUI may temporarily point directly at one known-good Ollama endpoint to send a prompt and receive a response.
- OmniRoute may temporarily route one request to one known-good Ollama endpoint and compare direct versus routed behavior.
- Mem0/LightRAG may use already-proven state/retrieval dependencies with synthetic disposable data where their primary contract requires it.

Temporary validation wiring must be recorded and removed/disabled before closure unless explicitly approved as permanent architecture.

## 5. Smoke-test authority and HX-5 runner rule

- `/smoke-tests/*.md` defines **what each component must prove**.
- `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` defines **how HX executes and retains the proof**.
- `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md` defines the permanent HX-5 client toolset and bootstrap.
- `tools/hx-smoke-runner/` contains the repository-owned helper implementation and scoped AI instructions.

After CentCom runner activation, execute later component smoke tests remotely from HX-5 whenever the product exposes a LAN/API/protocol/native-client/UI surface.

Do not leave general test scripts, Python environments, fixture libraries, runner dependencies, manifests, or evidence bundles on the system under test. A local SUT command invoked remotely over approved SSH is an exception only when local execution is intrinsic to the component.

An AI agent must not modify smoke-test acceptance criteria inside an in-progress run. If an authority is defective or stale, correct it in a separate reviewed repository change, commit it, and start a new run ID.

## 6. Application companion rule

When a major application has a product-specific MCP server or native Web UI, those are part of that application's base build.

Examples:
- Qdrant = Qdrant + Qdrant Web UI + Qdrant MCP.
- PostgreSQL = PostgreSQL + PostgreSQL MCP.
- LightRAG = LightRAG + LightRAG MCP.
- Docling = Docling + Granite-Docling + Docling MCP.
- Crawl4AI = Crawl4AI + Crawl4AI MCP.
- n8n = n8n + n8n MCP.

HX-15 FastMCP is a shared/custom MCP development host. It is not a prerequisite for product-specific MCP servers.

## 7. Model-placement rule

- HX-16 owns Granite-Docling 258M inside the Docling boundary. CPU-first base validation; GPU only if measured need justifies it later.
- HX-4 owns the shared embedding/reranking plane.
- BGE-M3 is the primary/default HX embedding model.
- Nomic Embed Text v1.5 is also installed as a benchmark/fallback.
- BGE-family reranker is hosted on HX-4.
- Never mix embeddings from different models in one Qdrant collection.
- A model change requires a new collection and re-embedding.

## 8. OmniRoute catalog rule

OmniRoute discovery does not equal HX approval.

Maintain two explicit controls:
- approved provider allowlist;
- approved model allowlist.

Provider approval does not approve the provider's entire model catalog. Free/no-auth/discovered providers are not automatically active.

## 9. NGINX rule

HX-7 NGINX is dev/test only.

Use it to render/proxy UIs for applications being actively developed when useful.

Do not use HX-7 as a general reverse proxy for Qdrant, LightRAG, n8n, Open WebUI, databases, MCP servers, or normal HX ecosystem services.

## 10. Documentation and execution-artifact rule

- Agents edit authoritative Markdown and approved execution artifacts only.
- `docs/**/*.md` = current control, architecture, standards, runbooks, server records, and evidence indexes.
- `smoke-tests/*.md` = current component acceptance authorities.
- `docs/03-runbooks/**/*.sh` and `tools/hx-smoke-runner/*` = approved repository execution helpers where present.
- Human HTML mirrors live under `human-html/` and are not execution authority.
- Only one current version stays active.
- Superseded versions go to `archive/`.
- Do not create duplicate active documents with timestamps, `(1)`, `final-final`, or model-name prefixes.
- Stable active filenames are mandatory.

Before declaring work complete, update the current server record, build state, and any affected decision/standard document. Do not mark planned tooling as installed until live HX-5 evidence exists.
