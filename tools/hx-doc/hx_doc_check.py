#!/usr/bin/env python3
"""Repository consistency checks for the HX Eco-System documentation set.

Each check exists because the corresponding defect was actually found in this
repository. The check is the thing that stops it coming back.

  links       every internal path reference resolves, unless it is an
              explicitly declared forward reference
  vocabulary  SKILL-REGISTRY.md uses only lifecycle states that
              SKILL-GOVERNANCE.md defines
  frontmatter active control documents carry document/status/date
  duplicates  no versioned or dated duplicate of an active document
  evidence    .gitignore cannot swallow retained evidence

Usage:  hx_doc_check.py [--quiet]
Exit 0 when everything passes, 1 otherwise.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# A path reference is a forward reference when the document says so. These are
# the phrasings the repository already uses to declare an intentional gap.
FORWARD_MARKERS = re.compile(
    r"no active|does not exist|did not exist|not yet created|not yet exist"
    r"|authority gap|planned|to be created|when the build reaches"
    r"|external to this repository|not a repository path"
    r"|future `docs/",
    re.I,
)
# Paths that belong to an upstream project, not to this repository.
UPSTREAM_PREFIXES = ("deploy/", "docs/LightRAG", "integrations/", ".agents/")

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_REF = re.compile(r"`((?:\.{0,2}/)?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.(?:md|sh|py|html|yaml|txt))`")

failures: list[str] = []
notes: list[str] = []


# Trees that are not HX documentation and are not ours to lint:
#   .git       plumbing
#   archive    superseded history, never current authority
#   human-html generated output; findings belong in the Markdown source
#   .claude    agent tool wiring, written by the tools themselves
#   graft      a gitignored local code-graph cache, absent in a clean checkout
SKIP_TREES = (".git", "archive", "human-html", ".claude", "graft")


def active_markdown() -> list[Path]:
    out = []
    for p in sorted(REPO.rglob("*.md")):
        parts = p.relative_to(REPO).parts
        if parts[0] in SKIP_TREES:
            continue
        out.append(p)
    return out


def check_links() -> None:
    """Every internal path reference resolves, or is a declared forward ref."""
    bad = 0
    for md in active_markdown():
        text = md.read_text(encoding="utf-8")
        lines = text.split("\n")
        # nearest preceding heading per line, so an "authority gap" section
        # covers the bullets underneath it
        heading_for: list[str] = []
        current = ""
        for line in lines:
            if line.startswith("#"):
                current = line
            heading_for.append(current)

        for kind, pattern in (("link", MD_LINK), ("ref", PATH_REF)):
            for lineno, line in enumerate(lines):
                for m in pattern.finditer(line):
                    target = m.group(1).split("#")[0]
                    if not target or target.startswith(("http", "mailto")):
                        continue
                    if target.lstrip("/").startswith(UPSTREAM_PREFIXES):
                        continue
                    candidates = [
                        (md.parent / target).resolve(),
                        (REPO / target.lstrip("/")).resolve(),
                    ]
                    if any(c.exists() for c in candidates):
                        continue
                    context = line + " " + heading_for[lineno]
                    if FORWARD_MARKERS.search(context):
                        continue
                    rel = md.relative_to(REPO).as_posix()
                    failures.append(f"links: {rel}:{lineno + 1} broken {kind} -> {target}")
                    bad += 1
    if not bad:
        notes.append("links: every internal reference resolves")


def check_vocabulary() -> None:
    """The registry may only use lifecycle states the governance doc defines."""
    gov = (REPO / "skills/SKILL-GOVERNANCE.md").read_text(encoding="utf-8")
    reg = (REPO / "skills/SKILL-REGISTRY.md").read_text(encoding="utf-8")
    section = re.search(r"## 4\. Registry status(.*?)(?=\n## )", gov, re.S)
    if not section:
        failures.append("vocabulary: cannot find 'Registry status' in SKILL-GOVERNANCE.md")
        return
    defined = set(re.findall(r"`([A-Z][A-Z_]+)`", section.group(1)))
    used = set(re.findall(r"`([A-Z][A-Z_]+(?: / [A-Z_]+)?)`", reg))
    used |= set(re.findall(r"\*\*([A-Z][A-Z_]+)\*\*", reg))
    # classification names are a separate vocabulary defined in section 3
    classes = set(re.findall(r"### ([A-Z_]+)", gov))
    unknown = sorted(
        s for s in used
        if s.split(" / ")[0] not in defined and s not in classes and s != "TBD"
    )
    if unknown:
        for u in unknown:
            failures.append(
                f"vocabulary: SKILL-REGISTRY.md uses '{u}', "
                f"not defined in SKILL-GOVERNANCE.md section 4"
            )
    else:
        notes.append(f"vocabulary: registry states all defined ({len(defined)} allowed)")


def check_frontmatter() -> None:
    """Active control documents carry document/status/date."""
    missing = 0
    for md in sorted((REPO / "docs/00-control").glob("*.md")):
        if md.name.startswith("_"):
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            notes.append(f"frontmatter: {md.name} has none (operational file, allowed)")
            continue
        head = text.split("---", 2)[1]
        for key in ("document", "status", "date"):
            if not re.search(rf"^{key}:", head, re.M):
                failures.append(f"frontmatter: docs/00-control/{md.name} missing '{key}'")
                missing += 1
    if not missing:
        notes.append("frontmatter: control documents complete")


def check_duplicates() -> None:
    """DOCUMENT-CONTROL.md: exactly one active copy, stable filenames."""
    pattern = re.compile(r"(-v\d+(\.\d+)*|\(\d+\)|final-final|_\d{8}|-\d{4}-\d{2}-\d{2})\.md$")
    bad = 0
    for md in active_markdown():
        if pattern.search(md.name):
            failures.append(
                f"duplicates: {md.relative_to(REPO).as_posix()} has a version/date in "
                "its filename; active documents use stable names"
            )
            bad += 1
    if not bad:
        notes.append("duplicates: no versioned filenames in the active tree")


def check_evidence_not_ignored() -> None:
    """.gitignore must not swallow retained evidence."""
    probe = "docs/05-evidence/hx-9/postgresql/RUNID/supporting/session.log"
    r = subprocess.run(
        ["git", "-C", str(REPO), "check-ignore", "-q", probe],
        capture_output=True,
    )
    if r.returncode == 0:
        failures.append(
            "evidence: .gitignore would silently drop retained evidence logs "
            f"(matched {probe})"
        )
    else:
        notes.append("evidence: retained evidence logs are committable")


def main() -> int:
    quiet = "--quiet" in sys.argv
    for fn in (
        check_links,
        check_vocabulary,
        check_frontmatter,
        check_duplicates,
        check_evidence_not_ignored,
    ):
        fn()

    if not quiet:
        for n in notes:
            print(f"OK    {n}")
    for f in failures:
        print(f"FAIL  {f}")

    print()
    if failures:
        print(f"hx-doc-check: {len(failures)} problem(s) found.")
        return 1
    print(f"hx-doc-check: PASS ({len(notes)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
