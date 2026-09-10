#!/usr/bin/env bash
# HX-12 wrapper for the common base block. All logic lives in ../common/.
# Pins and the host -> IP map are in ../common/hx-base.env.
set -euo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../common" && pwd)/01-base-admin-network-updates.sh" hx-12
