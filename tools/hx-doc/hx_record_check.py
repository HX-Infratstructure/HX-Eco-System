#!/usr/bin/env python3
"""Check server records against the template, and surface open items.

The template is otherwise only advice. This makes it a gate, and keeps the
UNRESOLVED provenance fields visible instead of letting them fade into a file
nobody re-reads.

Reports per record:
  MISSING    a required section the template defines is absent
  UNRESOLVED a field explicitly recorded as not yet known
  DRIFT      the record's state disagrees with docs/00-control/hx-fleet.tsv

Usage:
  hx_record_check.py             report
  hx_record_check.py --strict    exit 1 on UNRESOLVED as well as MISSING/DRIFT
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RECORDS = REPO / "docs/02-server-records"
TSV = REPO / "docs/00-control/hx-fleet.tsv"

# Section headings the template requires, matched loosely on the key words so
# a record can word its own heading naturally.
REQUIRED = [
    ("Identity and Network", r"identity and network"),
    ("Operating System", r"operating system"),
    ("GPU Configuration", r"gpu"),
    ("Storage Layout", r"storage"),
    ("Runtime", r"runtime|ollama runtime"),
    ("Model / Application Provenance", r"provenance|model$|model\b"),
    ("Functional Validation", r"functional validation|validation"),
    ("Final State", r"final .*state"),
]


def fleet() -> dict[str, dict[str, str]]:
    with TSV.open(encoding="utf-8", newline="") as fh:
        return {r["id"].strip(): r for r in csv.DictReader(fh, delimiter="\t")}


def main() -> int:
    strict = "--strict" in sys.argv
    servers = fleet()
    hard = soft = 0
    checked = 0

    for md in sorted(RECORDS.glob("*.md")):
        if md.name.startswith("_"):
            continue
        checked += 1
        rel = md.relative_to(REPO).as_posix()
        text = md.read_text(encoding="utf-8")
        headings = [h.lower() for h in re.findall(r"^#{1,3}\s+(.*)$", text, re.M)]

        problems: list[tuple[str, str]] = []

        # A record may declare sections that genuinely do not apply, as the
        # template instructs. One line, with a reason:
        #   **Not applicable:** GPU, Storage, Runtime - no GPU or application
        #   workload on this host.
        na = re.search(r"\*\*Not applicable:\*\*\s*(.+?)\s*[-—]\s*(.+)", text)
        exempt = set()
        if na:
            exempt = {s.strip().lower() for s in na.group(1).split(",") if s.strip()}

        for label, pattern in REQUIRED:
            if any(re.search(pattern, h) for h in headings):
                continue
            if any(e in label.lower() for e in exempt):
                continue
            problems.append(("MISSING", f"no section for {label}"))

        for m in re.finditer(r"^\s*([A-Za-z][\w /-]*?):\s*UNRESOLVED", text, re.M):
            problems.append(("UNRESOLVED", m.group(1).strip()))

        row = servers.get(md.stem)
        if row is None:
            problems.append(("DRIFT", f"{md.stem} is not in hx-fleet.tsv"))
        else:
            declared = row.get("state", "").strip().replace("_", " ").upper()
            stated = re.search(r"^\*\*(?:Build )?[Ss]tate:?\*\*\s*(.+?)\s*$", text, re.M)
            if not stated:
                problems.append(
                    ("DRIFT", f"no '**State:**' line; hx-fleet.tsv says '{declared}'"))
            else:
                # Compare the whole normalised state. The old test took the
                # first word of the fleet value and asked whether it appeared
                # anywhere in the record, so NOT STARTED was satisfied by
                # NOT APPLICABLE, and IN PROGRESS by INSTALLED.
                got = stated.group(1).strip().strip("*").replace("_", " ").upper()
                # HX-1 to HX-3 closed before the scaffold existed and state the
                # state and the gate on one line as "PASS / CLOSED". Compare the
                # state part; the gate has its own check.
                got = got.split("/")[0]
                got = " ".join(got.split())
                if got != " ".join(declared.split()):
                    problems.append(
                        ("DRIFT", f"record says '{got}', hx-fleet.tsv says '{declared}'"))

        if not problems:
            print(f"OK    {rel}")
            continue

        print(f"      {rel}")
        for kind, detail in problems:
            print(f"  {kind:11}{detail}")
            if kind == "UNRESOLVED":
                soft += 1
            else:
                hard += 1

    print()
    print(f"{checked} record(s) checked, {hard} problem(s), {soft} unresolved field(s).")
    if soft:
        print("UNRESOLVED fields are recorded gaps, not errors. Close them while the")
        print("server is still reachable; --strict fails the build on them.")
    return 1 if (hard or (strict and soft)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
