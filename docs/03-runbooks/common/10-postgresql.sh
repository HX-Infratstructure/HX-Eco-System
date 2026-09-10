#!/usr/bin/env bash
# HX-9 PostgreSQL - PGDG vendor repository.
# Usage: ./10-postgresql.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-9)" >&2; exit 2; }
hx_require_host "$1"

cat <<'SOURCE'
PACKAGE SOURCE NOTE
This is the one place a base build uses apt for application software.
It uses the PostgreSQL Global Development Group repository at
apt.postgresql.org, which is the vendor's own channel, not the Ubuntu archive
and not Snap. PGDG is already named as the PostgreSQL product authority in
skills/SKILL-REGISTRY.md.

The strict alternative is building PostgreSQL from the source tarball, which
also means initdb, the service user, and the unit by hand. That is a lot of
moving parts for no gain. If you want the strict-literal reading instead, say
so and this block gets rewritten as a source build.
SOURCE

sudo apt install -y curl ca-certificates
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -fsSL -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc \
  https://www.postgresql.org/media/keys/ACCC4CF8.asc
. /etc/os-release
echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] \
https://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME}-pgdg main" \
  | sudo tee /etc/apt/sources.list.d/pgdg.list >/dev/null

sudo apt update
sudo apt install -y "postgresql-${HX_POSTGRES_MAJOR}"

# Listen on the LAN, matching the fleet posture.
PGCONF="/etc/postgresql/${HX_POSTGRES_MAJOR}/main/postgresql.conf"
PGHBA="/etc/postgresql/${HX_POSTGRES_MAJOR}/main/pg_hba.conf"
sudo sed -i "s/^#\?listen_addresses.*/listen_addresses = '*'/" "$PGCONF"
grep -q '192.168.50.0/24' "$PGHBA" || \
  echo "host    all             all             192.168.50.0/24         scram-sha-256" \
  | sudo tee -a "$PGHBA" >/dev/null

sudo systemctl restart postgresql
hx_app_validate postgresql
sudo -u postgres psql -tAc 'select version()'
hx_app_done postgresql "$HX_HOST" "PostgreSQL ${HX_POSTGRES_MAJOR}" "postgresql://${HX_IP}:5432"

cat <<'NOTE'
HX-9 is a shared host: PostgreSQL and Redis each close separately. PostgreSQL
MCP is a separate companion gate.

Set the postgres role password before anything connects over the LAN:
  sudo -u postgres psql -c "\password postgres"
Do not put that password in the repository.
NOTE
