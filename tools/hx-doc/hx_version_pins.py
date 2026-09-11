#!/usr/bin/env python3
"""Audit the HX product version pins against what upstream currently ships.

The skill registry pins upstream *commits*; hx_upstream_drift.py watches those.
This watches the *product* pins - Ollama, the NVIDIA driver, the reranker model
and runtime, and the Python dependencies. That is the gap that let Ollama
0.34.0 ship four days before the documents were written without anyone knowing.

It also enforces the package-source policy: application software comes from
PyPI, GitHub releases, direct binaries, or Hugging Face. The Ubuntu archive is
acceptable for drivers, build toolchains and library headers only. Snap is
never permitted, for anything. Either case is reported as REVIEW with a
migration note.

Usage:
  hx_version_pins.py                  report
  hx_version_pins.py --markdown       table for an issue body
  hx_version_pins.py --fail-on-outdated   exit 1 if anything is OUTDATED
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]

BASE_ENV = REPO / "docs/03-runbooks/common/hx-base.env"
REQUIREMENTS = REPO / "tools/hx-smoke-runner/requirements.txt"
HX12_RUNBOOK = REPO / "docs/03-runbooks/HX-12/README.md"

# Package sources approved for application software.
APP_SOURCES = {"pypi", "github", "binary", "huggingface", "npm", "source"}
# Acceptable for drivers only. Owner decision 2026-09-11: the Ubuntu archive
# is permitted for the NVIDIA driver, for build toolchains and for library
# headers. Snap is not on this list because Snap is never permitted.
DRIVER_ONLY_SOURCES = {"ubuntu-archive"}
# Never permitted, for anything, driver included. .coderabbit.yaml states this
# and it is the standing rule.
NEVER_SOURCES = {"snap"}
# Vendor-operated repositories. Not the Ubuntu archive, not Snap.
VENDOR_REPO_SOURCES = {"npm", "source"}


def source_problem(pin: dict) -> str:
    """The package-source problem with this pin, or "" when there is none.

    Separate from the reporting loop so the rule can be tested without going
    near the network, which is the only reason the rest of this tool is slow.
    """
    if pin["source"] in NEVER_SOURCES:
        return ("Snap is never permitted; migrate to PyPI, a GitHub release, "
                "or a direct binary")
    if pin["source"] in DRIVER_ONLY_SOURCES and pin["kind"] != "driver":
        return (f"application from {pin['source']}; migrate to PyPI, "
                "a GitHub release, or a direct binary")
    return ""



def http(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "hx-version-pins"})
    if "api.github.com" in url:
        req.add_header("Accept", "application/vnd.github+json")
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


# --------------------------------------------------------------------------
# Collect the pins from the files that hold them.
# --------------------------------------------------------------------------

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def collect() -> list[dict]:
    pins: list[dict] = []
    env = read(BASE_ENV)

    def env_val(name: str) -> str | None:
        m = re.search(rf'^{name}="([^"]*)"', env, re.M)
        return m.group(1) if m else None

    if (v := env_val("HX_OLLAMA_VERSION")):
        pins.append(dict(package="ollama", pinned=v, source="github",
                         kind="app", where="hx-base.env",
                         probe=("github", "ollama/ollama")))

    if (v := env_val("HX_NVIDIA_PKG_VERSION")):
        branch = env_val("HX_NVIDIA_BRANCH") or ""
        pins.append(dict(package=f"nvidia-driver-{branch}-server-open", pinned=v,
                         source="ubuntu-archive", kind="driver", where="hx-base.env",
                         probe=("ubuntu", f"nvidia-driver-{branch}-server-open")))

    if (v := env_val("HX_RERANKER_RUNTIME_VERSION")):
        pins.append(dict(package=env_val("HX_RERANKER_RUNTIME") or "infinity-emb",
                         pinned=v, source="pypi", kind="app", where="hx-base.env",
                         probe=("pypi", env_val("HX_RERANKER_RUNTIME") or "infinity-emb")))

    if (model := env_val("HX_RERANKER_MODEL")) and (rev := env_val("HX_RERANKER_REVISION")):
        pins.append(dict(package=model, pinned=rev[:12], source="huggingface",
                         kind="model", where="hx-base.env",
                         probe=("hf", model), full_pin=rev))

    # Application pins for the remaining fleet.
    # (env var, display name, source, probe kind, probe ref)
    APPS = [
        ("HX_OMNIROUTE_VERSION",   "omniroute",     "npm",     "npm",    "omniroute"),
        ("HX_NGINX_VERSION",       "nginx",         "binary",  "nginx",  ""),
        ("HX_OPEN_WEBUI_VERSION",  "open-webui",    "pypi",    "pypi",   "open-webui"),
        ("HX_REDIS_VERSION",       "redis",         "github",  "github", "redis/redis"),
        ("HX_QDRANT_VERSION",      "qdrant",        "github",  "github", "qdrant/qdrant"),
        ("HX_LIGHTRAG_VERSION",    "lightrag-hku",  "pypi",    "pypi",   "lightrag-hku"),
        ("HX_DEEPAGENTS_VERSION",  "deepagents",    "pypi",    "pypi",   "deepagents"),
        ("HX_MEM0_VERSION",        "mem0ai",        "pypi",    "pypi",   "mem0ai"),
        ("HX_NODE_VERSION",        "nodejs",        "binary",  "node",   ""),
        ("HX_N8N_VERSION",         "n8n",           "npm",     "npm",    "n8n"),
        ("HX_FASTMCP_VERSION",     "fastmcp",       "pypi",    "pypi",   "fastmcp"),
        ("HX_DOCLING_VERSION",     "docling",       "pypi",    "pypi",   "docling"),
        ("HX_CRAWL4AI_VERSION",    "crawl4ai",      "pypi",    "pypi",   "crawl4ai"),
    ]
    for var, name, source, probe_kind, ref in APPS:
        if (v := env_val(var)):
            pins.append(dict(package=name, pinned=v, source=source, kind="app",
                             where="hx-base.env", probe=(probe_kind, ref)))

    if (ver := env_val("HX_POSTGRES_VERSION")):
        # Built from the upstream source tarball (D-020), not any repository.
        pins.append(dict(package="postgresql", pinned=ver, source="source",
                         kind="app", where="hx-base.env",
                         probe=("postgres", env_val("HX_POSTGRES_MAJOR") or "")))

    if (m := env_val("HX_GRANITE_DOCLING_MODEL")) and (r := env_val("HX_GRANITE_DOCLING_REVISION")):
        pins.append(dict(package=m, pinned=r[:12], source="huggingface",
                         kind="model", where="hx-base.env", probe=("hf", m)))

    for line in read(REQUIREMENTS).splitlines():
        m = re.match(r"^([A-Za-z0-9_.-]+)==([0-9][\w.]*)\s*$", line.strip())
        if m:
            pins.append(dict(package=m.group(1), pinned=m.group(2), source="pypi",
                             kind="app", where="requirements.txt",
                             probe=("pypi", m.group(1))))

    for m in re.finditer(r"`([a-z0-9_.-]+)==([0-9][\w.]*)`", read(HX12_RUNBOOK)):
        pins.append(dict(package=m.group(1), pinned=m.group(2), source="pypi",
                         kind="app", where="HX-12 runbook",
                         probe=("pypi", m.group(1))))

    return pins


# --------------------------------------------------------------------------
# Resolve what upstream currently ships.
# --------------------------------------------------------------------------

def latest(kind: str, ref: str) -> str:
    if kind == "pypi":
        return http(f"https://pypi.org/pypi/{ref}/json")["info"]["version"]
    if kind == "github":
        return http(f"https://api.github.com/repos/{ref}/releases/latest")["tag_name"].lstrip("v")
    if kind == "hf":
        return (http(f"https://huggingface.co/api/models/{ref}").get("sha") or "?")[:12]
    if kind == "npm":
        return http(f"https://registry.npmjs.org/{ref}")["dist-tags"]["latest"]
    if kind == "node":
        data = http("https://nodejs.org/dist/index.json")
        lts = [x for x in data if x.get("lts")]
        return (lts[0]["version"] if lts else data[0]["version"]).lstrip("v")
    if kind == "nginx":
        # nginx.org labels one release as the stable line.
        page = urllib.request.urlopen(
            urllib.request.Request("https://nginx.org/en/download.html",
                                   headers={"User-Agent": "hx-version-pins"}),
            timeout=30).read().decode("utf-8", "replace")
        i = page.find("Stable version")
        m = re.search(r"nginx-(\d+\.\d+\.\d+)", page[i:i + 2000]) if i >= 0 else None
        return m.group(1) if m else "?"
    if kind == "postgres":
        for v in http("https://www.postgresql.org/versions.json"):
            if str(v.get("major")) == str(ref):
                return f"{v['major']}.{v['latestMinor']}"
        return "?"
    if kind == "ubuntu":
        # Compare against the *binary* actually installable on noble/amd64, not
        # the source-package version. A source build can exist without a
        # published binary for this flavour, which reads as false drift.
        # Proposed is excluded: it is not enabled on HX hosts.
        url = ("https://api.launchpad.net/1.0/ubuntu/+archive/primary"
               f"?ws.op=getPublishedBinaries&binary_name={ref}"
               "&exact_match=true&status=Published")
        versions, seen = [], set()
        while url and url not in seen:
            seen.add(url)
            data = http(url)
            for e in data.get("entries", []):
                link = e.get("distro_arch_series_link", "")
                if "/noble/" not in link or not link.endswith("/amd64"):
                    continue
                if e.get("pocket") not in ("Updates", "Security", "Release"):
                    continue
                versions.append(e["binary_package_version"])
            url = data.get("next_collection_link")
        # Numeric sort, not lexicographic: "595.9.05" sorts above "595.71.05"
        # as text, so the reported latest driver was wrong whenever a minor
        # number crossed a digit boundary.
        def vkey(v: str) -> tuple[int, ...]:
            return tuple(int(p) for p in re.findall(r"\d+", v))

        return max(set(versions), key=vkey) if versions else "not in noble"
    return "?"


def main() -> int:
    as_markdown = "--markdown" in sys.argv
    fail_on_outdated = "--fail-on-outdated" in sys.argv

    rows = []
    outdated = policy = 0

    for pin in collect():
        try:
            newest = latest(*pin["probe"])
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError) as exc:
            newest = f"unreachable ({exc.__class__.__name__})"

        note = source_problem(pin)
        if note:
            status = "REVIEW"
            policy += 1
        elif newest.startswith("unreachable") or newest in ("?", "not in noble"):
            status = "REVIEW"
            note = "could not resolve the current upstream version"
            policy += 1
        elif pin["kind"] == "model":
            status = "OK" if newest == pin["pinned"] else "REVIEW"
            if status == "REVIEW":
                note = "upstream model revision moved; the pin still resolves, re-review before changing it"
                policy += 1
        elif pin["pinned"] == newest:
            status = "OK"
        elif pin["source"] == "ubuntu-archive":
            status = "OUTDATED"
            note = "driver; archive has a newer build"
            outdated += 1
        else:
            status = "OUTDATED"
            outdated += 1

        rows.append((pin["package"], pin["pinned"], newest, pin["source"],
                     pin["where"], status, note))

    if as_markdown:
        print("| Package | Pinned | Latest | Source | Declared in | Status |")
        print("|---|---|---|---|---|---|")
        for p, pinned, new, src, where, st, note in rows:
            flag = {"OK": "OK", "OUTDATED": "**OUTDATED**", "REVIEW": "**REVIEW**"}[st]
            suffix = f"<br/>{note}" if note else ""
            print(f"| `{p}` | `{pinned}` | `{new}` | {src} | {where} | {flag}{suffix} |")
    else:
        print(f"{'PACKAGE':34} {'PINNED':22} {'LATEST':22} {'SOURCE':15} STATUS")
        print("-" * 108)
        for p, pinned, new, src, where, st, note in rows:
            print(f"{p:34} {pinned:22} {new:22} {src:15} {st}")
            if note:
                print(f"{'':34} -> {note}")

    print()
    print(f"{len(rows)} pins checked, {outdated} outdated, {policy} need review.")
    if outdated:
        print("Update the pin, rebuild or upgrade the affected servers, then record")
        print("the resolved version in each server record.")
    return 1 if (fail_on_outdated and outdated) else 0


if __name__ == "__main__":
    raise SystemExit(main())
