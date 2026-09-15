# HX-5 Layer 0/1 Post-Reboot Validation — 2026-09-15

## Result

Layer 0/1 persistence is substantially proven after reboot. One blocking closure item remains: four Netplan packages are still reported upgradeable.

## PASS evidence

- Hostname: `hx-5`
- FQDN: `hx-5.hx.local.arpa`
- IPv4: `192.168.50.205/24`
- Default gateway: `192.168.50.1`
- DNS: `192.168.50.200`
- Chrony: active and enabled
- Chrony selected source: `192.168.50.200` (HX-1), reference ID `C0A832C8`
- UFW: inactive and disabled
- SSH: active on port 22
- `ssh.socket`: active and enabled; this is the reboot-persistence mechanism while `ssh.service` itself is disabled
- NOPASSWD sudo: PASS
- AD machine trust: `adcli testjoin -D hx.local.arpa` PASS
- SSSD service: active
- Domain identity resolution: PASS
- NVIDIA driver/module: `595.99.02`
- GPUs after reboot: RTX 5060 8151 MiB and RTX 5060 Ti 16311 MiB
- `/srv/ollama`: mounted, ext4, ~797G total / ~757G available

## NTP detail

`chronyc tracking` showed reference `192.168.50.200`, stratum 4, normal leap status, and sub-millisecond offset. `chronyc sources -v` marked HX-1 as the selected source (`^*`). External Chrony sources remain configured as non-selected fallbacks; HX-1 is the active authoritative source.

## SSH persistence detail

Post-reboot evidence:

```text
ssh.service: active / disabled
ssh.socket:  active / enabled
port 22
```

This confirms Ubuntu socket activation is providing persistent SSH availability. The service being disabled is not a failure in this configuration.

## Storage enumeration note

Before reboot the Ollama filesystem appeared as `/dev/nvme1n1p3`; after reboot it appeared as `/dev/nvme0n1p3`. The filesystem remained mounted correctly at `/srv/ollama`. Device-name renumbering across boots is expected and is exactly why the authoritative mount uses filesystem UUID rather than `/dev/nvme*n*p*` names.

## Deferred finding

Two failed SSSD responder sockets remain after reboot:

```text
sssd-nss.socket
sssd-pam-priv.socket
```

Core SSSD/domain functions pass. This remains part of the existing HX4-F02 deferred/non-blocking fleet finding. The third previously observed socket (`sssd-pam.socket`) is no longer failed after this reboot.

## Remaining closure item

The following packages remain upgradeable:

```text
libnetplan1
netplan-generator
netplan.io
python3-netplan
```

Layer 0/1 should not be marked fully closed until the package state is reconciled and a final post-update validation confirms network/DNS/NTP/domain/SSH persistence remains intact.
