#!/usr/bin/env bash
# HX pre-block foundation - the state every host must reach before Block 1.
#
# Usage: ./00-foundation.sh <hx-host>      e.g. hx-6
#
# Establishes identity, time authority, the admin account, fleet-key access and
# SSH persistence. Block 1 then refuses to proceed unless all of it is true, so
# a skipped run here is caught rather than inherited.
#
# D-026: this script VALIDATES network state and never writes it. The address,
# gateway and DNS come from the installer. A mismatch stops the run rather than
# being corrected here, because changing host networking is not an authority
# the build process holds.
#
# Idempotent. Safe to re-run; the fleet key is present exactly once afterwards.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-6)" >&2; exit 2; }
hx_require_host "$1"

FQDN_WANT="$HX_HOST.$HX_DOMAIN"
ADMIN_HOME="/home/$HX_ADMIN_USER"

echo "--- network, validated not written (D-026) ---"
ADDRS="$(ip -4 -br addr)"
ROUTES="$(ip route)"
RESOLV="$(resolvectl status)"
grep -q "$HX_IP/24" <<<"$ADDRS" || { echo "STOP: expected IP $HX_IP/24 not found"; exit 11; }
grep -q "^default via $HX_GATEWAY " <<<"$ROUTES" || { echo "STOP: expected gateway $HX_GATEWAY not found"; exit 12; }
grep -q "$HX_DC_IP" <<<"$RESOLV" || { echo "STOP: expected HX-1 DNS $HX_DC_IP not found"; exit 13; }
echo "network: PASS (unchanged)"

echo "--- identity ---"
sudo hostnamectl set-hostname "$HX_HOST"
# The FQDN has to resolve locally. Rewrite the 127.0.1.1 line rather than
# appending, so re-running does not accumulate entries.
sudo sh -c "set -e
tmp=/etc/hosts.hx.tmp
grep -v '^127\.0\.1\.1[[:space:]]' /etc/hosts > \"\$tmp\"
printf '127.0.1.1\t%s %s\n' '$FQDN_WANT' '$HX_HOST' >> \"\$tmp\"
chown root:root \"\$tmp\"; chmod 0644 \"\$tmp\"
mv \"\$tmp\" /etc/hosts"
echo "hostname -f: $(hostname -f)"

echo "--- time authority: HX-1 ---"
if ! command -v chronyc >/dev/null 2>&1; then
  sudo apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y chrony
fi
# A drop-in, so the distribution pool file stays untouched and re-running does
# not duplicate directives the way an appended line would.
sudo sh -c "set -e
mkdir -p /etc/chrony/conf.d
printf 'server %s iburst prefer\n' '$HX_NTP_SERVER' > /etc/chrony/conf.d/10-hx-fleet.conf
chmod 0644 /etc/chrony/conf.d/10-hx-fleet.conf"
# Order matters. chrony must be running before the old source is touched, and
# on Ubuntu the chrony package removes systemd-timesyncd outright - so on a
# fresh install there is nothing left to disable, and nothing to restore if
# this goes wrong. Only disable it where it actually still exists.
sudo systemctl enable --now chrony
# apt-get install starts chrony before this script writes the drop-in, and
# `enable --now` does nothing to a service that is already running - so chrony
# keeps the configuration it started with and never reads HX-1 at all. Both
# HX-3 and HX-4 failed this way: the drop-in was on disk two seconds after
# chrony started, and stayed unread. Restart, do not assume.
sudo systemctl restart chrony
if systemctl list-unit-files systemd-timesyncd.service >/dev/null 2>&1; then
  sudo systemctl disable --now systemd-timesyncd 2>/dev/null || true
fi
sudo chronyc -a makestep >/dev/null 2>&1 || true

# Cold-start selection takes longer than it looks: chrony has to reach the
# server, collect enough samples to trust it, and only then prefer it over the
# pool. HX-4 selected a public source first and reached HX-1 about a minute
# later, so a sixty-second window reported a false failure. Three minutes.
HX_NTP_OK=0
for _ in $(seq 1 36); do
  if hx_ntp_selected "$(chronyc sources 2>/dev/null || true)" "$HX_NTP_SERVER"; then
    HX_NTP_OK=1
    break
  fi
  sleep 5
done
chronyc sources -v || true

if [ "$HX_NTP_OK" -ne 1 ]; then
  # Leave chrony running. There is no fallback to return to - the package
  # removed systemd-timesyncd - so stopping chrony here would leave the host
  # with no time source at all. That is not a clock problem on a domain-joined
  # host: Kerberos rejects a skewed ticket, SSSD stops resolving identities,
  # and domain logins fail. chrony is keeping time from the pool meanwhile; it
  # has simply not settled on HX-1 yet, and Block 1 refuses the build until it
  # does.
  echo "STOP: $HX_NTP_SERVER is not the selected source after 3 minutes." >&2
  echo "      chrony is left running, so this host still keeps time." >&2
  echo "      Re-check with: chronyc sources" >&2
  exit 42
fi
echo "time authority: $HX_NTP_SERVER selected"

echo "--- admin account and sudo ---"
id "$HX_ADMIN_USER" >/dev/null 2>&1 || sudo useradd -m -s /bin/bash "$HX_ADMIN_USER"
sudo sh -c 'set -e
tmp=/etc/sudoers.d/90-hx-admin.tmp
umask 022
printf "%s\n" "hxsa ALL=(ALL:ALL) NOPASSWD: ALL" > "$tmp"
chown root:root "$tmp"; chmod 0440 "$tmp"
visudo -cf "$tmp"
mv "$tmp" /etc/sudoers.d/90-hx-admin
visudo -c'

echo "--- fleet key (D-027: from the committed public key) ---"
[ -f "$HX_FLEET_KEY_PUB" ] || { echo "STOP: $HX_FLEET_KEY_PUB missing from the runbooks"; exit 43; }
# Verify what we are about to install before installing it.
hx_require_fleet_key "$HX_FLEET_KEY_PUB" "$HX_FLEET_KEY_FINGERPRINT"
KEY_LINE="$(cat "$HX_FLEET_KEY_PUB")"
sudo -u "$HX_ADMIN_USER" sh -c "set -e
umask 077
mkdir -p '$ADMIN_HOME/.ssh'
touch '$ADMIN_HOME/.ssh/authorized_keys'
grep -qxF \"\$1\" '$ADMIN_HOME/.ssh/authorized_keys' || printf '%s\n' \"\$1\" >> '$ADMIN_HOME/.ssh/authorized_keys'
chmod 700 '$ADMIN_HOME/.ssh'
chmod 600 '$ADMIN_HOME/.ssh/authorized_keys'" _ "$KEY_LINE"
sudo chown -R "$HX_ADMIN_USER:$HX_ADMIN_USER" "$ADMIN_HOME/.ssh"
ssh-keygen -lf "$ADMIN_HOME/.ssh/authorized_keys"

echo "--- ssh persistence ---"
sudo systemctl enable ssh.socket 2>/dev/null || sudo systemctl enable ssh
systemctl is-enabled ssh || true
systemctl is-enabled ssh.socket || true

echo
echo "Foundation complete on $HX_HOST."
echo "Next: prove it from the workstation, not from here."
echo "  tools/hx-doc/hx-fleet-access $HX_HOST"
echo "Then run 01-base-admin-network-updates.sh $HX_HOST."
