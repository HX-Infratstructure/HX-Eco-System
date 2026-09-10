# Mem0 Authority Map for HX

Use the current repository version of each path.

## Ecosystem and state authority

1. `README.md`
2. `AGENTS.md`
3. `docs/00-control/CURRENT-STATE.md`
4. `docs/00-control/BUILD-STATE.md`
5. `docs/00-control/DECISIONS.md`
6. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`
7. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`

## Mem0 execution authority

When created and current:

```text
docs/02-server-records/HX-13.md
docs/03-runbooks/HX-13/
```

At the 2026-09-09 review point neither active authority exists. A skill must not substitute for them.

## Skills authority

```text
skills/README.md
skills/AGENTS.md
skills/SKILL-GOVERNANCE.md
skills/SKILL-REGISTRY.md
skills/mem0/README.md
skills/mem0/hx-mem0-advisor/SKILL.md
```

Skills provide expertise. They do not own infrastructure-changing commands or acceptance criteria.

## Validation authority

```text
docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md
docs/01-architecture/HX-SMOKE-TESTING-OPERATING-MODEL.md
smoke-tests/mem0-smoke-test.md
smoke-tests/mcp-companion-smoke-test.md
docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md
docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md
tools/hx-smoke-runner/AGENTS.md when CentCom is used
```

Current smoke-roadmap position:

```text
E3  HX-13 Mem0 core
    requires: B5 Qdrant PASS + A2 accepted embedding PASS + one approved LLM PASS
    live coupling: dedicated disposable Qdrant collection + synthetic memory only

E4  HX-13 Mem0 MCP
    requires: accepted E3 Mem0 PASS
    live coupling: parent Mem0 service only
```

Mem0 BASE closure requires current roadmap/runbook gates, deterministic memory lifecycle proof, assigned MCP proof, cleanup, reboot/persistence evidence, and state/server-record updates.

## External authority

```text
Official project: mem0ai/mem0
Official docs: https://docs.mem0.ai/
Official skill catalog: mem0ai/mem0/skills/
Official skill guidance: subordinate to HX architecture/execution/validation authority
```

## Precedence

```text
OWNER DECISION
  > CURRENT HX CONTROL / ARCHITECTURE
  > LIVE HX EVIDENCE
  > CURRENT HX RUNBOOK / SERVER RECORD
  > HX VALIDATION AUTHORITY
  > OFFICIAL MEM0 PRODUCT / SOURCE GUIDANCE
  > REVIEWED OFFICIAL MEM0 AGENT SKILLS
  > HISTORICAL REFERENCE
  > GENERAL MODEL KNOWLEDGE
```

If current official Mem0 behavior proves an HX runbook or smoke test technically invalid, stop. Correct the HX authority separately before continuing the run; do not silently rewrite acceptance criteria during execution.
