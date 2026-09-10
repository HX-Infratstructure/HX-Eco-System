# hx-doc — repository consistency tooling

Three small tools. Each one exists because the corresponding failure was found
in this repository during the 2026-09-10 audit, and each converts a written
rule into something that fails loudly.

No third-party dependencies. Python 3 standard library only.

| Tool | Replaces | Rule it enforces |
|---|---|---|
| `hx-render-html` | hand-written HTML mirrors | a mirror always matches its Markdown source |
| `hx-doc-check` | manual proofreading | links resolve, vocabulary is defined, filenames are stable, evidence is committable |
| `hx-upstream-drift` | remembering to re-check pins | the registry's reviewed commits still match upstream |

## hx-render-html

Generates every file under `human-html/` from its authoritative Markdown.

```bash
./tools/hx-doc/hx-render-html            # regenerate
./tools/hx-doc/hx-render-html --check    # CI: fail if any mirror is stale
```

`human-html/**` is generated output. Do not edit it by hand; edit the Markdown
and re-render. The mirrors were previously hand-written abridgements, and the
most important one had lost the entire ecosystem-cornerstone section.

## hx-doc-check

```bash
./tools/hx-doc/hx-doc-check
```

Checks:

- **links** — every internal path reference resolves. A reference to something
  that does not exist yet is allowed when the document says so; the recognised
  phrasings are listed in `FORWARD_MARKERS` in the script.
- **vocabulary** — `SKILL-REGISTRY.md` uses only lifecycle states that
  `SKILL-GOVERNANCE.md` defines.
- **frontmatter** — active control documents carry `document`, `status`, `date`.
- **duplicates** — no `-v1.2`, dated, or `(1)` filename in the active tree.
- **evidence** — `.gitignore` cannot silently drop retained evidence logs.

## hx-upstream-drift

Reads the pinned commits out of `skills/SKILL-REGISTRY.md` itself, so it cannot
fall out of step with the registry.

```bash
./tools/hx-doc/hx-upstream-drift                  # report
./tools/hx-doc/hx-upstream-drift --fail-on-drift  # non-zero when behind
./tools/hx-doc/hx-upstream-drift --markdown       # table for an issue body
```

Drift is information, not a failure. When a pin is behind, re-review that
source and update both the reviewed commit and the `Last reviewed` date in the
registry.
