# HX Docling Skill

Docling on HX-16 uses the governed HX wrapper:

```text
skills/docling/hx-docling-advisor/
```

## HX placement

```text
HX-16 — 192.168.50.216
Docling + Granite-Docling 258M + Docling MCP
State: NOT STARTED
Deployment: native Ubuntu Linux; systemd for long-running services where applicable
Granite-Docling BASE: CPU-first
```

Granite-Docling 258M remains inside the HX-16 Docling boundary. Upstream remote-VLM or GPU examples do not move that model to HX-4 or another inference host.

## Source model

Docling provides both an official packaged usage skill and an official product-specific MCP project. The HX wrapper uses a layered source model:

1. **HX architecture, owner decisions, future HX-16 server record/runbook, and smoke authorities** for placement, execution, CPU-first model policy, companion boundaries, and acceptance.
2. **Official Docling documentation, source, releases, and package metadata** as primary product/runtime authority.
3. **The packaged `docling` usage skill** under `docling/.agents/skills/docling/` as reviewed `VENDOR_OFFICIAL` agent expertise.
4. **Official `docling-project/docling-mcp`** as the preferred `VENDOR_OFFICIAL` companion source, still subordinate to the future HX-16 runbook and D2 smoke authority.

The repository-root Docling development skills are contributor guidance and are not the packaged usage skill. They remain reference-only for HX-16 runtime work.

## Reviewed upstream

```text
Docling repository: docling-project/docling
Reviewed main: cdc2477e12107f45bf8b6813571f31f9e795ba07
Latest reviewed release: v2.126.0 — 2026-09-04
Packaged usage skill: docling/.agents/skills/docling/
Reviewed usage SKILL blob: f6bdfa26aee4b0df5a4cdfb6b496286e3b9eedd6
Usage references: 6
Python requirement: >=3.10,<4.0
License: MIT

Docling MCP repository: docling-project/docling-mcp
Reviewed MCP main: a8a41e6014ba3a148261702e760421086e9c80e3
Latest reviewed MCP release: v3.2.0 — 2026-09-01
MCP package at reviewed main: 3.2.0
MCP Python requirement: >=3.10
MCP license: MIT
```

These values establish reproducible provenance. They do not select the eventual HX-16 package versions, extras, environment, model revision/cache, service layout, or MCP transport.

## Official usage skill disposition

| Upstream capability | HX disposition | Boundary |
|---|---|---|
| Local CLI and Python SDK conversion | `ACCEPT + ADAPT` | Use within the future accepted HX-16 package/environment. |
| `DoclingDocument`, Markdown/JSON export, OCR, tables, layout | `ACCEPT + ADAPT` | Product expertise; task-specific options remain explicit. |
| `granite_docling` / Granite-Docling-258M | `ADAPT` | Preserve HX D-006: model stays HX-16 and BASE is CPU-first. |
| `docling-slim` modular extras | `ADAPT` | Future runbook selects exact package/extras. |
| `DocumentExtractor` beta | `REFERENCE_ONLY` for BASE | Later application scope only when beta behavior is explicitly accepted. |
| RAG/chunking/framework loaders | `REFERENCE_ONLY` for BASE | Later integration; no permanent RAG wiring during Docling BASE. |
| Service Client / remote VLM / remote URL processing | `OWNER_DECISION_REQUIRED` | Do not introduce new remote/egress/service architecture implicitly. |
| Containerized Docling Serve | `REJECT_FOR_HX` | Conflicts with native Linux/systemd policy. |
| Managed Docling / IBM watsonx replacing HX-16 | `REJECT_FOR_HX` | Conflicts with current local/native placement. |
| `library-skills` / symlink deployment | `REFERENCE_ONLY` | Possible derived agent deployment only; `skills/` remains canonical. |
| Contributor development skills | `REFERENCE_ONLY` | Not HX-16 runtime/product skill authority. |

## MCP boundary

The official `docling-project/docling-mcp` project is the preferred product-specific companion source. Upstream currently supports local, remote, and hybrid conversion modes; stdio, SSE, and streamable-HTTP transports; `uvx` quickstarts; and optional RAG/information-extraction toolsets.

HX does **not** convert those options into defaults:

- exact package/version, local/remote mode, transport, process, listener, cache, and systemd unit remain future HX-16 runbook decisions;
- remote mode requiring Docling Serve is reference-only for current BASE unless separately approved;
- containerized Docling Serve is rejected under the current native rule;
- managed-service replacement is rejected unless the owner changes HX-16 architecture;
- optional LlamaIndex/Milvus, LlamaStack, smolagents, and similar toolsets remain outside BASE unless separately admitted;
- HX-15 FastMCP is not a prerequisite for the product-specific Docling MCP;
- permanent MCP client registration/agent binding remains integration-phase work.

## Smoke-test alignment

The wrapper is explicitly bound to the current proof chain:

```text
D1  HX-16 Docling + Granite-Docling
    requires: CentCom active + Granite model staged locally
    live coupling: NONE
    fixture: self-generated local PDF
    proof: normal Docling conversion + Granite-Docling CPU path

D2  HX-16 Docling MCP
    requires: accepted D1 PASS
    live coupling: parent Docling service only
    proof: real MCP negotiation + advertised tool + safe known-answer tool call
```

Exact authorities:

- `smoke-tests/docling-smoke-test.md`
- `docs/04-application-standards/MCP-STANDARD.md`
- `smoke-tests/mcp-companion-smoke-test.md`
- current smoke roadmap and CentCom operating procedures.

A historical Docling v2.101.0 CLI bug could ignore `--device cpu` for VLM on a GPU-visible host. Upstream fixed it in June 2026 before the reviewed v2.126.0 release. The current smoke authority therefore remains technically defensible; the installed version and observed CPU execution must still be verified during D1.

## Governed intake verification

The `hx-docling-advisor` wrapper was created under the current skill-creation workflow, audited against `skills/AGENTS.md`, `SKILL-GOVERNANCE.md`, HX D-006/native rules, the BASE roadmap, and the D1/D2 smoke authorities.

Validation result:

```text
Skill validator: PASS
Packaged artifact: skill.zip
Files: 7
Archive size: 13,506 bytes
```

No execution/audit helper is bundled because HX-16 has no current server record or runbook and the exact package/service/MCP choices are intentionally not pinned yet. The current smoke test already contains the deterministic validation procedure.

**Skill validation proves the reusable expertise package only. It is not Docling runtime evidence and does not advance HX-16 BUILD-STATE.**

## Current execution boundary

HX-16 remains **NOT STARTED**. There is no active HX-16 server record or runbook. This skill does not select:

- exact Docling package/source/extras;
- Python environment/venv path;
- Granite-Docling model revision or cache path;
- long-running Docling process/service shape;
- listener/network exposure;
- Docling MCP version/mode/transport/systemd unit;
- remote Docling Serve architecture;
- permanent RAG/Qdrant/LightRAG integrations.

Those choices remain owner/runbook-controlled.
