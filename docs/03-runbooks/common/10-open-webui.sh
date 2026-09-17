#!/usr/bin/env bash
# HX-8 Open WebUI - PyPI wheel into a native venv, run under systemd.
# Usage: ./10-open-webui.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"
# shellcheck source=./hx-app-lib.sh
. "$SCRIPT_DIR/hx-app-lib.sh"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (hx-8)" >&2; exit 2; }
hx_require_host "$1"

# /srv/openwebui is a dedicated volume and everything below writes into it:
# the SQLite database, uploads and the Hugging Face cache all live there. With
# the volume unmounted that tree lands on / and disappears the moment it is
# mounted. Same shape as 03-storage-ollama.sh and 10-omniroute.sh.
findmnt /srv/openwebui >/dev/null || {
  echo "STOP: /srv/openwebui is not a mounted filesystem." >&2
  echo "      The dedicated volume must be mounted before Open WebUI is installed." >&2
  exit 34
}

hx_app_user openwebui /srv/openwebui

sudo -u openwebui test -w /srv/openwebui || {
  echo "STOP: /srv/openwebui is not writable by the openwebui service identity." >&2
  exit 34
}

# The pinned Open WebUI release declares a requires_python range, recorded as
# HX_OPEN_WEBUI_PY_MIN and HX_OPEN_WEBUI_PY_MAX. hx_app_venv builds with the
# system python3, so the interpreter is an inherited assumption rather than a
# pin. Ubuntu 24.04 ships 3.12 and satisfies it; a host outside the range fails
# during pip resolution with a message about wheels rather than about Python.
hx_require_python_range "$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')" \
  "$HX_OPEN_WEBUI_PY_MIN" "$HX_OPEN_WEBUI_PY_MAX"

# Extras are opt-in. `all` pulls thirteen packages including Azure Search,
# Pinecone, Oracle and Elasticsearch clients, which is the line D-010 draws for
# HX-6: shipping a connector is not approving it. HX_OPEN_WEBUI_EXTRAS is empty
# until a named HX capability needs one.
if [ -n "${HX_OPEN_WEBUI_EXTRAS:-}" ]; then
  OPEN_WEBUI_SPEC="open-webui[${HX_OPEN_WEBUI_EXTRAS}]==${HX_OPEN_WEBUI_VERSION}"
  echo "Extras requested: ${HX_OPEN_WEBUI_EXTRAS}"
else
  OPEN_WEBUI_SPEC="open-webui==${HX_OPEN_WEBUI_VERSION}"
  echo "No extras requested; installing the base package only."
fi

hx_app_venv openwebui /srv/openwebui/venv "$OPEN_WEBUI_SPEC"

OPEN_WEBUI_BIN=/srv/openwebui/venv/bin/open-webui
[ -x "$OPEN_WEBUI_BIN" ] || { echo "STOP: $OPEN_WEBUI_BIN is missing after install" >&2; exit 30; }

# An installer's exit code is not proof of what landed. HX-6 spent a build day
# on npm reporting success while silently dropping a package, so the version is
# read back from the thing that will actually run.
OPEN_WEBUI_INSTALLED="$(sudo -u openwebui "$OPEN_WEBUI_BIN" --version 2>/dev/null | tr -cd '0-9.' || true)"
case "$OPEN_WEBUI_INSTALLED" in
  [0-9]*) ;;
  *) echo "STOP: open-webui --version produced no usable version (got '${OPEN_WEBUI_INSTALLED}')" >&2; exit 31 ;;
esac
if [ "$OPEN_WEBUI_INSTALLED" != "$HX_OPEN_WEBUI_VERSION" ]; then
  echo "STOP: installed open-webui ${OPEN_WEBUI_INSTALLED} != pinned ${HX_OPEN_WEBUI_VERSION}" >&2
  echo "      hx-base.env is the version authority; reconcile the pin or the install, never fall back" >&2
  exit 33
fi

sudo install -d -o openwebui -g openwebui -m 750 "$HX_OPEN_WEBUI_DATA_DIR"
sudo install -d -o openwebui -g openwebui -m 750 /srv/openwebui/hf

cat <<PROV

=== PROVENANCE - copy into docs/02-server-records/HX-8.md, section 6 ===
Component:        Open WebUI ${OPEN_WEBUI_INSTALLED}
Source URI:       https://pypi.org/project/open-webui/${HX_OPEN_WEBUI_VERSION}/
Install method:   pip wheel into a native venv at /srv/openwebui/venv
Extras:           ${HX_OPEN_WEBUI_EXTRAS:-none}
Installed version: ${OPEN_WEBUI_INSTALLED}   (${OPEN_WEBUI_BIN} --version)
Python:           $(python3 -c 'import sys; print(sys.version.split()[0])')
Data directory:   ${HX_OPEN_WEBUI_DATA_DIR}
=======================================================================
PROV

# ---------------------------------------------------------------------------
# Runtime contract.
#
# Authentication stays ON. Upstream's default is WEBUI_AUTH=True, and this
# block used to override it to False. On a LAN-facing UI wired to a proven
# Ollama endpoint for the D-008 proof, that leaves the inference plane open to
# anything that can reach the port. The first account is created manually and
# becomes admin; no bootstrap credentials are persisted by this block.
# ---------------------------------------------------------------------------
# WEBUI_SECRET_KEY signs sessions. Left unset, the CLI generates one into its
# working directory and nothing manages it; losing or moving that file
# invalidates every session silently. Generated once here, kept out of the unit.
if [ ! -f "$HX_OPEN_WEBUI_ENV_FILE" ]; then
  umask 077
  printf 'WEBUI_SECRET_KEY=%s\n' "$(openssl rand -hex 32)" \
    | sudo tee "$HX_OPEN_WEBUI_ENV_FILE" >/dev/null
  echo "Wrote $HX_OPEN_WEBUI_ENV_FILE (secret generated once; not re-generated on a rerun)."
else
  echo "$HX_OPEN_WEBUI_ENV_FILE exists; leaving the generated secret in place."
fi

# root:root 0600. systemd reads this as PID 1 before dropping to User=, so the
# service identity never needs it. Values are never echoed and never become
# Environment= lines, so `systemctl show` does not print them.
sudo chown root:root "$HX_OPEN_WEBUI_ENV_FILE"
sudo chmod 600 "$HX_OPEN_WEBUI_ENV_FILE"
sudo stat -c '%U:%G %a %n' "$HX_OPEN_WEBUI_ENV_FILE"

hx_app_unit --env-file "$HX_OPEN_WEBUI_ENV_FILE" \
  hx-open-webui "HX Open WebUI ${OPEN_WEBUI_INSTALLED}" openwebui /srv/openwebui \
  "${OPEN_WEBUI_BIN} serve --host 0.0.0.0 --port ${HX_OPEN_WEBUI_PORT}" \
  "DATA_DIR=${HX_OPEN_WEBUI_DATA_DIR}" \
  "HF_HOME=/srv/openwebui/hf" \
  "WEBUI_AUTH=True" \
  "ENABLE_SIGNUP=False"

hx_app_validate hx-open-webui "$HX_OPEN_WEBUI_PORT" /health
hx_app_done hx-open-webui "$HX_HOST" "Open WebUI ${OPEN_WEBUI_INSTALLED}" "http://${HX_IP}:${HX_OPEN_WEBUI_PORT}"

cat <<'NOTE'
OPERATOR ACTION REQUIRED before this server can close.

Authentication is ON and signup is closed, so no account exists yet. Create the
first account, which becomes the administrator, before anyone else can reach the
UI. Leaving ENABLE_SIGNUP=False with no account means nobody can sign in; that
is deliberate, so the window where the UI is open is one you choose.

BASE PASS also needs D-008: temporarily point Open WebUI at one already-proven
Ollama endpoint, send one prompt, confirm a response renders, capture evidence,
then remove the temporary connection.
NOTE
