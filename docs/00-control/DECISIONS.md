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

## D-018 — Host firewall and inference listener posture — PROPOSED, awaiting owner ratification

The HX LAN is treated as a trusted lab segment. The common base runbook
disables `ufw` on every server, and Ollama listens on `0.0.0.0:11434` with no
authentication. This is consistent with the standing rule that firewall,
segmentation and TLS changes are not imposed without owner approval, and with
KISS.

This entry does not change behaviour. It records behaviour that previously
existed only as an emergent property of two runbook scripts, so it can be
approved, revisited, or reversed as a decision rather than rediscovered.

Blast radius as it stands: any host that can reach the HX LAN can call any HX
inference endpoint without credentials, and can reach any service port on any
HX server.

**Owner action required:** ratify as written, or amend. Until ratified this
entry is a record of current state, not an approval.

## D-019 — OmniRoute product identity — PROPOSED, owner confirmation required

No document in this repository names the upstream project behind "OmniRoute".
The HX-6 install block targets `diegosouzapw/OmniRoute` (npm package
`omniroute`, MIT, currently 3.8.50), because its described role matches HX-6
exactly: a single-endpoint AI gateway with hundreds of discoverable providers,
quota-aware fallback, and an OpenAI-compatible API. D-010's insistence that
"discovery does not equal approval" and that "free/no-auth/discovered providers
are not automatically active" reads as written against precisely that product.

**This is an inference, not a record.** Confirm it before HX-6 is built. If
OmniRoute is a different product, or something HX built, say so and the HX-6
block is rewritten; nothing else depends on this.

If confirmed, note that the headless server installs from npm. The project's
GitHub release assets are desktop application builds only, and its documented
container path is not used here.
