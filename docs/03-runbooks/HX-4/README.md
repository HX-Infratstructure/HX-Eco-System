# HX-4 Current Runbook

**Host:** hx-4  
**Expected IP:** `192.168.50.204`  
**Role:** Meta-X / GPT-OSS 20B + shared embedding/reranking plane

## Sequence
1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install `nvidia-driver-595-server-open`; reboot.
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama; reboot/health validation.
4. Install GPT-OSS 20B.
5. Install shared embedding runtime and BGE-M3 + Nomic v1.5.
6. Install selected BGE-family reranker.
7. API/model smoke tests, resource observation, reboot persistence.
8. Update HX-4 server record and BUILD-STATE before closure.

Do not mount/wipe unrelated disks. Do not import prior application state.
