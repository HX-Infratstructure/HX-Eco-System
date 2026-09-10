# Current Docling Upstream Guidance

## Primary product authority

Use current official Docling sources for version-sensitive claims:

- Documentation: `https://docling-project.github.io/docling/`
- Repository: `https://github.com/docling-project/docling`
- Releases: `https://github.com/docling-project/docling/releases`
- Agent Skills: `https://docling-project.github.io/docling/usage/agent_skills/`
- Agentic AI blog: `https://docling.ai/blog/20260901_00_docling-and-agentic-ai/`

Reviewed source state:

```text
Repository: docling-project/docling
Reviewed branch: main
Reviewed commit: cdc2477e12107f45bf8b6813571f31f9e795ba07
Reviewed date: 2026-09-09
Latest non-prerelease release: v2.126.0
Release published: 2026-09-04
Project/package license: MIT
Python requirement: >=3.10,<4.0
```

The reviewed package metadata reports `docling-slim` 2.126.0 and modular extras for formats, OCR, local/remote models, VLM, chunking, Service Client, and CLI. Treat these as packaging capabilities; exact HX-16 package/extras remain a runbook decision.

## Official packaged usage skill

The usage skill is shipped inside the Docling Python package at:

```text
docling/.agents/skills/docling/
|- SKILL.md
`- references/
   |- cli.md
   |- python-sdk.md
   |- extraction.md
   |- rag.md
   |- service-client.md
   `- slim-packaging.md
```

Reviewed skill blob:

```text
SKILL.md: f6bdfa26aee4b0df5a4cdfb6b496286e3b9eedd6
```

Reviewed reference blobs:

```text
cli.md:            3eda34458db46722fe9037e78a3b59f45dbe87c8
extraction.md:     c7a53655c80f761967ca1a204c7ff5a78e9bf417
python-sdk.md:     a61612ec24123d04838fa8b8d98ce7c65bfc0412
rag.md:            b5492831252174627ba01c24e97f420188c9bd85
service-client.md: 37c1b8c45035fc3147e2729f37c0fe0abd55d5cb
slim-packaging.md: 2d824ed5a8158fc132799c86a3e0aed73b635c3f
```

The upstream SKILL frontmatter includes vendor-specific fields beyond the HX/ChatGPT packaging schema. Do not copy it wholesale into HX; consume it as `VENDOR_OFFICIAL` guidance behind the HX wrapper.

## Usage versus development skills

Official Docling documentation distinguishes:

- usage skill: packaged under `docling/.agents/skills/docling/` for agents using Docling;
- development skills: repository-root `.agents/skills/` for contributors working on Docling.

At the reviewed commit, contributor skills include `dignified-python` and `building-pydantic-ai-agents`. They are not shipped as the Docling usage skill and are `REFERENCE_ONLY` for HX-16 runtime work.

## Granite-Docling identity

Current official model catalog records:

```text
Preset: granite_docling
Model: Granite-Docling-258M
Parameters: 258M
Transformers: supported
MLX: supported
API: Ollama supported
Output: DocTags
```

This aligns with HX D-006 placement of Granite-Docling 258M on HX-16. Upstream support for remote/API use does not move the HX model.

## CPU-path history

Upstream issue #3597 documented that Docling v2.101.0 could ignore `--device cpu` for the VLM CLI path on a GPU-visible host. PR #3599, merged 2026-06-16 at merge commit `846f81ae48d917a009346a8a866fba028d1350ce`, passed accelerator options into the VLM pipeline and added a regression test.

The reviewed v2.126.0 release is later than this fix. The current usage references also describe Granite-Docling Transformers as CPU/GPU capable. HX should still verify the installed version and observed CPU execution during D1 rather than relying only on documentation.

## Version discipline

Before material build/upgrade recommendations:

1. identify current accepted HX package/version/extras if any;
2. verify the current stable Docling release and release notes;
3. verify CLI/API behavior for the installed version;
4. verify Granite-Docling model/revision and cache availability;
5. reconcile package/model/MCP compatibility;
6. classify any architecture-impacting recommendation against HX authority.

Do not turn latest stable, a `uvx` example, or a vendor service recommendation into an HX implementation decision.
