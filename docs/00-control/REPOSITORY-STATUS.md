---
document: HX Eco-System Repository Status
status: current
date: 2026-09-09
authority: HX-Eco-System repository control
---

# HX Eco-System — Repository Status

## Status

**Agent-facing repository initialization and SSOT reconciliation: PASS**

Repository: `HX-Infratstructure/HX-Eco-System`  
Branch: `main`  
Visibility: private

## Authority model

- `AGENTS.md` — agent operating contract.
- `docs/**/*.md` — active authoritative agent-facing documentation.
- `docs/03-runbooks/**/*.sh` — current approved execution artifacts for the named build stage.
- `human-html/**/*.html` — human-readable mirrors; not agent authority.
- `archive/**` — superseded historical material only.

Agents must not use `archive/` or `human-html/` as current truth unless explicitly asked.

## Reconciliation completed 2026-09-09

- Full HX-2 as-built record promoted to active GitHub server record.
- Full HX-3 as-built record promoted to active GitHub server record.
- Bootstrap HX-2/HX-3 summaries archived.
- HX-4 three-block base runbook imported.
- HX-5 three-block base runbook imported.
- HX-4/HX-5 Block 1 sudoers temporary-file defect corrected and syntax-validated before promotion.
- Corrected HX-4/HX-5 Block 1 scripts also updated in the Drive project SSOT.
- Full owner-approved model-placement and embedding standard promoted; bootstrap summary archived.
- Canonical v1.3 deployment plan promoted; bootstrap summary archived.
- Deployment-plan and model-placement HTML mirrors expanded for human review; prior bootstrap mirrors archived.
- Repository tree checked for `.local.env`; none is committed.

## Intentional limitations

- HX-1 has a concise current baseline record because a more detailed current clean-rebuild HX-1 as-built record has not yet been established in the new SSOT. Do not fabricate missing detail from historical HX-Infrastructure material.
- HX-4 and HX-5 runbooks contain the approved common base blocks. Server-specific model/application installation steps are added only when finalized and executed.
- HX-4 through HX-17 remain NOT STARTED until current execution evidence proves otherwise.

## Current next execution target

**HX-4 — Meta-X / Ollama / GPT-OSS 20B + shared BGE-M3 / Nomic embedding plane + BGE-family reranker.**

Use `docs/03-runbooks/HX-4/` and the deployment/model standards in `docs/00-control/`.
