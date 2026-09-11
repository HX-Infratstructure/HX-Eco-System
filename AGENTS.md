# AGENTS.md — HX Eco-System Agent Operating Contract

This repository is designed to be immediately understandable by agentic coding and infrastructure agents.

## 1. Required reading order

Before changing anything:

1. `README.md`
2. `docs/00-control/CURRENT-STATE.md`
3. `docs/00-control/BUILD-STATE.md`
4. `docs/00-control/DECISIONS.md`
5. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`
6. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`
7. Relevant current server record under `docs/02-server-records/`
8. Relevant runbook under `docs/03-runbooks/`
9. Relevant standard under `docs/04-application-standards/`
10. If a governed component skill exists, read `skills/SKILL-GOVERNANCE.md`, `skills/SKILL-REGISTRY.md`, and the approved component wrapper under `skills/<component>/`.
11. **Only if validating:** `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`.
12. `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md`.
13. If executing a component smoke test, the exact authority under `smoke-tests/`.
14. If using the HX-5 runner, `tools/hx-smoke-runner/AGENTS.md`.

Do not read `archive/` or `human-html/` as current authority unless explicitly asked.

## 2. Truth order

1. Explicit current instruction from the infrastructure owner.
2. Current active control/architecture Markdown in `docs/` and the exact current component acceptance authority in `smoke-tests/` when testing.
3. Current live evidence from the server being worked on.
4. Current approved runbook/execution artifact.
5. Governed HX wrapper skill plus current official vendor guidance for product-specific expertise.
6. Historical/archive material, only as reference.
7. General model knowledge.

If current live evidence or current official vendor requirements contradict an active document, stop treating the document as sufficient proof and report the contradiction. Do not silently let a vendor skill redesign HX.

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

## 4. Ecosystem-first rule

The HX ecosystem architecture is the cornerstone. Validation is subordinate to it.

Before executing or designing a smoke test, an agent must understand and be able to state:

- the component's assigned HX server and target IP;
- the server's role and current build state;
- the applicable LAN/domain/deployment baseline;
- the component's architectural layer and ownership boundary;
- required versus validation-only dependencies;
- applicable model/data placement rules;
- the current dependency/build priority and BASE PASS boundary.

`docs/01-architecture/ARCHITECTURE-ORIENTATION.md` is the foundational orientation authority. Smoke-testing documents are validation-layer authorities and must not redefine ecosystem placement, permanent integration, server roles, or network architecture.

If an agent cannot answer the foundational questions above, it is not ready to execute validation.

## 5. Two-roadmap rule

HX maintains two complementary evergreen roadmaps:

1. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md` — deployment/build order and BASE PASS boundaries.
2. `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` — ordered proof dependencies, prior PASS evidence, companion gates, and permitted limited validation integration.

The smoke roadmap inherits the deployment roadmap. It never authorizes testing a component before the SUT is installed/ready.

A downstream smoke test must reference the current prior PASS evidence it relies on. Do not force unnecessary integration merely to make the sequence look connected; HX uses **cumulative proof with minimal live coupling**.

## 6. Governed skills rule

`skills/` is the canonical HX capability library for reusable agent expertise.

- Read `skills/SKILL-GOVERNANCE.md` and `skills/SKILL-REGISTRY.md` before operational use of a component skill.
- HX wrappers load current HX context before vendor/community guidance.
- Vendor-official skills are preferred over community skills for product-specific expertise.
- A skill may guide planning, native installation/configuration decisions, troubleshooting, upgrades, and validation preparation, but it does not replace the HX runbook or smoke-test authority.
- External skills cannot authorize host-placement changes, container/cloud/embedded deployment, cluster topology, network/security/storage changes, model-placement changes, permanent integration, or changes to PASS criteria.
- Agent-specific skill installations are derived from the canonical `skills/` source; do not maintain divergent hand-edited copies.
- Skills never contain actual passwords, PATs, API keys, private keys, service-account secrets, or sshpass passwords.

Qdrant is the first approved reference implementation at `skills/qdrant/hx-qdrant-advisor/`.

## 7. Base-build rule

The current program is base stand-up, not full integration.

A base build may include small, reversible functional smoke tests against already-proven dependencies when they prove the application actually works.

Examples:
- Open WebUI may temporarily point directly at one known-good Ollama endpoint to send a prompt and receive a response.
- OmniRoute may temporarily route one request to one known-good Ollama endpoint and compare direct versus routed behavior.
- Mem0/LightRAG may use already-proven state/retrieval dependencies with synthetic disposable data where their primary contract requires it.

Temporary validation wiring must be recorded and removed/disabled before closure unless explicitly approved as permanent architecture.

## 8. Smoke-test authority and HX-5 runner rule

- `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` defines **which proof runs next and which prior PASS evidence it consumes**.
- `docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md` defines **how the validation subsystem fits together after ecosystem context is established**.
- `/smoke-tests/*.md` defines **what each component must prove**.
- `docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md` defines **how HX executes and retains the proof**.
- `docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md` defines the permanent HX-5 client toolset and bootstrap.
- `tools/hx-smoke-runner/` contains the repository-owned helper implementation and scoped AI instructions.

After CentCom runner activation, execute later component smoke tests remotely from HX-5 whenever the product exposes a LAN/API/protocol/native-client/UI surface.

Do not leave general test scripts, Python environments, fixture libraries, runner dependencies, manifests, or evidence bundles on the system under test. A local SUT command invoked remotely over approved SSH is an exception only when local execution is intrinsic to the component.

An AI agent must not modify smoke-test acceptance criteria inside an in-progress run. If an authority is defective or stale, correct it in a separate reviewed repository change, commit it, and start a new run ID.

## 9. Application companion rule

When a major application has a product-specific MCP server or native Web UI, those are part of that application's base build.

Examples:
- Qdrant = Qdrant + Qdrant Web UI + Qdrant MCP.
- PostgreSQL = PostgreSQL + PostgreSQL MCP.
- LightRAG = LightRAG + LightRAG MCP.
- Docling = Docling + Granite-Docling + Docling MCP.
- Crawl4AI = Crawl4AI + Crawl4AI MCP.
- n8n = n8n + n8n MCP.

HX-15 FastMCP is a shared/custom MCP development host. It is not a prerequisite for product-specific MCP servers.

## 10. Model-placement rule

- HX-16 owns Granite-Docling 258M inside the Docling boundary. CPU-first base validation; GPU only if measured need justifies it later.
- HX-4 owns the shared embedding/reranking plane.
- BGE-M3 is the primary/default HX embedding model.
- Nomic Embed Text v1.5 is also installed as a benchmark/fallback.
- BGE-family reranker is hosted on HX-4.
- Never mix embeddings from different models in one Qdrant collection.
- A model change requires a new collection and re-embedding.

## 11. OmniRoute catalog rule

OmniRoute discovery does not equal HX approval.

Maintain two explicit controls:
- approved provider allowlist;
- approved model allowlist.

Provider approval does not approve the provider's entire model catalog. Free/no-auth/discovered providers are not automatically active.

## 12. NGINX rule

HX-7 NGINX is dev/test only.

Use it to render/proxy UIs for applications being actively developed when useful.

Do not use HX-7 as a general reverse proxy for Qdrant, LightRAG, n8n, Open WebUI, databases, MCP servers, or normal HX ecosystem services.

## 13. Change rule — everything goes through a pull request

`main` is not a working branch. Every change, including a one-line fix, goes
through a pull request so CodeRabbit reviews it. Review is not optional.

```bash
git checkout -b <type>/<short-name>

# work, then regenerate anything derived and check it:
tools/hx-doc/hx-fleet && tools/hx-doc/hx-render-html && tools/hx-doc/hx-doc-check

# commit before pushing - git push sends commits, not working-tree edits:
git add -A
git status          # confirm the diff is what you mean to submit
git commit

# review locally before the push, not after it:
coderabbit review --agent

git push -u origin HEAD && gh pr create
```

`coderabbit review --agent` before every push is required, not a convenience.
The hosted reviewer runs after the push, applies the configuration from the
base branch rather than the branch under review, and on a public repository it
can refuse for the day once the review limit is reached. The command line
reviewer has none of those limits: it reads the working tree and the
configuration as they are now.

The first push of the day that skipped it shipped two defects: a duplicate
`with:` key that stopped a workflow from starting at all, and a `path_filters`
entry that turned the filter list into an allow list and would have excluded
every file in the repository from review. The command line reviewer reported
both before they reached the branch.

It runs from a CodeRabbit API key. `coderabbit auth status` reports whether one
is configured.

A pull request stacked on another branch is reviewed too: `.coderabbit.yaml`
matches every base branch, not just `main`. Naming only `main` there silently
skipped stacked work, which is an unreviewed change.

Keep a pull request under 100 changed files. CodeRabbit skips anything larger,
and a skipped review is the same as no review. Generated output and archive are
already filtered out in `.coderabbit.yaml`, which is what usually pushes a
change over the line.

When CodeRabbit raises something, fix it. Small, medium or large. If a finding
is wrong, say why on the thread rather than ignoring it.

## 14. Repository tooling rule

Written rules that nothing checks will drift. These tools are the enforcement
layer; treat a failure as a real defect, not as noise to work around.

| Command | Enforces |
|---|---|
| `tools/hx-doc/hx-doc-check` | links resolve, registry vocabulary is defined, control frontmatter is complete, filenames are stable, evidence is committable |
| `tools/hx-doc/hx-proof` | the proof DAG is valid and its generated blocks are current |
| `tools/hx-doc/hx-render-html` | every `human-html/` mirror matches its Markdown source |
| `tools/hx-doc/hx-upstream-drift` | the registry's pinned upstream commits are still current |

If a check is wrong, fix the check in a reviewed change. Do not bypass it and
do not weaken it to make an existing document pass.

### Proof chain

`docs/00-control/hx-proof.tsv` is the source for the smoke-test dependency
chain. Before running a step, ask whether it may run at all:

```bash
tools/hx-doc/hx-proof --ready B2
```

`hx-smoke-promote` enforces the same DAG: a PASS is refused when a required
prior step has not passed and been cited in `prior_pass_evidence`. There is no
bypass flag. If a dependency genuinely does not apply, change `requires` in the
TSV through a reviewed pull request.

### Graft

`graft` indexes 70 of 388 files here: the Python tools and the shell blocks. It
does not read Markdown, where every authority in this repository lives, and it
produces no call edges for shell.

- `graft blast` before changing anything under `tools/`.
- `graft ask` to locate a shell helper across the runbook blocks.
- An empty result means **not in the graph**, never **does not exist**. Fall
  back to `hx-doc-check`, `grep`, or the document itself.
- It runs from WSL on the current workstation. `graft upgrade` wipes the bash
  registration; re-run `tools/hx-doc/hx-graft-bash` afterwards.

## 15. Documentation and execution-artifact rule

- Agents edit authoritative Markdown and approved execution artifacts only.
- `docs/**/*.md` = current control, architecture, standards, runbooks, server records, and evidence indexes.
- `skills/**/*.md`, `skills/**/SKILL.md`, and skill metadata = canonical governed agent-capability source, subordinate to HX architecture/runbooks/smoke authority.
- `smoke-tests/*.md` = current component acceptance authorities; they do not define ecosystem architecture.
- `docs/03-runbooks/**/*.sh` and `tools/hx-smoke-runner/*` = approved repository execution helpers where present.
- Human HTML mirrors live under `human-html/` and are not execution authority.
- `human-html/**` is **generated output**. Never hand-edit it. Edit the Markdown
  source and run `tools/hx-doc/hx-render-html`.
- Before committing a documentation change, run `tools/hx-doc/hx-doc-check` and
  `tools/hx-doc/hx-render-html`. CI runs both and fails the change otherwise.
- Only one current version stays active.
- Superseded versions go to `archive/`.
- Do not create duplicate active documents with timestamps, `(1)`, `final-final`, or model-name prefixes.
- Stable active filenames are mandatory.

Before declaring work complete, update the current server record, build state, and any affected decision/standard document. Do not mark planned tooling as installed until live evidence exists.
