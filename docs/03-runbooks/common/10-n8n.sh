#!/usr/bin/env bash
# HX-14 n8n - npm, on Node from the official binary tarball.
# Usage: ./10-n8n.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-14)" >&2; exit 2; }
hx_require_host "$1"

hx_node_install "$HX_NODE_VERSION"

hx_app_user n8n /srv/n8n
sudo npm install -g "n8n@${HX_N8N_VERSION}"
n8n --version || true

hx_app_unit hx-n8n "HX n8n ${HX_N8N_VERSION}" n8n /srv/n8n \
  "/usr/local/bin/n8n start" \
  "HOME=/srv/n8n" \
  "N8N_USER_FOLDER=/srv/n8n" \
  "N8N_HOST=0.0.0.0" \
  "N8N_PORT=${HX_N8N_PORT}" \
  "N8N_DIAGNOSTICS_ENABLED=false" \
  "GENERIC_TIMEZONE=UTC"

hx_app_validate hx-n8n "$HX_N8N_PORT" /healthz
hx_app_done hx-n8n "$HX_HOST" "n8n ${HX_N8N_VERSION}" "http://${HX_IP}:${HX_N8N_PORT}"

cat <<'NOTE'
n8n keeps its data under /srv/n8n by default with SQLite. Moving it to the
HX-9 PostgreSQL instance is integration-phase work, not part of the base build.

n8n MCP is a separate companion gate.
NOTE
