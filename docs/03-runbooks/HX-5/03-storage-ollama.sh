#!/usr/bin/env bash
# HX-5 wrapper for the common base block. All logic lives in ../common/.
# Pins and the host->IP map are in ../common/hx-base.env.
set -euo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../common" && pwd)/03-storage-ollama.sh" hx-5
