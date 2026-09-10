---
document: HX Crawl4AI Skill Intake
status: current
date: 2026-09-09
component: Crawl4AI
hx_host: HX-17
---

# HX Crawl4AI Skills

Canonical HX wrapper:

```text
skills/crawl4ai/hx-crawl4ai-advisor/
```

Status: **APPROVED** for advisory expertise. HX-17 itself remains **NOT STARTED**.

## Role

HX-17 / `192.168.50.217` is assigned:

```text
Crawl4AI native web acquisition/extraction
+ assigned Crawl4AI MCP companion
```

The BASE roadmap requires native Crawl4AI, deterministic crawl-to-Markdown proof, the MCP companion proof, cleanup, and reboot/persistence evidence where applicable. It does not authorize production RAG ingestion.

## Source hierarchy

| Source | Class | Reviewed point | HX disposition |
|---|---|---|---|
| `unclecode/crawl4ai` docs/source/releases | `VENDOR_OFFICIAL` | main `862f6bccb9c063f49b9d42701baa0eea17a4993f`; release `v0.9.3` | **PRIMARY PRODUCT AUTHORITY** |
| Official downloadable Crawl4AI assistant skill | `VENDOR_OFFICIAL` | current docs advertise compatibility with Crawl4AI `0.7.4`; asset blob `21785b0214567f4772562697cbc49f6c9486e58f` | `REFERENCE_ONLY` for current product facts |
| `brettdavies/crawl4ai-skill` | `COMMUNITY / EXPERT REFERENCE` | main `c696921b133dd962f766f596655767c0b894d206`; release `v2.0.1`; verified Crawl4AI `0.8.9` | `APPROVED_AS_REFERENCE` |
| ExplainX Brett skill listing | `SECONDARY / DISCOVERY` | reviewed 2026-09-09 | discovery metadata only; not trust/version authority |
| Official `deploy/docker/mcp_bridge.py` | `VENDOR_OFFICIAL` MCP source | current official main | behavior/reference accepted; HX deployment mode unresolved |

Detailed source record: `upstream/SOURCE.md`.

## Why one HX wrapper

The external material contains useful product expertise but also assumptions that conflict with or exceed current HX authority:

- official self-hosting/MCP guidance is coupled to Docker-server architecture;
- the official assistant skill is still labeled for Crawl4AI 0.7.4;
- the Brett community skill is verified against 0.8.9, not current 0.9.3;
- Brett's bundle assumes other host tools such as `defuddle`, `/fetch-web`, `/browse`, and qmd;
- one Brett helper script hard-codes `openai/gpt-4o-mini` for schema generation;
- upstream documents proxies, anti-detection, credentials/sessions, cloud/API and server security defaults that cannot silently become HX policy.

`hx-crawl4ai-advisor` loads HX first, then uses current official 0.9.x product guidance and only selectively consults older/community skill material.

## Accepted/adapted expertise

Normally usable after current version verification:

- `AsyncWebCrawler`, `BrowserConfig`, `CrawlerRunConfig`;
- `crwl` CLI and Python SDK;
- `crawl4ai-setup` / `crawl4ai-doctor`;
- local Playwright/Chromium dependency reasoning;
- `raw:` inline HTML processing;
- Markdown generation;
- CSS/XPath schema extraction;
- content filters;
- batch/deep/adaptive crawling and URL discovery;
- target-specific JS wait/timing configuration;
- troubleshooting and upgrade analysis.

## Gated/rejected expertise

| Guidance | HX handling |
|---|---|
| Docker/Podman/Kubernetes | `REJECT_FOR_HX` under current architecture |
| Hosted/cloud replacement of HX-17 | `REJECT_FOR_HX` unless owner changes placement |
| Hard-coded external LLM provider/model | `REJECT_FOR_HX` as a default |
| Proxies, anti-detection, stored cookies/login sessions, persistent browser profiles, CDP/remote browser | `OWNER_DECISION_REQUIRED` when they alter network/security/credential/persistence behavior |
| Official Docker-coupled MCP deployment | `OWNER_DECISION_REQUIRED` for HX implementation; source expertise retained |
| Production LightRAG/Qdrant ingestion | `REFERENCE_ONLY` for BASE / later integration |
| Direct `npx skills add` or cloning Brett into an agent skill directory | `REJECT_FOR_HX` as canonical deployment; HX derives deployments from `skills/` |

## Validation authority

```text
D3 — HX-17 Crawl4AI core
     prerequisite: CentCom active
     input: deterministic inline raw: HTML
     integration: none
     authority: smoke-tests/crawl4ai-smoke-test.md

D4 — HX-17 Crawl4AI MCP
     prerequisite: accepted D3 PASS
     integration: parent Crawl4AI only
     authority: smoke-tests/mcp-companion-smoke-test.md
```

The current D3 test remains compatible with reviewed official 0.9.3 behavior: current source/docs support `raw:`, `AsyncWebCrawler.arun`, `BrowserConfig(headless=True, verbose=False)`, Markdown output, and `crawl4ai-doctor`.

Skill approval does not modify the D3/D4 smoke criteria.

## MCP status

HX requires Crawl4AI MCP as the HX-17 companion, but its exact native implementation is not yet pinned. Current official source implements MCP as part of the self-hosted server tree under `deploy/docker`. HX will not containerize it merely because that is the vendor layout.

Before D4 becomes executable, the future HX-17 runbook must select and document the native-compatible MCP package/dependency, service mode, transport, listener, process/systemd layout, and any owner-approved network/auth controls.

## Current authority gaps

No active HX-17 server record or runbook exists at this review point. Therefore this skill does **not** select:

- Crawl4AI package/version/package source;
- Python environment;
- browser/runtime/cache/profile paths;
- long-running service/listener design;
- proxy/egress/auth/session policy;
- LLM/provider bindings;
- exact MCP implementation/transport;
- permanent downstream RAG/agent/workflow integration.

## Canonical package

The validated wrapper package is generated from the canonical `hx-crawl4ai-advisor/` directory. Agent-specific installations are derived deployments and must not become independent sources of truth.
