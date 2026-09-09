#!/usr/bin/env bash
set -euo pipefail
realm list
systemctl is-active sssd
id 'jarvisr@hx.local.arpa'
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
curl -fsSL https://ollama.com/install.sh | sh
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
ollama --version
systemctl is-active ollama
systemctl is-enabled ollama
systemctl show ollama --property=Environment --value | tr ' ' '\n' | grep '^OLLAMA_'
ls -ld /srv/ollama /srv/ollama/models
ss -ltn | grep ':11434'
curl -s http://127.0.0.1:11434/api/version
curl -s http://192.168.50.204:11434/api/version
echo "Block 3 complete; ready for server-specific model/application installation"
