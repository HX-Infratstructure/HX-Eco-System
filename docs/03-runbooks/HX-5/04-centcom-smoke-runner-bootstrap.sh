#!/usr/bin/env bash
set -euo pipefail

if [[ "$(hostname -s)" != "hx-5" ]]; then
  echo "ERROR: this bootstrap is authorized only for HX-5 CentCom." >&2
  exit 1
fi

HX_ECO_REPO="${HX_ECO_REPO:-$HOME/src/HX-Eco-System}"
HX_SMOKE_ROOT="${HX_SMOKE_ROOT:-$HOME/hx-smoke-runs}"
HX_SMOKE_VENV="${HX_SMOKE_VENV:-$HOME/.venvs/hx-smoke-runner}"
TOOLS_DIR="$HX_ECO_REPO/tools/hx-smoke-runner"

[[ -d "$HX_ECO_REPO/.git" ]] || {
  echo "ERROR: expected authenticated HX-Eco-System checkout at $HX_ECO_REPO" >&2
  echo "Set HX_ECO_REPO to the existing checkout path and rerun." >&2
  exit 1
}
[[ -f "$TOOLS_DIR/requirements.txt" ]] || { echo "ERROR: runner tools missing from repo checkout." >&2; exit 1; }

sudo apt-get update
sudo apt-get install -y \
  ca-certificates \
  curl \
  git \
  jq \
  openssh-client \
  postgresql-client \
  python3 \
  python3-pip \
  python3-venv \
  redis-tools

mkdir -p "$(dirname "$HX_SMOKE_VENV")" "$HX_SMOKE_ROOT" "$HOME/.local/bin"
python3 -m venv "$HX_SMOKE_VENV"
"$HX_SMOKE_VENV/bin/python" -m pip install --upgrade pip
"$HX_SMOKE_VENV/bin/python" -m pip install -r "$TOOLS_DIR/requirements.txt"

# Playwright-managed Chromium only; no Node/npm stack and no container runtime.
sudo "$HX_SMOKE_VENV/bin/python" -m playwright install-deps chromium
"$HX_SMOKE_VENV/bin/python" -m playwright install chromium

for name in hx-smoke-new hx-smoke-promote hx-smoke-ui-capture hx-smoke-doctor; do
  ln -sfn "$TOOLS_DIR/$name" "$HOME/.local/bin/$name"
done

chmod 0700 "$HX_SMOKE_ROOT"

cat <<EOF_SUMMARY
HX-5 CentCom smoke-runner bootstrap complete.
HX_ECO_REPO=$HX_ECO_REPO
HX_SMOKE_ROOT=$HX_SMOKE_ROOT
HX_SMOKE_VENV=$HX_SMOKE_VENV

Next:
  export PATH="$HOME/.local/bin:\$PATH"
  hx-smoke-doctor
  hx-smoke-doctor --remote   # activation proof against already-proven HX-2
EOF_SUMMARY
