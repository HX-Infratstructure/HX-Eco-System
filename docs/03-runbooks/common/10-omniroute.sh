#!/usr/bin/env bash
# HX-6 OmniRoute AI gateway - npm, on Node from the official binary tarball.
# Usage: ./10-omniroute.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-6)" >&2; exit 2; }
hx_require_host "$1"

# Node.js comes from nodejs.org as a checksum-verified direct binary.
# Not Snap, not the Ubuntu archive, not NodeSource.
hx_node_install "$HX_NODE_VERSION"

hx_app_user omniroute /srv/omniroute
sudo npm install -g "omniroute@${HX_OMNIROUTE_VERSION}"
omniroute --version || true

hx_app_unit hx-omniroute "HX OmniRoute ${HX_OMNIROUTE_VERSION}" omniroute /srv/omniroute \
  "/usr/local/bin/omniroute" \
  "HOME=/srv/omniroute" \
  "PORT=${HX_OMNIROUTE_PORT}" \
  "HOST=0.0.0.0"

hx_app_validate hx-omniroute "$HX_OMNIROUTE_PORT" /v1/models
hx_app_done hx-omniroute "$HX_HOST" "OmniRoute ${HX_OMNIROUTE_VERSION}" "http://${HX_IP}:${HX_OMNIROUTE_PORT}"

cat <<'NOTE'
OPERATOR ACTION REQUIRED before this server can close.

D-010 and the OmniRoute catalog standard are the point of this server, and the
product ships with hundreds of providers discovered by default:

  1. Build the explicit approved-provider allowlist.
  2. Build the explicit approved-model allowlist.
  3. Confirm no free, no-auth or discovered provider is active without approval.
  4. Confirm no cloud provider or cloud model is active without approval.

Discovery is not approval. Approving a provider does not approve its catalogue.

BASE PASS also needs D-009: one temporary route to one already-proven Ollama
endpoint, direct-versus-routed known-answer evidence, then remove the route.
NOTE
