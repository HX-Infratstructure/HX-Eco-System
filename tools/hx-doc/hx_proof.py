#!/usr/bin/env python3
"""Generate and validate the smoke-test proof DAG from docs/00-control/hx-proof.tsv.

The proof chain is the dependency structure this programme actually runs on:
each step declares which earlier proof it needs before it may run. It used to
live in two hand-maintained places that could disagree - a per-phase table and
a mermaid diagram - and nothing checked either against the other. The diagram
carried 19 nodes - the foundation plus 18 of the 29 steps - so 11 steps were
missing from the picture: every MCP companion gate, both Web UI gates and the
reranker.

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
    """Every proof step from hx-proof.tsv, keyed by id, in file order.

    Refuses a blank or duplicate id: either one silently overwrote an
    earlier row, dropping a step from the tables and the DAG while
    validation still reported success.
    """
    with TSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        headers = set(reader.fieldnames or [])
        rows = list(reader)
    if not rows:
        raise SystemExit(f"ERROR: {TSV} has no rows")

    required = {"id", "phase", "sut", "component", "authority",
                "requires", "integration", "status"}
    missing = sorted(required - headers)
    if missing:
        raise SystemExit(f"ERROR: {TSV} is missing column(s): {', '.join(missing)}")

    # A blank or duplicate id silently overwrote an earlier row, dropping a
    # proof step from the generated table and the DAG while validation still
    # reported success.
    out: dict[str, dict[str, str]] = {}
    for n, r in enumerate(rows, start=2):
        sid = (r.get("id") or "").strip()
        if not sid:
            raise SystemExit(f"ERROR: {TSV} line {n}: blank id")
        if sid in out:
            raise SystemExit(f"ERROR: {TSV} line {n}: duplicate id '{sid}'")
        out[sid] = {k: (v or "").strip() for k, v in r.items()}
    return out


def requires_of(step: dict[str, str]) -> list[str]:
    """The step ids this step depends on. NONE and - both mean no dependency."""
    raw = step.get("requires", "NONE")
    if raw in ("", "NONE", "-"):
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


# --------------------------------------------------------------------------
# Validation. Every check here exists because the hand-maintained version
# could get it wrong and nothing would say so.
# --------------------------------------------------------------------------

def validate(all_steps: dict[str, dict[str, str]]) -> list[str]:
    """Problems found in the step table; an empty list means it is sound.

    Checks the fleet host, the authority file, the status value, that every
    named dependency exists, and that the dependency graph has no cycle.
    """
    problems: list[str] = []

    # An unreadable or empty fleet inventory used to leave hosts empty, which
    # skipped the SUT check entirely and let a misspelled host validate clean.
    # A check that cannot fail is a defect.
    if not FLEET.exists():
        problems.append(f"fleet inventory not found: {FLEET.relative_to(REPO).as_posix()}")
        hosts: set[str] = set()
    else:
        with FLEET.open(encoding="utf-8", newline="") as fh:
            hosts = {(r.get("id") or "").strip().lower()
                     for r in csv.DictReader(fh, delimiter="\t")}
        hosts.discard("")
        if not hosts:
            problems.append(
                f"fleet inventory has no hosts: {FLEET.relative_to(REPO).as_posix()}")

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
        """Depth-first colouring that records the trail of any cycle found."""
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

# A step in one of these states cannot be run now regardless of its
# dependencies. NOT_EXECUTABLE means an implementation decision is still open.
NOT_RUNNABLE = {"NOT_EXECUTABLE"}


def blockers(sid: str, all_steps: dict[str, dict[str, str]]) -> list[str]:
    """Required steps that have not passed. Empty does not by itself mean ready."""
    return [
        dep for dep in requires_of(all_steps.get(sid, {}))
        if all_steps.get(dep, {}).get("status") != PASSED
    ]


def runnable(sid: str, all_steps: dict[str, dict[str, str]]) -> bool:
    """Ready to execute now: dependencies satisfied and not itself blocked."""
    step = all_steps.get(sid, {})
    if step.get("status") in NOT_RUNNABLE or step.get("status") == PASSED:
        return False
    return not blockers(sid, all_steps)


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def phase_table(phase: str, all_steps: dict[str, dict[str, str]]) -> str:
    """The Markdown table of one phase, as written into the roadmap."""
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
    """The whole dependency graph as a mermaid flowchart."""
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
    """Write the generated roadmap blocks, or report drift when check is set.

    Returns the number of blocks handled and the problems found. A missing
    or repeated marker is drift in itself: the surrounding text is
    unchanged, so comparing content alone reported a lost or duplicated
    table as current.
    """
    text = ROADMAP.read_text(encoding="utf-8")
    count = 0

    def repl(m: re.Match[str]) -> str:
        """Replace one marked block with freshly generated content."""
        nonlocal count
        count += 1
        kind, phase = m.group(2), m.group(3)
        body = phase_table(phase, all_steps) if kind.startswith("TABLE") else dag(all_steps)
        return m.group(1) + body + m.group(5)

    new = BLOCK.sub(repl, text)
    rel = ROADMAP.relative_to(REPO).as_posix()

    # A deleted marker leaves the surrounding text untouched, so comparing
    # content alone reported success for a roadmap that had silently lost a
    # phase table or the diagram. Require the full marker set.
    expected = {s["phase"] for s in all_steps.values()}
    # Count the markers, do not collect them into a set. Two markers for the
    # same phase render two identical tables, and a set reduced that to one
    # value, so --check reported no drift for a duplicated table.
    found_tables = re.findall(r"<!-- HX-PROOF:TABLE phase=([0-9A-G]+) -->", text)
    dag_blocks = len(re.findall(r"<!-- HX-PROOF:DAG -->", text))
    gaps = []
    for phase in sorted(expected | set(found_tables)):
        seen = found_tables.count(phase)
        if phase not in expected:
            gaps.append(f"{rel}: table marker for phase {phase}, which has no steps")
        elif seen == 0:
            gaps.append(f"{rel}: no generated table for phase {phase}")
        elif seen > 1:
            gaps.append(
                f"{rel}: expected one HX-PROOF:TABLE phase={phase} block, found {seen}"
            )
    if dag_blocks != 1:
        gaps.append(f"{rel}: expected exactly one HX-PROOF:DAG block, found {dag_blocks}")
    if gaps:
        return count, gaps

    if new == text:
        return count, []
    if check:
        return count, [rel]
    ROADMAP.write_text(new, encoding="utf-8", newline="\n")
    return count, [rel]


def main() -> int:
    """Command entry point. Returns the process exit status."""
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
        if step["status"] in NOT_RUNNABLE:
            print(f"  NOT RUNNABLE — status is {step['status']}; an implementation")
            print("  decision is still open. Dependencies are not the blocker.")
            return 1
        # runnable() already excludes PASS. Reporting a closed proof as READY
        # made --ready and runnable() disagree, and invited a re-run that
        # would overwrite accepted evidence.
        if step["status"] == PASSED:
            print("  ALREADY PASSED — this proof is closed. There is nothing to run.")
            return 1
        if runnable(sid, all_steps):
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
            elif s["status"] in NOT_RUNNABLE:
                mark = "n/a    "
            elif blocked:
                mark = "blocked"
            else:
                mark = "READY  "
            waiting = f"  waits on {','.join(blocked)}" if blocked else ""
            print(f"{mark} {sid:3} {s['sut']:6} {s['component'][:44]:44}{waiting}")
        ready = [s for s in all_steps if runnable(s, all_steps)]
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
