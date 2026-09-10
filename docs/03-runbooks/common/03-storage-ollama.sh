#!/usr/bin/env bash
# HX common base block 3 - verify domain/GPU/storage, install pinned Ollama.
# Usage: ./03-storage-ollama.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-4)" >&2; exit 2; }
hx_require_host "$1"

realm list
systemctl is-active sssd
id "$HX_DOMAIN_TEST_USER" || { echo "STOP: domain user resolution failed" >&2; exit 15; }
nvidia-smi
systemctl --failed --no-pager
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
df -hT

findmnt /srv/ollama || { echo "STOP: /srv/ollama is not mounted"; exit 20; }
sudo find /srv/ollama -mindepth 1 -maxdepth 1 ! -name lost+found -printf '%f\n'
if sudo find /srv/ollama -mindepth 1 -maxdepth 1 ! -name lost+found -print -quit | grep -q .; then
  echo "STOP: existing content found in /srv/ollama"
  exit 21
fi

# Pin the Ollama version so a new server matches the recorded fleet baseline.
# Clear HX_OLLAMA_VERSION in hx-base.env to take the current release instead,
# and record the resolved version in the server record before closing it.
if [ -n "${HX_OLLAMA_VERSION:-}" ]; then
  echo "Installing pinned Ollama $HX_OLLAMA_VERSION"
  curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION="$HX_OLLAMA_VERSION" sh
else
  echo "WARNING: no Ollama pin set; installing current release"
  curl -fsSL https://ollama.com/install.sh | sh
fi

sudo mkdir -p /srv/ollama/models
sudo chown -R ollama:ollama /srv/ollama
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/storage.conf >/dev/null <<'EOC'
[Service]
Environment="OLLAMA_MODELS=/srv/ollama/models"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NO_CLOUD=1"
EOC
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl enable ollama

INSTALLED="$(ollama --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
echo "Ollama installed version: $INSTALLED"
if [ -n "${HX_OLLAMA_VERSION:-}" ] && [ "$INSTALLED" != "$HX_OLLAMA_VERSION" ]; then
  echo "STOP: installed Ollama $INSTALLED does not match pin $HX_OLLAMA_VERSION" >&2
  exit 22
fi

systemctl is-active ollama
systemctl is-enabled ollama
systemctl show ollama --property=Environment --value | tr ' ' '\n' | grep '^OLLAMA_'
ls -ld /srv/ollama /srv/ollama/models
ss -ltn | grep ':11434'
curl -s http://127.0.0.1:11434/api/version
curl -s "http://$HX_IP:11434/api/version"
echo
echo "Block 3 complete on $HX_HOST; ready for server-specific model/application installation"
