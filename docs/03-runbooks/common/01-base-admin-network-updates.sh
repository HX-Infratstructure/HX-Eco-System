#!/usr/bin/env bash
# HX common base block 1 - identity, network, admin sudo, updates, reboot.
# Usage: ./01-base-admin-network-updates.sh <hx-host>      e.g. hx-4
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-4)" >&2; exit 2; }
hx_require_host "$1"

hostnamectl
ip -br addr
ip route
ip -4 -br addr | grep -q "$HX_IP/24" || { echo "STOP: expected IP $HX_IP/24 not found"; exit 11; }
ip route | grep -q "^default via $HX_GATEWAY " || { echo "STOP: expected gateway $HX_GATEWAY not found"; exit 12; }
resolvectl status
resolvectl status | grep -q "$HX_DC_IP" || { echo "STOP: expected HX-1 DNS $HX_DC_IP not found"; exit 13; }

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

systemctl is-active ssh
sudo sshd -T | grep '^port '
sudo apt update
sudo apt upgrade -y
apt list --upgradable 2>/dev/null || true
systemctl --failed --no-pager
echo "Block 1 complete on $HX_HOST; rebooting"
sudo reboot
