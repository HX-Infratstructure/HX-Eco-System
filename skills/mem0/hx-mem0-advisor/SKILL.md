---
name: hx-mem0-advisor
description: Guide Mem0 work inside the HX Eco-System using HX architecture and execution authority plus current official Mem0 documentation and skills. Use for HX-13 Mem0 OSS planning, native self-hosted installation/configuration reasoning, memory lifecycle and scoping, Qdrant/Ollama provider integration, Python/TypeScript SDK usage, framework integration, developer workflow review, validation, troubleshooting, upgrades, and the assigned Mem0 MCP capability. Never let Mem0 Platform, Vercel, repository-writing pipeline skills, coding-assistant plugins, or upstream defaults override HX-13 placement, native/systemd deployment, approved dependencies, network/security rules, execution authority, or BASE PASS criteria.
---

# HX Mem0 Advisor

Apply current Mem0 expertise without allowing Platform-first quickstarts, coding-assistant plugins, or upstream integration automation to redesign HX-13.

## Authority order

1. Current infrastructure-owner instruction.
2. Current HX control/architecture Markdown.
3. Current live HX-13 evidence.
4. Current HX-13 server record/runbook/standards when they exist.
5. HX smoke roadmap and exact Mem0/MCP smoke authority when validating.
6. Current official Mem0 documentation and `mem0ai/mem0` source.
7. Reviewed official Mem0 skills as subordinate product/developer expertise.
8. Historical reference and general model knowledge only where higher authorities do not answer.

Before material work, follow the scoped preflight in `skills/AGENTS.md`: read root `AGENTS.md` and `README.md`, establish current component state, read `skills/SKILL-GOVERNANCE.md`, `skills/SKILL-REGISTRY.md`, and `skills/mem0/README.md`, then load this wrapper and only the references required for the task. Do not use `human-html/` or `archive/` as execution authority.

Read `references/hx-context.md` and `references/authority-map.md` first.

## Establish HX context

Before material Mem0 work, state:

- HX-13 / `192.168.50.213`;
- current build state;
- Mem0 OSS + assigned MCP role;
- accepted dependencies and prerequisite PASS evidence;
- accepted runtime/package/service/data/network choices if already pinned;
- task type and BASE boundary.

If execution depends on an unpinned choice, return `OWNER_DECISION_REQUIRED`; do not inherit defaults from an upstream skill, quickstart, or plugin.

## Verify current upstream

Read `references/upstream.md` for every version-sensitive task.

At the 2026-09-09 review point:

- official `mem0ai/mem0` main is pinned in the reference file;
- Python `mem0ai` source version is 2.0.20;
- TypeScript `mem0ai` source version is 3.1.6;
- the official skills graph contains six skills;
- the official skill guidance tests Python `mem0ai` 2.x and npm `mem0ai` 3.x ranges.

These are upstream facts, not automatic HX runtime selections.

## Use the official Mem0 skill graph selectively

Read `references/mem0-agent-skills.md` when a task overlaps SDK usage, CLI, Vercel AI SDK, repo integration, integration testing, OSS-to-Platform migration, coding-assistant plugins, or MCP.

Use these HX dispositions:

- official `mem0` reference skill -> `ADAPT`: use OSS/self-hosted guidance for HX-13; Platform guidance is reference only unless owner-approved.
- `mem0-cli` -> `REFERENCE_ONLY` for HX-13 BASE unless an HX runbook explicitly selects it; current CLI guidance is Platform/API-key oriented.
- `mem0-vercel-ai-sdk` -> `REFERENCE_ONLY`; not an HX-13 BASE runtime dependency.
- `mem0-integrate` -> `REFERENCE_ONLY` for the HX infrastructure repo unless explicitly authorized for a target application repo; it creates branches/files and is not HX execution authority.
- `mem0-test-integration` -> `REFERENCE_ONLY`; it does not replace HX smoke-test authority.
- `mem0-oss-to-platform` -> `REJECT_FOR_HX_RUNTIME` unless the owner explicitly changes HX-13 from self-hosted OSS to hosted Platform.
- Mem0 coding-assistant plugins/MCP integrations -> `REFERENCE_ONLY` until separately admitted for their exact HX role.

Do not direct-install the upstream six-skill bundle as a second canonical HX source.

## Recommendation labels

Use exactly these labels for material recommendations:

- `ACCEPT` — compatible with current HX authority.
- `ADAPT` — useful Mem0 principle, implementation must fit HX.
- `REFERENCE_ONLY` — useful knowledge outside current HX runtime/BASE scope.
- `REJECT_FOR_HX` — conflicts with an explicit HX decision.
- `REJECT_FOR_HX_RUNTIME` — conflicts specifically with HX-13 runtime architecture.
- `OWNER_DECISION_REQUIRED` — chooses or changes unresolved HX architecture.

Typical classifications:

- Docker/Podman/Kubernetes -> `REJECT_FOR_HX` unless owner changes the native standard.
- Mem0 Platform replacing native HX-13 OSS -> `REJECT_FOR_HX_RUNTIME` unless owner changes placement/runtime policy.
- Hosted `mcp.mem0.ai` as the assigned HX-13 MCP -> `OWNER_DECISION_REQUIRED`; do not assume it is the companion implementation.
- archived `mem0ai/mem0-mcp` -> `REFERENCE_ONLY`; do not select an archived project by default.
- portable coding-assistant `mem0-agent-plugin` -> `REFERENCE_ONLY` for agent workstation/editor use, not proof of HX-13 MCP design.
- Qdrant on HX-10 and approved HX Ollama providers -> normally `ACCEPT` when current dependency/evidence gates are met.
- changing Qdrant collection ownership, embedding model/dimensions, permanent model routing, firewall/TLS/access policy, service exposure, or storage layout -> `OWNER_DECISION_REQUIRED` unless already pinned.

## HX-13 architecture boundary

Current placement:

```text
HX-13 / 192.168.50.213
└── Mem0 OSS + assigned MCP capability
    ├── vector dependency: HX-10 Qdrant when selected/approved
    ├── embedding dependency: approved HX Ollama embedding endpoint
    └── LLM dependency: approved HX local model endpoint
```

Use native Linux. Long-running services use systemd where applicable. Do not containerize Mem0 or its dependencies.

Do not treat a Python SDK import as proof of a complete service/runtime design. The current HX-13 runbook and server record do not yet exist; package source, environment layout, service/API shape, listening endpoint, persistence/config path, and exact MCP implementation remain implementation-time owner/runbook decisions.

## Memory correctness rules

- Preserve explicit memory scope (`user_id`, `agent_id`, `app_id`, `run_id`, or approved filters) and never collapse identities implicitly.
- Keep synthetic validation identities and collections isolated from production data.
- Keep vector dimensions aligned with the accepted embedding model and Qdrant collection.
- Never mix embedding model identities in one Qdrant collection.
- Distinguish memory extraction/inference behavior from deterministic storage/retrieval verification.
- Do not make Mem0 the source of truth for data owned by PostgreSQL or another authoritative system without an explicit architecture decision.
- Treat permanent memory retention, deletion, consolidation, graph memory, and cross-agent sharing as data-lifecycle decisions, not tutorial defaults.

## Developer-workflow boundary

The official Mem0 skills are also designed for Claude Code, Codex, Cursor, OpenCode, OpenClaw, and related coding assistants. That capability is separate from the HX-13 runtime role.

Do not install a Mem0 coding-assistant plugin across the HX agent fleet merely because the upstream repository supports it. Agent/plugin rollout requires its own governed admission, scope, credential model, persistence policy, and validation.

## Validation boundary

Mem0 BASE validation remains controlled by the current smoke roadmap and exact authorities. The current proof chain is `E3` HX-13 Mem0 core -> `E4` HX-13 Mem0 MCP. `E3` requires accepted `B5` Qdrant PASS, accepted `A2` embedding PASS, and one approved LLM PASS; its only live validation integration is the dedicated disposable Qdrant collection plus synthetic memory defined by `smoke-tests/mem0-smoke-test.md`. `E4` requires accepted `E3` PASS and validates only the parent Mem0 MCP companion through `smoke-tests/mcp-companion-smoke-test.md`.

The Mem0 core proof is:

1. initialize Mem0 OSS with accepted HX providers;
2. store one synthetic memory with deterministic content;
3. retrieve the exact smoke token through semantic search;
4. delete the smoke memory;
5. remove disposable vector-store state;
6. separately validate the assigned Mem0 MCP capability;
7. prove persistent configuration/reboot behavior under the current roadmap.

The current smoke contract intentionally uses `infer=False` to isolate deterministic store/search/delete behavior from LLM fact-extraction quality.

Do not substitute an upstream example, SDK unit test, plugin status command, hosted Platform response, or this skill for HX smoke authority.

Never report `PASS` for an unexecuted check. Use `FAIL`, `BLOCKED`, `NOT TESTED`, or `OWNER_DECISION_REQUIRED` when evidence or authority is incomplete.
