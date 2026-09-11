# Shared helpers for HX application installs.
# Sourced by the per-server 10-*.sh blocks. Not executable on its own.
#
# Validation here is deliberately minimal, per the operating definition:
#   does the service start, and does it survive a reboot.
# Nothing else is checked. Add more only when explicitly asked.

# Create a dedicated system user and its home directory.
hx_app_user() {
  local user="$1" home="$2"
  sudo mkdir -p "$home"
  id -u "$user" >/dev/null 2>&1 || \
    sudo useradd --system --home-dir "$home" --shell /usr/sbin/nologin "$user"
  sudo chown -R "$user:$user" "$home"
}

# Build a venv and install one pinned PyPI package into it.
# hx_app_venv <user> <venv-path> <pip-spec> [extra pip args...]
hx_app_venv() {
  local user="$1" venv="$2" spec="$3"; shift 3
  sudo apt install -y python3-venv          # language runtime, not application software
  sudo -u "$user" python3 -m venv "$venv"
  sudo -u "$user" "$venv/bin/python" -m pip install --upgrade pip
  sudo -u "$user" "$venv/bin/python" -m pip install "$spec" "$@"
  echo "Installed: $spec"
}

# Write a simple systemd unit, enable it, and start it.
# hx_app_unit <name> <description> <user> <workdir> <exec-line> [env "K=V" ...]
hx_app_unit() {
  local name="$1" desc="$2" user="$3" workdir="$4" exec_line="$5"; shift 5
  local env_lines=""
  for kv in "$@"; do env_lines+="Environment=\"$kv\"\n"; done

  sudo tee "/etc/systemd/system/${name}.service" >/dev/null <<UNIT
[Unit]
Description=${desc}
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${user}
Group=${user}
WorkingDirectory=${workdir}
$(printf "%b" "$env_lines")
ExecStart=${exec_line}
Restart=on-failure
RestartSec=5
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
UNIT

  sudo systemctl daemon-reload
  sudo systemctl enable --now "$name"
}

# Wait for a TCP port to answer, then confirm the service is up.
# hx_app_validate <unit> [port] [health-path]
hx_app_validate() {
  local unit="$1" port="${2:-}" path="${3:-/}"
  if [ -n "$port" ]; then
    echo "Waiting for $unit on port $port ..."
    for _ in $(seq 1 60); do
      curl -fsS -o /dev/null "http://127.0.0.1:${port}${path}" 2>/dev/null && break
      sleep 5
    done
  fi
  systemctl is-active "$unit"
  systemctl is-enabled "$unit"
  [ -n "$port" ] && { ss -ltn | grep ":$port" || true; }
  echo "$unit: started and enabled"
}

# Print the closing note every application block ends with.
# hx_app_done <unit> <host> <what> [url]
# Closing summary for a completed block.
#
# hx_app_done <unit|NONE> <host> <what> [url | reboot-check]
#
# Pass NONE as the unit for a library or CLI that has no daemon. It used to
# take a unit name unconditionally, so five blocks that never create a unit
# told the operator to run `systemctl is-active hx-<name>` after the reboot -
# a command that can only fail. With NONE the fourth argument is the check to
# run after a reboot instead, and it is required; with a unit name the fourth
# argument is the optional endpoint URL.
hx_app_done() {
  local unit="$1" host="$2" what="$3"
  local url="" recheck=""
  if [ "$unit" = "NONE" ]; then
    recheck="${4:?hx_app_done NONE requires the check to run after a reboot}"
  else
    url="${4:-}"
  fi
  cat <<DONE

${what} installed on ${host}.
$( [ -n "$url" ] && echo "  endpoint  ${url}" )

Reboot-persistence check, after the host comes back:
$( if [ "$unit" = "NONE" ]; then
     echo "  ${recheck}"
     echo "  (no unit: this component is a library or CLI, not a daemon)"
   else
     echo "  systemctl is-active ${unit}"
   fi )

Then record the installed version in docs/02-server-records/${host^^}.md,
set state and gate for ${host^^} in docs/00-control/hx-fleet.tsv, and run
tools/hx-doc/hx-fleet.
DONE
}

# Install Node.js from the official direct binary tarball, under /usr/local.
# Not Snap, not the Ubuntu archive, not NodeSource. Idempotent.
hx_node_install() {
  local version="$1"
  if command -v node >/dev/null 2>&1 && [ "v$version" = "$(node --version)" ]; then
    echo "Node.js v$version already installed"
    return 0
  fi
  local tarball="node-v${version}-linux-x64.tar.xz"
  local url="https://nodejs.org/dist/v${version}/${tarball}"
  local tmp; tmp="$(mktemp -d)"
  curl -fsSL "$url" -o "$tmp/$tarball"
  curl -fsSL "https://nodejs.org/dist/v${version}/SHASUMS256.txt" -o "$tmp/SHASUMS256.txt"
  ( cd "$tmp" && grep " $tarball\$" SHASUMS256.txt | sha256sum -c - )
  sudo tar -xJf "$tmp/$tarball" -C /usr/local --strip-components=1 \
    --exclude=CHANGELOG.md --exclude=LICENSE --exclude=README.md
  rm -rf "$tmp"
  node --version
  npm --version
}
