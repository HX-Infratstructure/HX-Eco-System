# HX-5 Current Runbook

**Host:** hx-5  
**Expected IP:** `192.168.50.205`  
**Role:** CentCom / Ornith / DeepSeek Harness / dev-test

## Sequence
1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install `nvidia-driver-595-server-open`; reboot.
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama; reboot/health validation.
4. Resolve/accept current GPU symmetry decision before workload placement assumptions.
5. Install Ornith model.
6. Install DeepSeek Harness only at its scheduled priority after the model fleet/OmniRoute foundation is available.
7. Update HX-5 server record and BUILD-STATE before closure.

Do not mount/wipe unrelated disks. Keep HX-5 headroom for CentCom/Harness/dev-test rather than moving shared embedding infrastructure here.
