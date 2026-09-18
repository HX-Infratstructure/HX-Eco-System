# HX-Eco-System Build State

**Date:** 2026-09-15  
**Owner:** Jarvis Richardson  
**Method:** KISS / one server at a time

Outstanding infrastructure findings are tracked in `docs/00-control/FINDINGS.md`.

<!-- HX-FLEET:TABLE columns=id,role,state,gate,note -->
| Server | Assignment | State | Gate | Notes |
|---|---|---|---|---|
| HX-1 | Samba AD / DNS / Kerberos / NTP | **PASS** | **CLOSED** | Clean base retained; foundation for the whole fleet |
| HX-2 | Qwen-X / Ollama | **PASS** | **CLOSED** | Qwen3.8-27B Q6_K; 2 x RTX 4070 Ti SUPER 16GB; model source URI UNRESOLVED |
| HX-3 | Coder-X / Ollama | **PASS** | **CLOSED** | GLM-4.7-Flash Q5_K_M (bartowski GGUF) primary + Qwen3-Coder-30B-A3B-Instruct Q6_K retained rollback; 2 x RTX 5060 Ti 16GB |
| HX-4 | Meta-X / GPT-OSS 20B + BGE-M3 + Nomic + BGE reranker | **PASS** | **CLOSED** | Meta-X gpt-oss:20b + BGE-M3 1024d + Nomic v1.5 768d + bge-reranker-v2-m3 on infinity-emb 7997; 2 x RTX 5060 Ti 16GB; reranker artifact hash UNRESOLVED |
| HX-5 | CentCom / Ornith / DeepSeek Harness / dev-test | **IN PROGRESS** | **CENTCOM RUNNER NEXT** | Layer 0/1 CLOSED; Ollama 0.34.0 PASS; ornith-1.5:35b BASE PASS incl. CLI/API/LAN/dual-GPU placement/reboot; CentCom smoke-runner activation remains |
| HX-6 | OmniRoute | **NOT STARTED** | — | Provider and model allowlists required (D-010) |
| HX-7 | NGINX dev/test only | **IN PROGRESS** | **C4 DEFERRED** | Not the ecosystem reverse proxy (D-004) |
| HX-8 | Open WebUI | **PASS** | **CLOSED** | Open WebUI 0.11.3 on Python 3.12.3; D-008 proved against HX-2, HX-3, HX-4 and HX-5; owner kept the four direct connections, D-008 removal clause open |
| HX-9 | PostgreSQL + MCP / Redis + MCP | **NOT STARTED** | — | Two applications on one host; each closes separately |
| HX-10 | Qdrant + Web UI + MCP | **NOT STARTED** | — | One embedding identity per collection (D-005) |
| HX-11 | LightRAG + MCP | **NOT STARTED** | — | Needs HX-10 and HX-4 proof first |
| HX-12 | Deep Agents (LangChain) LOB agent factory | **NOT STARTED** | — | Prose runbook; pin deepagents version at implementation time |
| HX-13 | Mem0 + assigned MCP | **NOT STARTED** | — | MCP implementation not yet selected |
| HX-14 | n8n + MCP | **NOT STARTED** | — | Install from GitHub release or npm tarball, not Snap |
| HX-15 | FastMCP shared/custom MCP development host | **NOT STARTED** | — | Not a prerequisite for product-specific MCP servers |
| HX-16 | Docling + Granite-Docling 258M + MCP | **NOT STARTED** | — | Granite-Docling stays here, CPU-first (D-006) |
| HX-17 | Crawl4AI + MCP | **NOT STARTED** | — | Native install; official MCP bridge is Docker-coupled, needs a native choice |
<!-- /HX-FLEET:TABLE -->


## Closed-server notes

### HX-2
- Domain membership / SSSD: PASS
- NVIDIA 595.91.07: PASS
- 2 x GeForce RTX 4070 Ti SUPER 16 GB: PASS
- Dedicated `/srv/ollama` storage: PASS
- Ollama 0.34.0: PASS
- Qwen3.8-27B Q6_K: PASS
- CLI/API/LAN/reboot persistence: PASS
- Current Ollama cloud state is temporary local-only configuration.

### HX-3
- Ubuntu 24.04.5 / kernel 7.0.0-31: PASS
- Domain membership / SSSD: PASS
- NVIDIA 595.91.07: PASS
- 2 x RTX 5060 Ti 16 GB: PASS
- Dedicated `/srv/ollama` storage: PASS
- Ollama 0.34.0: PASS
- `Coder-X-GLM-Flash` (primary): PASS
- `coder-x:qwen3-coder-30b-q6_k` (retained rollback, still installed): PASS
- CLI/API/LAN/reboot persistence: PASS
- Longer boot time is informational only; do not diagnose/remediate unless explicitly asked.

### HX-4
- Ubuntu 24.04.5 / kernel 7.0.0-31: PASS
- Domain membership / SSSD: PASS
- NVIDIA 595.91.07: PASS
- 2 x RTX 5060 Ti 16 GB: PASS
- Dedicated `/srv/ollama` storage: PASS
- Ollama 0.34.0: PASS
- `meta-x:gpt-oss-20b`: PASS
- `hx-embed-primary:bge-m3` at 1024d: PASS
- `hx-embed-alt:nomic-v1.5` at 768d: PASS
- `hx-reranker` on infinity-emb 0.0.77, port 7997: PASS
- Proof steps A1, A2, A3: PASS, retained under `docs/05-evidence/hx-4/`
- CLI/API/LAN/reboot persistence: PASS
- First server closed on run-bundle evidence rather than inline proof.
- A1-A3 ran before CentCom exists and HX-4 was its own runner station, so those
  LAN calls were not remote. Recorded in the server record, not smoothed over.
- Reranker artifact SHA-256 is UNRESOLVED; the checkpoint is pinned to an
  immutable revision but the runtime fetches it and no per-file hash was taken.
- Three `sssd` socket units are failed (HX4-F02). Identity resolution works.

## HX-5 current state

- Layer 0/1 reconciled foundation: PASS / CLOSED
- HX-1 DNS / Kerberos / NTP relationship: PASS
- Fleet-key SSH and NOPASSWD sudo: PASS
- NVIDIA 595.99.02 and mixed RTX 5060 + RTX 5060 Ti visibility: PASS
- Dedicated `/srv/ollama` UUID-backed storage: PASS across reboot
- Ollama 0.34.0 installed from SHA-256-verified upstream archive: PASS
- `OLLAMA_HOST=0.0.0.0:11434`: PASS; live listener `*:11434`
- `OLLAMA_MODELS=/srv/ollama/models`: PASS
- `ornith-1.5:35b`: INSTALLED / PASS
- Ornith model ID: `9f3b89b25219`
- Ornith model blob SHA-256: `aaeb640f98a892980ef54876024293cc8d6987a86523aa1b947ffa9274ef800a`
- Ornith projector blob SHA-256: `d9ce31026d1cb1f3f8d5152e2e2a014d9d2b302b6c93a7dc07bb0a0487f52837`
- CLI inference: PASS
- localhost HTTP API inference: PASS
- LAN HTTP API inference: PASS
- workload placement: PASS at observed `17% CPU / 83% GPU`, both GPUs active
- Ollama / model / storage / inference reboot persistence: PASS
- CentCom smoke-runner bootstrap and doctor gates: PENDING / NEXT
- DeepSeek Harness: future scheduled workload; not a prerequisite for CentCom smoke-runner activation

## Planned retrospective audit

After HX-5 current closeout, HX-2, HX-3, and HX-4 require a read-only retrospective Layer 0/1 audit against the reconciled HX-5 foundation standard. This does not invalidate their existing functional state; it closes the evidence-standard gap exposed during HX-5 reconciliation.

## Operating rule

A server becomes `PASS / CLOSED` only after its required base, domain, workload, functional, and reboot-persistence gates are satisfied and its as-built server record is updated.
