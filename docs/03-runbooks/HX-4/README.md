# HX-4 Current Runbook

**Host:** hx-4  
**Expected IP:** `192.168.50.204`  
**Role:** Meta-X / GPT-OSS 20B + shared embedding/reranking plane

## Execution

Steps 1-3 are the shared base blocks. Run them from this directory; each one
refuses to run on any host other than `hx-4`.

```bash
./01-base-admin-network-updates.sh    # reboots
./02-domain-nvidia.sh                 # reboots
./03-storage-ollama.sh
./05-gpt-oss.sh                       # Meta-X generation model
./06-embeddings.sh                    # BGE-M3 primary + Nomic v1.5 alternate
./../common/04-reranker.sh hx-4       # last: needs the models in place
```

Execution order is 01, 02, 03, 05, 06, then 04. The reranker's number is
historical — it was written before the model blocks existed. Blocks 05 and 06
add models to the Ollama block 3 installs; only the cross-encoder reranker
needs a second runtime, because Ollama does not serve cross-encoders.

Implementation lives in `../common/`; version pins and the host -> IP map live
in `../common/hx-base.env`. Ollama and the NVIDIA driver are pinned to the
fleet baseline, and block 3 stops if the installed Ollama does not match the
pin. See `../README.md` before changing a pin.

## Sequence
1. Base/admin/network validation; apt update + upgrade; reboot.
2. Join `hx.local.arpa`; validate SSSD/domain user; install the pinned `nvidia-driver-595-server-open`; reboot.
3. Validate GPU/storage; require inspected `/srv/ollama`; install/configure Ollama; reboot/health validation.
4. Install the Meta-X generation model: `./05-gpt-oss.sh`. Pinned by
   `HX_GPT_OSS_MODEL`; the block refuses to run while that pin is empty.
5. Install the shared embedding plane: `./06-embeddings.sh`. BGE-M3 primary at
   1024 dimensions, Nomic Embed Text v1.5 alternate at 768 (D-005). Each model
   is proved by its embedding dimension, not by service health.
6. Install the pinned BGE reranker: `../common/04-reranker.sh hx-4`.
   Model `BAAI/bge-reranker-v2-m3` @ `953dc6f6`, served by `infinity-emb`
   0.0.77 from PyPI under systemd on port 7997. Not Snap, not the Ubuntu archive.
7. API/model smoke tests, resource observation, reboot persistence.
8. Update HX-4 server record and BUILD-STATE before closure.

Do not mount/wipe unrelated disks. Do not import prior application state.

## Model pins

`HX_GPT_OSS_MODEL`, `HX_EMBED_PRIMARY_MODEL` and `HX_EMBED_ALT_MODEL` are set in
`../common/hx-base.env`. Blocks 05 and 06 exit 30 rather than install an
unpinned model, on the same rule block 3 applies to Ollama itself: "whatever
was current that day" is not a baseline a server record can state.

Two gaps to close before build day:

- `HX_EMBED_PRIMARY_MODEL` is `bge-m3:latest`, and `latest` is a floating tag,
  not a pin. Replace it with the fixed tag once the digest recorded at install
  is known.
- `tools/hx-doc/hx-preflight` cannot resolve an Ollama model tag. It checks
  downloads, PyPI, npm, Hugging Face and apt. These three pins are proved by
  the blocks themselves — 05 by a known-answer prompt, 06 by embedding
  dimension — not by preflight.
