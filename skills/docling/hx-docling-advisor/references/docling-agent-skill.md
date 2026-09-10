# Official Docling Usage Skill - HX Disposition

## Reviewed source

```text
Publisher: docling-project
Repository: docling-project/docling
Path: docling/.agents/skills/docling/
Reviewed main: cdc2477e12107f45bf8b6813571f31f9e795ba07
Usage skill count: 1
On-demand references: 6
HX classification: VENDOR_OFFICIAL external source behind HX_NATIVE + WRAPPER
```

The official skill is a short router with progressive disclosure. That design is compatible with HX, but the upstream architecture choices remain subordinate to HX.

## Reference-by-reference disposition

| Upstream reference | HX disposition | HX rule |
|---|---|---|
| `cli.md` | `ACCEPT + ADAPT` | Use local CLI for supported document tasks; keep BASE local/deterministic and gate remote URLs/services. |
| `python-sdk.md` | `ACCEPT + ADAPT` | Use `DocumentConverter`, `PipelineOptions`, exports, batching, tables, OCR, and VLM guidance within accepted HX package/model choices. |
| `extraction.md` | `REFERENCE_ONLY` for BASE | `DocumentExtractor` is beta; use only in explicit later application scope that accepts beta behavior. |
| `rag.md` | `REFERENCE_ONLY` for BASE | Chunking/loaders are useful later; do not create permanent LightRAG/Qdrant/other ingestion architecture during Docling BASE. |
| `service-client.md` | `REFERENCE_ONLY / OWNER_DECISION_REQUIRED` | Remote service is not current HX-16 BASE. Containerized Docling Serve and managed replacement conflict with current architecture. |
| `slim-packaging.md` | `ADAPT` | Modular extras can improve footprint, but the future HX-16 runbook selects exact package/extras. |

## Accepted product expertise

Use current official guidance for:

- converting supported file formats into `DoclingDocument`;
- Markdown or structured JSON export;
- handling born-digital versus scanned/complex-layout documents;
- OCR engine and table-structure behavior;
- page-range and output choices;
- local Python SDK and CLI usage;
- Granite-Docling VLM options;
- chunking or framework integration when the task explicitly enters later integration scope.

## HX adaptations and rejections

- `uvx --from docling ...` -> `REFERENCE_ONLY` as an ephemeral convenience, not the HX-16 long-running deployment model.
- `uvx library-skills` / symlinked agent skill -> `REFERENCE_ONLY` for possible derived agent deployment; canonical HX source remains `skills/`.
- remote URL conversion -> `OWNER_DECISION_REQUIRED` when it changes network/egress assumptions.
- remote VLM / `--enable-remote-services` -> `OWNER_DECISION_REQUIRED`.
- self-hosted `docling-serve` by container -> `REJECT_FOR_HX`.
- managed Docling/IBM watsonx replacing HX-16 -> `REJECT_FOR_HX`.
- upstream statements that VLM normally needs GPU -> `ADAPT`; HX BASE is explicitly CPU-first for Granite-Docling 258M.
- contributor development skills under repo-root `.agents/skills/` -> `REFERENCE_ONLY`; they are not the packaged usage skill.

## Validation discipline

The vendor skill's quick verification guidance is useful diagnostic advice, but it does not define HX PASS.

HX D1 must prove both:

1. deterministic normal Docling conversion of the self-generated smoke PDF;
2. Granite-Docling 258M VLM processing of the same PDF with `--device cpu`.

Then D2 separately proves the Docling MCP companion. Do not replace this with vendor examples, generic successful conversion, or agent-skill invocation.
