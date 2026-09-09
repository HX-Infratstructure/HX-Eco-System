# Runbooks

Current approved execution runbooks only. Archive superseded runbooks; do not keep multiple active variants.

HX-4 and HX-5 use the current three-block common base pattern:
1. base/admin/network validation + apt update/upgrade, then reboot;
2. domain join + NVIDIA 595 Server Open, then reboot;
3. domain/GPU/storage validation + Ollama base, then server-specific model/application work.

The scripts must not alter hostname/IP/DNS/gateway/partitions/mounts unless the owner explicitly approves that change. Old unmounted disks are not touched.
