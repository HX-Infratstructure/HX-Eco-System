#!/usr/bin/env bash
# HX-8 Open WebUI - PyPI, native venv, systemd.
# Usage: ./10-open-webui.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   ($3)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user openwebui /srv/open-webui
hx_app_venv openwebui /srv/open-webui/venv "open-webui==${HX_OPEN_WEBUI_VERSION}"

hx_app_unit hx-open-webui "HX Open WebUI ${HX_OPEN_WEBUI_VERSION}" openwebui /srv/open-webui \
  "/srv/open-webui/venv/bin/open-webui serve --host 0.0.0.0 --port ${HX_OPEN_WEBUI_PORT}" \
  "DATA_DIR=/srv/open-webui/data" \
  "WEBUI_AUTH=False" \
  "HF_HOME=/srv/open-webui/hf"

hx_app_validate hx-open-webui "$HX_OPEN_WEBUI_PORT" /health
hx_app_done hx-open-webui "$HX_HOST" "Open WebUI ${HX_OPEN_WEBUI_VERSION}" "http://${HX_IP}:${HX_OPEN_WEBUI_PORT}"

cat <<'NOTE'
BASE PASS also needs decision D-008: temporarily point Open WebUI at one
already-proven Ollama endpoint, send one prompt, confirm a response renders,
capture evidence, then remove the temporary connection.
NOTE
