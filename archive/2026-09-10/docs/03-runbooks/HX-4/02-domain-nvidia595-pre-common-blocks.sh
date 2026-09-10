#!/usr/bin/env bash
set -euo pipefail
DOMAIN="hx.local.arpa"
sudo apt install -y realmd sssd-ad sssd-tools adcli krb5-user samba-common-bin
realm discover "$DOMAIN"
if realm list | grep -q 'configured: kerberos-member'; then
  echo "Server is already joined to $DOMAIN"
else
  sudo realm join "$DOMAIN" -U Administrator
fi
realm list
systemctl is-active sssd
id 'jarvisr@hx.local.arpa'
sudo apt install -y linux-headers-$(uname -r) nvidia-driver-595-server-open
echo "Block 2 complete; rebooting"
sudo reboot
