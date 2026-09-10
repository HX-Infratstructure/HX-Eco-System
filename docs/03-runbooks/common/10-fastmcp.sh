#!/usr/bin/env bash
# HX-15 FastMCP shared MCP development host - PyPI.
# Usage: ./10-fastmcp.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-15)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user fastmcp /srv/fastmcp
hx_app_venv fastmcp /srv/fastmcp/venv "fastmcp==${HX_FASTMCP_VERSION}"

/srv/fastmcp/venv/bin/fastmcp version

hx_app_done hx-fastmcp "$HX_HOST" "FastMCP ${HX_FASTMCP_VERSION}"

cat <<'NOTE'
HX-15 is a development and runtime host for shared or custom MCP servers, not a
single service. The base install is the pinned runtime. The smoke test creates
a disposable test server, proves tool discovery and one tool call, then removes
it.

FastMCP is not a prerequisite for any product-specific MCP server.
NOTE
