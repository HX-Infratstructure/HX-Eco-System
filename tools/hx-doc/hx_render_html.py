#!/usr/bin/env python3
"""Generate the human-html mirrors from the authoritative Markdown.

The mirrors under human-html/ were hand-written summaries that drifted from
their sources. They are now generated, so a mirror cannot silently lose
content that its source document contains.

Usage:
  hx_render_html.py            regenerate every mirror
  hx_render_html.py --check    exit 1 if any mirror is out of date (CI mode)

No third-party dependencies. Standard library only, matching the repository's
native/minimal-dependency rule.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# Source -> mirror mapping. Keeps the established human-html/ layout.
SOURCES: list[tuple[Path, Path]] = []


def _collect() -> None:
    SOURCES.append((REPO / "README.md", REPO / "human-html/README.html"))
    for md in sorted((REPO / "docs").rglob("*.md")):
        if md.name.startswith("_"):
            continue  # templates are not published to the human view
        rel = md.relative_to(REPO / "docs")
        SOURCES.append((md, REPO / "human-html" / rel.with_suffix(".html")))
    for name in ("README", "SKILL-GOVERNANCE", "SKILL-REGISTRY", "AGENTS"):
        md = REPO / "skills" / f"{name}.md"
        if md.exists():
            SOURCES.append((md, REPO / "human-html/skills" / f"{name}.html"))
    for md in sorted((REPO / "skills").glob("*/README.md")):
        component = md.parent.name
        SOURCES.append((md, REPO / "human-html/skills" / component / "README.html"))


# --------------------------------------------------------------------------
# Minimal CommonMark/GFM subset covering what HX documents actually use.
# --------------------------------------------------------------------------

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def inline(text: str) -> str:
    """Escape, then apply inline markup. Code spans are protected first."""
    spans: list[str] = []

    def stash(m: re.Match[str]) -> str:
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = INLINE_CODE.sub(stash, text)
    text = html.escape(text, quote=False)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)

    def link(m: re.Match[str]) -> str:
        href = m.group(2)
        if href.endswith(".md"):
            href = href[:-3] + ".html"  # keep mirror-to-mirror links working
        return f'<a href="{html.escape(href, quote=True)}">{m.group(1)}</a>'

    text = LINK.sub(link, text)
    text = text.replace("&lt;br/&gt;", "<br/>").replace("&lt;br&gt;", "<br/>")

    def unstash(m: re.Match[str]) -> str:
        return f"<code>{html.escape(spans[int(m.group(1))], quote=False)}</code>"

    return re.sub(r"\x00(\d+)\x00", unstash, text)


def split_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.split("\n")
    meta: dict[str, str] = {}
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for raw in lines[1:i]:
                    if ":" in raw:
                        k, v = raw.split(":", 1)
                        meta[k.strip()] = v.strip()
                return meta, lines[i + 1:]
    return meta, lines


def render_body(lines: list[str]) -> str:
    out: list[str] = []
    i = 0
    n = len(lines)

    def close_lists(stack: list[str]) -> None:
        while stack:
            out.append(f"</{stack.pop()}>")

    list_stack: list[str] = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code / mermaid
        if stripped.startswith("```"):
            close_lists(list_stack)
            lang = stripped[3:].strip()
            i += 1
            buf: list[str] = []
            while i < n and lines[i].strip() != "```":
                buf.append(lines[i])
                i += 1
            i += 1
            body = html.escape("\n".join(buf), quote=False)
            if lang == "mermaid":
                out.append(f'<pre class="mermaid">{body}</pre>')
            else:
                cls = f' class="lang-{html.escape(lang, quote=True)}"' if lang else ""
                out.append(f"<pre><code{cls}>{body}</code></pre>")
            continue

        # table
        if (
            "|" in stripped
            and i + 1 < n
            and re.match(r"^\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1].strip())
            and "-" in lines[i + 1]
        ):
            close_lists(list_stack)

            def cells(row: str) -> list[str]:
                row = row.strip()
                if row.startswith("|"):
                    row = row[1:]
                if row.endswith("|"):
                    row = row[:-1]
                return [c.strip() for c in row.split("|")]

            head = cells(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(cells(lines[i]))
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            body_rows = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(
                f'<div class="tw"><table><thead><tr>{th}</tr></thead>'
                f"<tbody>{body_rows}</tbody></table></div>"
            )
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_lists(list_stack)
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            close_lists(list_stack)
            out.append("<hr/>")
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            close_lists(list_stack)
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            joined = " ".join(x for x in buf if x)
            out.append(f"<blockquote>{inline(joined)}</blockquote>")
            continue

        # list item
        lm = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line)
        if lm:
            indent = len(lm.group(1))
            ordered = lm.group(2).endswith(".")
            tag = "ol" if ordered else "ul"
            depth = indent // 2 + 1
            while len(list_stack) > depth:
                out.append(f"</{list_stack.pop()}>")
            if len(list_stack) < depth:
                out.append(f"<{tag}>")
                list_stack.append(tag)
            elif list_stack and list_stack[-1] != tag:
                out.append(f"</{list_stack.pop()}>")
                out.append(f"<{tag}>")
                list_stack.append(tag)
            out.append(f"<li>{inline(lm.group(3))}</li>")
            i += 1
            continue

        # blank line
        if not stripped:
            close_lists(list_stack)
            i += 1
            continue

        # paragraph
        close_lists(list_stack)
        buf = []
        while i < n and lines[i].strip() and not re.match(
            r"^\s*(#{1,6}\s|```|>|[-*+]\s|\d+\.\s|(-{3,}|\*{3,}|_{3,})$)", lines[i]
        ) and "|" not in lines[i]:
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append(f"<p>{inline(' '.join(buf))}</p>")
        else:
            out.append(f"<p>{inline(stripped)}</p>")
            i += 1

    close_lists(list_stack)
    return "\n".join(out)


STYLE = """
:root{--bg:#f7f8f9;--fg:#14181d;--fg2:#4c5764;--rule:#d8dde2;--surf:#fff;
--surf2:#eceff2;--accent:#8f4f12;--ok:#1f5f52}
@media(prefers-color-scheme:dark){:root{--bg:#0f1215;--fg:#e5e8eb;--fg2:#a3adb7;
--rule:#262c33;--surf:#161a1e;--surf2:#1c2127;--accent:#d5943e;--ok:#6cbfae}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);margin:0;
font:16px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:32px 20px 72px}
.banner{background:var(--surf);border:1px solid var(--rule);border-left:4px solid var(--accent);
border-radius:3px;padding:12px 16px;margin-bottom:28px;font-size:14px;color:var(--fg2)}
.banner b{color:var(--fg)}
h1{font-size:30px;line-height:1.2;margin:0 0 4px;letter-spacing:-.02em}
h2{font-size:21px;margin:34px 0 10px;padding-bottom:5px;border-bottom:1px solid var(--rule)}
h3{font-size:17px;margin:24px 0 8px}
h4,h5,h6{font-size:15px;margin:18px 0 6px}
p{margin:0 0 12px;max-width:76ch}
ul,ol{margin:0 0 12px;padding-left:24px;max-width:76ch}
li{margin:3px 0}
code{background:var(--surf2);border:1px solid var(--rule);border-radius:3px;
padding:1px 5px;font:13px ui-monospace,Menlo,Consolas,monospace;word-break:break-word}
pre{background:var(--surf2);border:1px solid var(--rule);border-radius:3px;
padding:12px 14px;overflow-x:auto;margin:0 0 14px}
pre code{background:none;border:none;padding:0;font-size:12.5px;line-height:1.5}
blockquote{border-left:3px solid var(--accent);background:var(--surf);margin:0 0 14px;
padding:10px 16px;color:var(--fg2);max-width:76ch}
.tw{overflow-x:auto;margin:0 0 16px;border:1px solid var(--rule);border-radius:3px}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--surf)}
th,td{border-bottom:1px solid var(--rule);padding:8px 12px;text-align:left;vertical-align:top}
th{background:var(--surf2);font-weight:600;white-space:nowrap}
tr:last-child td{border-bottom:none}
hr{border:none;border-top:1px solid var(--rule);margin:26px 0}
a{color:var(--accent)}
.mermaid{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;white-space:pre}
footer{margin-top:44px;padding-top:16px;border-top:1px solid var(--rule);
font-size:12.5px;color:var(--fg2)}
"""


def build(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    meta, lines = split_frontmatter(text)
    title = meta.get("document")
    if not title:
        for line in lines:
            m = re.match(r"^#\s+(.*)$", line.strip())
            if m:
                title = re.sub(r"[`*]", "", m.group(1))
                break
    title = title or md_path.stem
    rel = md_path.relative_to(REPO).as_posix()
    bits = [f"status: {meta[k]}" for k in ("status", "version", "date") if k in meta]
    meta_line = f" &middot; {' &middot; '.join(bits)}" if bits else ""
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)}</title><style>{STYLE}</style></head><body>"
        f'<div class="wrap"><div class="banner"><b>Human mirror.</b> '
        f"Generated from <code>{rel}</code>, which is the authoritative source. "
        f"This page is not execution authority. Do not edit it by hand; "
        f"run <code>tools/hx-doc/hx-render-html</code>.{meta_line}</div>"
        f"{render_body(lines)}"
        f'<footer>Generated by <code>tools/hx-doc/hx_render_html.py</code> '
        f"from <code>{rel}</code>.</footer></div></body></html>\n"
    )


def main() -> int:
    _collect()
    check = "--check" in sys.argv
    stale: list[str] = []
    written = 0
    for src, dst in SOURCES:
        want = build(src)
        have = dst.read_text(encoding="utf-8") if dst.exists() else None
        if have == want:
            continue
        if check:
            stale.append(dst.relative_to(REPO).as_posix())
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(want, encoding="utf-8", newline="\n")
            written += 1

    generated = {d.relative_to(REPO).as_posix() for _, d in SOURCES}
    orphans = [
        p.relative_to(REPO).as_posix()
        for p in sorted((REPO / "human-html").rglob("*.html"))
        if p.relative_to(REPO).as_posix() not in generated
    ]

    if check:
        for s in stale:
            print(f"STALE   {s}")
        for o in orphans:
            print(f"ORPHAN  {o}")
        if stale or orphans:
            print(
                f"\nFAIL: {len(stale)} stale, {len(orphans)} orphaned. "
                "Run tools/hx-doc/hx-render-html and commit the result."
            )
            return 1
        print(f"OK: {len(SOURCES)} mirrors are current.")
        return 0

    print(f"Rendered {written} changed of {len(SOURCES)} mirrors.")
    for o in orphans:
        print(f"ORPHAN (no source, delete or add a source): {o}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
