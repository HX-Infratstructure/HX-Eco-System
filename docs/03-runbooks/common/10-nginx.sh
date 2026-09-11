#!/usr/bin/env bash
# HX-7 NGINX dev/test rendering only - upstream stable source, built natively.
# Usage: ./10-nginx.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-7)" >&2; exit 2; }
hx_require_host "$1"

# D-004 and the NGINX role standard: HX-7 renders UIs for applications under
# active development. It is NOT the ecosystem front door for Qdrant, LightRAG,
# n8n, Open WebUI, databases, or MCP servers.
sudo apt install -y build-essential libpcre2-dev zlib1g-dev libssl-dev   # toolchain and headers

URL="https://nginx.org/download/nginx-${HX_NGINX_VERSION}.tar.gz"
tmp="$(mktemp -d)"
hx_fetch_verified "$URL" "$tmp/nginx.tar.gz" "${HX_NGINX_SHA256:-}"
tar -xzf "$tmp/nginx.tar.gz" -C "$tmp"
(
  cd "$tmp/nginx-${HX_NGINX_VERSION}"
  ./configure \
    --prefix=/srv/nginx \
    --sbin-path=/usr/local/sbin/nginx \
    --conf-path=/srv/nginx/nginx.conf \
    --pid-path=/run/nginx.pid \
    --error-log-path=/srv/nginx/logs/error.log \
    --http-log-path=/srv/nginx/logs/access.log \
    --with-http_ssl_module \
    --with-http_v2_module
  make -j"$(nproc)"
  sudo make install
)
rm -rf "$tmp"

nginx -v
sudo mkdir -p /srv/nginx/conf.d
grep -q 'conf.d/\*.conf' /srv/nginx/nginx.conf || \
  sudo sed -i 's#^\(\s*\)include\s\+mime.types;#\1include mime.types;\n\1include /srv/nginx/conf.d/*.conf;#' /srv/nginx/nginx.conf
sudo nginx -t

sudo tee /etc/systemd/system/hx-nginx.service >/dev/null <<'UNIT'
[Unit]
Description=HX NGINX (development and test rendering only)
After=network-online.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/local/sbin/nginx -t
ExecStart=/usr/local/sbin/nginx
ExecReload=/usr/local/sbin/nginx -s reload
ExecStop=/usr/local/sbin/nginx -s quit
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable --now hx-nginx
hx_app_validate hx-nginx 80
hx_app_done hx-nginx "$HX_HOST" "NGINX ${HX_NGINX_VERSION}" "http://${HX_IP}/"

cat <<'NOTE'
Put development server blocks in /srv/nginx/conf.d/ and reload. Remove a
temporary development proxy when the work that needed it is finished.
NOTE
