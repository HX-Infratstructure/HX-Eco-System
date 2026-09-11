#!/usr/bin/env bash
# HX-13 Mem0 OSS - PyPI, native venv, systemd.
# Usage: ./10-mem0.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-13)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user mem0 /srv/mem0
hx_app_venv mem0 /srv/mem0/venv "mem0ai==${HX_MEM0_VERSION}"

# Mem0 OSS is a library. HX runs it behind a small local service so it has a
# unit to start and a port to prove, and which service that is has not been
# decided. Reporting the block as done named a unit hx-mem0 that nothing
# creates, so the reboot check could only fail. The block stops here instead.
cat <<'NOTE'
OPERATOR DECISION REQUIRED before this server can close:
Mem0 OSS ships as a Python library, not a daemon. Choose one:
  a) run it inside the assigned Mem0 MCP server, and make that the unit; or
  b) wrap it in a small local FastAPI service and make that the unit.
The registry records the Mem0 MCP implementation as not yet selected, so this
is not decided by implication. Approved dependencies are HX-10 Qdrant and one
approved HX Ollama endpoint.
NOTE

exit 3
