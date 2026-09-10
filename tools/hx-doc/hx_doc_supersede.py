#!/usr/bin/env python3
"""Perform the DOCUMENT-CONTROL.md supersession procedure in one command.

The rule is six manual steps. The history shows six commits spent archiving a
single README, plus three stray marker files created and then deleted. The rule
is fine; doing it by hand is where the churn comes from.

Given an active document, this:
  1. creates archive/<today>/<same-path>/
  2. copies the current Markdown there with a --suffix
  3. archives the matching human-html mirror if one exists
  4. leaves the active file in place for you to edit
  5. reminds you to re-render the mirror

Usage:
  hx_doc_supersede.py docs/00-control/DECISIONS.md --suffix pre-d019
  hx_doc_supersede.py skills/SKILL-REGISTRY.md --suffix v1.6 --dry-run
"""
from __future__ import annotations

import shutil
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    args: list[str] = []
    suffix = ""
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--suffix" and i + 1 < len(argv):
            suffix = argv[i + 1]
            i += 2
            continue
        if a.startswith("--suffix="):
            suffix = a.split("=", 1)[1]
        elif not a.startswith("--"):
            args.append(a)
        i += 1

    if len(args) != 1 or not suffix:
        print(__doc__.strip())
        return 2

    active = (REPO / args[0]).resolve()
    if not active.exists():
        print(f"ERROR: {args[0]} does not exist", file=sys.stderr)
        return 1
    try:
        rel = active.relative_to(REPO)
    except ValueError:
        print(f"ERROR: {args[0]} is outside the repository", file=sys.stderr)
        return 1
    if rel.parts[0] in ("archive", "human-html"):
        print("ERROR: that path is archive or generated output, not an active document",
              file=sys.stderr)
        return 1

    stamp = date.today().isoformat()
    archive_dir = REPO / "archive" / stamp / rel.parent
    archived = archive_dir / f"{active.stem}-{suffix}{active.suffix}"

    if archived.exists():
        print(f"ERROR: {archived.relative_to(REPO).as_posix()} already exists; "
              "choose another --suffix", file=sys.stderr)
        return 1

    # The mirror is generated, so archive the source's rendered form only when
    # one is already committed.
    mirror = None
    if rel.parts[0] == "docs":
        mirror = REPO / "human-html" / Path(*rel.parts[1:]).with_suffix(".html")
    elif rel.parts[0] == "skills":
        mirror = REPO / "human-html/skills" / Path(*rel.parts[1:]).with_suffix(".html")
    elif rel.name == "README.md":
        mirror = REPO / "human-html/README.html"
    mirror_archived = None
    if mirror and mirror.exists():
        mirror_rel = mirror.relative_to(REPO)
        mirror_archived = (REPO / "archive" / stamp / mirror_rel.parent /
                           f"{mirror.stem}-{suffix}{mirror.suffix}")

    plan = [f"archive  {archived.relative_to(REPO).as_posix()}"]
    if mirror_archived:
        plan.append(f"archive  {mirror_archived.relative_to(REPO).as_posix()}")

    if dry:
        print("dry run, nothing written:")
        for line in plan:
            print("  " + line)
        return 0

    archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(active, archived)
    if mirror_archived:
        mirror_archived.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(mirror, mirror_archived)

    for line in plan:
        print(line)
    print(f"\nActive file untouched: {rel.as_posix()}")
    print("Now edit it, then run:")
    print("  tools/hx-doc/hx-render-html")
    print("  tools/hx-doc/hx-doc-check")
    print("Commit the edit and the archive copy together, in one commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
