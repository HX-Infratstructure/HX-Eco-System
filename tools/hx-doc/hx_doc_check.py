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

import posixpath
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
# Absolute paths that belong to a server, not to this repository. A server
# record has to be able to name the file that holds a host's configuration -
# `/etc/netplan/50-cloud-init.yaml` - without the gate reading it as a
# repository reference. Root-relative repository paths such as `/docs/...` are
# not listed here and are still resolved and checked. The target is normalised
# first: `/etc/../docs/x.md` is spelt through a system root but names a
# repository path, so it is classified by where it resolves, not how it reads.
SYSTEM_ROOTS = ("/etc/", "/var/", "/usr/", "/srv/", "/opt/", "/run/",
                "/boot/", "/proc/", "/sys/", "/dev/", "/tmp/")

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
# Generated or vendored trees. Nothing here is authored, so a link, a
# heading or a filename inside one is not a finding against this repository.
# openwiki/ is written by the OpenWiki CLI and replaced wholesale by
# `openwiki --init`, the same class as human-html/.
# Paths a ratified decision removed. The tool that wrote one can scaffold it
# again without being asked, so absence is asserted rather than assumed.
WITHDRAWN_PATHS = {
    ".github/workflows/openwiki-update.yml":
        "D-025 withdrew scheduled OpenWiki generation and deleted this file",
}

SKIP_TREES = (".git", "archive", "human-html", ".claude", "graft", "openwiki")


def active_markdown() -> list[Path]:
    """Every current Markdown document, excluding generated and archived trees."""
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
                    if posixpath.normpath(target).startswith(SYSTEM_ROOTS):
                        continue
                    if target.lstrip("/").startswith(UPSTREAM_PREFIXES):
                        continue
                    candidates = [
                        (md.parent / target).resolve(),
                        (REPO / target.lstrip("/")).resolve(),
                    ]
                    # A traversal such as ../../outside/file.md resolved out of
                    # the repository and passed on whatever happened to exist on
                    # the machine running the check.
                    candidates = [c for c in candidates if c.is_relative_to(REPO)]
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
    # git check-ignore: 0 means ignored, 1 means not ignored, anything else is
    # an error. Treating "anything but 0" as success let a git failure, such as
    # running outside a work tree, report the evidence path as committable.
    if r.returncode == 0:
        failures.append(
            "evidence: .gitignore would silently drop retained evidence logs "
            f"(matched {probe})"
        )
    elif r.returncode == 1:
        notes.append("evidence: retained evidence logs are committable")
    else:
        failures.append(
            f"evidence: git check-ignore failed (exit {r.returncode}); "
            "the evidence path was not checked"
        )


def check_unit_claims() -> None:
    """A block may only report a unit it actually creates.

    hx_app_done prints a reboot-persistence check. Five blocks named a unit
    that nothing in the file creates, so the operator was told to run
    `systemctl is-active hx-<name>` for a unit that does not exist, and that
    check could only fail. A library or CLI passes NONE and states the command
    to run instead.
    """
    common = REPO / "docs/03-runbooks/common"
    bad = 0
    for sh in sorted(common.glob("*.sh")):
        raw = sh.read_text(encoding="utf-8")
        # Comments mention unit paths, and so does an rm. Neither creates
        # anything, and matching them would make this check unfailable.
        code = "\n".join(
            line for line in raw.splitlines() if not line.lstrip().startswith("#")
        )
        # A trailing backslash continues one command across lines, so join
        # them the way the shell does. Without this a call whose arguments
        # wrap reads as two statements and the unit name is never found.
        code = code.replace("\\\n", " ")
        for unit in re.findall(r"hx_app_done\s+([A-Za-z0-9_-]+)", code):
            if unit == "NONE":
                continue
            path = rf"/etc/systemd/system/{re.escape(unit)}\.service"
            creates_it = (
                # Leading long options may precede the unit name, so skip
                # any `--opt value` pairs rather than pinning the name to
                # the first argument. Naming one option here would break
                # the next one.
                re.search(
                    rf"hx_app_unit\s+(?:--\S+\s+\S+\s+)*{re.escape(unit)}\b",
                    code,
                )
                # A write, not merely a mention: tee, cp, install or a redirect.
                or re.search(rf"(tee|cp|install)\b[^\n]*{path}", code)
                or re.search(rf">\s*{path}", code)
            )
            if not creates_it:
                rel = sh.relative_to(REPO).as_posix()
                failures.append(
                    f"units: {rel} reports unit '{unit}' but nothing in the file "
                    "creates it; pass NONE and state the check to run instead"
                )
                bad += 1
    if not bad:
        notes.append("units: every reported unit is created by its own block")


def check_generated_authority_claims() -> None:
    """A generated block may not restate who is authoritative.

    OpenWiki appends a setup block to AGENTS.md and rewrites it on every run.
    The first one said "Treat source code and tests as authoritative", which
    contradicts section 2 of the same file: owner instruction, then the control
    Markdown in docs/ and the acceptance authority in smoke-tests/, then live
    evidence. Source code is not in that list at all.

    A generated block that amends the contract every agent reads first is drift
    with a schedule attached, so the rule is checked and not remembered.

    The limit of this check, stated plainly: it catches the observed wording
    class, an authority claim that never names the control Markdown. It cannot
    prove that some future rewording agrees with section 2.
    """
    text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- OPENWIKI:START -->(.*?)<!-- OPENWIKI:END -->", text, re.S)
    if not m:
        notes.append("authority: AGENTS.md carries no generated block")
        return
    block = m.group(1)
    # Sentence by sentence, and both word orders. A regex anchored on
    # "source code ... authoritative" misses "authoritative sources include
    # source code", which says the same wrong thing backwards. Naming docs/
    # does not license either: section 2 has no entry for source code at all.
    sentences = block.replace("!", ".").replace("?", ".").split(".")
    claims_code = False
    for one in sentences:
        # smoke-tests/ is a directory name, not the word "tests". Leaving it in
        # made section 2's own wording fail this check, because the sentence
        # naming the acceptance authority in smoke-tests/ also says "authority".
        low = one.lower().replace("smoke-tests", " ").replace("gate-tests", " ")
        # Whole words, not substrings: "attests" contains "tests", so a
        # sentence such as "the control Markdown in docs/ attests to the
        # authority order" was refused while claiming nothing.
        words = re.findall("[a-z]+", low)
        pairs = set(zip(words, words[1:]))
        if ("source", "code") not in pairs and "tests" not in words:
            continue
        # "authoritative" and "the authority" say the same thing in different
        # parts of speech.
        if "authorit" not in low:
            continue
        # A sentence that denies it is the correction, not the defect.
        if "not authorit" in low or "never authorit" in low:
            continue
        claims_code = True
        break
    if claims_code:
        failures.append(
            "authority: the generated AGENTS.md block calls source code or "
            "tests authoritative; section 2 does not list them, it lists the "
            "control Markdown in docs/, smoke-tests/, live evidence and the "
            "approved runbook"
        )
        return
    if "authoritative" in block.lower() and "docs/" not in block:
        failures.append(
            "authority: the generated AGENTS.md block makes an authority claim "
            "without naming the control Markdown in docs/; section 2 defines "
            "the truth order and a generated block does not amend it"
        )
        return
    notes.append("authority: the generated AGENTS.md block keeps the truth order")


def _outside_fences(text: str) -> list:
    """Return the lines of text that are not inside a fenced code block.

    Backtick and tilde fences both count. A heading or a table row inside an
    example belongs to the example; letting it through makes these checks pass
    on text that is neither a section nor an index entry.
    """
    kept, fence_char, fence_len = [], None, 0
    for line in text.splitlines():
        # Up to three leading spaces may precede a fence line. Four or more,
        # or a tab, make an indented code block, so such a line neither opens
        # nor closes a fence. Stripping all indentation let a four-space
        # example line open a fence and hide everything after it.
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.lstrip(" ")
        char = stripped[:1]
        run = len(stripped) - len(stripped.lstrip(char)) if char in ("`", "~") else 0
        if indent > 3:
            run = 0
        if fence_char is None:
            if run >= 3:
                fence_char, fence_len = char, run
                continue
            kept.append(line)
        # CommonMark closing rule: the same character, at least as many of it
        # as opened the fence, and nothing after it but whitespace. Comparing
        # only the first three characters let "```not-a-close" end a fence, and
        # let a three-character run end a four-character one, so text inside
        # an example leaked out and was read as structure.
        elif (char == fence_char and run >= fence_len
              and not stripped[run:].strip()):
            fence_char, fence_len = None, 0
    return kept


# A Markdown link destination or an angle-bracket autolink, with a host that
# has a dot in it. "https:// yet" contains a scheme and links nothing.
_UPSTREAM_LINK = re.compile(
    r"\]\(https?://[^\s)/]+\.[^\s)]+\)|<https?://[^\s>/]+\.[^\s>]+>")


def check_tooling_docs() -> None:
    """Every tooling document is complete and ordered, and the index is true.

    CodeRabbit was adopted with its facts spread across three files and no
    document saying what it was. OpenWiki was then adopted the same way. This
    check makes the third repeat fail the build.

    What it enforces: a document in docs/06-tooling/ has the five required
    headings, in the order the index gives, with two distinct real links under
    Upstream, the documentation and the source;
    an index row that names a file has that file; a document that exists is
    linked from a row of the index table. Fenced examples are ignored
    throughout.

    What it cannot enforce, said plainly: nothing here knows that a tool was
    adopted. A row with no file is backlog and is reported, not failed, so the
    gap stays visible instead of turning the build red forever. D-024 carries
    the obligation to add the row.
    """
    home = REPO / "docs/06-tooling"
    index = home / "README.md"
    if not index.exists():
        failures.append("tooling: docs/06-tooling/README.md is missing")
        return
    index_text = index.read_text(encoding="utf-8")

    required = ("What it is", "Why we have it", "When to use it",
                "How to use it", "Upstream")
    bad = 0

    # Parse, do not match substrings, and read only rows of the Index table.
    # "wiki.md" is a substring of "openwiki.md"; a link in prose, or in a
    # fenced example, is not a row a reader scans.
    table, found_index, inside = [], False, False
    for line in _outside_fences(index_text):
        if line.startswith("## "):
            inside = line.strip() == "## Index"
            found_index = found_index or inside
            continue
        if inside and line.lstrip().startswith("|"):
            table.append(line)
    if not found_index:
        failures.append(
            "tooling: docs/06-tooling/README.md has no '## Index' section")
        return
    linked = set(re.findall(r"\[[^\]]+\]\(([A-Za-z0-9._-]+\.md)\)",
                            "\n".join(table)))

    for link in sorted(linked):
        if not (home / link).exists():
            failures.append(
                f"tooling: the index links {link} but docs/06-tooling/{link} "
                "does not exist")
            bad += 1

    for md in sorted(home.glob("*.md")):
        if md.name == "README.md":
            continue
        if md.name not in linked:
            failures.append(
                f"tooling: docs/06-tooling/{md.name} is not linked from the "
                "index, so nobody will find it")
            bad += 1
        # An -agents.md is an operating guide, not a tool description; the
        # five sections belong to the tool's own document.
        if md.name.endswith("-agents.md"):
            continue
        order, body, current = [], {}, None
        for line in _outside_fences(md.read_text(encoding="utf-8")):
            if line.startswith("## "):
                current = line[3:].strip()
                order.append(current)
                body.setdefault(current, [])
            elif current is not None:
                body[current].append(line)
        missing = [section for section in required if section not in order]
        for section in missing:
            failures.append(
                f"tooling: docs/06-tooling/{md.name} has no "
                f"'## {section}' heading")
            bad += 1
        # The index says "in this order". Membership alone let a shuffled
        # document pass.
        if not missing:
            positions = [order.index(section) for section in required]
            if positions != sorted(positions):
                failures.append(
                    f"tooling: docs/06-tooling/{md.name} has the required "
                    "headings out of order; the index requires "
                    + ", ".join(required))
                bad += 1
        # The point of Upstream is that nobody has to search for the product's
        # documentation or its source. The index promises both, so a document
        # needs two distinct real links: one link, or the same URL twice,
        # leaves a reader searching for the other.
        if "Upstream" in body:
            urls = {found.lstrip("](<").rstrip(")>") for found in
                    _UPSTREAM_LINK.findall("\n".join(body["Upstream"]))}
            if not urls:
                failures.append(
                    f"tooling: docs/06-tooling/{md.name} has an 'Upstream' "
                    "heading with no link under it")
                bad += 1
            elif len(urls) < 2:
                failures.append(
                    f"tooling: docs/06-tooling/{md.name} has only one link "
                    "under 'Upstream'; it needs the documentation and the source")
                bad += 1

    # Rows of the Index table only. Counting the phrase across the whole README
    # let a sentence of prose inflate the number of undocumented tools.
    pending = sum(1 for row in table if "not written yet" in row)
    if not bad:
        notes.append("tooling: every tooling document is complete and indexed")
    # D-024 says a backlog row is reported on every run. The count used to
    # ride on the all-complete note, so any failure in this check hid it.
    if pending:
        notes.append(
            f"tooling: {pending} tool(s) still undocumented, listed in the index")


def check_withdrawn_paths() -> None:
    """A path a ratified decision deleted has not come back on its own."""
    for rel, why in WITHDRAWN_PATHS.items():
        if (REPO / rel).exists():
            failures.append(f"withdrawn: {rel} exists; {why}")
    if not failures or not any(f.startswith("withdrawn:") for f in failures):
        notes.append(f"withdrawn: {len(WITHDRAWN_PATHS)} withdrawn path(s) absent")


def check_omniroute_version_consistency() -> None:
    """The OmniRoute baseline is stated identically everywhere it is documented.

    The HX-6 runbook once targeted 3.8.51 while hx-base.env and the run sheet
    pinned 3.8.50, and nothing caught the split. Machine authority is
    hx-base.env -> common/10-omniroute.sh -> installed version; the documents
    describe that state, so they must agree with the pin and with each other.
    """
    env = (REPO / "docs/03-runbooks/common/hx-base.env").read_text(
        encoding="utf-8")
    m = re.search(r'^HX_OMNIROUTE_VERSION="([^"]+)"', env, re.M)
    if not m:
        failures.append("versions: HX_OMNIROUTE_VERSION missing from hx-base.env")
        return
    pin = m.group(1)

    run_sheet = (REPO / "docs/03-runbooks/RUN-SHEET.md").read_text(
        encoding="utf-8")
    # The build-order row is the run sheet's only OmniRoute version statement.
    row = re.search(r"\|\s*6\s*\|\s*HX-6\s*\|\s*OmniRoute ([0-9][\w.]*)",
                    run_sheet)
    if not row:
        failures.append("versions: RUN-SHEET.md build-order row no longer states "
                        "the HX-6 OmniRoute version")
    elif row.group(1) != pin:
        failures.append(f"versions: RUN-SHEET.md lists OmniRoute {row.group(1)} "
                        f"but hx-base.env pins {pin}")

    readme = (REPO / "docs/03-runbooks/HX-6/README.md").read_text(
        encoding="utf-8")
    target = re.search(r"\*\*Target OmniRoute release:\*\* `([0-9][\w.]*)`", readme)
    if not target:
        failures.append("versions: HX-6 runbook no longer states a target "
                        "OmniRoute release")
    elif target.group(1) != pin:
        failures.append(f"versions: HX-6 runbook targets OmniRoute "
                        f"{target.group(1)} but hx-base.env pins {pin}")

    if not any(f.startswith("versions:") for f in failures):
        notes.append(f"versions: OmniRoute baseline {pin} consistent across "
                     "hx-base.env, RUN-SHEET.md and the HX-6 runbook")


def main() -> int:
    """Run every check and report. Returns the process exit status."""
    quiet = "--quiet" in sys.argv
    # Named, because the summary used to print len(notes). check_frontmatter
    # appends two notes, so the count was one higher than the number of checks
    # that ran - a tool whose whole job is catching a number reported against
    # the wrong thing, doing exactly that.
    checks = (
        check_links,
        check_vocabulary,
        check_frontmatter,
        check_duplicates,
        check_evidence_not_ignored,
        check_unit_claims,
        check_generated_authority_claims,
        check_tooling_docs,
        check_withdrawn_paths,
        check_omniroute_version_consistency,
    )
    for fn in checks:
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
    print(f"hx-doc-check: PASS ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
