#!/usr/bin/env bash
# HX-4 wrapper for the common block. All logic lives in ../common/.
# Pins and the host->IP map are in ../common/hx-base.env.
set -euo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../common" && pwd)/05-gpt-oss.sh" hx-4
