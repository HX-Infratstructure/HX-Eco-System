#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture deterministic HX Web UI evidence from HX-5 CentCom."
    )
    parser.add_argument("url")
    parser.add_argument("expect", help="Visible text that proves live application/backend state")
    parser.add_argument("output", help="PNG or WebP output path")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    meta = output.with_suffix(output.suffix + ".meta.txt")

    started = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout_ms)
        marker = page.get_by_text(args.expect, exact=False).first
        marker.wait_for(state="visible", timeout=args.timeout_ms)
        title = page.title()
        final_url = page.url
        page.screenshot(path=str(output), full_page=True, animations="disabled")
        browser.close()

    meta.write_text(
        "\n".join(
            [
                f"UTC={started}",
                "RUNNER=hx-5",
                f"URL={final_url}",
                f"TITLE={title}",
                f"EXPECTED_VISIBLE_TEXT={args.expect}",
                "UI_CAPTURE=PASS",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"UI_CAPTURE_PASS output={output}")
    print(f"UI_CAPTURE_META={meta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
