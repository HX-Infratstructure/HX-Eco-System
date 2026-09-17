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

# F3: /srv/omniroute is a dedicated volume, and hx_app_user runs `mkdir -p`.
# With the volume unmounted that silently creates the tree on / and the whole
# install lands there, to disappear the moment the volume is mounted. The same
# gap was found on HX-7 after the fact; 03-storage-ollama.sh has always done
# this correctly and this is the same shape.
findmnt /srv/omniroute >/dev/null || {
  echo "STOP: /srv/omniroute is not a mounted filesystem." >&2
  echo "      The dedicated volume must be mounted before OmniRoute is installed." >&2
  exit 34
}

hx_app_user omniroute /srv/omniroute

# Creating the user and chowning the tree is not the same as being able to
# write to it. A read-only mount passes findmnt and fails everything after.
sudo -u omniroute test -w /srv/omniroute || {
  echo "STOP: /srv/omniroute is not writable by the omniroute service identity." >&2
  exit 34
}

# Prove the pinned package resolves from the official registry, explicitly, so
# the check does not depend on the caller's npm configuration. Resolution and
# provenance are recorded before install; the install itself is pinned to the
# same version string.
echo "--- omniroute provenance, observed at install time ---"
echo "requested version: ${HX_OMNIROUTE_VERSION}"
npm view "omniroute@${HX_OMNIROUTE_VERSION}" version dist.integrity dist.tarball \
  --registry=https://registry.npmjs.org/

sudo npm install -g --registry=https://registry.npmjs.org/ "omniroute@${HX_OMNIROUTE_VERSION}"

# `|| true` hid a failed install, and the unit below then pointed at a path
# that may not exist. Fail here, and use the path that was actually installed.
OMNIROUTE_BIN="$(command -v omniroute)"
[ -x "$OMNIROUTE_BIN" ] || { echo "STOP: omniroute is not on PATH after install" >&2; exit 30; }

# F1: machine authority is hx-base.env -> this block -> the installed version.
# Capture what actually landed, normalize only the leading "v" some CLIs print,
# and fail hard on any mismatch before the unit is written or hx_app_done can
# report success. No fallback to latest or any other version.
OMNIROUTE_INSTALLED="$(omniroute --version 2>/dev/null || true)"
OMNIROUTE_INSTALLED="${OMNIROUTE_INSTALLED#v}"
case "$OMNIROUTE_INSTALLED" in
  [0-9]*) ;;
  *) echo "STOP: omniroute --version produced no usable version (got '${OMNIROUTE_INSTALLED}')" >&2; exit 31 ;;
esac
echo "actual installed version: ${OMNIROUTE_INSTALLED}"
echo "command path: ${OMNIROUTE_BIN}"
npm list -g --depth=0 omniroute
if [ "$OMNIROUTE_INSTALLED" != "$HX_OMNIROUTE_VERSION" ]; then
  echo "STOP: installed omniroute ${OMNIROUTE_INSTALLED} != pinned ${HX_OMNIROUTE_VERSION}" >&2
  echo "      hx-base.env is the version authority; reconcile the pin or the install, never fall back" >&2
  exit 33
fi

hx_app_unit hx-omniroute "HX OmniRoute ${OMNIROUTE_INSTALLED}" omniroute /srv/omniroute \
  "$OMNIROUTE_BIN" \
  "HOME=/srv/omniroute" \
  "PORT=${HX_OMNIROUTE_PORT}" \
  "HOST=0.0.0.0"

hx_app_validate hx-omniroute "$HX_OMNIROUTE_PORT" /v1/models

# F4: 20128 is LAN-facing and 20132 is loopback-only. hx_app_validate proves
# 20128 answers; this proves 20132 exists and is not reachable from the LAN.
# Environment text is not evidence - the binding is read from ss.
hx_require_loopback_listener "$(sudo ss -lntH)" "$HX_OMNIROUTE_LIVE_WS_PORT"
hx_app_done hx-omniroute "$HX_HOST" "OmniRoute ${OMNIROUTE_INSTALLED}" "http://${HX_IP}:${HX_OMNIROUTE_PORT}"

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
