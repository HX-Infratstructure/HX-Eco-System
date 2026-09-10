# Redis Authority Map for HX

Use the current repository version of each path.

## Ecosystem and state authority

1. `README.md`
2. `docs/00-control/CURRENT-STATE.md`
3. `docs/00-control/BUILD-STATE.md`
4. `docs/00-control/DECISIONS.md`
5. `docs/01-architecture/ARCHITECTURE-ORIENTATION.md`
6. `docs/00-control/HX-ECO-SYSTEM-BASE-IMPLEMENTATION-PRIORITY.md`

## Redis execution authority

When created and current:

```text
docs/02-server-records/HX-9.md
docs/03-runbooks/HX-9/
```

A skill must not substitute for a missing HX-9 runbook or server record.

## Skills authority

```text
skills/README.md
skills/SKILL-GOVERNANCE.md
skills/SKILL-REGISTRY.md
skills/redis/README.md
skills/redis/hx-redis-advisor/SKILL.md
```

## Validation authority

```text
docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md
smoke-tests/redis-smoke-test.md
smoke-tests/mcp-companion-smoke-test.md
docs/04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md
docs/04-application-standards/HX-5-CENTCOM-SMOKE-RUNNER-TOOLSET-AND-BOOTSTRAP.md
```

Redis BASE closure requires the current roadmap/runbook gates, Redis known-answer proof, Redis MCP proof, cleanup, reboot persistence, evidence, and state/server-record updates.

## Precedence

```text
OWNER DECISION
  > CURRENT HX CONTROL / ARCHITECTURE
  > LIVE HX EVIDENCE
  > CURRENT HX RUNBOOK / SERVER RECORD
  > HX VALIDATION AUTHORITY
  > OFFICIAL REDIS PRODUCT GUIDANCE
  > REVIEWED OFFICIAL REDIS AGENT SKILLS
  > HISTORICAL REFERENCE
  > GENERAL MODEL KNOWLEDGE
```

If current official Redis behavior proves an HX runbook or smoke test technically invalid, stop. Correct the HX authority separately before continuing; do not rewrite acceptance criteria during execution.
