#!/usr/bin/env bash
# HX-17 Crawl4AI - PyPI, native venv, Playwright Chromium.
# Usage: ./10-crawl4ai.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-17)" >&2; exit 2; }
hx_require_host "$1"

hx_app_user crawl4ai /srv/crawl4ai
hx_app_venv crawl4ai /srv/crawl4ai/venv "crawl4ai==${HX_CRAWL4AI_VERSION}"

# Crawl4AI drives a real browser. Playwright's own Chromium only, no container.
#
# Playwright resolves and verifies its own browser build, so there is no
# separate URL for this block to checksum. What that costs is traceability:
# the build that lands depends on the Playwright version crawl4ai pulled.
# Record the resolved Playwright and Chromium builds in the server record so
# the browser is identified as precisely as everything else on the host.
sudo /srv/crawl4ai/venv/bin/python -m playwright install-deps chromium
sudo -u crawl4ai env HOME=/srv/crawl4ai \
  /srv/crawl4ai/venv/bin/python -m playwright install chromium

# Print the Playwright version that resolved, so the server record can name the
# build lineage of the browser this host will run.
/srv/crawl4ai/venv/bin/python -m playwright --version

# The doctor is the stated validation for this block, so it has to be able
# to fail. `|| true` made it decoration.
sudo -u crawl4ai env HOME=/srv/crawl4ai /srv/crawl4ai/venv/bin/crawl4ai-doctor

hx_app_done NONE "$HX_HOST" "Crawl4AI ${HX_CRAWL4AI_VERSION}" \
  "sudo -u crawl4ai env HOME=/srv/crawl4ai /srv/crawl4ai/venv/bin/crawl4ai-doctor"

cat <<'NOTE'
Crawl4AI is a library and CLI, not a daemon, so the core install has no unit.
Validation is: a deterministic raw: crawl produces Markdown, and it still works
after a reboot.

The official Crawl4AI MCP bridge is coupled to their Docker server tree, which
HX does not use. The native MCP implementation is not yet selected; do not
invent one here.
NOTE
