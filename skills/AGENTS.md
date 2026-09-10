# AGENTS.md — HX Skills Library

These instructions apply to `skills/` and to agents creating, reviewing, deploying, or using HX component skills.

## Required context

Before using a component skill:

1. read repository root `AGENTS.md` and `README.md`;
2. establish current HX state/architecture for the component;
3. read `skills/SKILL-GOVERNANCE.md`;
4. read `skills/SKILL-REGISTRY.md`;
5. read the component `skills/<component>/README.md`;
6. load the approved HX wrapper `SKILL.md`;
7. load only the wrapper references needed for the task.

Do not use `human-html/` or `archive/` as execution authority.

## Operating contract

- `skills/` is the canonical skill source. Agent-specific skill directories are derived deployments only.
- HX owner decisions and active repository architecture outrank all skill content.
- Load HX context before consulting vendor/community guidance.
- Prefer vendor-official skills over community skills when both cover the same product problem.
- Do not invent an upstream skill source. Keep the component in `DISCOVERY` until a real source is found and reviewed.
- Do not copy an entire fast-changing vendor skill tree into HX when a live/meta-skill model provides fresher contextual loading.
- Skills may guide installation/configuration/testing, but approved HX runbooks/execution artifacts remain the place for infrastructure-changing commands.
- HX smoke-test files remain the acceptance authority. A skill may identify a defect in a test, but it cannot rewrite criteria during the same run.
- Never place passwords, PATs, API keys, bearer tokens, private keys, service-account secrets, or sshpass passwords in skill content.
- Do not let a skill introduce Docker/Cloud/embedded deployment, cluster topology, firewall/TLS/DNS/routing changes, storage redesign, or model-placement changes without owner approval.

## Adding a component skill

1. identify the exact HX component/host/scope;
2. inspect the real upstream source and classify it;
3. record upstream provenance/version/commit;
4. create an HX wrapper when vendor assumptions can conflict with HX;
5. keep detailed HX context in `references/`, not an oversized `SKILL.md`;
6. add the source/component to `SKILL-REGISTRY.md`;
7. validate and package the wrapper using the current skill-creation tooling;
8. mark `APPROVED` only after validation succeeds for the stated scope;
9. deploy to Claude/Codex/OpenCode only from this canonical source when that deployment mechanism is defined.

## Wrapper response pattern

For material decisions, prefer:

```text
HX CONTEXT
VENDOR GUIDANCE CONSULTED
RECONCILIATION: ACCEPT | ADAPT | REJECT_FOR_HX | OWNER_DECISION_REQUIRED
EXECUTION AUTHORITY
VALIDATION AUTHORITY
STOP CONDITIONS
```

## Qdrant reference implementation

`skills/qdrant/hx-qdrant-advisor/` is the first approved wrapper and establishes the pattern for future component skills.
