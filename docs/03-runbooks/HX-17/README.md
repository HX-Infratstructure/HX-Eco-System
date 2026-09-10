# HX-17 Current Runbook

**Host:** hx-17
**Expected IP:** `192.168.50.217`
**Role:** Crawl4AI + MCP

## Execution

Steps 1-2 are the shared base blocks. Run them from this directory; each one
refuses to run on any host other than `hx-17`.

```bash
./01-base-admin-network-updates.sh # reboots
./02-domain-nvidia.sh              # reboots
```

Implementation lives in `../common/`; version pins and the host -> IP map live
in `../common/hx-base.env`. See `../README.md` before changing a pin.

## Sequence

1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install the pinned NVIDIA
   driver; reboot.
3. Install the Crawl4AI + MCP application software.
   Application software comes from PyPI, a GitHub release, or a direct binary.
   Not Snap. Not the Ubuntu archive.
4. Validation: the service starts, and it survives a reboot.
5. Fill in `docs/02-server-records/HX-17.md`, then set `state` and
   `gate` for `HX-17` in `docs/00-control/hx-fleet.tsv` and run
   `tools/hx-doc/hx-fleet`.

Do not mount/wipe unrelated disks. Do not import prior application state.
