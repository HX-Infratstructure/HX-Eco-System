# Brett Davies Crawl4AI community skill review

Source: `https://github.com/brettdavies/crawl4ai-skill`

Review date: 2026-09-09

## Provenance

- Classification: `COMMUNITY / EXPERT REFERENCE`
- Reviewed main: `c696921b133dd962f766f596655767c0b894d206`
- Latest reviewed release: `v2.0.1`
- Release date: 2026-06-16
- Skill entrypoint blob: `9ad9095283f2efc67d1499667fa604409e36fd7a`
- `VERSION` blob: `55485e179379afad176ee5c7bf81d2456bd7b8c2`
- Verified Crawl4AI library version: `0.8.9`
- Skill license: MIT OR Apache-2.0

The repository records v2.0.1 as a docs-only patch over v2.0.0. The v2.0.0 bundle was refreshed and tested against Crawl4AI 0.8.9.

## Useful expertise

The skill provides good reusable patterns for:

- `crwl` CLI and Python SDK routing;
- BrowserConfig/CrawlerRunConfig separation;
- Markdown generation and content filtering;
- deterministic CSS-schema extraction;
- LLM-based extraction when deterministic extraction is unsuitable;
- multi-URL crawling with `arun_many()`;
- URL discovery;
- sessions/authentication;
- proxies and anti-detection;
- `raw:`/local HTML rendering;
- troubleshooting and escalation structure.

It also contains scripts, templates, evals, fixtures, and a large mirrored SDK reference.

## HX adaptations

### Keep as principles after current verification

- CLI/SDK configuration concepts.
- Structured deterministic extraction before LLM extraction where appropriate.
- Batch-crawl and content-filter patterns.
- `raw:` processing.
- Explicit timing/wait configuration rather than assuming `<body>` proves JS readiness.

### Do not inherit as HX defaults

The skill routes static pages to `defuddle`/`fetch-web`, local conversions to `markdown-convert`, mutating browser flows to `/browse`, and escalation to qmd. These are assumptions about another agent-tool ecosystem. HX does not gain those dependencies from this source.

Its default `wait_until="networkidle"` is useful for some JS-heavy pages and remains supported upstream, but current official Crawl4AI also uses `load` and `domcontentloaded` for other cases. Treat timing as workload-specific.

Its `generate_schema.py` hard-codes `provider="openai/gpt-4o-mini"`. That is not an HX-approved default. Any LLM extraction/schema generation must use an owner-approved HX provider/model path.

Its scripts use PEP 723 / `uv run` and dependency floors such as `crawl4ai>=0.8.9`. They are examples, not approved HX-17 execution artifacts or package policy.

## Why the tree is not vendored

The community bundle is intentionally not copied wholesale because:

1. its product pin is older than current official 0.9.3;
2. its complete SDK mirror can drift from official source;
3. its scripts/templates carry host/provider defaults not established by HX;
4. HX runbooks and smoke tests remain execution/acceptance authority;
5. direct installation would create a second canonical skill source alongside `skills/`.

Consult individual community files only when they materially improve a task, then verify the relevant API/behavior against current official Crawl4AI documentation/source.

## ExplainX listing

ExplainX lists the skill and provides `npx skills add` instructions. Treat that site as discovery/secondary metadata only.

At review, ExplainX displayed `Updated Aug 26, 2026` and review entries dated November/December 2024. The Brett repository's own changelog records the initial release as 2025-12-02 and current main/release as June 2026. That chronology does not reconcile. Do not use ExplainX update dates, ratings, review timestamps, star/install counts, or generic implementation guidance as HX admission evidence.
