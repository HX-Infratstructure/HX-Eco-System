#!/usr/bin/env bash
# HX-6 OmniRoute AI gateway - built from the owner-approved upstream release
# branch, run natively under systemd.
#
# Not npm-global: 3.8.51 is not published to the npm registry, and the owner
# decision of 2026-09-17 is to deploy that release from source rather than take
# the older published 3.8.50. Registry provenance therefore does not apply here;
# the source commit is the provenance.
#
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

# /srv/omniroute is a dedicated volume and everything below writes into it.
# With the volume unmounted the whole build lands on / and disappears the
# moment it is mounted. Prove the mount before anything is created.
findmnt /srv/omniroute >/dev/null || {
  echo "STOP: /srv/omniroute is not a mounted filesystem." >&2
  echo "      The dedicated volume must be mounted before OmniRoute is built." >&2
  exit 34
}

hx_app_user omniroute /srv/omniroute

# Creating the user and chowning the tree is not the same as being able to
# write to it. A read-only mount passes findmnt and fails everything after.
sudo -u omniroute test -w /srv/omniroute || {
  echo "STOP: /srv/omniroute is not writable by the omniroute service identity." >&2
  exit 34
}

# ---------------------------------------------------------------------------
# Source, pinned to a commit rather than to a branch tip.
# ---------------------------------------------------------------------------
hx_require_source_pin "$HX_OMNIROUTE_COMMIT"

sudo install -d -o omniroute -g omniroute -m 750 "$HX_OMNIROUTE_APP_DIR"
sudo install -d -o omniroute -g omniroute -m 750 "$HX_OMNIROUTE_DATA_DIR"

if [ ! -d "$HX_OMNIROUTE_APP_DIR/.git" ]; then
  sudo -u omniroute git clone --branch "$HX_OMNIROUTE_BRANCH" \
    "$HX_OMNIROUTE_REPO" "$HX_OMNIROUTE_APP_DIR"
else
  sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" fetch --tags origin "$HX_OMNIROUTE_BRANCH"
fi

# The branch is how the commit is found; the commit is what is built. A branch
# tip moves, so checking one out at execution time would make two runs of this
# block produce different servers under the same recorded version.
sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" checkout -q --detach "$HX_OMNIROUTE_COMMIT"

OMNIROUTE_SHA="$(sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" rev-parse HEAD)"
[ "$OMNIROUTE_SHA" = "$HX_OMNIROUTE_COMMIT" ] || {
  echo "STOP: checked out $OMNIROUTE_SHA, expected $HX_OMNIROUTE_COMMIT" >&2
  exit 38
}

# A dirty tree means the built artifact is not the recorded commit.
sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" diff --quiet || {
  echo "STOP: $HX_OMNIROUTE_APP_DIR has uncommitted changes; the build would not be $OMNIROUTE_SHA" >&2
  exit 38
}

# ---------------------------------------------------------------------------
# Build. npm ci, because the lockfile is committed and a build day should not
# resolve its own dependency tree.
# ---------------------------------------------------------------------------
sudo -u omniroute env HOME=/srv/omniroute npm ci \
  --prefix "$HX_OMNIROUTE_APP_DIR" --no-audit --no-fund
sudo -u omniroute env HOME=/srv/omniroute npm run build \
  --prefix "$HX_OMNIROUTE_APP_DIR"

# `omniroute serve` runs the standalone bundle the build produces. Without it
# the CLI would fall back to a path that does not exist here.
[ -f "$HX_OMNIROUTE_APP_DIR/dist/server.js" ] || {
  echo "STOP: dist/server.js is absent after the build; there is nothing to serve." >&2
  exit 38
}

OMNIROUTE_CLI="$HX_OMNIROUTE_APP_DIR/bin/omniroute.mjs"
[ -f "$OMNIROUTE_CLI" ] || { echo "STOP: $OMNIROUTE_CLI is missing" >&2; exit 30; }

# ---------------------------------------------------------------------------
# Provenance and the version gate.
# ---------------------------------------------------------------------------
OMNIROUTE_INSTALLED="$(node "$OMNIROUTE_CLI" --version 2>/dev/null || true)"
OMNIROUTE_INSTALLED="${OMNIROUTE_INSTALLED#v}"
case "$OMNIROUTE_INSTALLED" in
  [0-9]*) ;;
  *) echo "STOP: omniroute --version produced no usable version (got '${OMNIROUTE_INSTALLED}')" >&2; exit 31 ;;
esac
if [ "$OMNIROUTE_INSTALLED" != "$HX_OMNIROUTE_VERSION" ]; then
  echo "STOP: built omniroute ${OMNIROUTE_INSTALLED} != pinned ${HX_OMNIROUTE_VERSION}" >&2
  echo "      hx-base.env is the version authority; reconcile the pin or the commit, never fall back" >&2
  exit 33
fi

cat <<PROV

=== PROVENANCE - copy into docs/02-server-records/HX-6.md, section 6 ===
Component:        OmniRoute ${OMNIROUTE_INSTALLED}
Source URI:       ${HX_OMNIROUTE_REPO}
Branch:           ${HX_OMNIROUTE_BRANCH}
Source commit:    ${OMNIROUTE_SHA}
package.json:     $(node -p "require('${HX_OMNIROUTE_APP_DIR}/package.json').version")
Built CLI:        ${OMNIROUTE_INSTALLED}   (node ${OMNIROUTE_CLI} --version)
App directory:    ${HX_OMNIROUTE_APP_DIR}
Node:             $(node --version)
npm:              $(npm --version)
Install method:   source build from the release branch, npm ci + npm run build
=======================================================================
PROV

# ---------------------------------------------------------------------------
# Runtime contract. Seven non-secret entries in the unit, four secrets in a
# root-owned EnvironmentFile.
# ---------------------------------------------------------------------------
hx_require_bind_var "$HX_OMNIROUTE_BIND_VAR"
hx_require_supplied_secret HX_OMNIROUTE_INITIAL_PASSWORD "${HX_OMNIROUTE_INITIAL_PASSWORD:-}"

# Generated once. Re-generating on a rerun would invalidate every key and token
# already issued against them, so an existing file is left alone.
if [ ! -f "$HX_OMNIROUTE_ENV_FILE" ]; then
  umask 077
  {
    printf 'JWT_SECRET=%s\n'                 "$(openssl rand -hex 32)"
    printf 'API_KEY_SECRET=%s\n'             "$(openssl rand -hex 32)"
    printf 'OMNIROUTE_WS_BRIDGE_SECRET=%s\n' "$(openssl rand -hex 32)"
    printf 'INITIAL_PASSWORD=%s\n'           "$HX_OMNIROUTE_INITIAL_PASSWORD"
  } | sudo tee "$HX_OMNIROUTE_ENV_FILE" >/dev/null
  echo "Wrote $HX_OMNIROUTE_ENV_FILE (secrets generated once; not re-generated on a rerun)."
else
  echo "$HX_OMNIROUTE_ENV_FILE exists; leaving the generated secrets in place."
fi

# root:root 0600. systemd reads this as PID 1 before dropping to User=, so the
# service identity never needs it. Values are never echoed and never become
# Environment= lines, so `systemctl show` does not print them.
sudo chown root:root "$HX_OMNIROUTE_ENV_FILE"
sudo chmod 600 "$HX_OMNIROUTE_ENV_FILE"
sudo stat -c '%U:%G %a %n' "$HX_OMNIROUTE_ENV_FILE"

HX_APP_ENV_FILE="$HX_OMNIROUTE_ENV_FILE"
hx_app_unit hx-omniroute "HX OmniRoute ${OMNIROUTE_INSTALLED}" omniroute "$HX_OMNIROUTE_APP_DIR" \
  "$(command -v node) ${OMNIROUTE_CLI} serve" \
  "HOME=/srv/omniroute" \
  "DATA_DIR=${HX_OMNIROUTE_DATA_DIR}" \
  "PORT=${HX_OMNIROUTE_PORT}" \
  "${HX_OMNIROUTE_BIND_VAR}=${HX_OMNIROUTE_BIND_ADDR}" \
  "REQUIRE_API_KEY=true" \
  "LIVE_WS_HOST=${HX_OMNIROUTE_LIVE_WS_HOST}" \
  "LIVE_WS_PORT=${HX_OMNIROUTE_LIVE_WS_PORT}"

hx_app_validate hx-omniroute "$HX_OMNIROUTE_PORT" /v1/models

# 20128 is LAN-facing and 20132 is loopback-only. hx_app_validate proves 20128
# answers; this proves 20132 exists and is not reachable from the LAN.
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
