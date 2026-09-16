#!/usr/bin/env bash
# HX common base block 1 - identity, network, admin sudo, updates, reboot.
# Usage: ./01-base-admin-network-updates.sh <hx-host>      e.g. hx-4
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-4)" >&2; exit 2; }
hx_require_host "$1"

# ===========================================================================
# FOUNDATION GATE
#
# The 2026-09-16 Layer 0/1 audit found that this block validated only what it
# configured. Identity, time authority and fleet-key access were never
# configured by any block, so nothing ever checked them - on any host, ever.
# Three of four closed servers failed at least one of them.
#
# 00-foundation.sh establishes this state. This gate refuses to continue
# without it, so a skipped foundation run is caught rather than inherited.
#
# D-026: network is validated here and never written. A mismatch stops the
# build; correcting host networking is not an authority this process holds.
# ===========================================================================
hostnamectl
ip -br addr
ip route

# `cmd | grep -q` makes grep close the pipe at its first match, which kills the
# writer with SIGPIPE (141). Under `set -o pipefail` that fails the pipeline
# even though the match succeeded, so match on captured output instead.
# HX-4 lists a third link after eno1, which is enough for resolvectl to still
# be writing when grep leaves.
ADDRS="$(ip -4 -br addr)"
ROUTES="$(ip route)"
grep -q "$HX_IP/24" <<<"$ADDRS" || { echo "STOP: expected IP $HX_IP/24 not found"; exit 11; }
grep -q "^default via $HX_GATEWAY " <<<"$ROUTES" || { echo "STOP: expected gateway $HX_GATEWAY not found"; exit 12; }
RESOLV="$(resolvectl status)"
printf '%s\n' "$RESOLV"
grep -q "$HX_DC_IP" <<<"$RESOLV" || { echo "STOP: expected HX-1 DNS $HX_DC_IP not found"; exit 13; }

# Identity. A short name here means the FQDN is not resolvable locally.
hx_require_fqdn "$(hostname -f)" "$HX_HOST.$HX_DOMAIN"

# Time authority. HX-1 must be the selected source, not merely configured.
hx_require_ntp_source "$(chronyc sources 2>/dev/null || true)" "$HX_NTP_SERVER"

# Fleet access. The approved key, by fingerprint - not merely some key.
hx_require_fleet_key "/home/$HX_ADMIN_USER/.ssh/authorized_keys" "$HX_FLEET_KEY_FINGERPRINT"

# SSH persistence. Ubuntu may carry this on the socket rather than the service.
hx_require_ssh_persistence \
  "$(systemctl is-enabled ssh 2>/dev/null || true)" \
  "$(systemctl is-enabled ssh.socket 2>/dev/null || true)"

echo "FOUNDATION GATE: PASS"

sudo sh -c 'set -e
tmp=/etc/sudoers.d/90-hx-admin.tmp
umask 022
printf "%s\n" "hxsa ALL=(ALL:ALL) NOPASSWD: ALL" > "$tmp"
chown root:root "$tmp"
chmod 0440 "$tmp"
visudo -cf "$tmp"
mv "$tmp" /etc/sudoers.d/90-hx-admin
visudo -c'

# Verify the NOPASSWD policy actually took effect.
# `set -e` aborts before any trailing "$?" echo, so test explicitly.
if sudo -n true; then
  echo "NOPASSWD sudo: PASS"
else
  echo "STOP: NOPASSWD sudo did not take effect" >&2
  exit 14
fi

# Owner decision D-018: the HX LAN is a trusted lab segment and hosts run with
# no local firewall. Do not add rules here without explicit owner approval.
sudo ufw disable || true
sudo systemctl disable --now ufw || true
sudo ufw status || true
systemctl is-enabled ufw || true
systemctl is-active ufw || true
sudo nft list ruleset || true
systemctl is-active firewalld || echo "firewalld unit not found or inactive"

# Access itself is proven by the foundation gate above and, externally, by
# tools/hx-doc/hx-fleet-access. These two lines are evidence, not a control:
# `is-active` was true on HX-2 and HX-3 the whole time the fleet could not
# log in to either.
systemctl is-active ssh
sudo sshd -T | grep '^port '

# D-028: hold the NVIDIA branch before any upgrade runs, so routine patching
# cannot move the driver. Held packages are named, not silently skipped.
HX_INSTALLED="$(dpkg-query -W -f='${Package}\n' 2>/dev/null || true)"
HX_NVIDIA_HOLD="$(hx_nvidia_hold_list "$HX_INSTALLED" "$HX_NVIDIA_BRANCH")"
if [ -n "$HX_NVIDIA_HOLD" ]; then
  echo "D-028: holding the NVIDIA $HX_NVIDIA_BRANCH branch:"
  printf '  %s\n' $HX_NVIDIA_HOLD
  # shellcheck disable=SC2086  # deliberate word splitting: one package per arg
  sudo apt-mark hold $HX_NVIDIA_HOLD
else
  echo "D-028: no NVIDIA $HX_NVIDIA_BRANCH packages installed; nothing to hold"
fi

sudo apt update
sudo apt upgrade -y
apt list --upgradable 2>/dev/null || true
systemctl --failed --no-pager
echo "Block 1 complete on $HX_HOST; rebooting"
sudo reboot
