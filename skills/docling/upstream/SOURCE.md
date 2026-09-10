# Docling Upstream Source Record

## Classification

```text
Component: Docling / Granite-Docling 258M / Docling MCP
HX host: HX-16 / 192.168.50.216
HX wrapper: skills/docling/hx-docling-advisor/
HX classification: HX_NATIVE + WRAPPER
Primary external class: VENDOR_OFFICIAL
Review date: 2026-09-09
```

## Official Docling product source

```text
Organization: docling-project
Repository: docling-project/docling
Reviewed branch: main
Reviewed commit: cdc2477e12107f45bf8b6813571f31f9e795ba07
Latest non-prerelease release at review: v2.126.0
Release published: 2026-09-04
Package metadata at reviewed main: docling-slim 2.126.0
Python requirement: >=3.10,<4.0
License: MIT
Documentation: https://docling-project.github.io/docling/
Agent Skills: https://docling-project.github.io/docling/usage/agent_skills/
Agentic AI article: https://docling.ai/blog/20260901_00_docling-and-agentic-ai/
```

## Packaged Docling usage skill

Official packaged path:

```text
docling/.agents/skills/docling/
├── SKILL.md
└── references/
    ├── cli.md
    ├── extraction.md
    ├── python-sdk.md
    ├── rag.md
    ├── service-client.md
    └── slim-packaging.md
```

Reviewed blobs:

```text
SKILL.md:        f6bdfa26aee4b0df5a4cdfb6b496286e3b9eedd6
cli.md:          3eda34458db46722fe9037e78a3b59f45dbe87c8
extraction.md:   c7a53655c80f761967ca1a204c7ff5a78e9bf417
python-sdk.md:   a61612ec24123d04838fa8b8d98ce7c65bfc0412
rag.md:          b5492831252174627ba01c24e97f420188c9bd85
service-client:  37c1b8c45035fc3147e2729f37c0fe0abd55d5cb
slim-packaging:  2d824ed5a8158fc132799c86a3e0aed73b635c3f
```

The packaged usage skill is vendor expertise, not copied wholesale into HX. Its upstream frontmatter and deployment assumptions are not the HX control plane. The stable canonical HX source remains `skills/docling/hx-docling-advisor/`.

Official Docling documentation also distinguishes repository-root development skills from the packaged usage skill. Contributor skills are not admitted as HX-16 runtime authority.

## Granite-Docling source context

At the reviewed Docling commit, the official model catalog identifies:

```text
Preset: granite_docling
Model: Granite-Docling-258M
Parameters: 258M
Transformers: supported
MLX: supported
API option: Ollama
Output format: DocTags
```

This aligns with HX decision D-006: Granite-Docling 258M remains on HX-16 and BASE validation is CPU-first.

Historical compatibility note: issue #3597 documented a v2.101.0 VLM CLI device-selection defect; PR #3599 fixed accelerator-option propagation and merged on 2026-06-16 at `846f81ae48d917a009346a8a866fba028d1350ce`. The reviewed v2.126.0 release is later than that fix.

## Official Docling MCP source

```text
Organization: docling-project
Repository: docling-project/docling-mcp
Reviewed branch: main
Reviewed commit: a8a41e6014ba3a148261702e760421086e9c80e3
Latest non-prerelease release at review: v3.2.0
Release published: 2026-09-01
Package at reviewed main: docling-mcp 3.2.0
Python requirement: >=3.10
MCP SDK range for 3.x: >=2.0.0,<3.0.0
License: MIT
```

Docling MCP is an official product-specific companion source. Current upstream supports remote, local, and hybrid conversion modes and multiple MCP transports. Those capabilities do not select HX-16 deployment architecture.

## HX consumption mode

```text
HX architecture / owner decisions
  > future HX-16 server record and runbook
  > HX smoke roadmap + exact D1/D2 tests
  > official current Docling product guidance
  > packaged Docling usage skill
  > official Docling MCP guidance
  > historical/general knowledge
```

Re-review when:

- Docling changes major version or packaged skill layout/behavior materially;
- Granite-Docling model identity/runtime support changes materially;
- Docling MCP changes major version, conversion modes, transport model, or compatibility materially;
- HX-16 runbook selects exact package/model/MCP choices;
- HX changes the CPU-first, native/systemd, or companion-service architecture.
