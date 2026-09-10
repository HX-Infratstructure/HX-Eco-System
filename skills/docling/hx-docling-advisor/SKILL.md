---
name: hx-docling-advisor
description: Guide Docling work inside the HX Eco-System using HX architecture and execution authority plus current official Docling product guidance, the packaged Docling usage skill, and official Docling MCP guidance. Use for HX-16 Docling and Granite-Docling planning, native installation/configuration reasoning, CLI/Python SDK conversion, OCR, tables, VLM processing, structured extraction, chunking/RAG preparation, packaging, validation, troubleshooting, upgrades, and the Docling MCP companion. Never let upstream container, managed-service, remote-service, GPU-first, agent-symlink, or RAG defaults override HX-16 placement, native/systemd deployment, CPU-first Granite-Docling BASE proof, companion MCP boundary, or HX smoke-test authority.
---

# HX Docling Advisor

Apply current Docling expertise without allowing upstream quickstarts, managed services, containerized Docling Serve, or generic agent integrations to redesign HX-16.

## Authority order

1. Current infrastructure-owner instruction.
2. Current HX control and architecture Markdown.
3. Current live HX-16 evidence.
4. Current HX-16 server record/runbook/standards when they exist.
5. HX smoke roadmap and exact Docling/MCP smoke authority when validating.
6. Current official Docling documentation, source, release notes, and package metadata.
7. Reviewed official packaged Docling usage skill as subordinate product expertise.
8. Reviewed official `docling-project/docling-mcp` guidance as subordinate companion expertise.
9. Historical reference and general model knowledge only where higher authorities do not answer.

Before material work, follow the scoped preflight in `skills/AGENTS.md`: read root `AGENTS.md` and `README.md`, establish current component state, read `skills/SKILL-GOVERNANCE.md`, `skills/SKILL-REGISTRY.md`, and `skills/docling/README.md`, then load this wrapper and only the references required for the task. Do not use `human-html/` or `archive/` as execution authority.

Read `references/hx-context.md` and `references/authority-map.md` first.

## Establish HX context

Before material Docling work, state:

- HX-16 / `192.168.50.216`;
- current build state;
- Docling + Granite-Docling 258M + Docling MCP role;
- native Linux/systemd boundary;
- Granite-Docling placement and CPU-first BASE rule;
- current package/environment/model-cache/service choices if pinned;
- task type and BASE or later-integration boundary;
- required prior smoke proof.

If execution depends on an unpinned choice, return `OWNER_DECISION_REQUIRED`; do not inherit a default from the vendor skill, `uvx`, Docling Serve, MCP examples, or managed services.

## Verify current upstream

Read `references/upstream.md` for version-sensitive work.

At the 2026-09-09 review point:

- `docling-project/docling` main is pinned in the reference file;
- latest non-prerelease Docling release is `v2.126.0`;
- the packaged usage skill is one `docling` router plus six on-demand references;
- Docling requires Python 3.10+;
- the official model catalog identifies preset `granite_docling` as Granite-Docling-258M;
- official `docling-project/docling-mcp` is active, with current main and release recorded in `references/docling-mcp.md`.

These facts are upstream context, not automatic HX package/version/runtime selections.

## Use the official Docling usage skill selectively

Read `references/docling-agent-skill.md` when the task involves CLI conversion, Python SDK, extraction, RAG/chunking, remote service use, or slim packaging.

Use these HX dispositions:

- local CLI and Python SDK conversion -> `ACCEPT` or `ADAPT` within the accepted HX-16 environment;
- `DoclingDocument`, Markdown/JSON export, table/OCR/layout guidance -> normally `ACCEPT` or `ADAPT`;
- `granite_docling` VLM guidance -> `ADAPT` to the owner-approved HX-16 CPU-first BASE rule;
- `docling-slim` extras -> `ADAPT`; exact package/extras remain runbook-controlled;
- `DocumentExtractor` beta -> `REFERENCE_ONLY` for BASE; use only when an explicit later application task accepts beta behavior;
- RAG/framework loaders/chunking -> `REFERENCE_ONLY` for BASE and useful later-integration expertise;
- `DoclingServiceClient`, remote VLM, or remote URL processing -> `OWNER_DECISION_REQUIRED` when they change HX network/egress/service architecture;
- containerized `docling-serve` -> `REJECT_FOR_HX` under the current native rule;
- managed Docling/IBM watsonx replacing HX-16 -> `REJECT_FOR_HX` unless the owner changes placement/runtime policy;
- `library-skills` symlink installation -> `REFERENCE_ONLY` as a possible derived agent deployment mechanism, never the canonical HX skill source;
- upstream contributor-only development skills -> `REFERENCE_ONLY`, not HX-16 runtime guidance.

Do not copy or direct-install the upstream packaged skill as a second canonical HX authority.

## Recommendation labels

Use exactly these labels for material recommendations:

- `ACCEPT` - compatible with current HX authority.
- `ADAPT` - useful Docling principle, implementation must fit HX.
- `REFERENCE_ONLY` - useful knowledge outside current HX BASE/runtime scope.
- `REJECT_FOR_HX` - conflicts with an explicit HX decision.
- `OWNER_DECISION_REQUIRED` - selects or changes unresolved HX architecture.

## HX-16 architecture boundary

```text
HX-16 / 192.168.50.216
|- Docling native document processing
|- Granite-Docling 258M inside the Docling boundary
|  `- CPU-first BASE validation
`- Docling MCP companion
```

Use native Linux. Long-running services use systemd where applicable. Do not containerize Docling, Docling Serve, Granite-Docling, or the Docling MCP companion unless the owner explicitly changes the rule.

Granite-Docling stays on HX-16. Do not move it to HX-4 or another inference host merely because upstream supports remote VLM execution. GPU acceleration is not part of BASE; consider it only after measured need and owner approval.

The current HX-16 runbook and server record do not exist. Package source, exact package/extras, Python environment, model-cache path, process/service shape, listeners, and MCP transport/unit remain implementation-time owner/runbook decisions.

## Document-processing correctness rules

- Distinguish born-digital, scanned/image-only, and complex-layout documents before changing OCR/VLM behavior.
- Preserve `DoclingDocument` as the structured representation when downstream structure matters; Markdown is a projection, not a lossless replacement.
- Treat OCR engine, table-structure mode, page ranges, image retention, enrichment, and model selection as task-dependent choices, not global defaults.
- Keep remote URLs and remote model/service calls out of BASE validation unless explicitly authorized.
- Keep BASE deterministic: self-generated local PDF, locally staged Granite-Docling, no external source document, no cloud model, and no download-at-test-time dependency.
- Do not make Docling responsible for Qdrant, LightRAG, or production RAG ingestion during BASE. Those are later integration concerns.
- Record installed Docling version and Granite-Docling model/revision during validation; verify version-specific CLI/API behavior before relying on current examples.

## CPU-first Granite-Docling rule

The current owner decision is stronger than an upstream performance rule of thumb: Granite-Docling 258M is validated on CPU first.

Current upstream history matters here. Docling v2.101.0 had a bug where `--pipeline vlm --device cpu` could ignore the CPU request on a GPU-visible host. That issue was fixed upstream in June 2026 before the reviewed v2.126.0 release. Re-verify the installed version and observed device during HX-16 validation; do not weaken the current smoke criterion merely because older upstream guidance said VLM normally benefits from GPU.

## Docling MCP boundary

Read `references/docling-mcp.md` for MCP-specific work.

The official `docling-project/docling-mcp` repository is the preferred vendor companion source, but its defaults are not HX architecture. Current upstream recommends remote mode by default and also offers local and hybrid modes, `uvx`, multiple transports, managed services, and optional RAG toolsets.

For HX-16:

- official Docling MCP source -> `ACCEPT + ADAPT`;
- exact package version, mode, transport, process layout, and systemd unit -> `OWNER_DECISION_REQUIRED` until the HX-16 runbook pins them;
- remote mode requiring Docling Serve or managed service -> `REFERENCE_ONLY` for current BASE unless separately approved;
- containerized Docling Serve -> `REJECT_FOR_HX`;
- LlamaIndex/Milvus, LlamaStack, smolagents, and other optional MCP toolsets -> `REFERENCE_ONLY` for BASE unless separately admitted;
- HX-15 FastMCP is not a prerequisite for the product-specific Docling MCP.

## Validation boundary

Docling BASE validation remains controlled by the current smoke roadmap and exact authorities. The current proof chain is `D1` HX-16 Docling + Granite-Docling -> `D2` HX-16 Docling MCP.

`D1` requires CentCom active and Granite-Docling staged locally. It uses no live component integration: the test creates its own deterministic local PDF, verifies normal Docling conversion, then verifies the `granite_docling` VLM path on CPU. Exact authority: `smoke-tests/docling-smoke-test.md`.

`D2` requires accepted `D1` PASS and validates only the parent Docling MCP companion through `smoke-tests/mcp-companion-smoke-test.md`.

Reboot/persistence, cleanup, retained evidence, server-record update, and BUILD-STATE closure follow current HX roadmap rules.

Do not substitute a vendor quickstart, `docling --help`, successful import, generated Markdown alone, MCP tool discovery alone, or this skill for the HX smoke authority.

Never report `PASS` for an unexecuted check. Use `FAIL`, `BLOCKED`, `NOT TESTED`, or `OWNER_DECISION_REQUIRED` when evidence or authority is incomplete.

## Stop conditions

Stop rather than improvise when:

- the HX-16 runbook/server record needed for execution is absent;
- package/extras/environment/model-cache/service/MCP choices required for execution are not pinned;
- a recommendation introduces containers, managed replacement, remote VLM/service architecture, GPU placement, new network exposure, storage changes, or permanent RAG integration without owner authority;
- the installed Docling version cannot honor the required CPU-first Granite-Docling smoke path;
- test cleanup could remove non-smoke files or persistent model/cache/configuration;
- required MCP implementation/mode/transport is not selected for a task that needs it;
- current official Docling behavior contradicts the active HX runbook or smoke test.

If official behavior proves an HX smoke test technically invalid, stop the run. Correct the HX authority separately and begin a new validation run; never reinterpret PASS in place.
