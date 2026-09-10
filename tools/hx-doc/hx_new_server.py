#!/usr/bin/env python3
"""Scaffold everything a server needs before its build starts.

Twelve servers remain. Each one needs three runbook wrappers, a server record,
and a runbook README. Doing that by hand twelve more times is twelve more
chances to leave out a section.

Creates, from docs/00-control/hx-fleet.tsv and the record template:
  docs/03-runbooks/<HX-N>/01-base-admin-network-updates.sh
  docs/03-runbooks/<HX-N>/02-domain-nvidia.sh
  docs/03-runbooks/<HX-N>/03-storage-ollama.sh      (inference hosts only)
  docs/03-runbooks/<HX-N>/README.md
  docs/02-server-records/<HX-N>.md

Usage:
  hx_new_server.py hx-9              scaffold HX-9
  hx_new_server.py hx-9 --no-ollama  skip the Ollama block (non-inference host)
  hx_new_server.py hx-9 --force      overwrite existing files
"""
from __future__ import annotations

import csv
import stat
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TSV = REPO / "docs/00-control/hx-fleet.tsv"
TEMPLATE = REPO / "docs/02-server-records/_TEMPLATE.md"

WRAPPER = """#!/usr/bin/env bash
# {upper} wrapper for the common base block. All logic lives in ../common/.
# Pins and the host -> IP map are in ../common/hx-base.env.
set -euo pipefail
exec "$(cd -- "$(dirname -- "${{BASH_SOURCE[0]}}")/../common" && pwd)/{block}.sh" {host}
"""

README = """# {upper} Current Runbook

**Host:** {host}
**Expected IP:** `{ip}`
**Role:** {role}

## Execution

Steps 1-{last} are the shared base blocks. Run them from this directory; each one
refuses to run on any host other than `{host}`.

```bash
{commands}
```

Implementation lives in `../common/`; version pins and the host -> IP map live
in `../common/hx-base.env`. See `../README.md` before changing a pin.

## Sequence

1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install the pinned NVIDIA
   driver; reboot.
{step3}{appstep}. Install the {role} application software.
   Application software comes from PyPI, a GitHub release, or a direct binary.
   Not Snap. Not the Ubuntu archive.
{valstep}. Validation: the service starts, and it survives a reboot.
{recstep}. Fill in `docs/02-server-records/{upper}.md`, then set `state` and
   `gate` for `{upper}` in `docs/00-control/hx-fleet.tsv` and run
   `tools/hx-doc/hx-fleet`.

Do not mount/wipe unrelated disks. Do not import prior application state.
"""


def fleet() -> dict[str, dict[str, str]]:
    with TSV.open(encoding="utf-8", newline="") as fh:
        return {r["id"].strip().lower(): r for r in csv.DictReader(fh, delimiter="\t")}


def write(path: Path, content: str, executable: bool, force: bool) -> str:
    if path.exists() and not force:
        return f"skip   {path.relative_to(REPO).as_posix()} (exists)"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    if executable:
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return f"write  {path.relative_to(REPO).as_posix()}"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    with_ollama = "--no-ollama" not in sys.argv

    if len(args) != 1:
        print(__doc__.strip())
        return 2

    host = args[0].strip().lower()
    servers = fleet()
    if host not in servers:
        print(f"ERROR: {host} is not in {TSV.relative_to(REPO).as_posix()}", file=sys.stderr)
        print(f"       known: {', '.join(sorted(servers))}", file=sys.stderr)
        return 1

    row = servers[host]
    upper = row["id"].strip()
    ip, role = row["ip"].strip(), row["role"].strip()
    rb = REPO / "docs/03-runbooks" / upper

    blocks = ["01-base-admin-network-updates", "02-domain-nvidia"]
    if with_ollama:
        blocks.append("03-storage-ollama")

    out = []
    for block in blocks:
        out.append(write(rb / f"{block}.sh",
                         WRAPPER.format(upper=upper, block=block, host=host),
                         True, force))

    last = len(blocks)
    width = max(len(b) for b in blocks) + 6
    commands = "\n".join(
        (f"./{b}.sh".ljust(width) + "# reboots") if i < 2 else f"./{b}.sh"
        for i, b in enumerate(blocks)
    )
    step3 = ("3. Validate GPU/storage; install the pinned Ollama; service health.\n"
             if with_ollama else "")
    n = last + 1
    out.append(write(rb / "README.md",
                     README.format(upper=upper, host=host, ip=ip, role=role,
                                   last=last, commands=commands, step3=step3,
                                   appstep=n, valstep=n + 1, recstep=n + 2),
                     False, force))

    record = TEMPLATE.read_text(encoding="utf-8")
    record = (record
              .replace("# HX-N — <Role> Server Configuration",
                       f"# {upper} — {role} Server Configuration")
              .replace("**IP:** `192.168.50.2NN`", f"**IP:** `{ip}`")
              .replace("**FQDN:** `hx-N.hx.local.arpa`",
                       f"**FQDN:** `{host}.hx.local.arpa`")
              .replace("> Copy this file to `HX-N.md` when a server build starts. Every heading below is\n"
                       "> required. Delete a section only when it genuinely does not apply, and say why\n"
                       "> in one line rather than removing it silently.\n\n",
                       f"> Scaffolded by `tools/hx-doc/hx-new-server {host}`. Fill every section as the\n"
                       f"> build proceeds. `tools/hx-doc/hx-record-check` reports what is still open.\n\n"))
    out.append(write(REPO / "docs/02-server-records" / f"{upper}.md", record, False, force))

    for line in out:
        print(line)
    print(f"\n{upper} scaffolded. Next: run the blocks, then fill the record.")
    print("Remember to set state/gate in docs/00-control/hx-fleet.tsv and run tools/hx-doc/hx-fleet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
