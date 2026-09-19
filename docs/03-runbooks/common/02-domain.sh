#!/usr/bin/env bash
# HX common base block 2 - domain join, then the NVIDIA driver on the hosts
# that carry a GPU, then reboot.
# Usage: ./02-domain.sh <hx-host>
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./hx-base.env
. "$SCRIPT_DIR/hx-base.env"

[ $# -eq 1 ] || { echo "Usage: ${0##*/} <hx-host>   (e.g. hx-4)" >&2; exit 2; }
hx_require_host "$1"

sudo apt install -y realmd sssd-ad sssd-tools adcli krb5-user samba-common-bin
realm discover "$HX_DOMAIN"
# Captured rather than piped. `realm list | grep -q` is the HX4-F01 pattern:
# under pipefail a writer killed at the match turns "already joined" into an
# interactive re-join. HX4-F05 deferred this until the block was next touched.
HX_CHANGED=0
REALMS="$(realm list)"
if grep -q 'configured: kerberos-member' <<<"$REALMS"; then
  echo "Server is already joined to $HX_DOMAIN"
else
  # Interactive: this prompts for the domain administrator password.
  sudo realm join "$HX_DOMAIN" -U Administrator
  HX_CHANGED=1
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
  NVIDIA_BEFORE="$(dpkg-query -W -f='${Version}' "$NVIDIA_PKG" 2>/dev/null || true)"
  if [ -n "${HX_NVIDIA_PKG_VERSION:-}" ]; then
    echo "Installing pinned $NVIDIA_PKG=$HX_NVIDIA_PKG_VERSION"
    sudo apt install -y "linux-headers-$(uname -r)" "${NVIDIA_PKG}=${HX_NVIDIA_PKG_VERSION}"
  else
    echo "WARNING: no NVIDIA pin set; installing current archive version"
    sudo apt install -y "linux-headers-$(uname -r)" "$NVIDIA_PKG"
  fi
  dpkg -l "$NVIDIA_PKG" | tail -1
  # A driver that changed, or one installed but not loaded (the first run was
  # interrupted before its reboot), still needs the reboot.
  NVIDIA_AFTER="$(dpkg-query -W -f='${Version}' "$NVIDIA_PKG" 2>/dev/null || true)"
  if [ "$NVIDIA_AFTER" != "$NVIDIA_BEFORE" ] || [ ! -d /sys/module/nvidia ]; then
    HX_CHANGED=1
  fi
else
  echo "$HX_HOST carries no GPU, so Block 2 is domain join only here."
fi

# Nothing ran after this block's reboot, so nothing proved the join, SSSD and
# the driver survived it. The re-run is that proof: on a host where nothing
# changed, the checks above are the post-reboot evidence, and a second reboot
# would only start the cycle again.
if [ "$HX_CHANGED" -eq 0 ]; then
  echo "Block 2 already in place on $HX_HOST: joined to $HX_DOMAIN, sssd active, $HX_DOMAIN_TEST_USER resolves. Nothing changed, so no reboot."
  exit 0
fi
echo "Block 2 complete on $HX_HOST; rebooting"
sudo reboot
