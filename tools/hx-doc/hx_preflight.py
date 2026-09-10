#!/usr/bin/env python3
"""Confirm every download the install blocks make still works, before build day.

A 404 discovered on a lab machine costs lab time. This checks the same things
from anywhere, in about thirty seconds:

  - every direct download URL the blocks fetch resolves
  - every pinned PyPI version still exists and is not yanked
  - every pinned npm version still exists
  - every pinned Hugging Face model revision still resolves
  - the pinned NVIDIA driver is still installable on noble/amd64

It downloads nothing. It only asks whether the thing is there.

Usage:
  hx_preflight.py           check everything
  hx_preflight.py --quiet   only print problems
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
BASE_ENV = REPO / "docs/03-runbooks/common/hx-base.env"

results: list[tuple[str, str, str]] = []   # (status, label, detail)


def env() -> dict[str, str]:
    text = BASE_ENV.read_text(encoding="utf-8")
    return dict(re.findall(r'^(HX_[A-Z0-9_]+)="([^"]*)"', text, re.M))


def head(url: str) -> int:
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "hx-preflight"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        # Some CDNs refuse HEAD; fall back to a ranged GET of one byte.
        if e.code in (403, 405, 501):
            req = urllib.request.Request(
                url, headers={"User-Agent": "hx-preflight", "Range": "bytes=0-0"})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return r.status
            except Exception:
                return e.code
        return e.code
    except urllib.error.URLError:
        return 0


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "hx-preflight"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def record(ok: bool, label: str, detail: str = "") -> None:
    results.append(("OK" if ok else "FAIL", label, detail))


def check_urls(e: dict[str, str]) -> None:
    urls = {
        "ollama install script":
            "https://ollama.com/install.sh",
        f"postgresql {e.get('HX_POSTGRES_VERSION','?')} source":
            f"https://ftp.postgresql.org/pub/source/v{e.get('HX_POSTGRES_VERSION')}"
            f"/postgresql-{e.get('HX_POSTGRES_VERSION')}.tar.bz2",
        "postgresql sha256":
            f"https://ftp.postgresql.org/pub/source/v{e.get('HX_POSTGRES_VERSION')}"
            f"/postgresql-{e.get('HX_POSTGRES_VERSION')}.tar.bz2.sha256",
        f"qdrant {e.get('HX_QDRANT_VERSION','?')} linux binary":
            f"https://github.com/qdrant/qdrant/releases/download/v{e.get('HX_QDRANT_VERSION')}"
            "/qdrant-x86_64-unknown-linux-gnu.tar.gz",
        f"redis {e.get('HX_REDIS_VERSION','?')} source":
            f"https://github.com/redis/redis/archive/refs/tags/{e.get('HX_REDIS_VERSION')}.tar.gz",
        f"nginx {e.get('HX_NGINX_VERSION','?')} source":
            f"https://nginx.org/download/nginx-{e.get('HX_NGINX_VERSION')}.tar.gz",
        f"node v{e.get('HX_NODE_VERSION','?')} linux-x64":
            f"https://nodejs.org/dist/v{e.get('HX_NODE_VERSION')}"
            f"/node-v{e.get('HX_NODE_VERSION')}-linux-x64.tar.xz",
        f"node v{e.get('HX_NODE_VERSION','?')} SHASUMS256":
            f"https://nodejs.org/dist/v{e.get('HX_NODE_VERSION')}/SHASUMS256.txt",
    }
    for label, url in urls.items():
        code = head(url)
        record(code in (200, 206), f"download  {label}", f"HTTP {code}" if code != 200 else "")


def check_pypi(e: dict[str, str]) -> None:
    pkgs = {
        "open-webui": e.get("HX_OPEN_WEBUI_VERSION"),
        "lightrag-hku": e.get("HX_LIGHTRAG_VERSION"),
        "mem0ai": e.get("HX_MEM0_VERSION"),
        "docling": e.get("HX_DOCLING_VERSION"),
        "crawl4ai": e.get("HX_CRAWL4AI_VERSION"),
        "deepagents": e.get("HX_DEEPAGENTS_VERSION"),
        "fastmcp": e.get("HX_FASTMCP_VERSION"),
        e.get("HX_RERANKER_RUNTIME", "infinity-emb"): e.get("HX_RERANKER_RUNTIME_VERSION"),
    }
    req = REPO / "tools/hx-smoke-runner/requirements.txt"
    if req.exists():
        for line in req.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([A-Za-z0-9_.-]+)==([0-9][\w.]*)\s*$", line.strip())
            if m:
                pkgs[m.group(1)] = m.group(2)

    for name, version in pkgs.items():
        if not version:
            continue
        try:
            data = get_json(f"https://pypi.org/pypi/{name}/{version}/json")
            files = data.get("urls") or []
            if not files:
                record(False, f"pypi      {name}=={version}", "no distribution files")
            elif any(f.get("yanked") for f in files):
                record(False, f"pypi      {name}=={version}", "YANKED")
            else:
                record(True, f"pypi      {name}=={version}")
        except urllib.error.HTTPError as exc:
            record(False, f"pypi      {name}=={version}", f"HTTP {exc.code}")
        except Exception as exc:
            record(False, f"pypi      {name}=={version}", exc.__class__.__name__)


def check_npm(e: dict[str, str]) -> None:
    for name, version in (("omniroute", e.get("HX_OMNIROUTE_VERSION")),
                          ("n8n", e.get("HX_N8N_VERSION"))):
        if not version:
            continue
        try:
            data = get_json(f"https://registry.npmjs.org/{name}/{version}")
            record(bool(data.get("version")), f"npm       {name}@{version}")
        except Exception as exc:
            record(False, f"npm       {name}@{version}", exc.__class__.__name__)


def check_hf(e: dict[str, str]) -> None:
    for model, rev in ((e.get("HX_RERANKER_MODEL"), e.get("HX_RERANKER_REVISION")),
                       (e.get("HX_GRANITE_DOCLING_MODEL"), e.get("HX_GRANITE_DOCLING_REVISION"))):
        if not model or not rev:
            continue
        code = head(f"https://huggingface.co/api/models/{model}/revision/{rev}")
        record(code == 200, f"hf        {model}@{rev[:12]}",
               f"HTTP {code}" if code != 200 else "")


def check_driver(e: dict[str, str]) -> None:
    branch, pin = e.get("HX_NVIDIA_BRANCH"), e.get("HX_NVIDIA_PKG_VERSION")
    if not branch or not pin:
        return
    name = f"nvidia-driver-{branch}-server-open"
    url = ("https://api.launchpad.net/1.0/ubuntu/+archive/primary"
           f"?ws.op=getPublishedBinaries&binary_name={name}"
           "&exact_match=true&status=Published")
    found, seen = set(), set()
    try:
        while url and url not in seen:
            seen.add(url)
            data = get_json(url)
            for entry in data.get("entries", []):
                link = entry.get("distro_arch_series_link", "")
                if "/noble/" in link and link.endswith("/amd64") \
                   and entry.get("pocket") in ("Updates", "Security", "Release"):
                    found.add(entry["binary_package_version"])
            url = data.get("next_collection_link")
        record(pin in found, f"apt       {name}={pin}",
               "" if pin in found else f"not published for noble/amd64; available: {sorted(found)}")
    except Exception as exc:
        record(False, f"apt       {name}={pin}", exc.__class__.__name__)


def main() -> int:
    quiet = "--quiet" in sys.argv
    e = env()
    print("HX pre-flight - checking that every pinned artifact is still fetchable\n")
    for fn in (check_urls, check_pypi, check_npm, check_hf, check_driver):
        fn(e)

    failed = 0
    for status, label, detail in results:
        if status == "FAIL":
            failed += 1
            print(f"FAIL  {label}" + (f"   {detail}" if detail else ""))
        elif not quiet:
            print(f"OK    {label}")

    print()
    if failed:
        print(f"{len(results)} checks, {failed} FAILED. Fix the pin in "
              "docs/03-runbooks/common/hx-base.env before build day.")
        return 1
    print(f"{len(results)} checks, all clear. Every pinned artifact is fetchable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
