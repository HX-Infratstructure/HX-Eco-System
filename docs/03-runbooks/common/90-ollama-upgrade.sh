#!/usr/bin/env bash
# Upgrade Ollama in place to the fleet pin in hx-base.env.
# Official install script only - not Snap, not the Ubuntu archive.
#
# Usage: ./90-ollama-upgrade.sh <hx-host>
#
# Safe to re-run. The install script replaces the binary and leaves
# /etc/systemd/system/ollama.service.d/storage.conf and /srv/ollama alone,
# so models are not re-downloaded.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-2)" >&2; exit 2; }
hx_require_host "$1"

BEFORE="$(ollama --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo none)"
echo "Installed: $BEFORE   Target: $HX_OLLAMA_VERSION"
if [ "$BEFORE" = "$HX_OLLAMA_VERSION" ]; then
  echo "Already at the fleet pin; nothing to do."
  exit 0
fi

echo "Models present before upgrade:"
ollama list || true

hx_ollama_install "$HX_OLLAMA_VERSION" "${HX_OLLAMA_ARCHIVE_SHA256:-}"

sudo systemctl daemon-reload
sudo systemctl restart ollama

AFTER="$(ollama --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
[ "$AFTER" = "$HX_OLLAMA_VERSION" ] || {
  echo "STOP: installed $AFTER but the pin is $HX_OLLAMA_VERSION" >&2
  exit 30
}

# Validation: does it start, and are the models still there.
systemctl is-active ollama
systemctl is-enabled ollama
ollama list
curl -fsS "http://$HX_IP:11434/api/version"; echo

cat <<SUMMARY

Ollama upgraded on $HX_HOST: $BEFORE -> $AFTER

Reboot-persistence check (run after the host comes back):
  systemctl is-active ollama && ollama --version && ollama list

Then update the Ollama version in docs/02-server-records/${HX_HOST^^}.md.
SUMMARY
