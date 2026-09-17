---
document: HX Eco-System Owner-Approved Decisions
status: current
date: 2026-09-09
---

# HX Eco-System — Owner-Approved Decisions

## D-001 — Clean-room rebuild
HX-1 clean Samba foundation is retained. HX-2 through HX-17 are rebuilt from scratch. Old HX-Infrastructure configuration and closure claims are reference-only.

## D-002 — Native deployment
Native Linux + systemd. No Docker, Podman, or Kubernetes unless explicitly changed by the owner.

## D-003 — Application companion services
Product-specific MCP servers and native Web UIs are part of the parent application's base build where applicable.

## D-004 — NGINX
HX-7 NGINX is limited to dev/test application rendering. It is not the common reverse proxy for HX ecosystem services.

## D-005 — Embedding/reranking placement
HX-4 Meta-X hosts BGE-M3 as primary/default embedding model, Nomic Embed Text v1.5 as alternate benchmark/fallback, and a BGE-family reranker. Never mix embedding-model vector spaces in one Qdrant collection.

## D-006 — Granite-Docling placement
Granite-Docling 258M stays with Docling on HX-16. Base validation is CPU-first. GPU acceleration is considered only if measured need later justifies it.

## D-007 — HX-5 headroom
Even if HX-5 is upgraded to 2 x 16 GB GPUs, shared embedding/reranking remains on HX-4. HX-5 headroom is reserved for CentCom, Ornith, DeepSeek Harness, and dev/test work.

## D-008 — Open WebUI base functional test
HX-8 Open WebUI BASE PASS includes a temporary direct connection to one already-proven Ollama endpoint, one prompt, one model response in the UI, evidence capture, and cleanup/removal of the temporary connection.

## D-009 — OmniRoute base functional test
HX-6 OmniRoute BASE PASS includes one temporary route to one already-proven Ollama endpoint, direct-versus-routed known-answer validation, evidence capture, and cleanup/removal of the temporary test route.

## D-010 — OmniRoute provider/model catalog
OmniRoute maintains an explicit approved-provider allowlist and an explicit approved-model allowlist. Discovery/support does not equal approval. Approving a provider does not approve its entire model catalog.

## D-011 — Active document rule
Only the latest version of a document remains active. Superseded versions go under `archive/`. Active Markdown is agent authority; HTML is a human mirror.

## D-012 — DeepSeek Harness meta-agent role
DeepSeek Harness on HX-5 is the HX meta-agent/orchestration layer for AI-agent and AI-solution construction. Worker agents invoked beneath the Harness are sub-agents that receive bounded application-building work packages. Harness BASE PASS requires more than runtime health: it must complete a bounded multi-agent solution-building smoke test that proves task decomposition, sub-agent delegation, artifact handoff, creation of a runnable AI application, independent validation, and Harness-level synthesis of the final PASS/FAIL result. Detailed authority: `HX-ECO-SYSTEM-DEEPSEEK-HARNESS-IMPLEMENTATION-ADDENDUM.md`.

## D-013 — Deep Agents LOB agent factory role
Deep Agents by LangChain on HX-12 is the HX line-of-business agent factory/application-agent harness. It is complementary to, not a replacement for, the HX-5 DeepSeek Harness meta-agent. Deep Agents BASE PASS requires an explicit tool-calling-capable HX model plus a bounded LOB Agent Factory smoke test that proves real filesystem artifact creation, creation/configuration of domain sub-agents, actual `task` delegation, business-rule/tool use, correct execution of a generated LOB agent package, short-lived thread continuity, independent validation, evidence capture, and reboot persistence. A package import or plain LLM response is not sufficient. Detailed authority: `HX-ECO-SYSTEM-DEEP-AGENTS-IMPLEMENTATION-ADDENDUM.md`.

## D-014 — HX-5 CentCom smoke-test runner role
After HX-5 closes its own base inference foundation, CentCom becomes the standard remote execution station for subsequent HX component smoke tests. Disposable test projects, runner/client tooling, synthetic fixtures, manifests, logs, and cleanup verification live on HX-5 rather than on the application host. The system under test keeps only its installed application, approved configuration, and explicitly smoke-namespaced temporary data required by the test. Remote API/protocol/client execution is preferred; approved SSH is used only when the component's primary contract genuinely requires local execution. Cleanup and cleanup verification are mandatory parts of PASS. DeepSeek Harness is not a prerequisite for enabling the CentCom smoke-runner role. Detailed authority: `../04-application-standards/HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`.

**Amended 2026-09-17 — authorised substitute runner.** CentCom remains the
preferred and standard fleet proof station whenever it is available. It is not
the only station a proof may run from. An authorised substitute may be used
when CentCom is unavailable or not yet established, provided it is:

- off the system under test;
- on the HX LAN;
- able to reach the target service;
- running the approved HX proof tooling from `tools/hx-smoke-runner/`;
- recording `runner_host` in the evidence manifest;
- equipped with Playwright headless Chromium when the component's smoke-test
  authority requires UI proof.

The operator workstation, including its WSL environment, is a valid substitute
when those conditions are met. The existing `HX_SMOKE_ALLOW_HOST` export is how
a station is authorised; no second mechanism is introduced, and no server is
special-cased.

**Why this is an amendment and not a withdrawal.** HX7-F02 established that
eight proof steps carried `requires A5` while needing only a runner that is not
the system under test. That is an artificial dependency, not a technical one:
the tooling stopped depending on a CentCom-only shell some time ago, and the
station actually used is already recorded per run. CentCom keeps its role as
the standard station and gains nothing and loses nothing here.

## D-015 — Ecosystem architecture is the cornerstone
The HX ecosystem architecture and current configuration context must be understood before validation is designed or executed. Validation sits on top of the ecosystem; it does not define the ecosystem. Agents must establish server ownership, target IP, current state, foundational network/domain/deployment rules, model/data placement, dependency boundaries, and BASE PASS expectations before selecting or running a smoke test. `../01-architecture/ARCHITECTURE-ORIENTATION.md` is the foundational orientation authority; smoke-test documents must inherit rather than redefine that architecture.

## D-016 — Ordered smoke-test proof roadmap
HX maintains a separate evergreen smoke-test roadmap in addition to the base implementation roadmap. The implementation roadmap defines deployment/build order; `HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md` defines proof order, required prior PASS evidence, companion gates, and the minimum temporary integrations permitted during validation. Downstream smoke tests must reference current prior PASS evidence when they rely on earlier capabilities. HX favors cumulative proof with minimal live coupling: do not force unnecessary cross-service integration merely to make tests sequential. Temporary smoke-test dependencies do not automatically become permanent production architecture.

## D-017 — Governed HX skills capability layer
HX maintains a canonical `skills/` library as an AI-agent expertise layer between ecosystem context and execution. Component skills may combine HX-native instructions with current vendor-official expertise, but skills do not supersede owner decisions, active HX architecture, live evidence, runbooks, or smoke-test acceptance criteria. Agent-specific skill installations are derived deployments from the canonical repository source, not independently maintained authorities. External skills are classified and registered before operational use; vendor-official sources are preferred over community sources. Skills never store actual credentials, PATs, API keys, private keys, service-account secrets, or sshpass passwords. Qdrant is the first approved reference implementation through `skills/qdrant/hx-qdrant-advisor/`, which preserves HX-10/native-systemd/vector-space/smoke-test rules while consuming the current official Qdrant Advisor guidance live.

## D-018 — Host firewall and inference listener posture — RATIFIED 2026-09-11

The HX LAN is treated as a trusted lab segment.

**No UFW is used anywhere on the fleet.** The common base runbook disables it on
every server, and that is the intended posture, not a gap. Ollama listens on
`0.0.0.0:11434` with no authentication, and that listener posture stands as
stated.

This is consistent with the standing rule that firewall, segmentation and TLS
changes are not imposed without owner approval, and with KISS.

Intended blast radius: on a built HX host, any host that can reach the HX LAN
can call its inference endpoint without credentials and reach the service ports
it exposes. That is accepted, and it is what the build scripts produce. It is a
statement of intent, not a survey: three of seventeen servers are built, and
each server record states the posture actually observed as that server closes.

Where these statements come from: they are read from
`docs/03-runbooks/common/01-base-admin-network-updates.sh`, which disables
`ufw`, and from `docs/03-runbooks/common/03-storage-ollama.sh`, which sets
`OLLAMA_HOST=0.0.0.0:11434`. They describe what the build scripts do. HX-1 to
HX-3 are the only servers built so far, so a server record states the observed
posture as each server closes; the decision itself does not wait on that.

This entry closes. Do not re-raise UFW or listener hardening as a finding
against this repository: it is a decided posture, not an open item.

## D-019 — OmniRoute product identity — RATIFIED 2026-09-10

HX-6 OmniRoute is `https://github.com/diegosouzapw/OmniRoute.git`, confirmed by
the infrastructure owner. MIT licence. The headless server installs from the
npm package `omniroute`, pinned in `docs/03-runbooks/common/hx-base.env`.

The project's GitHub release assets are desktop application builds, and its
documented container path is not used. HX installs from npm onto Node.js taken
from the official nodejs.org binary tarball.

D-010 applies in full and is the reason this server exists: the product
discovers hundreds of providers by default, and discovery is not approval.
Build the explicit provider allowlist and the explicit model allowlist before
HX-6 closes.

## D-020 — PostgreSQL install source — RATIFIED 2026-09-10

HX-9 PostgreSQL is built from the official source tarball at
`https://www.postgresql.org/ftp/source/v18.6/`, not from the PGDG repository.
The owner chose the source build so no application software on the fleet comes
from an apt repository.

`docs/03-runbooks/common/10-postgresql.sh` downloads
`postgresql-18.6.tar.bz2`, verifies it against the SHA-256 published beside it
and pinned in `hx-base.env`, builds with `./configure --prefix=/srv/postgresql`,
runs `initdb`, and installs the `hx-postgresql` unit.

Every application on the fleet now comes from PyPI, npm, a GitHub release, an
upstream source tarball, a direct binary, or Hugging Face. The Ubuntu archive
is used only for the NVIDIA driver and for build toolchains and library headers.

## D-021 — Snap is never a package source — RATIFIED 2026-09-11

Two rules in the repository disagreed. `.coderabbit.yaml` told the reviewer
"Snap is never permitted". `hx-base.env` and `tools/hx-doc/hx_version_pins.py`
said the Ubuntu archive and Snap were both acceptable for drivers.

The owner ratified the `.coderabbit.yaml` wording: **Snap is never permitted,
for anything, the NVIDIA driver included.**

The Ubuntu archive is unchanged by this. It stays available for the NVIDIA
driver, for build toolchains and for library headers, and nothing else, as
D-020 records.

`hx_version_pins.py` reports a Snap pin as REVIEW whatever it is for.
`tools/hx-doc/hx-gate-tests` holds five checks on that rule: a Snap
application is refused, a Snap driver is refused, the Ubuntu archive is allowed
for a driver, the Ubuntu archive is refused for an application, and PyPI is
accepted.

## D-022 — BGE reranker checkpoint and runtime — RATIFIED 2026-09-10

D-005 placed a BGE-family reranker on HX-4 without naming one. The owner
directed the exact checkpoint and runtime on 2026-09-10:

- `BAAI/bge-reranker-v2-m3` at revision
  `953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e`;
- served by `infinity-emb` 0.0.77 from PyPI, under systemd, on port 7997.

The revision is an immutable commit, so a later upstream edit cannot change the
model under a stable name. The authoritative pins are in
`docs/03-runbooks/common/hx-base.env`, and `tools/hx-doc/hx-version-pins`
checks them against upstream.

This was recorded in the Model Placement and Embedding Standard as item 10 two
days after that document was approved at v1.0, without a decision to point at.
The standard is v1.1 now and cites this entry.

## D-023 — a write-capable token in Actions secrets, for OpenWiki — SUPERSEDED BY D-025 on 2026-09-14

OpenWiki generates `openwiki/` from the code. PR #10 teaches the repository
that the tree is generated. This entry covers refreshing it on a schedule.

The owner directed this on 2026-09-11 after the cost and the exposure were put
in writing. It is recorded before the secrets exist, not after.

**What is accepted.** Two Actions secrets on a repository that is public:

- `OPENWIKI_PR_TOKEN` — a fine-grained personal access token or GitHub App
  token, scoped to this repository only, with **Contents: read and write** and
  **Pull requests: read and write**;
- `ANTHROPIC_API_KEY` — a model key. Every scheduled run is billable.

The repository being public does not expose either secret. It does mean that a
leak of `OPENWIKI_PR_TOKEN` gives write access to something the whole world can
already read. That is the accepted risk.

**Why the default token will not do.** A pull request opened with
`GITHUB_TOKEN` does not start `pull_request` workflows, so the checks in
`hx-checks.yml` would never run on generated documentation. The weak option is
also the broken one.

**The conditions, all of which `.github/workflows/openwiki-update.yml` meets.**

1. `add-paths` is `openwiki` and nothing else. The upstream example also lists
   `AGENTS.md`, `CLAUDE.md` and the workflow file itself. `AGENTS.md` is the
   contract every agent reads first, and no job in this repository may rewrite
   its own workflow.
2. Every action is pinned to a commit, and every package to a version,
   OpenWiki included. Upstream ships the install unpinned.
3. OpenWiki pull requests are **not** auto-merged. A human reads the generated
   documentation before it lands.
4. The job refuses to start when either secret is missing, instead of spending
   the model budget and failing at the last step.
5. Weekly, not daily. Fleet documentation does not change daily and every run
   is paid.
6. Telemetry is off and LangSmith tracing is removed. Nothing about this
   repository is sent to a third-party trace store.

**The residual risk, stated plainly.** `workflow_dispatch` runs the workflow
file from the ref the operator picks. A branch that edits that file can
therefore read both secrets, and no line inside the file can prevent it,
because the attacker would be editing that line too. The control is who holds
write access to this repository, plus branch protection on the default branch.
The checkout is pinned to the default branch so that generated documentation
always describes `main`; that is a correctness measure, not a security one, and
it is not recorded as one.

**Reversal.** Delete the workflow file and revoke both secrets. Running
`openwiki --update` by hand from inside Claude Code costs nothing, because the
host integration uses the session's model instead of a key. That stays the
fallback.
## D-024 — operational tooling is documented before it is adopted — RATIFIED WHEN PR #15 MERGES

The owner directed this on 2026-09-12, stating the requirement directly:
every operational tool gets its own directory covering what it is, why we
have it, and how and when to use it. That direction is context, not the
record. It was given in conversation, and a conversation is not an auditable
reference.

**The record is the merge.** This entry reaches `main` only when pull
request #15 is merged there, and GitHub keeps that event immutably: the
account that merges it, the merge commit and the time. Until then it is a
proposal on a branch and binds nothing. Once merged, that event is the only
approval claimed, and the account in GitHub's record is the approver of
record. To read it:

```bash
gh pr view 15 --repo HX-Infratstructure/HX-Eco-System --json mergedBy,mergeCommit,mergedAt
```

This repository has a single operator who merges their own pull requests, so
the merge is the approval and there is no separate review step. Like D-018 to
D-023, this entry names the role; the account is in GitHub's record rather
than repeated here.

An operational tool is something this repository depends on but does not
contain: OpenWiki, CodeRabbit, graft. Each gets one document under
`docs/06-tooling/` carrying five sections - what it is, why we have it, when
to use it, how to use it, and upstream links - before it is relied on.

**Why this is a decision and not a habit.** CodeRabbit was adopted with its
facts spread across `DECISIONS.md`, `RUN-SHEET.md` and `AGENTS.md`, and
nothing that said what it was or when to use it. OpenWiki was then adopted the
same way: a decision entry, a block in `AGENTS.md`, a workflow file, and no
document. The second occurrence is what makes it a pattern. A habit would fail
a third time silently.

`hx-doc-check` enforces what it can: a document present in `docs/06-tooling/`
carries all five sections, an index row naming a file has that file, and a
document nobody links to fails. Three gate tests break each of those on
purpose.

**The limit, stated rather than implied.** No check knows that a tool was
adopted. A row with no document is backlog: reported on every run, not failed,
so the gap stays visible instead of turning the build red forever. Adding the
row is this decision's obligation, carried by the person adopting the tool.

**The upstream-links section is not decoration.** Two capabilities upstream
documents and this repository was not using are verifiable here: before the
commit that carries this decision, neither `openwiki/INSTRUCTIONS.md` nor
`.openwikiignore` existed, so wiki coverage was unsteered and nothing in this
repository's configuration excluded `archive/`, `human-html/` or `graft/`.
Both files are documented upstream and neither was reachable from anything in
this repository.

Whether the first run actually read those trees is not established, and an
earlier draft of this entry said it had. The run's own record points the other
way: no evidence reference in `openwiki/.claims/` cites `archive/`,
`human-html/` or `graft/`, and none appears in `openwiki/.page-manifest.json`;
the evidence it did cite is all under `tools/`, `docs/`, `skills/` and
`.github/`. The ignore file is a guard for later runs, not the repair of a
demonstrated scan.

The owner's account of how that happened - adoption driven by the README and
the installed package while the product's own documentation went unread, with
the owner supplying the URL - is recorded as the owner's account, not as
measured evidence. The verifiable part is the absence of the two files.

**Tools already in use.** CodeRabbit and graft predate this decision and stay
in use: `AGENTS.md` section 13 requires a CodeRabbit review before every push,
and section 14 routes symbol lookups to graft. This decision does not suspend
either. It makes their documents owed. Until each exists, those two sections
are their operating instructions, and the index names them as backlog so the
debt is visible on every `hx-doc-check` run.

Backlog on ratification: CodeRabbit and graft are listed in the index with no
document. Each is its own pull request.

## D-025 — OpenWiki generation is manual, not scheduled — RATIFIED 2026-09-14

Replaces D-023.

D-023 authorised two Actions secrets so a weekly workflow could regenerate
`openwiki/` with a paid model run. That posture is withdrawn.

**What changes.** `.github/workflows/openwiki-update.yml` is deleted.
`OPENWIKI_PR_TOKEN` and `ANTHROPIC_API_KEY` were both created as repository
secrets and the workflow ran at least once: the scheduled run of 2026-09-13
passed its secrets preflight, spent model budget, and pushed branch
`openwiki/update` (commit 5b20167, produced with `claude-sonnet-5`), which is
open as PR #16. As of this entry, both secrets remain in repository settings;
revoking both is a required owner action, not a hypothetical. The token was
granted Contents: read and write and Pull requests: read and write, so it had
repository write access for as long as it existed; the preflight that proved
the secrets present is Actions run 34759222774 on the same date.

**How openwiki/ is generated now.** By hand, from a host-agent session, using
that session's model rather than an API key — the fallback D-023 already
recorded. Each run records the provider, model and commit it was produced
from in `openwiki/.last-update.json`, and that record is what makes a tree
auditable.

**Why.** Three problems close at once: the repository no longer needs to hold
a write-capable token; no scheduled job spends model budget unattended again;
and the
`workflow_dispatch` residual risk D-023 documented — a branch that edits the
workflow file can read both secrets, and no line inside the file can prevent
it — goes away with the file.

**What this costs.** Refresh becomes a matter of discipline rather than a
cron, and a generated tree nobody regenerates goes stale silently. Any
decision to make `openwiki/` required agent reading must therefore carry an
explicit freshness condition. That is a separate decision and is not granted
here.

**Provider.** No provider is pinned; the run records what produced it. The
tree of record as of this entry was generated by `z-ai/glm-5.2` at commit
0aa14e3.

**Reversal.** Restore the workflow file from `archive/`, recreate both
secrets, and re-ratify D-023's conditions.

## D-026 — host networking is validated, never written — RATIFIED 2026-09-16

The foundation block and the shared base block both check the host's address,
default route and DNS server against `docs/00-control/hx-fleet.tsv`. Neither
writes any of them. A mismatch stops the build with exit 11, 12 or 13.

**Why.** Correcting a host's networking is not an authority this process holds.
A block that silently rewrote `netplan` to match the inventory would make the
inventory true by force rather than by agreement, and would hide the fact that
somebody had provisioned the host differently from the record.

**What it means in practice.** When a foundation exit says the address is
wrong, the answer is to fix the host or fix the inventory, deliberately, and
then re-run. It is never to make the block write the value.

## D-027 — the fleet public key ships with the runbooks — RATIFIED 2026-09-16

`docs/03-runbooks/common/hx-fleet-key.pub` is committed. The foundation block
installs the fleet key from that file and refuses to continue when the file is
missing, or when what lands in `authorized_keys` does not carry the recorded
fingerprint `SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk`.

**Why.** A public key in the repository makes the install path reviewable: the
key a host will accept is visible in a diff before any host accepts it. Pasting
a key by hand during a build is the failure that left HX-2 and HX-3
unreachable by the fleet key, which the Layer 0/1 audit had to stop for.

**The private half never leaves the operator workstation** and is not in this
repository in any form.

## D-028 — the NVIDIA branch is held at the Block 2 pin — RATIFIED 2026-09-16

On a host that carries a GPU, the base block holds every installed package
matching the pinned driver branch before `apt upgrade` runs, so routine
patching cannot move the driver as a side effect.

**Why.** A driver move changes what a closed server record describes. It should
be an explicit decision with a re-proof, not something that arrives with a
security update.

**Scope.** The hold applies only where a driver is installed, which is the
hosts in `HX_GPU_HOSTS`. On a CPU-only host the filter matches nothing and the
block reports that there is nothing to hold, which is correct.

**Open.** The holds were released to move the fleet to `595.91.07` and have not
been reapplied at the new pin. Whether they are re-held is an open question
recorded against HX5-F03, not settled here.

## D-029 — a host holds all four service principal names — RATIFIED 2026-09-16

Every domain-joined host carries `host/<SHORT>`, `host/<fqdn>`,
`RestrictedKrbHost/<SHORT>` and `RestrictedKrbHost/<fqdn>`, and its
`dNSHostName` is the FQDN. Short-form principals alone are not sufficient.

**Why.** HX-5 was the reconciled reference and carried all four. HX-2, HX-3 and
HX-4 carried two each and had to be corrected, and the correction turned out to
be setting `dNSHostName`, because Samba derives the FQDN-form principals from
it. Adding the principals directly is refused while `dNSHostName` holds the
short name.

**How it is read.** From the directory, on HX-1. HX5-F12 established that the
keytab lists only what was issued to the host and `kvno` reports only what a
KDC will serve, so neither settles what Active Directory stores.

## D-030 — `openwiki init` is not run in this repository — RATIFIED 2026-09-17

OpenWiki is run in update mode only. `openwiki init` is not run here again.

**Why.** `init` is a setup command, and installing
`.github/workflows/openwiki-update.yml` is part of what setup does. D-025
withdrew that workflow. The setup path writes the file whenever it is missing,
so D-025's deletion is precisely what arms its recreation, and the next `init`
restores it. Update mode never touches the path.

`.openwikiignore` does not prevent this and was never able to. It governs what
the documentation agent may read and write, not what setup installs. HX7-F01
carries the code and the evidence.

**Backstop, not the control.** `hx_doc_check.py` carries `WITHDRAWN_PATHS` and
fails when a path a ratified decision deleted exists again. It caught the
2026-09-17 recurrence on the first run. It stays as it is. This decision is the
control; that gate is what catches the decision being broken.
