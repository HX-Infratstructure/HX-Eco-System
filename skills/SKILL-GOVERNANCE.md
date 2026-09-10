---
document: HX Eco-System Skill Governance
status: current
version: 1.0
date: 2026-09-09
authority: HX-Eco-System clean rebuild
---

# HX Eco-System — Skill Governance

## 1. Governing principle

Skills augment HX expertise; they do not define HX architecture.

```text
OWNER DECISION
    > CURRENT HX CONTROL / ARCHITECTURE
    > LIVE HX EVIDENCE
    > CURRENT HX RUNBOOK / STANDARD
    > GOVERNED HX SKILL + CURRENT OFFICIAL VENDOR GUIDANCE
    > HISTORICAL REFERENCE
    > GENERAL MODEL KNOWLEDGE
```

If current official vendor guidance exposes a real incompatibility in an HX runbook, report the contradiction and update the smallest affected HX authority through normal review. Do not silently override the HX architecture from inside a skill.

## 2. Canonical location

The canonical HX skill library is:

```text
skills/
```

Agent-specific skill locations are derived deployments only. Do not create independently maintained Claude-, Codex-, OpenCode-, or other agent-specific source trees.

When deployment automation is introduced later, it must deploy from this canonical directory or from a reviewed package built from it.

## 3. Skill classifications

### HX_NATIVE
Authored for HX and governed entirely by HX.

### VENDOR_OFFICIAL
Published by the software vendor/project. This is the preferred external source class for product expertise.

### COMMUNITY
Published by a third party. Community skills require explicit review of provenance, scope, behavior, links/scripts, and architecture assumptions before they can move beyond `DISCOVERY` or `PILOT`.

### WRAPPER
HX-authored skill that loads HX context first, then invokes or consults an external skill/source. Wrappers are the preferred pattern for vendor skills that may otherwise recommend architecture choices outside HX policy.

### META
Skill that routes to or dynamically loads narrower skills. A vendor meta-skill is useful when the upstream knowledge base changes frequently.

## 4. Registry status

Use only these registry lifecycle states:

- `DISCOVERY` — source identified; not approved for operational use.
- `PILOT` — reviewed enough for bounded evaluation.
- `APPROVED` — validated for the stated HX scope.
- `BLOCKED` — known conflict/risk prevents use.
- `RETIRED` — no longer active; retain provenance/history as required.

Two further states apply to sources HX consults but never installs as a second
authority. They are registry states, not admission grades:

- `APPROVED_AS_REFERENCE` — reviewed and approved to be consulted as expert
  reference. It is not an HX authority and is not installed or deployed.
- `REFERENCE_ONLY` — retained for context or future evaluation. It has not been
  approved for operational use. Add `/ LATER_INTEGRATION` when the source is
  expected to be re-evaluated for a later programme phase.

Approval is scoped. A skill approved for troubleshooting is not automatically approved to execute infrastructure changes.

## 5. Admission checklist

Before a new external skill becomes `APPROVED`, record:

1. component and HX host/role;
2. source organization/project;
3. source URL/repository;
4. vendor/community classification;
5. exact reviewed version/commit when available;
6. live-update behavior, if any;
7. intended triggers and use cases;
8. associated runbook/standard;
9. associated smoke-test authority;
10. associated MCP/plugin/hook when relevant;
11. known conflicts with HX architecture;
12. whether an HX wrapper is required;
13. validation result for the HX wrapper/package.

## 6. Vendor-content policy

Prefer current official vendor skills for product-specific reasoning when available.

For fast-changing vendor skill systems:

- prefer live/contextual retrieval over vendoring the full tree;
- record the reviewed upstream commit/source for provenance;
- keep the HX wrapper stable and local;
- fetch only the branch relevant to the current task;
- cite or record canonical vendor documentation used for material decisions.

Vendor skill content is not copied wholesale into HX unless offline/availability requirements justify it and the owner approves that maintenance burden.

## 7. HX-wrapper rule

A wrapper must:

1. identify the component's HX host/role and current architecture boundary;
2. load HX authority before vendor advice;
3. explain how to access current vendor skill guidance;
4. distinguish accepted, adapted, rejected, and owner-decision-required recommendations;
5. point to HX execution/runbook authority;
6. point to HX smoke-test authority;
7. define explicit stop conditions;
8. avoid embedding credentials or secrets;
9. avoid copying general-purpose deployment code that bypasses HX runbooks;
10. remain concise enough for progressive loading.

## 8. Architecture conflict rule

External skills cannot authorize:

- moving a workload to another HX server;
- introducing Docker, Podman, Kubernetes, or another container platform;
- replacing local/native deployment with vendor Cloud/embedded deployment;
- changing gateway, DNS, AD/domain, NTP, routing, or network topology;
- adding firewall/TLS/access restrictions without owner approval;
- repartitioning/mounting/reusing disks outside current authority;
- changing shared model placement;
- changing permanent cross-service integration;
- modifying smoke-test PASS criteria during a run.

When vendor guidance recommends one of these, classify it as `OWNER_DECISION_REQUIRED` or `REJECT_FOR_HX` according to current owner decisions.

## 9. Execution-artifact rule

Skills may contain deterministic helper scripts when they materially improve repeatability, but infrastructure-changing code must not become hidden execution authority inside a skill.

For HX component builds:

- runbooks and approved execution artifacts remain under the current repository runbook/standards structure;
- skills tell agents what to consider, what to check, and which authority to execute;
- vendor-provided scripts are reviewed before use;
- no vendor installer is run merely because a skill suggests it.

## 10. Validation rule

Skills can assist with validation reasoning, but HX smoke-test authorities remain decisive.

A vendor quickstart, health endpoint, or vendor skill does not replace:

- `HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`;
- the exact file under `smoke-tests/`;
- CentCom cleanup/evidence rules;
- reboot persistence;
- server-record/BUILD-STATE closure.

If a vendor skill reveals that an HX smoke test is technically invalid for the current version, stop the run, correct the authority separately, and use a new run ID.

## 11. Secrets and credentials

Skills must never contain actual:

- passwords;
- PATs;
- API keys;
- bearer tokens;
- private keys;
- service-account secrets;
- `sshpass` passwords.

Skills may document credential **names**, environment-variable identifiers, secret-store names, and the required access pattern.

Credential handoff to Claude/agents will be handled through a separate owner-approved cornerstone completion/handoff process. Do not use the skill library as a secret store.

## 12. Packaging and quality gate

A new HX wrapper skill must:

- have valid `SKILL.md` frontmatter;
- keep the skill name lowercase and hyphenated;
- include required agent metadata where used by the HX skill packaging workflow;
- remove template/example files not needed by the skill;
- pass the current skill validator;
- package successfully before being marked `APPROVED`;
- remain below the platform package-size limit.

If scripts are included, execute representative validation before approval.

## 13. Update rule

When an HX skill changes:

1. update the canonical source under `skills/`;
2. update the registry if scope/status/upstream provenance changed;
3. validate/package the skill again;
4. update agent deployment copies only from the canonical version;
5. archive superseded governance/registry documents when replaced under normal repository document control.

For live vendor meta-skills, a new upstream commit does not require copying new vendor content into HX. Re-review when upstream behavior, trust, or the HX-relevant guidance materially changes.

## 14. Retirement rule

Retire a skill when:

- the component leaves the HX architecture;
- the upstream source is abandoned/untrusted;
- a better authoritative skill supersedes it;
- the wrapper no longer matches HX architecture;
- the skill creates unacceptable ambiguity or duplicate authority.

Mark it `RETIRED` in the registry before removing active deployment copies.
