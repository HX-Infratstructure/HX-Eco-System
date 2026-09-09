# Crawl4AI Smoke Test

## 1. Title & Purpose

Crawl4AI is the HX web acquisition component on HX-17. This smoke test validates that Crawl4AI is installed correctly and can process deterministic HTML into usable Markdown without depending on a public website or external LLM.

**Scope:** Crawl4AI core crawl/extraction function only. Crawl4AI MCP remains a separate companion gate.

## 2. Prerequisites

- Crawl4AI is installed natively in the accepted HX-17 Python environment.
- The installed version is recorded before execution; re-check the current stable upstream release at implementation time.
- Crawl4AI post-install setup has been completed:

```bash
crawl4ai-setup
```

- The installation doctor command is available:

```bash
crawl4ai-doctor
```

- The browser/runtime dependencies installed by Crawl4AI are present. If Chromium setup was not completed automatically, install the required Playwright browser during component installation, not as hidden smoke-test remediation.
- Python is available in the same accepted Crawl4AI environment.
- No environment variable is required for this deterministic raw-HTML smoke test.
- No external website, API key, LLM, proxy, database, Docker, Podman, Kubernetes, or temporary container is required.

## 3. Test Steps

1. Run the installation doctor.

```bash
crawl4ai-doctor
```

Resolve installation/browser errors before continuing.

2. Save the following as `crawl4ai_smoke.py` in the disposable test workspace.

```python
import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig

TOKEN = "HX-CRAWL4AI-SMOKE-9271"
HTML = f"""
<!doctype html>
<html>
  <head><title>HX Crawl4AI Smoke Test</title></head>
  <body>
    <main>
      <h1>HX Crawl4AI Smoke Test</h1>
      <p>This page is synthetic and exists only for the smoke test.</p>
      <p>Smoke token: <strong>{TOKEN}</strong></p>
      <ul>
        <li>alpha</li>
        <li>beta</li>
      </ul>
    </main>
  </body>
</html>
"""


async def main():
    browser = BrowserConfig(headless=True, verbose=False)
    async with AsyncWebCrawler(config=browser) as crawler:
        result = await crawler.arun(f"raw:{HTML}")

    assert result.success, f"crawl failed: {getattr(result, 'error_message', '')}"

    markdown_obj = result.markdown
    markdown = getattr(markdown_obj, "raw_markdown", None) or str(markdown_obj)

    assert "HX Crawl4AI Smoke Test" in markdown, markdown
    assert TOKEN in markdown, markdown
    assert "alpha" in markdown and "beta" in markdown, markdown

    print(f"CRAWL4AI_SMOKE_PASS token={TOKEN}")


if __name__ == "__main__":
    asyncio.run(main())
```

3. Run the test in the accepted Crawl4AI environment.

```bash
python3 crawl4ai_smoke.py
```

4. Record the Crawl4AI version, Python version, `crawl4ai-doctor` result, and smoke-test console output with the normal HX evidence.

## 4. Sample Data

The sample HTML is embedded directly in the script. Its known values are:

```text
Title: HX Crawl4AI Smoke Test
Token: HX-CRAWL4AI-SMOKE-9271
List values: alpha, beta
```

The test uses Crawl4AI's supported `raw:<html>...</html>` input path, which removes public-network variability while still exercising the Crawl4AI processing and Markdown-generation path.

## 5. Expected Output

`crawl4ai-doctor` must complete without an unresolved critical installation/browser failure.

The Python test must end with:

```text
CRAWL4AI_SMOKE_PASS token=HX-CRAWL4AI-SMOKE-9271
```

Pass means:

- Crawl4AI imports successfully;
- the crawler starts and completes successfully;
- the result reports success;
- generated Markdown contains the title;
- generated Markdown contains the exact smoke token;
- generated Markdown contains both list values.

This test intentionally does not depend on live internet content. A later integration test can validate external web access, Crawl4AI MCP, and downstream RAG ingestion separately.

## 6. Cleanup / Teardown

No remote content, collection, database record, browser profile, or application state is created by the smoke test.

After evidence capture:

```bash
rm -f crawl4ai_smoke.py
```

If the test workspace itself is disposable, remove that workspace according to the HX test-project procedure once that procedure is defined.

**Do not remove the installed Crawl4AI browser/runtime files during cleanup. No containers are created by this test.**
