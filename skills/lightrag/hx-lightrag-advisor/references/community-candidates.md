# Community LightRAG Skill and MCP Candidates

These sources are useful references but are **not vendor-official LightRAG authority** and are not automatically approved operational dependencies.

## Claude query skill

```text
Repository: zwovadis/lightrag-claude-skill
Reviewed main commit: 4711ced79bbc8b450b5aae444a5984905bdfbf48
Reviewed date: 2026-09-09
Classification: COMMUNITY
Scope: Claude Code skill for LightRAG REST query endpoints
HX status: REFERENCE_ONLY
```

Useful ideas:

- `/query`, `/query/stream`, and `/query/data` usage;
- query-mode guidance;
- API-key/client examples.

Restrictions:

- assumptions such as `localhost` must be adapted to HX-11 direct LAN access;
- do not treat this query-only client skill as an install/configuration authority;
- verify endpoint/auth behavior against current `HKUDS/LightRAG` before use.

## Claude persistent-memory skill set

```text
Repository: butchokoy25/lightrag-claude-skills
Reviewed main commit: b71a1901a13698baf6c466aeab664eed4a532531
Reviewed date: 2026-09-09
Classification: COMMUNITY
Scope: seven Claude skills + two session hooks + helpers/MCP config for persistent memory
HX status: REFERENCE_ONLY / LATER_INTEGRATION
```

This project adds Node.js helpers, Claude `SessionStart`/`Stop` hooks, memory synchronization, and MCP configuration. Those behaviors are broader agent-memory/integration architecture and are **not part of the HX-11 base build**.

Do not install those hooks or merge their MCP configuration as part of LightRAG BASE stand-up.

## Community MCP candidates

Multiple third-party LightRAG MCP repositories exist. One reviewed example:

```text
Repository: desimpkins/daniel-lightrag-mcp
Reviewed main commit: 9fc0aedd422a66b37c81fed5252c8311dbcc320c
Last commit observed: 2025-08-22
Classification: COMMUNITY
HX status: DISCOVERY / REFERENCE_ONLY
```

The HX architecture assigns an MCP companion to LightRAG, but the exact implementation must be reviewed and selected separately. A marketplace listing or `pip install` instruction is not sufficient approval.

## Admission rule

Before any community LightRAG skill, hook, helper, or MCP becomes operational in HX:

1. review current source and maintainer activity;
2. inspect scripts/hooks/config mutations;
3. identify credentials and network assumptions;
4. reconcile against HX server ownership and native deployment;
5. define bounded HX scope;
6. validate/package under `skills/SKILL-GOVERNANCE.md` when it is a skill;
7. validate MCP behavior under the HX MCP companion smoke authority when it is an MCP implementation.
