---
document: HX Crawl4AI Upstream Source Record
status: current
date: 2026-09-09
component: Crawl4AI
---

# Crawl4AI Upstream Source Record

## Primary official product source

```text
Project: Crawl4AI
Repository: unclecode/crawl4ai
Reviewed main: 862f6bccb9c063f49b9d42701baa0eea17a4993f
Reviewed stable release: v0.9.3
Release date: 2026-08-31
Official documentation: https://docs.crawl4ai.com/
Docs line: v0.9.x
License: Apache-2.0
Python: >=3.10
Classification: VENDOR_OFFICIAL
HX status: PRIMARY PRODUCT AUTHORITY
```

Official package metadata exposes `crawl4ai-setup`, `crawl4ai-doctor`, `crwl`, model-download and migration entrypoints. Current core usage continues to center on `AsyncWebCrawler`, configuration objects, Markdown/structured extraction, local browser dependencies and `raw:` processing.

`v0.9.3` is a security release. Re-check current release/security guidance at implementation time, especially for untrusted PDF content or self-hosted server exposure.

## Official assistant skill

The official documentation currently advertises a downloadable Crawl4AI skill package, but labels it:

```text
Version 0.7.4 compatible
```

Current asset at reviewed official main:

```text
docs/md_v2/assets/crawl4ai-skill.zip
blob: 21785b0214567f4772562697cbc49f6c9486e58f
size: 78441 bytes
```

Classification: `VENDOR_OFFICIAL / REFERENCE_ONLY` for current product facts.

Reason: current product authority is 0.9.3/0.9.x. Do not direct-install an older vendor skill as a second HX authority.

## Reviewed community skill

```text
Repository: brettdavies/crawl4ai-skill
Reviewed main: c696921b133dd962f766f596655767c0b894d206
Latest reviewed release: v2.0.1
Release date: 2026-06-16
SKILL.md blob: 9ad9095283f2efc67d1499667fa604409e36fd7a
VERSION: 0.8.9
VERSION blob: 55485e179379afad176ee5c7bf81d2456bd7b8c2
License: MIT OR Apache-2.0
Classification: COMMUNITY / EXPERT REFERENCE
HX status: APPROVED_AS_REFERENCE
```

Strong reference areas include CLI/SDK usage, Markdown/content-filter patterns, CSS-schema extraction, batch crawling, URL discovery, sessions, anti-detection/proxy concepts, `raw:` rendering, recipes and troubleshooting.

Known HX mismatches:

- verified against 0.8.9 rather than current 0.9.3;
- host-specific routing to tools not established in HX;
- bundled execution scripts/templates are not HX runbooks;
- schema-generation helper hard-codes `openai/gpt-4o-mini`;
- large mirrored SDK reference can drift;
- direct agent-host installation would bypass canonical `skills/` governance.

## ExplainX listing

Source reviewed:

`https://explainx.ai/skills/brettdavies/crawl4ai-skill/crawl4ai`

Classification: `SECONDARY / DISCOVERY ONLY`.

ExplainX is useful for discovery and generic agent-host install instructions. It is not used as version, product, trust, release or quality authority. At review it displayed an Aug. 26, 2026 update while showing reviews dated late 2024; the Brett repository changelog records the initial release as Dec. 2, 2025. That chronology does not reconcile, so ratings/review dates/install counts are excluded from HX admission evidence.

## Official MCP source

Current official Crawl4AI source contains MCP under the self-hosted server tree:

```text
deploy/docker/mcp_bridge.py
deploy/docker/server.py
```

Current v0.9.3 release notes state `mcp` is capped below 2 because the bridge uses the v1 low-level API.

Classification: `VENDOR_OFFICIAL` source expertise.

HX disposition:

- protocol/tool behavior: `ACCEPT + ADAPT`;
- vendor Docker deployment: `REJECT_FOR_HX`;
- exact HX-17 native MCP implementation/transport/service layout: `OWNER_DECISION_REQUIRED` until the runbook pins it.

## HX wrapper

```text
skills/crawl4ai/hx-crawl4ai-advisor/
```

The wrapper keeps official current product guidance primary, curates community expertise, and preserves the HX-17 native/runtime/security/smoke boundaries.

## Re-review triggers

Re-review when:

- stable Crawl4AI product version materially changes;
- the official assistant skill is updated to the current product line;
- MCP moves to a standalone/native package or changes protocol/dependencies;
- Playwright/browser/runtime setup changes;
- extraction/deep/adaptive crawling APIs materially change;
- new security advisories affect selected HX usage;
- Brett's skill updates its Crawl4AI compatibility pin;
- HX-17 runbook resolves currently open package/service/MCP decisions.
