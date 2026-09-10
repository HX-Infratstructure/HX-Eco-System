#!/usr/bin/env bash
# Install the HX shared reranker on HX-4.
#
# Model   : pinned BGE cross-encoder, fixed to an immutable commit revision.
# Runtime : Infinity from PyPI, run under systemd. No container, no Snap,
#           no Ubuntu archive package.
#
# Usage: ./04-reranker.sh hx-4
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-4)" >&2; exit 2; }
hx_require_host "$1"

echo "Model   : $HX_RERANKER_MODEL @ $HX_RERANKER_REVISION"
echo "Runtime : $HX_RERANKER_RUNTIME $HX_RERANKER_RUNTIME_VERSION"
echo "Listen  : $HX_RERANKER_HOST:$HX_RERANKER_PORT"

# python3-venv is a language runtime, not application software.
sudo apt install -y python3-venv

sudo mkdir -p "$HX_RERANKER_HOME"
id -u reranker >/dev/null 2>&1 || sudo useradd --system --home-dir "$HX_RERANKER_HOME" --shell /usr/sbin/nologin reranker
sudo chown -R reranker:reranker "$HX_RERANKER_HOME"

sudo -u reranker python3 -m venv "$HX_RERANKER_VENV"
sudo -u reranker "$HX_RERANKER_VENV/bin/python" -m pip install --upgrade pip
sudo -u reranker "$HX_RERANKER_VENV/bin/python" -m pip install \
  "infinity-emb[${HX_RERANKER_EXTRAS}]==${HX_RERANKER_RUNTIME_VERSION}"

"$HX_RERANKER_VENV/bin/infinity_emb" --version || true

sudo tee /etc/systemd/system/hx-reranker.service >/dev/null <<UNIT
[Unit]
Description=HX shared reranker (${HX_RERANKER_MODEL})
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=reranker
Group=reranker
Environment="HF_HOME=${HX_RERANKER_HOME}/hf"
ExecStart=${HX_RERANKER_VENV}/bin/infinity_emb v2 \
  --model-id ${HX_RERANKER_MODEL} \
  --revision ${HX_RERANKER_REVISION} \
  --served-model-name hx-reranker \
  --host ${HX_RERANKER_HOST} \
  --port ${HX_RERANKER_PORT}
Restart=on-failure
RestartSec=5
TimeoutStartSec=900

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable --now hx-reranker

# First start downloads the model, so allow time before checking.
echo "Waiting for the reranker to come up (first run downloads the model)..."
for _ in $(seq 1 90); do
  if curl -fsS "http://127.0.0.1:${HX_RERANKER_PORT}/health" >/dev/null 2>&1; then break; fi
  sleep 10
done

# Validation: does the service start.
systemctl is-active hx-reranker
systemctl is-enabled hx-reranker
curl -fsS "http://${HX_IP}:${HX_RERANKER_PORT}/health"; echo

cat <<SUMMARY

Reranker installed on $HX_HOST.
  endpoint   http://${HX_IP}:${HX_RERANKER_PORT}
  rerank     POST http://${HX_IP}:${HX_RERANKER_PORT}/rerank
  model      $HX_RERANKER_MODEL @ ${HX_RERANKER_REVISION}

Reboot-persistence check (run after the host comes back):
  systemctl is-active hx-reranker && curl -fsS http://127.0.0.1:${HX_RERANKER_PORT}/health

Then record the model, revision, runtime and version in docs/02-server-records/HX-4.md.
SUMMARY
