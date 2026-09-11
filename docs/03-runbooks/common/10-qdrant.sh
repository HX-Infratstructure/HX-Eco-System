#!/usr/bin/env bash
# HX-10 Qdrant + Web UI - prebuilt Linux binary from the GitHub release.
# Usage: ./10-qdrant.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-10)" >&2; exit 2; }
hx_require_host "$1"

TARBALL="qdrant-x86_64-unknown-linux-gnu.tar.gz"
URL="https://github.com/qdrant/qdrant/releases/download/v${HX_QDRANT_VERSION}/${TARBALL}"

hx_app_user qdrant /srv/qdrant
sudo -u qdrant mkdir -p /srv/qdrant/{bin,storage,snapshots,static}

tmp="$(mktemp -d)"
hx_fetch_verified "$URL" "$tmp/$TARBALL" "${HX_QDRANT_SHA256:-}"
tar -xzf "$tmp/$TARBALL" -C "$tmp"
sudo install -o qdrant -g qdrant -m 0755 "$tmp/qdrant" /srv/qdrant/bin/qdrant
rm -rf "$tmp"

# The dashboard ships in the release as a static bundle served by Qdrant itself.
sudo -u qdrant tee /srv/qdrant/config.yaml >/dev/null <<CONF
storage:
  storage_path: /srv/qdrant/storage
  snapshots_path: /srv/qdrant/snapshots
service:
  host: 0.0.0.0
  http_port: ${HX_QDRANT_PORT}
CONF

hx_app_unit hx-qdrant "HX Qdrant ${HX_QDRANT_VERSION}" qdrant /srv/qdrant \
  "/srv/qdrant/bin/qdrant --config-path /srv/qdrant/config.yaml"

hx_app_validate hx-qdrant "$HX_QDRANT_PORT" /healthz
/srv/qdrant/bin/qdrant --version
hx_app_done hx-qdrant "$HX_HOST" "Qdrant ${HX_QDRANT_VERSION}" "http://${HX_IP}:${HX_QDRANT_PORT}"

cat <<'NOTE'
Web UI is at /dashboard on the same port and is a separate companion gate, as
is Qdrant MCP.

D-005 still applies: never mix embeddings from different model identities in
one collection. A model change means a new collection and re-embedding.
NOTE
