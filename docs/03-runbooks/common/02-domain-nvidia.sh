#!/usr/bin/env bash
# HX common base block 2 - domain join, then the NVIDIA driver on the hosts
# that carry a GPU, then reboot.
# Usage: ./02-domain-nvidia.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-4)" >&2; exit 2; }
hx_require_host "$1"

sudo apt install -y realmd sssd-ad sssd-tools adcli krb5-user samba-common-bin
realm discover "$HX_DOMAIN"
if realm list | grep -q 'configured: kerberos-member'; then
  echo "Server is already joined to $HX_DOMAIN"
else
  # Interactive: this prompts for the domain administrator password.
  sudo realm join "$HX_DOMAIN" -U Administrator
fi
realm list
systemctl is-active sssd
id "$HX_DOMAIN_TEST_USER" || { echo "STOP: domain user resolution failed" >&2; exit 15; }

# Pin the driver so a newly built server matches the recorded fleet baseline.
# Clear HX_NVIDIA_PKG_VERSION in hx-base.env to accept the current archive
# version instead, and record the resolved version in the server record.
PCI_VENDORS="$(cat /sys/bus/pci/devices/*/vendor 2>/dev/null || true)"
GPU_PLAN="$(hx_require_gpu_expectation "$HX_HOST" "$HX_GPU_HOSTS" "$PCI_VENDORS")" || exit $?

if [ "$GPU_PLAN" = install ]; then
  NVIDIA_PKG="nvidia-driver-${HX_NVIDIA_BRANCH}-server-open"
  if [ -n "${HX_NVIDIA_PKG_VERSION:-}" ]; then
    echo "Installing pinned $NVIDIA_PKG=$HX_NVIDIA_PKG_VERSION"
    sudo apt install -y "linux-headers-$(uname -r)" "${NVIDIA_PKG}=${HX_NVIDIA_PKG_VERSION}"
  else
    echo "WARNING: no NVIDIA pin set; installing current archive version"
    sudo apt install -y "linux-headers-$(uname -r)" "$NVIDIA_PKG"
  fi
  dpkg -l "$NVIDIA_PKG" | tail -1
else
  echo "$HX_HOST carries no GPU, so Block 2 is domain join only here."
fi
echo "Block 2 complete on $HX_HOST; rebooting"
sudo reboot
