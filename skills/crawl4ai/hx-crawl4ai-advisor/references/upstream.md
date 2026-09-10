# Crawl4AI upstream provenance

Review date: 2026-09-09 (America/Chicago)

## Official product

Repository: `unclecode/crawl4ai`

- Reviewed main: `862f6bccb9c063f49b9d42701baa0eea17a4993f`
- Reviewed main date: 2026-08-31
- Latest reviewed non-prerelease release: `v0.9.3`
- Release published: 2026-08-31
- Official docs: `https://docs.crawl4ai.com/`
- Docs line at review: `v0.9.x`
- License in current `pyproject.toml`: Apache-2.0
- Python requirement: `>=3.10`

Current package entrypoints include:

```text
crawl4ai-download-models
crawl4ai-migrate
crawl4ai-setup
crawl4ai-doctor
crwl
```

Default dependencies include Playwright/Patchright and the normal Crawl4AI runtime stack. Optional extras include PDF, torch/transformer/cosine, sync, and `all`. Exact HX extras are not selected by this skill.

## Current release relevance

`v0.9.3` is a security release. Material current fixes include PDF-path arbitrary file-write/SSRF/resource-limit/XSS issues and a Playground DOM-XSS issue. It also includes server/MCP fixes and caps `mcp` below 2 because the current `mcp_bridge` uses the v1 low-level API.

For version selection or untrusted-content exposure, re-check the latest stable release and security guidance at implementation time.

`v0.9.0` introduced breaking architecture/security changes for the self-hosted Docker server, while official release notes state the core pip SDK/in-process path was unchanged by that server migration. This explains why several 0.8.9 community patterns remain recognizable, but it does not make a 0.8.9 reference current authority.

## Current API facts relevant to HX smoke

Current official source/docs confirm:

- `AsyncWebCrawler` remains the core async crawler;
- `arun(url, config=...)` remains supported;
- inline raw HTML is supported with `raw:`;
- `BrowserConfig(headless=True, verbose=False)` appears in current official examples;
- Markdown remains a primary crawl output;
- `crawl4ai-setup` and `crawl4ai-doctor` are current package entrypoints.

Therefore the current HX deterministic `raw:` smoke-test shape remains technically compatible at this review point.

## Official assistant skill

Official docs currently advertise an AI Assistant Skill ZIP with:

- complete SDK reference;
- extraction scripts;
- schema generation;
- compatibility label: Crawl4AI `0.7.4`.

Current repository asset at reviewed main:

- `docs/md_v2/assets/crawl4ai-skill.zip`
- blob: `21785b0214567f4772562697cbc49f6c9486e58f`
- size: 78,441 bytes

Because the advertised compatibility is older than current 0.9.3, classify this source as `VENDOR_OFFICIAL / REFERENCE_ONLY` for current HX product facts. Do not install it as a second canonical HX skill.

## Current server/MCP caution

The official self-hosted server and its MCP bridge live under `deploy/docker`, including `deploy/docker/mcp_bridge.py` and `deploy/docker/server.py`. Current server docs expose MCP transports/tools through that server architecture.

HX does not use containerized workloads. Treat the official bridge as product/MCP behavior evidence only until the HX-17 runbook selects a native-compatible implementation. Do not infer that copying `deploy/docker` files to systemd is approved or technically complete.

## Re-review triggers

Re-review upstream when:

- Crawl4AI stable version changes materially;
- package entrypoints or raw-HTML behavior changes;
- browser/runtime installation changes;
- extraction or deep/adaptive crawling APIs change;
- server/MCP architecture changes;
- a standalone official native MCP package appears;
- an official assistant skill is refreshed to the current product line;
- security advisories affect the selected HX-17 usage.
