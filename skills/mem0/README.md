# HX Mem0 Skill

Mem0 on HX-13 uses the governed HX wrapper:

```text
skills/mem0/hx-mem0-advisor/
```

## HX placement

```text
HX-13 — 192.168.50.213
Mem0 OSS + assigned MCP capability
State: NOT STARTED
Deployment: native Ubuntu Linux; systemd for long-running services where applicable
```

## Source model

Mem0 publishes an official skills graph inside `mem0ai/mem0`. The HX wrapper uses a layered source model:

1. **HX architecture, roadmap, future HX-13 runbook/server record, and smoke authorities** for placement, execution, dependencies, and acceptance.
2. **Official Mem0 documentation and `mem0ai/mem0` source** as primary product/API authority.
3. **Official Mem0 agent skills** as vendor-authored developer expertise, curated through HX boundaries.
4. **Coding-assistant plugins/MCP integrations** as separate capabilities requiring their own HX admission when relevant.

Reviewed upstream main:

```text
02f7a9b2c4fe38dedb96631e48c85c74ad58b605
```

The reviewed official catalog contains six skills: three reference skills (`mem0`, `mem0-cli`, `mem0-vercel-ai-sdk`) and three pipeline skills (`mem0-integrate`, `mem0-test-integration`, `mem0-oss-to-platform`).

## HX disposition

- `mem0` -> **ADAPT**: use the OSS/self-hosted guidance for HX-13.
- `mem0-cli` -> **REFERENCE_ONLY** for HX-13 BASE unless a runbook selects it.
- `mem0-vercel-ai-sdk` -> **REFERENCE_ONLY**.
- `mem0-integrate` -> **REFERENCE_ONLY** for HX infrastructure; use only on an explicitly authorized target application repository.
- `mem0-test-integration` -> **REFERENCE_ONLY**; it does not replace HX smoke validation.
- `mem0-oss-to-platform` -> **REJECT_FOR_HX_RUNTIME** unless the owner explicitly changes HX-13 from native/self-hosted OSS to hosted Platform.

## MCP and coding-assistant boundary

The official portable `integrations/mem0-agent-plugin` is a coding-assistant plugin (reviewed version 0.3.1) and includes a stdio MCP server. The official hosted MCP endpoint is Platform-oriented. The old standalone `mem0ai/mem0-mcp` repository is archived.

None of those facts automatically selects the **assigned HX-13 Mem0 MCP implementation**. That remains an owner/runbook decision.

## Canonical files

```text
skills/mem0/
├── README.md
├── upstream/
│   └── SOURCE.md
└── hx-mem0-advisor/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── authority-map.md
        ├── hx-context.md
        ├── upstream.md
        └── mem0-agent-skills.md
```

## Important boundary

Skill approval does not advance HX-13 build state and does not select the package version, environment layout, service/API shape, config/data paths, permanent Qdrant collection, model bindings, network/access pattern, memory-retention policy, graph-memory design, or assigned MCP implementation.

Validation remains controlled by `smoke-tests/mem0-smoke-test.md`, the companion MCP smoke test, cleanup, reboot/persistence evidence, and current HX closure rules.
