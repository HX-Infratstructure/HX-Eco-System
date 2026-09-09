---
document: HX Eco-System Document Control Standard
status: current
date: 2026-09-09
---

# Document Control Standard

## Objective
Keep the active repository unambiguous for human and agentic readers.

## Active-document rule
Exactly one current copy of a document is allowed in the active tree.

Active documents:
- use stable filenames;
- do not include version numbers or dates in filenames;
- carry version/date/status inside the document;
- live under `docs/`.

Do not keep active duplicates such as `-v1.2`, dated copies, `(1)`, `final-final`, or model-name-prefixed variants.

## Supersession procedure
1. Create `archive/YYYY-MM-DD/<same-active-path>/`.
2. Move/copy the prior active Markdown there with a version suffix if useful.
3. Archive the matching prior HTML mirror.
4. Replace the active Markdown at the stable path.
5. Replace the human HTML mirror at the stable mirrored path.
6. Verify only one active version remains.

## Authority
- `docs/**/*.md` = authoritative current content.
- `human-html/**/*.html` = derived human view.
- `archive/**` = historical only.
- Evidence documents observations; it does not independently override explicit owner decisions.

## Agent behavior
Agents must ignore `human-html/` and `archive/` during normal context loading unless explicitly asked.

## Pairing rule
Major planning, architecture, and standards documents should have one active Markdown source and one matching HTML human mirror. Operational state files may remain Markdown-only where an HTML mirror adds little value.
