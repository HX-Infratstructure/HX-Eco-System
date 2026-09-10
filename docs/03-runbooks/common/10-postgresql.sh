#!/usr/bin/env bash
# HX-9 PostgreSQL - official source tarball from postgresql.org, built natively.
# Usage: ./10-postgresql.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-9)" >&2; exit 2; }
hx_require_host "$1"

PGHOME="/srv/postgresql"
PGDATA="$PGHOME/data"

# Toolchain and library headers only. The application itself is built from the
# upstream source tarball, not taken from any distribution repository.
sudo apt install -y build-essential pkg-config \
  libreadline-dev zlib1g-dev libicu-dev libssl-dev

TARBALL="postgresql-${HX_POSTGRES_VERSION}.tar.bz2"
URL="https://ftp.postgresql.org/pub/source/v${HX_POSTGRES_VERSION}/${TARBALL}"

tmp="$(mktemp -d)"
curl -fsSL "$URL" -o "$tmp/$TARBALL"

# Verify against the hash published alongside the tarball and pinned in
# hx-base.env. A mismatch stops the build.
echo "${HX_POSTGRES_SHA256}  $tmp/$TARBALL" | sha256sum -c - || {
  echo "STOP: PostgreSQL tarball hash does not match the pin" >&2
  exit 30
}

tar -xjf "$tmp/$TARBALL" -C "$tmp"
(
  cd "$tmp/postgresql-${HX_POSTGRES_VERSION}"
  ./configure --prefix="$PGHOME" --with-openssl --with-icu
  make -j"$(nproc)"
  sudo make install
)
rm -rf "$tmp"

"$PGHOME/bin/postgres" --version

hx_app_user postgres "$PGHOME"
sudo -u postgres mkdir -p "$PGDATA"
sudo chmod 0700 "$PGDATA"

if [ ! -f "$PGDATA/PG_VERSION" ]; then
  sudo -u postgres "$PGHOME/bin/initdb" -D "$PGDATA" --encoding=UTF8 --locale=C.UTF-8
else
  echo "Existing cluster found at $PGDATA; leaving it alone"
fi

# Listen on the LAN, matching the fleet posture.
sudo -u postgres sed -i "s/^#\?listen_addresses.*/listen_addresses = '*'/" "$PGDATA/postgresql.conf"
sudo grep -q '192.168.50.0/24' "$PGDATA/pg_hba.conf" || \
  echo "host    all             all             192.168.50.0/24         scram-sha-256" \
  | sudo -u postgres tee -a "$PGDATA/pg_hba.conf" >/dev/null

sudo tee /etc/systemd/system/hx-postgresql.service >/dev/null <<UNIT
[Unit]
Description=HX PostgreSQL ${HX_POSTGRES_VERSION}
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
User=postgres
Group=postgres
Environment="PGDATA=${PGDATA}"
ExecStart=${PGHOME}/bin/postgres -D ${PGDATA}
ExecReload=/bin/kill -HUP \$MAINPID
KillSignal=SIGINT
TimeoutSec=300
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
sudo systemctl enable --now hx-postgresql

hx_app_validate hx-postgresql
sudo -u postgres "$PGHOME/bin/psql" -tAc 'select version()'
hx_app_done hx-postgresql "$HX_HOST" "PostgreSQL ${HX_POSTGRES_VERSION}" "postgresql://${HX_IP}:5432"

cat <<'NOTE'
Add the client tools to PATH for interactive use:
  echo 'export PATH=/srv/postgresql/bin:$PATH' | sudo tee /etc/profile.d/hx-postgresql.sh

Set the postgres role password before anything connects over the LAN:
  sudo -u postgres /srv/postgresql/bin/psql -c "\password postgres"
Do not put that password in the repository.

HX-9 is a shared host: PostgreSQL and Redis each close separately. PostgreSQL
MCP is a separate companion gate.
NOTE
