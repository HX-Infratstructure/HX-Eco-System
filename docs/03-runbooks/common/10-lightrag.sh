#!/usr/bin/env bash
# HX-11 LightRAG + API server - PyPI, native venv, systemd.
# Usage: ./10-lightrag.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-11)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user lightrag /srv/lightrag
hx_app_venv lightrag /srv/lightrag/venv "lightrag-hku[api]==${HX_LIGHTRAG_VERSION}"

# Storage and model bindings are HX-11 runbook decisions, not skill decisions.
# Point at the already-proven HX-4 embedding plane and one approved LLM.
hx_app_unit hx-lightrag "HX LightRAG ${HX_LIGHTRAG_VERSION}" lightrag /srv/lightrag \
  "/srv/lightrag/venv/bin/lightrag-server --host 0.0.0.0 --port ${HX_LIGHTRAG_PORT}" \
  "WORKING_DIR=/srv/lightrag/data" \
  "HF_HOME=/srv/lightrag/hf"

hx_app_validate hx-lightrag "$HX_LIGHTRAG_PORT" /health
hx_app_done hx-lightrag "$HX_HOST" "LightRAG ${HX_LIGHTRAG_VERSION}" "http://${HX_IP}:${HX_LIGHTRAG_PORT}"

cat <<'NOTE'
Before the smoke test, set the embedding and LLM bindings in the unit
environment: HX-4 for BGE-M3, and one approved HX Ollama endpoint. Record the
exact bindings in the HX-11 server record. LightRAG MCP is a separate gate.
NOTE
