#!/usr/bin/env python3
"""Render the fleet table from docs/00-control/hx-fleet.tsv into the documents.

The 17-server map was typed by hand in six places. They agreed on the day they
were written, which is the only day that is ever true. The TSV is now the
source; every table below is generated from it.

A document opts in by carrying a marker pair:

    <!-- HX-FLEET:TABLE columns=id,ip,role,state -->
    ...generated table...
    <!-- /HX-FLEET:TABLE -->

Usage:
  hx_fleet.py            regenerate every marked table and the shell IP map
  hx_fleet.py --check    exit 1 if any generated block is stale (CI mode)

Also writes docs/03-runbooks/common/hx-fleet-ips.env so the runbooks read the
same source instead of carrying their own copy of the host -> IP map.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TSV = REPO / "docs/00-control/hx-fleet.tsv"
IPS_ENV = REPO / "docs/03-runbooks/common/hx-fleet-ips.env"

HEADINGS = {
    "id": "Server",
    "ip": "IP",
    "role": "Assignment",
    "state": "State",
    "gate": "Gate",
    "note": "Notes",
}
BOLD = {"state", "gate"}   # columns rendered bold so status reads at a glance
CODE = {"ip"}              # columns rendered as code

BLOCK = re.compile(
    r"(<!-- HX-FLEET:TABLE columns=([a-z,]+) -->\n)(.*?)(<!-- /HX-FLEET:TABLE -->)",
    re.S,
)


def rows() -> list[dict[str, str]]:
    with TSV.open(encoding="utf-8", newline="") as fh:
        data = list(csv.DictReader(fh, delimiter="\t"))
    if not data:
        raise SystemExit(f"ERROR: {TSV} has no rows")
    return data


def cell(row: dict[str, str], col: str) -> str:
    value = (row.get(col) or "").strip()
    if not value:
        return "—"
    if col in CODE:
        return f"`{value}`"
    if col in BOLD:
        return "—" if value == "-" else f"**{value.replace('_', ' ')}**"
    return value


def table(cols: list[str], data: list[dict[str, str]]) -> str:
    head = "| " + " | ".join(HEADINGS.get(c, c) for c in cols) + " |"
    rule = "|" + "|".join("---" for _ in cols) + "|"
    body = [
        "| " + " | ".join(cell(r, c) for c in cols) + " |"
        for r in data
    ]
    return "\n".join([head, rule, *body]) + "\n"


def ips_env(data: list[dict[str, str]]) -> str:
    lines = [
        "# GENERATED from docs/00-control/hx-fleet.tsv by tools/hx-doc/hx-fleet.",
        "# Do not edit. Change the TSV and re-run the generator.",
        "",
        "hx_ip_for() {",
        "  case \"$1\" in",
    ]
    for r in data:
        host = r["id"].strip().lower()
        lines.append(f'    {host}) echo "{r["ip"].strip()}" ;;')
    lines += [
        "    *) return 1 ;;",
        "  esac",
        "}",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    check = "--check" in sys.argv
    data = rows()
    stale: list[str] = []
    written = 0
    blocks = 0

    # Only documents consume the fleet table. tools/ is excluded because its
    # README documents the marker syntax and must not have a table injected
    # into the example.
    targets = [REPO / "README.md"]
    for root in ("docs", "skills"):
        targets += sorted((REPO / root).rglob("*.md"))
    targets = [p for p in targets if p.exists()]

    for md in targets:
        text = md.read_text(encoding="utf-8")
        if "HX-FLEET:TABLE" not in text:
            continue

        def repl(m: re.Match[str]) -> str:
            nonlocal blocks
            blocks += 1
            cols = [c for c in m.group(2).split(",") if c]
            return m.group(1) + table(cols, data) + m.group(4)

        new = BLOCK.sub(repl, text)
        if new == text:
            continue
        rel = md.relative_to(REPO).as_posix()
        if check:
            stale.append(rel)
        else:
            md.write_text(new, encoding="utf-8", newline="\n")
            written += 1

    want_env = ips_env(data)
    have_env = IPS_ENV.read_text(encoding="utf-8") if IPS_ENV.exists() else None
    if have_env != want_env:
        rel = IPS_ENV.relative_to(REPO).as_posix()
        if check:
            stale.append(rel)
        else:
            IPS_ENV.parent.mkdir(parents=True, exist_ok=True)
            IPS_ENV.write_text(want_env, encoding="utf-8", newline="\n")
            written += 1

    if check:
        for s in stale:
            print(f"STALE   {s}")
        if stale:
            print(
                f"\nFAIL: {len(stale)} generated block(s) do not match "
                "docs/00-control/hx-fleet.tsv. Run tools/hx-doc/hx-fleet and commit."
            )
            return 1
        print(f"OK: {blocks} fleet table(s) and the shell IP map are current.")
        return 0

    print(f"Fleet: {len(data)} servers -> {blocks} table(s), {written} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
