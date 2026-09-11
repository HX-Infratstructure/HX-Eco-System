#!/usr/bin/env bash
# HX-9 Redis - GitHub release source tarball, built natively.
# Usage: ./10-redis.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-9)" >&2; exit 2; }
hx_require_host "$1"

# Built from the upstream release tarball rather than taken from the Ubuntu
# archive, per the HX package-source rule. The build is a plain make.
sudo apt install -y build-essential pkg-config    # toolchain, not application software

TARBALL="redis-${HX_REDIS_VERSION}.tar.gz"
# The published release tarball, not the GitHub tag archive: GitHub builds
# a tag archive on request and its bytes are not guaranteed stable, so it
# cannot carry a checksum pin.
URL="https://download.redis.io/releases/${TARBALL}"

tmp="$(mktemp -d)"
hx_fetch_verified "$URL" "$tmp/redis.tar.gz" "${HX_REDIS_SHA256:-}"
tar -xzf "$tmp/redis.tar.gz" -C "$tmp"
make -C "$tmp/redis-${HX_REDIS_VERSION}" -j"$(nproc)"
sudo make -C "$tmp/redis-${HX_REDIS_VERSION}" install
rm -rf "$tmp"

redis-server --version

hx_app_user redis /srv/redis
sudo -u redis mkdir -p /srv/redis/data

sudo tee /srv/redis/redis.conf >/dev/null <<CONF
bind 0.0.0.0
port 6379
dir /srv/redis/data
appendonly yes
daemonize no
CONF
sudo chown redis:redis /srv/redis/redis.conf

hx_app_unit hx-redis "HX Redis ${HX_REDIS_VERSION}" redis /srv/redis \
  "/usr/local/bin/redis-server /srv/redis/redis.conf"

hx_app_validate hx-redis
redis-cli -h "$HX_IP" PING
hx_app_done hx-redis "$HX_HOST" "Redis ${HX_REDIS_VERSION}" "redis://${HX_IP}:6379"

cat <<'NOTE'
HX-9 is a shared host: PostgreSQL and Redis each close separately. Redis MCP is
a separate companion gate.
NOTE
