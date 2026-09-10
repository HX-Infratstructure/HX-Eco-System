#!/usr/bin/env bash
# HX-16 Docling + Granite-Docling 258M - PyPI and Hugging Face, CPU-first.
# Usage: ./10-docling.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-16)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user docling /srv/docling
hx_app_venv docling /srv/docling/venv "docling==${HX_DOCLING_VERSION}"

# D-006: Granite-Docling stays with Docling on HX-16 and is CPU-first for base
# validation. Pre-fetch the pinned revision so first use is not a download.
sudo -u docling env HF_HOME=/srv/docling/hf \
  /srv/docling/venv/bin/python - <<PY
from huggingface_hub import snapshot_download
p = snapshot_download("${HX_GRANITE_DOCLING_MODEL}", revision="${HX_GRANITE_DOCLING_REVISION}")
print("Granite-Docling cached at", p)
PY

/srv/docling/venv/bin/docling --version

hx_app_done hx-docling "$HX_HOST" "Docling ${HX_DOCLING_VERSION} + Granite-Docling 258M"

cat <<'NOTE'
Docling is a CLI and library, not a daemon, so there is no unit for the core
install. Validation for the base build is: the CLI runs, and a conversion still
works after a reboot. The Docling MCP companion is the service that gets a unit
and is a separate gate.
NOTE
