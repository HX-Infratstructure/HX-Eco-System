#!/usr/bin/env python3
"""Generate and validate the smoke-test proof DAG from docs/00-control/hx-proof.tsv.

The proof chain is the dependency structure this programme actually runs on:
each step declares which earlier proof it needs before it may run. It used to
live in two hand-maintained places that could disagree - a per-phase table and
a mermaid diagram - and nothing checked either against the other. The diagram
had 19 nodes against the table's 29 steps: every MCP companion gate, both Web
UI gates and the reranker were missing from the picture.

The TSV is now the source. The tables and the diagram are generated from it,
the same way tools/hx-doc/hx-fleet generates the fleet tables.

Usage:
  hx_proof.py                 regenerate every marked block
  hx_proof.py --check         exit 1 if a generated block is stale (CI mode)
  hx_proof.py --ready <id>    can this step run yet, given what has passed
  hx_proof.py --list          one line per step, with readiness
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
TSV = REPO / "docs/00-control/hx-proof.tsv"
ROADMAP = REPO / "docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md"
FLEET = REPO / "docs/00-control/hx-fleet.tsv"

PASSED = "PASS"
BLOCK = re.compile(
    r"(<!-- HX-PROOF:(TABLE phase=([0-9A-G]+)|DAG) -->\n)(.*?)(<!-- /HX-PROOF -->)",
    re.S,
)

PHASE_TITLES = {
    "0": "Phase 0 — existing cornerstone proof",
    "A": "Phase A — inference proof and CentCom activation",
    "B": "Phase B — state and retrieval substrate",
    "C": "Phase C — routing, MCP development, and control capability",
    "D": "Phase D — knowledge acquisition",
    "E": "Phase E — RAG and memory",
    "F": "Phase F — agent and workflow consumers",
    "G": "Phase G — user interaction",
}


def steps() -> dict[str, dict[str, str]]:
    with TSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if not rows:
        raise SystemExit(f"ERROR: {TSV} has no rows")
    return {r["id"].strip(): {k: (v or "").strip() for k, v in r.items()} for r in rows}


def requires_of(step: dict[str, str]) -> list[str]:
    raw = step.get("requires", "NONE")
    if raw in ("", "NONE", "-"):
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


# --------------------------------------------------------------------------
# Validation. Every check here exists because the hand-maintained version
# could get it wrong and nothing would say so.
# --------------------------------------------------------------------------

def validate(all_steps: dict[str, dict[str, str]]) -> list[str]:
    problems: list[str] = []

    hosts = set()
    if FLEET.exists():
        with FLEET.open(encoding="utf-8", newline="") as fh:
            hosts = {r["id"].strip().lower() for r in csv.DictReader(fh, delimiter="\t")}

    for sid, step in all_steps.items():
        for dep in requires_of(step):
            if dep not in all_steps:
                problems.append(f"{sid}: requires '{dep}', which is not a step")

        authority = step.get("authority", "")
        if authority and authority not in ("-", "NONE") and not (REPO / authority).exists():
            problems.append(f"{sid}: authority not found - {authority}")

        sut = step.get("sut", "").lower()
        if sut not in ("", "-") and hosts and sut not in hosts:
            problems.append(f"{sid}: sut '{sut}' is not a host in hx-fleet.tsv")

        status = step.get("status", "")
        if status not in ("NOT_RUN", "PASS", "FAIL", "NOT_EXECUTABLE"):
            problems.append(f"{sid}: status '{status}' is not a recognised state")

    # Cycles. A proof chain that loops cannot be satisfied by anything.
    colour: dict[str, int] = {}

    def walk(node: str, trail: list[str]) -> None:
        colour[node] = 1
        for dep in requires_of(all_steps.get(node, {})):
            if dep not in all_steps:
                continue
            if colour.get(dep) == 1:
                cycle = " -> ".join(trail + [node, dep])
                problems.append(f"cycle in the proof chain: {cycle}")
            elif colour.get(dep, 0) == 0:
                walk(dep, trail + [node])
        colour[node] = 2

    for sid in all_steps:
        if colour.get(sid, 0) == 0:
            walk(sid, [])

    return problems


# --------------------------------------------------------------------------
# Readiness
# --------------------------------------------------------------------------

def blockers(sid: str, all_steps: dict[str, dict[str, str]]) -> list[str]:
    """Required steps that have not passed. Empty means ready to run."""
    return [
        dep for dep in requires_of(all_steps.get(sid, {}))
        if all_steps.get(dep, {}).get("status") != PASSED
    ]


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def phase_table(phase: str, all_steps: dict[str, dict[str, str]]) -> str:
    rows = [s for s in all_steps.values() if s["phase"] == phase]
    head = "| Step | SUT | Proof | Authority | Requires | Limited integration | Status |"
    rule = "|---|---|---|---|---|---|---|"
    body = []
    for s in rows:
        auth = s["authority"]
        auth_cell = f"[`{Path(auth).name}`](../../{auth})" if auth not in ("", "-") else "—"
        req = s["requires"] if s["requires"] not in ("", "NONE") else "—"
        integ = s["integration"] if s["integration"] not in ("", "NONE", "-") else "None"
        status = s["status"].replace("_", " ")
        marker = "**PASS**" if s["status"] == PASSED else status
        body.append(
            f"| **{s['id']}** | {s['sut']} | {s['component']} | {auth_cell} "
            f"| {req} | {integ} | {marker} |"
        )
    return "\n".join([head, rule, *body]) + "\n"


def dag(all_steps: dict[str, dict[str, str]]) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for sid, s in all_steps.items():
        label = f"<b>{sid}</b><br/>{s['component']}"
        lines.append(f'    {sid}["{label}"]')
    lines.append("")
    for sid, s in all_steps.items():
        for dep in requires_of(s):
            lines.append(f"    {dep} --> {sid}")
    lines.append("```")
    return "\n".join(lines) + "\n"


def render(all_steps: dict[str, dict[str, str]], check: bool) -> tuple[int, list[str]]:
    text = ROADMAP.read_text(encoding="utf-8")
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        kind, phase = m.group(2), m.group(3)
        body = phase_table(phase, all_steps) if kind.startswith("TABLE") else dag(all_steps)
        return m.group(1) + body + m.group(5)

    new = BLOCK.sub(repl, text)
    if new == text:
        return count, []
    rel = ROADMAP.relative_to(REPO).as_posix()
    if check:
        return count, [rel]
    ROADMAP.write_text(new, encoding="utf-8", newline="\n")
    return count, [rel]


def main() -> int:
    argv = sys.argv[1:]
    all_steps = steps()

    problems = validate(all_steps)
    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        print(f"\nhx-proof: {len(problems)} problem(s) in {TSV.relative_to(REPO).as_posix()}.")
        return 1

    if "--ready" in argv:
        i = argv.index("--ready")
        if i + 1 >= len(argv):
            print("usage: hx_proof.py --ready <step-id>", file=sys.stderr)
            return 2
        sid = argv[i + 1].strip().upper()
        if sid not in all_steps:
            print(f"ERROR: no step '{sid}'. Known: {', '.join(all_steps)}", file=sys.stderr)
            return 2
        step = all_steps[sid]
        blocked = blockers(sid, all_steps)
        print(f"{sid} — {step['component']} on {step['sut']}")
        print(f"  authority: {step['authority']}")
        print(f"  status:    {step['status']}")
        if not blocked:
            print("  READY — every required prior proof has passed.")
            return 0
        print("  NOT READY — these must pass first:")
        for dep in blocked:
            d = all_steps[dep]
            print(f"    {dep}  {d['component']}  [{d['status']}]")
        return 1

    if "--list" in argv:
        for sid, s in all_steps.items():
            blocked = blockers(sid, all_steps)
            if s["status"] == PASSED:
                mark = "PASS   "
            elif blocked:
                mark = "blocked"
            else:
                mark = "READY  "
            waiting = f"  waits on {','.join(blocked)}" if blocked else ""
            print(f"{mark} {sid:3} {s['sut']:6} {s['component'][:44]:44}{waiting}")
        ready = [s for s in all_steps if not blockers(s, all_steps)
                 and all_steps[s]["status"] != PASSED]
        print(f"\n{len(all_steps)} steps. Runnable now: {', '.join(ready) or 'none'}")
        return 0

    check = "--check" in argv
    count, stale = render(all_steps, check)

    if check:
        if stale:
            for s in stale:
                print(f"STALE   {s}")
            print("\nFAIL: generated blocks do not match hx-proof.tsv. "
                  "Run tools/hx-doc/hx-proof and commit.")
            return 1
        print(f"OK: {len(all_steps)} steps, {count} generated block(s) current.")
        return 0

    print(f"Proof chain: {len(all_steps)} steps -> {count} block(s) regenerated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
