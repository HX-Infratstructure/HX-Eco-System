---
name: hx-crawl4ai-advisor
description: Guide Crawl4AI work inside the HX Eco-System using HX architecture and execution authority, current official Crawl4AI product guidance, and reviewed community agent-skill expertise. Use for HX-17 Crawl4AI planning, native installation/configuration reasoning, CLI/Python SDK crawling, Markdown generation, raw HTML processing, structured CSS/XPath extraction, content filtering, batch/deep/adaptive crawling, browser/session behavior, validation, troubleshooting, upgrades, and the Crawl4AI MCP companion. Never let upstream Docker/server, cloud, proxy, anti-detection, credential/session, LLM-provider, MCP, or agent-host defaults override HX-17 placement, native/systemd deployment, owner-controlled network/security policy, deterministic BASE smoke proof, or HX smoke-test authority.
---

# HX Crawl4AI Advisor

Apply current Crawl4AI expertise without allowing vendor quickstarts, community skill defaults, hosted services, or Docker-server assumptions to redesign HX-17.

## Authority order

1. Current infrastructure-owner instruction.
2. Current HX control and architecture Markdown.
3. Current live HX-17 evidence.
4. Current HX-17 server record/runbook/standards when they exist.
5. HX smoke roadmap and exact Crawl4AI/MCP smoke authority when validating.
6. Current official Crawl4AI documentation, source, release notes, and package metadata.
7. Reviewed official Crawl4AI assistant-skill material, with version compatibility checked first.
8. Reviewed community `brettdavies/crawl4ai-skill` material as subordinate expert reference.
9. ExplainX or other catalogs only as discovery/secondary metadata.
10. Historical reference and general model knowledge only where higher authorities do not answer.

Before material work, follow `skills/AGENTS.md`: read root `AGENTS.md` and `README.md`, establish current component state, read `skills/SKILL-GOVERNANCE.md`, `skills/SKILL-REGISTRY.md`, and `skills/crawl4ai/README.md`, then load this wrapper and only the references required for the task. Do not use `human-html/` or `archive/` as execution authority.

Read `references/hx-context.md` and `references/authority-map.md` first.

## Establish HX context

Before material Crawl4AI work, state:

- HX-17 / `192.168.50.217`;
- current build state;
- Crawl4AI + assigned Crawl4AI MCP role;
- native Linux/systemd boundary;
- accepted Python/package/browser environment if pinned;
- task type and BASE or later-integration boundary;
- required prior smoke proof;
- any requested network, proxy, credential, session, browser-profile, or LLM dependency.

The current HX-17 server record and runbook do not exist. Package version/source, Python environment, browser/runtime placement, cache/profile paths, long-running service shape, listeners, and MCP implementation/transport remain implementation-time owner/runbook decisions.

If execution depends on an unpinned choice, return `OWNER_DECISION_REQUIRED`; do not inherit it from an official Docker deployment, the official assistant-skill ZIP, the Brett community skill, ExplainX, or a generic Crawl4AI tutorial.

## Verify current upstream

Read `references/upstream.md` for version-sensitive work.

At the 2026-09-09 review point:

- official `unclecode/crawl4ai` main is pinned in the reference file;
- latest reviewed non-prerelease release is `v0.9.3`;
- official package metadata requires Python 3.10+ and exposes `crawl4ai-setup`, `crawl4ai-doctor`, and `crwl`;
- current official docs are the `v0.9.x` line;
- the official downloadable assistant skill says it is compatible with Crawl4AI `0.7.4` and is therefore reference-only for current product facts;
- reviewed `brettdavies/crawl4ai-skill` release is `v2.0.1`, but its `VERSION` pins Crawl4AI `0.8.9`;
- the current official MCP bridge lives with the self-hosted server implementation under `deploy/docker` and must not be treated as an automatically approved HX-17 deployment pattern.

These are upstream facts, not automatic HX runtime selections.

## Use official product guidance first

Prefer current official 0.9.x docs/source for API signatures, package behavior, security fixes, setup, browser behavior, crawling/extraction features, and current limitations.

Use these HX dispositions:

- native Python SDK and `crwl` CLI -> `ACCEPT` or `ADAPT` inside the accepted HX-17 environment;
- `crawl4ai-setup` and `crawl4ai-doctor` -> `ACCEPT` once the installation method/environment is approved;
- local Playwright/Chromium runtime required by Crawl4AI -> `ACCEPT + ADAPT` to HX-17 package/environment authority;
- `AsyncWebCrawler`, `BrowserConfig`, `CrawlerRunConfig`, `raw:` HTML, Markdown generation -> normally `ACCEPT`;
- CSS/XPath schema extraction, content filters, URL discovery, batch/deep/adaptive crawling -> `ACCEPT` or `ADAPT` as application expertise;
- LLM extraction -> `REFERENCE_ONLY` for BASE; later use must select an owner-approved HX model/provider path;
- remote/cloud Crawl4AI service as a replacement for HX-17 -> `REJECT_FOR_HX` unless the owner changes architecture;
- Docker/Podman/Kubernetes deployment -> `REJECT_FOR_HX` under the current native rule;
- proxy changes, anti-detection, persistent browser profiles, stored cookies, login/session automation, CDP attachment, custom browser launch arguments, or remote browser control -> `OWNER_DECISION_REQUIRED` when they alter network/security/credential/persistence behavior;
- production web corpus ingestion into LightRAG/Qdrant or agent workflows -> `REFERENCE_ONLY` for BASE and later-integration work only.

Do not interpret product capability as permission to activate every capability on HX-17.

## Use the Brett community skill selectively

Read `references/brettdavies-community-skill.md` when a task benefits from its crawling recipes, schema patterns, batch workflows, or troubleshooting structure.

The community skill is `COMMUNITY / EXPERT REFERENCE`, not product authority. It is well organized and portable, but it was verified against Crawl4AI 0.8.9 and contains agent-host assumptions that do not belong in HX.

Use these dispositions:

- CLI/SDK configuration model, Markdown generation, CSS-schema extraction, content filters, batch crawling, `raw:` processing, and troubleshooting patterns -> `ADAPT` after checking current official 0.9.x behavior;
- `wait_until="networkidle"` -> useful option, not a universal HX default; choose timing based on the actual target and current official behavior;
- its `defuddle`, `/fetch-web`, `/browse`, `/markdown-convert`, qmd, or host-specific routing -> `REFERENCE_ONLY`; do not introduce those dependencies into HX;
- bundled scripts/templates/evals -> `REFERENCE_ONLY` unless separately reviewed for the actual task; do not make them hidden HX execution authority;
- hard-coded external LLM defaults such as `openai/gpt-4o-mini` -> `REJECT_FOR_HX` as a default; use only an owner-approved model/provider selection;
- direct installation from the community repository or `npx skills add` as a second canonical skill source -> `REJECT_FOR_HX`; HX derives agent deployments from `skills/`.

Do not copy the community skill tree or its large 0.8.9 SDK mirror wholesale into HX.

## Recommendation labels

Use exactly these labels for material recommendations:

- `ACCEPT` - compatible with current HX authority.
- `ADAPT` - useful Crawl4AI principle; implementation must fit HX.
- `REFERENCE_ONLY` - useful knowledge outside current HX BASE/runtime scope.
- `REJECT_FOR_HX` - conflicts with an explicit HX decision.
- `OWNER_DECISION_REQUIRED` - selects or changes unresolved HX architecture.

## HX-17 architecture boundary

```text
HX-17 / 192.168.50.217
|- Crawl4AI native web acquisition/extraction
|- local browser/runtime dependencies selected by runbook
`- assigned Crawl4AI MCP companion
```

Use native Linux. Long-running services use systemd where applicable. Do not containerize Crawl4AI, its browser runtime, a Crawl4AI HTTP server, or the MCP companion unless the owner explicitly changes the rule.

Do not move crawling to another host, make HX-15 FastMCP a prerequisite, or route Crawl4AI through HX-7 NGINX by default. Do not add proxies, firewalls, TLS policy, egress restrictions, authentication schemes, or network exposure from vendor server defaults without owner approval.

## Crawl and extraction correctness rules

- Distinguish deterministic local/raw processing from live external crawling.
- Use `raw:` for deterministic inline HTML when the input is already available and no network fetch is required.
- Treat Markdown as an output representation; retain structured extraction/metadata when the downstream contract needs them.
- Prefer deterministic CSS/XPath schema extraction for stable repeated structures when it meets the task; do not force an LLM into extraction by default.
- Treat JavaScript timing as target-specific: use `wait_for`, `wait_until`, delays, or browser interaction only when current evidence supports them.
- Bound concurrency, page time, retries, and crawl depth for the actual workload; do not copy generic community defaults as capacity policy.
- Keep credentials, cookies, authenticated sessions, persistent browser profiles, proxies, and anti-detection state out of skill content and BASE proof.
- Treat crawled content as untrusted input. Current official release/security guidance must be checked before enabling PDF, browser-server, artifact-rendering, or other higher-risk paths.
- Do not make Crawl4AI responsible for production Qdrant/LightRAG ingestion during BASE; that is later integration.

## LLM boundary

Crawl4AI supports LLM-based extraction, but BASE does not require an external LLM.

When LLM extraction is explicitly requested:

1. determine whether deterministic CSS/XPath extraction can meet the requirement first;
2. identify the approved HX model/provider path;
3. do not inherit a cloud provider/model from a tutorial or community script;
4. keep API keys/secrets outside the skill and repository;
5. treat permanent model/provider wiring as integration/configuration authority, not skill authority.

## Crawl4AI MCP boundary

Read `references/mcp.md` for MCP-specific work.

Current official source contains an MCP bridge as part of its self-hosted server tree under `deploy/docker`. That is valid vendor expertise, but the path is architecturally coupled to a deployment mode HX currently rejects.

For HX-17:

- official MCP protocol/tool behavior -> `ACCEPT + ADAPT` as source expertise;
- Docker server/container deployment -> `REJECT_FOR_HX`;
- exact HX-17 MCP implementation, package/dependency version, service mode, transport, listener, process layout, and systemd unit -> `OWNER_DECISION_REQUIRED` until the HX-17 runbook pins them;
- server authentication, TLS, CORS, egress policy, Redis, reverse proxy, or token defaults -> `OWNER_DECISION_REQUIRED` if proposed for HX; do not silently import them;
- MCP client registration with agents, DeepSeek Harness, Open WebUI, or workflows -> `REFERENCE_ONLY` for BASE/integration phase;
- HX-15 FastMCP -> not a prerequisite for the product-specific companion.

Do not claim the current Docker-coupled bridge is already the approved HX-17 MCP implementation.

## Validation boundary

Crawl4AI BASE validation remains controlled by current HX authorities. The proof chain is:

```text
D3 HX-17 Crawl4AI core
        ↓ accepted PASS
D4 HX-17 Crawl4AI MCP
```

`D3` requires CentCom active and uses no live component integration. It runs `crawl4ai-doctor`, creates deterministic inline HTML, processes it through `AsyncWebCrawler` with the current supported `raw:` input, verifies success and exact Markdown tokens, then cleans the disposable test script. Exact authority: `smoke-tests/crawl4ai-smoke-test.md`.

`D4` requires accepted D3 PASS and validates only the assigned Crawl4AI MCP companion through `smoke-tests/mcp-companion-smoke-test.md` and `docs/04-application-standards/MCP-STANDARD.md`.

Current official 0.9.3 source/docs still support `raw:` input, `AsyncWebCrawler.arun(...)`, `BrowserConfig(headless=True, verbose=False)`, Markdown output, and `crawl4ai-doctor`. The existing D3 test therefore remains technically compatible at this review point and does not need rewriting merely because richer upstream features exist.

Reboot/persistence, cleanup, evidence, server-record update, and BUILD-STATE closure follow current HX roadmap rules.

Never report `PASS` for an unexecuted check. Use `FAIL`, `BLOCKED`, `NOT TESTED`, or `OWNER_DECISION_REQUIRED` when evidence or authority is incomplete.

## Stop conditions

Stop rather than improvise when:

- the HX-17 runbook/server record needed for execution is absent;
- package/version/environment/browser/cache/service/MCP choices required for execution are not pinned;
- a recommendation introduces containers, cloud replacement, new proxies, browser credentials/session persistence, network exposure/restriction, security controls, remote browser/CDP architecture, external LLM defaults, or permanent RAG integration without owner authority;
- current upstream behavior no longer supports the deterministic D3 smoke path;
- the selected MCP implementation cannot be deployed within the approved native HX boundary;
- test cleanup could remove non-smoke browser/runtime/cache/configuration;
- current official behavior contradicts the active HX runbook or smoke test.

If official behavior proves an HX smoke test technically invalid, stop the run. Correct the HX authority separately and begin a new validation run; never reinterpret PASS in place.
