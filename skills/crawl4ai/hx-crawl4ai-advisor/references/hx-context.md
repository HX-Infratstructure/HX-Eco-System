# HX context for Crawl4AI

## Current HX-17 role

- Host: `HX-17`
- IP: `192.168.50.217`
- Assignment: Crawl4AI + assigned Crawl4AI MCP
- Current state at review: `NOT STARTED`
- Deployment: native Linux; long-running services use systemd where applicable
- Containers: not used unless the infrastructure owner explicitly changes the rule
- Normal application access: direct native server/port where a service endpoint is selected
- HX-7 NGINX: dev/test UI rendering only, not normal ecosystem routing
- HX-15 FastMCP: shared/custom MCP development/runtime; not a prerequisite for product-specific MCP

No active `docs/02-server-records/HX-17.md` or `docs/03-runbooks/HX-17/README.md` existed at the 2026-09-09 review point. Do not infer as-built state or installation decisions from this skill.

## BASE roadmap position

HX-17 is priority 11, after HX-16 Docling and before HX-11 LightRAG.

BASE PASS boundary:

```text
Native Crawl4AI
+ deterministic crawl/Markdown proof
+ assigned MCP companion smoke test
+ cleanup
+ reboot persistence where applicable
+ evidence/server record/BUILD-STATE closure
```

No production RAG ingestion is part of HX-17 BASE.

## Smoke proof chain

Current ordered proof:

```text
D3 — HX-17 Crawl4AI core
     prerequisite: CentCom active
     integration: none
     input: deterministic inline raw: HTML

D4 — HX-17 Crawl4AI MCP
     prerequisite: accepted D3 PASS
     integration: parent Crawl4AI service only
```

Authorities:

- `docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md`
- `smoke-tests/crawl4ai-smoke-test.md`
- `smoke-tests/mcp-companion-smoke-test.md`
- `docs/04-application-standards/MCP-STANDARD.md`

## Current D3 known-answer contract

The current smoke test:

1. runs `crawl4ai-doctor`;
2. creates local deterministic HTML with token `HX-CRAWL4AI-SMOKE-9271`;
3. creates `BrowserConfig(headless=True, verbose=False)`;
4. runs `AsyncWebCrawler.arun("raw:<html>...")`;
5. requires `result.success`;
6. verifies generated Markdown contains title, token, `alpha`, and `beta`;
7. records Crawl4AI/Python versions and output;
8. removes only the disposable script.

It deliberately requires no external website, LLM, proxy, DB, API key, or container.

## Owner-controlled decisions still open

Do not choose these inside the skill:

- exact Crawl4AI package/version pin and package source;
- Python environment/venv path;
- browser/runtime installation and cache/profile paths;
- whether Crawl4AI is SDK/CLI-only or has a long-running native service for BASE;
- any listener/port;
- proxy/egress/network/security/authentication policy;
- persistent browser profile/session/cookie handling;
- permanent LLM/provider binding;
- exact Crawl4AI MCP implementation/version/transport/listener/process/systemd layout;
- later LightRAG/Qdrant/agent/workflow integration.

## Non-negotiable HX rules

- Do not introduce Docker/Podman/Kubernetes from Crawl4AI quickstarts.
- Do not make HX-15 FastMCP a prerequisite for Crawl4AI MCP.
- Do not add firewall/TLS/access restrictions without owner approval.
- Do not copy credentials or API keys into this skill.
- Do not treat a community skill or catalog listing as architecture authority.
- Do not advance BUILD-STATE merely because the skill is approved.
