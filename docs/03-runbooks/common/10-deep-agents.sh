#!/usr/bin/env bash
# HX-12 Deep Agents LOB agent factory - PyPI.
# Usage: ./10-deep-agents.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-12)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user deepagents /srv/deepagents
hx_app_venv deepagents /srv/deepagents/venv "deepagents==${HX_DEEPAGENTS_VERSION}"

# Prove the package imports and the factory entry point resolves.
sudo -u deepagents /srv/deepagents/venv/bin/python - <<'PY'
import deepagents
from deepagents import create_deep_agent
print("deepagents import OK:", getattr(deepagents, "__version__", "unknown"))
print("create_deep_agent resolved:", callable(create_deep_agent))
PY

hx_app_done hx-deepagents "$HX_HOST" "Deep Agents ${HX_DEEPAGENTS_VERSION}"

cat <<'NOTE'
Deep Agents is a harness library, not a daemon, so the core install has no unit.

Before the LOB Agent Factory smoke test, configure one explicit owner-approved
HX model endpoint and run the tool-calling probe. D-013 is clear: if the chosen
model cannot call tools reliably, stop and record
MODEL/HARNESS COMPATIBILITY NOT ESTABLISHED. A plain chat completion is not
sufficient to close this server.
NOTE
