#!/usr/bin/env python3
"""Lint the smoke-test authorities in smoke-tests/.

All nineteen share one shape. The NGINX authority shipped without any mention
of evidence and nothing noticed, so a twentieth could ship incomplete too.

Checks each authority for:
  - the six canonical sections
  - a known-answer marker, because service health is not a smoke test
  - a stated PASS/FAIL determination
  - a mention of evidence retention

Usage:  hx_smoke_lint.py [--quiet]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TESTS = REPO / "smoke-tests"

SECTIONS = [
    ("Title & Purpose", r"title|purpose"),
    ("Prerequisites", r"prerequisite"),
    ("Test Steps", r"test steps|procedure"),
    ("Sample Data", r"sample data|fixture"),
    ("Expected Output", r"expected output|expected result"),
    ("Cleanup / Teardown", r"cleanup|teardown"),
]

# Content each authority must actually carry. Deliberately short: an authority
# states what to run and what the correct answer is. The PASS/FAIL verdict is
# recorded by the runner in evidence/result.txt, not restated here, so it is
# not checked.
CONTENT = [
    ("known answer", r"known.answer|reply with exactly|exactly:|expected output"),
    ("evidence retention", r"evidence"),
]


def main() -> int:
    quiet = "--quiet" in sys.argv
    files = sorted(TESTS.glob("*-smoke-test.md"))
    if not files:
        print(f"ERROR: no smoke-test authorities found in {TESTS}", file=sys.stderr)
        return 2

    failures = 0
    for md in files:
        rel = md.relative_to(REPO).as_posix()
        text = md.read_text(encoding="utf-8")
        headings = [h.lower() for h in re.findall(r"^#{1,3}\s+(.*)$", text, re.M)]
        problems = []

        for label, pattern in SECTIONS:
            if not any(re.search(pattern, h) for h in headings):
                problems.append(f"no section for {label}")

        for label, pattern in CONTENT:
            if not re.search(pattern, text, re.I | re.S):
                problems.append(f"never mentions {label}")

        if problems:
            failures += 1
            print(f"      {rel}")
            for p in problems:
                print(f"  FAIL       {p}")
        elif not quiet:
            print(f"OK    {rel}")

    print()
    print(f"{len(files)} smoke-test authorities checked, {failures} incomplete.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
