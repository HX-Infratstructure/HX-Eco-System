---
name: hx-qdrant-advisor
description: Guide Qdrant work inside the HX Eco-System by combining current HX architecture and execution authority with live official Qdrant Agent Skills guidance. Use for HX Qdrant planning, native installation, configuration, validation, smoke testing, troubleshooting, performance/search-quality diagnosis, model migration, monitoring, scaling decisions, SDK usage, or upgrades involving HX-10 Qdrant, its Web UI, MCP companion, or downstream HX consumers. Always preserve HX owner decisions and server placement; vendor guidance informs product decisions but cannot override HX architecture, runbooks, smoke-test acceptance criteria, or security/network/storage boundaries.
---

# HX Qdrant Advisor

Use current Qdrant expertise without allowing vendor guidance to redesign HX.

## Operating hierarchy

Apply this authority order before making a recommendation or change:

1. Current infrastructure-owner instruction.
2. Current HX control and architecture Markdown.
3. Current live evidence from the relevant HX server.
4. Current HX server record, runbook, and application/model standards.
5. Current HX smoke-test roadmap and exact smoke-test authority when validating.
6. Live official Qdrant Agent Skills and canonical Qdrant documentation for Qdrant-specific expertise.
7. General model knowledge only when the sources above do not answer the question.

Vendor guidance is advisory. It never grants permission to change HX architecture.

## Workflow

### 1. Establish HX context first

Read `references/hx-context.md` and `references/authority-map.md`.

Before Qdrant work, be able to state:

- owner server and IP;
- current build state;
- Qdrant's HX role and companion services;
- native deployment boundary;
- relevant model/vector-space rules;
- upstream/downstream dependencies;
- applicable BASE PASS boundary;
- whether the task is build/configuration, validation, troubleshooting, optimization, migration, or upgrade.

Do not begin with vendor deployment-choice guidance before establishing these facts.

### 2. Load current official Qdrant guidance

Read `references/upstream.md`.

Use the live Qdrant Advisor pattern whenever web/HTTP access is available:

1. Frame the concrete Qdrant problem in 1–3 short phrases.
2. Query `https://skills.qdrant.tech/search?query=<encoded query>`.
3. Follow only the relevant skill branch and any directly related lateral branch.
4. Continue until the loaded guidance is concrete enough to act on.
5. Follow canonical Qdrant documentation links from the skill when implementation detail is required.

Do not load the entire Qdrant skill hierarchy when one branch is sufficient.

If live vendor-skill access is unavailable, use the official `qdrant/skills` repository as fallback context and explicitly state that the guidance may not be as current as a live Advisor fetch.

### 3. Reconcile vendor advice with HX

Classify each material recommendation as one of:

- `ACCEPT` — compatible with current HX authority.
- `ADAPT` — Qdrant principle is useful but implementation must be changed to fit HX.
- `REJECT_FOR_HX` — conflicts with an explicit HX decision/boundary.
- `OWNER_DECISION_REQUIRED` — would change HX architecture or an unresolved implementation choice.

Typical examples:

- Docker/Podman/Kubernetes deployment -> `REJECT_FOR_HX` unless owner explicitly changes the native/systemd standard.
- Qdrant Cloud/embedded as replacement for HX-10 -> `REJECT_FOR_HX` unless owner explicitly changes server placement.
- Qdrant collection/index/search-quality guidance -> normally `ACCEPT` or `ADAPT` after checking HX model rules.
- Horizontal cluster expansion -> `OWNER_DECISION_REQUIRED`; BASE build currently targets the assigned HX-10 service, not an unapproved cluster.
- Firewall/TLS/DNS/routing redesign -> `OWNER_DECISION_REQUIRED`.

Never silently convert vendor defaults into HX architecture.

### 4. Execute from HX authority

For installation/configuration work, use the current HX-10 runbook and current owner decisions as execution authority.

Use live Qdrant guidance to improve choices inside that boundary, such as:

- configuration parameters;
- storage/index behavior;
- API/SDK usage;
- monitoring checks;
- search-quality diagnosis;
- version-specific upgrade precautions.

If the current HX runbook is incomplete or contradicts current verified Qdrant requirements, stop treating the runbook as sufficient. Report the contradiction and update the HX authority in a separate reviewed change before execution.

Do not create a parallel installation procedure inside this skill.

### 5. Validate through the HX smoke model

When validating Qdrant BASE PASS, follow the smoke-test roadmap and the exact current test authorities. Qdrant validation is intentionally layered:

1. Qdrant core vector lifecycle.
2. Qdrant native Web UI live-state proof.
3. Qdrant MCP companion discovery + safe known-answer tool call.
4. Cleanup and cleanup verification.
5. Reboot persistence and retained evidence.

After CentCom activation, execute remotely from HX-5 wherever the product surface permits it.

Do not replace the HX smoke-test acceptance criteria with a vendor quickstart or health check.

### 6. Preserve vector-space integrity

HX-4 owns shared retrieval inference.

- BGE-M3 is the primary/default embedding model at 1024 dimensions.
- Nomic Embed Text v1.5 is an alternate/benchmark model at its accepted dimension.
- Never mix vectors from different embedding model identities in one Qdrant collection.
- A model change requires a new collection and complete re-embedding.

Qdrant named-vector capability does not override this HX policy unless the owner explicitly changes the policy.

### 7. Keep base validation narrow

During base stand-up:

- use synthetic/disposable data only;
- avoid production corpus ingestion;
- do not create permanent cross-service routes merely for validation;
- do not create a second Qdrant instance for testing;
- remove smoke collections and other validation-only state after evidence capture;
- treat LightRAG/Mem0 connections as downstream tests, not Qdrant core BASE requirements.

### 8. Produce an auditable recommendation

For material Qdrant decisions, summarize:

```text
HX CONTEXT
  server / role / state / applicable authority

QDRANT GUIDANCE CONSULTED
  live skill branch(es) / canonical docs

RECONCILIATION
  ACCEPT / ADAPT / REJECT_FOR_HX / OWNER_DECISION_REQUIRED

EXECUTION AUTHORITY
  exact HX runbook/standard to follow

VALIDATION AUTHORITY
  exact HX smoke-test file(s), if applicable

STOP CONDITIONS
  any unresolved owner decision, stale prerequisite, or unsafe cleanup boundary
```

Keep the answer concise unless deeper analysis is requested.

## Stop conditions

Stop and report rather than improvising when:

- vendor guidance requires changing HX server placement or deployment architecture;
- a recommendation requires Docker, Cloud, embedded Qdrant, clustering, TLS/firewall/DNS/routing changes, or storage redesign not already approved;
- current live Qdrant behavior contradicts the active HX runbook or smoke authority;
- an embedding model/dimension decision would violate HX collection integrity rules;
- cleanup could affect non-smoke collections or production data;
- required credentials are unavailable;
- a version-specific change cannot be verified against current official Qdrant guidance.

## References

- `references/hx-context.md` — HX-10 role, ecosystem boundaries, and model rules.
- `references/authority-map.md` — exact HX repository authorities and validation sequence.
- `references/upstream.md` — official Qdrant skills provenance and live Advisor usage.
