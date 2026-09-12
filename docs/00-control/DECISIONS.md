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

## D-023 — a write-capable token in Actions secrets, for OpenWiki — RATIFIED 2026-09-11

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

## D-024 — operational tooling is documented before it is adopted — RATIFIED 2026-09-12

The owner approved this on 2026-09-12, in the same message that approved the
rollout plan carrying it as step 7, after stating the requirement directly:
every operational tool gets its own directory covering what it is, why we
have it, and how and when to use it.

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

**The upstream-links section is not decoration.** The OpenWiki work ran for
hours against the README and the installed package while the product's own
documentation went unread, and the owner had to supply the URL. Eight pages of
upstream documentation then produced seven findings, including two capabilities
the repository was not using at all: `openwiki/INSTRUCTIONS.md`, which steers
coverage, and `.openwikiignore`, which had been letting the generator scan
`archive/` and `human-html/`. A missing link is how that happens.

Backlog on ratification: CodeRabbit and graft are listed in the index with no
document. Each is its own pull request.
