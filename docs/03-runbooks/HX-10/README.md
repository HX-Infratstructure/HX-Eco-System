# HX-10 Current Runbook

> **Note added 2026-09-30.** HX-10 Qdrant was installed on 2026-09-26 from
> [HX-Exploration's Qdrant plan](https://github.com/HX-Infratstructure/HX-Exploration/tree/main/03-implementation-plans/HX-10/Qdrant).
> The current record is
> [HX-Exploration's HX-10 server record](https://github.com/HX-Infratstructure/HX-Exploration/blob/main/02-server-records/HX-10.md).

**Host:** hx-10
**Expected IP:** `192.168.50.210`
**Role:** Qdrant + Web UI + MCP

## Foundation — proof step `F0-HX-10`

Layer 0/1 is established once, by the shared foundation block. Run it before
step 1; `01-base-admin-network-updates.sh` refuses to continue without it and
names what is missing.

```bash
../common/00-foundation.sh hx-10
```

This host's gate is `F0-HX-10` in
[`hx-proof.tsv`](../../00-control/hx-proof.tsv). Row `F0` is the fleet-wide
standard and is already `PASS`, so it gates nothing. Record `F0-HX-10` from the
fifteen controls in section 9 of
[`HX-BASE-BLOCKS-1-2-CONFIGURATION-AUDIT.md`](../../00-control/HX-BASE-BLOCKS-1-2-CONFIGURATION-AUDIT.md),
never from `hx-proof --ready`, which reads the recorded verdict and re-runs none
of them.

## Execution

Steps 1-2 are the shared base blocks. Run them from this directory; each one
refuses to run on any host other than `hx-10`.

```bash
./01-base-admin-network-updates.sh # reboots
./02-domain.sh              # reboots
../common/10-qdrant.sh hx-10
```

Implementation lives in `../common/`; version pins and the host -> IP map live
in `../common/hx-base.env`. See `../README.md` before changing a pin.

## Sequence

1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; reboot. The block installs
   the pinned NVIDIA driver only on hosts listed in `HX_GPU_HOSTS`, which this
   host is not, so nothing is installed here. The reboot happens either way.
3. Install Qdrant:
   `../common/10-qdrant.sh hx-10`
   Versions are pinned in `../common/hx-base.env`. Application software
   comes from PyPI, a GitHub release, a direct binary, or Hugging Face.
   Not Snap. Not the Ubuntu archive.
4. Validation: the service starts, and it survives a reboot.
5. Fill in `docs/02-server-records/HX-10.md`, then set `state` and
   `gate` for `HX-10` in `docs/00-control/hx-fleet.tsv` and run
   `tools/hx-doc/hx-fleet`.

Do not mount/wipe unrelated disks. Do not import prior application state.
