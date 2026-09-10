# HX Docling Context

## Placement

```text
Server: HX-16
IP: 192.168.50.216
Role: Docling + Granite-Docling 258M + Docling MCP
Current state: NOT STARTED
Deployment: native Ubuntu Linux; systemd for long-running services where applicable
Containers: not used unless the owner explicitly changes the architecture
```

Docling is the HX document-processing component. Granite-Docling 258M stays inside the HX-16 Docling boundary. It is not part of the shared HX-4 embedding/reranking plane.

## Owner-approved model rule

D-006 establishes:

- Granite-Docling 258M remains on HX-16;
- BASE validation is CPU-first;
- GPU acceleration is considered only after measured need justifies it later.

Do not replace this with an upstream GPU-first optimization recommendation.

## Current roadmap position

The current base implementation roadmap places HX-16 at priority 10, first in Wave D Knowledge Acquisition.

Current BASE PASS summary:

```text
native Docling
accepted Python/package environment
normal deterministic local PDF conversion
Granite-Docling 258M CPU-first deterministic proof
Docling MCP companion proof
cleanup
reboot/persistence evidence where applicable
```

## Current smoke dependency model

The smoke roadmap defines:

```text
D1 HX-16 Docling + Granite-Docling
  prerequisite: CentCom active; Granite model staged
  live integration: NONE; self-generated local PDF only

D2 HX-16 Docling MCP
  prerequisite: accepted D1 PASS
  live integration: parent Docling service only
```

Exact core authority: `smoke-tests/docling-smoke-test.md`.
Exact companion authority: `smoke-tests/mcp-companion-smoke-test.md`.

The D1 test must not download the Granite model at execution time and must not depend on external URLs, cloud services, containers, or production documents.

## Current implementation gaps

As of the current clean rebuild state:

- HX-16 is NOT STARTED;
- no active HX-16 server record exists under `docs/02-server-records/`;
- no active HX-16 runbook exists under `docs/03-runbooks/`;
- exact Docling package/source and extras are not pinned by a runbook;
- exact Python environment/venv path is not pinned;
- Granite-Docling model revision/cache path is not pinned;
- long-running process/service shape is not pinned;
- listener/network exposure, if any, is not pinned;
- exact Docling MCP package version/mode/transport/systemd layout is not pinned;
- RAG, Qdrant, LightRAG, remote VLM, and managed-service integrations are not BASE assumptions.

Do not fill these gaps from an upstream quickstart.

## HX invariants

- One server -> validate -> record -> next server.
- Native Linux + systemd; no Docker/Podman/Kubernetes.
- Product-specific MCP belongs to the parent application's base build and is independently smoke-tested.
- HX-15 FastMCP is not a prerequisite for Docling MCP.
- HX-5 CentCom is the standard remote smoke runner after activation, while approved SSH may be used when the component contract genuinely requires local execution.
- Validation-only documents/workspaces are disposable and must be removed.
- Do not remove persistent Docling configuration or the staged Granite model during smoke cleanup.
- Skill approval or documentation never changes BUILD-STATE.
