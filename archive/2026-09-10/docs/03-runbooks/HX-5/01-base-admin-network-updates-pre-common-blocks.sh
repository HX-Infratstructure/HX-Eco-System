#!/usr/bin/env bash
set -euo pipefail
EXPECTED_HOST="hx-5"
EXPECTED_IP="192.168.50.205"
DC_IP="192.168.50.200"
GATEWAY="192.168.50.1"
printf '\n===== HX BASE BUILD: %s =====\n' "$EXPECTED_HOST"
hostnamectl
[ "$(hostname -s)" = "$EXPECTED_HOST" ] || { echo "STOP: expected hostname $EXPECTED_HOST"; exit 10; }
ip -br addr
ip route
ip -4 -br addr | grep -q "$EXPECTED_IP/24" || { echo "STOP: expected IP $EXPECTED_IP/24 not found"; exit 11; }
ip route | grep -q "^default via $GATEWAY " || { echo "STOP: expected gateway $GATEWAY not found"; exit 12; }
resolvectl status
resolvectl status | grep -q "$DC_IP" || { echo "STOP: expected HX-1 DNS $DC_IP not found"; exit 13; }
sudo sh -c 'set -e
tmp=/etc/sudoers.d/90-hx-admin.tmp
umask 022
printf "%s\n" "hxsa ALL=(ALL:ALL) NOPASSWD: ALL" > "$tmp"
chown root:root "$tmp"
chmod 0440 "$tmp"
visudo -cf "$tmp"
mv "$tmp" /etc/sudoers.d/90-hx-admin
visudo -c'
sudo -n true
echo "NOPASSWD sudo test exit code: $?"
sudo ufw disable
sudo systemctl disable --now ufw
sudo ufw status
systemctl is-enabled ufw || true
systemctl is-active ufw || true
sudo nft list ruleset
systemctl is-active firewalld || echo "firewalld unit not found or inactive"
systemctl is-active ssh
sudo sshd -T | grep '^port '
sudo apt update
sudo apt upgrade -y
apt list --upgradable 2>/dev/null || true
systemctl --failed --no-pager
echo "Block 1 complete; rebooting $EXPECTED_HOST"
sudo reboot
