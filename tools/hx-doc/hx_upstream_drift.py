#!/usr/bin/env python3
"""Report drift between the commits SKILL-REGISTRY.md pins and their upstreams.

Seven governed skills consume upstream product guidance as live authority. The
registry pins the exact commit each was reviewed at, alongside a "Last
reviewed" date. Nothing previously told the owner when an upstream moved on.

This reads the pins out of the registry itself, so it cannot fall out of step
with the registry the way a second hard-coded list would.

Usage:
  hx_upstream_drift.py              human-readable report
  hx_upstream_drift.py --fail-on-drift   exit 1 when any pin is behind
  hx_upstream_drift.py --markdown   emit a table for an issue body

Needs network access and, for a higher API rate limit, GITHUB_TOKEN or GH_TOKEN.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Output may contain names copied from upstream metadata; never let a console
# codepage turn a report into a crash.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
REGISTRY = REPO / "skills/SKILL-REGISTRY.md"

# Provenance blocks name the repository and the reviewed commit in plain text.
REPO_LINE = re.compile(r"^(?:Repository|Official Agent Skills|Reviewed external skill|Docling MCP repository|Reviewed community skill):\s*([\w.-]+/[\w.-]+)\s*$", re.M)
SHA_LINE = re.compile(r"^(?:Current reviewed main|Reviewed main|Reviewed Agent Skills main|Reviewed Neon main|Reviewed MCP main|Reviewed community main):\s*([0-9a-f]{40})\s*$", re.M)


def api(path: str) -> dict | list:
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "hx-upstream-drift",
        },
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pins() -> list[tuple[str, str, str]]:
    """Extract (component, repo, pinned_sha) from every provenance block."""
    text = REGISTRY.read_text(encoding="utf-8")
    found: list[tuple[str, str, str]] = []
    for block in re.finditer(r"^## ([^\n]+?) provenance\n+```text\n(.*?)```", text, re.S | re.M):
        component, body = block.group(1), block.group(2)
        repos = REPO_LINE.findall(body)
        shas = SHA_LINE.findall(body)
        for repo, sha in zip(repos, shas):
            found.append((component, repo, sha))
    return found


def main() -> int:
    fail_on_drift = "--fail-on-drift" in sys.argv
    as_markdown = "--markdown" in sys.argv

    entries = pins()
    if not entries:
        print("ERROR: no provenance pins found in SKILL-REGISTRY.md", file=sys.stderr)
        return 2

    rows, drifted, errors = [], 0, 0
    for component, repo, sha in entries:
        try:
            head = api(f"/repos/{repo}/commits?per_page=1")[0]["sha"]
            if head == sha:
                rows.append((component, repo, sha[:8], "current", 0))
                continue
            cmp_ = api(f"/repos/{repo}/compare/{sha}...{head}")
            behind = cmp_.get("ahead_by", 0)
            rows.append((component, repo, sha[:8], head[:8], behind))
            drifted += 1
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError) as exc:
            rows.append((component, repo, sha[:8], f"ERROR {exc}", -1))
            errors += 1

    if as_markdown:
        print("| Component | Upstream | Pinned | Upstream HEAD | Commits behind |")
        print("|---|---|---|---|---|")
        for c, r, p, h, b in rows:
            flag = "" if b == 0 else (" **drift**" if b > 0 else " **error**")
            print(f"| {c} | `{r}` | `{p}` | `{h}` | {b if b >= 0 else 'n/a'}{flag} |")
    else:
        for c, r, p, h, b in rows:
            state = "current" if b == 0 else (f"{b} behind -> {h}" if b > 0 else h)
            print(f"{'DRIFT ' if b > 0 else 'OK    ' if b == 0 else 'ERROR '}{c:28} {r:34} {p}  {state}")

    print()
    print(f"{len(rows)} pins checked, {drifted} drifted, {errors} unreachable.")
    if drifted:
        print("Re-review the drifted sources, then update the reviewed commit and")
        print("'Last reviewed' date in skills/SKILL-REGISTRY.md.")
    return 1 if (fail_on_drift and drifted) else 0


if __name__ == "__main__":
    raise SystemExit(main())
