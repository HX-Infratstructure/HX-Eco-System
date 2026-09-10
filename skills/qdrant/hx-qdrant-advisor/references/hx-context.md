# HX Qdrant Context

## Assigned host

- Server: `HX-10`
- IP: `192.168.50.210`
- Assignment: Qdrant + native Web UI + Qdrant MCP
- Current state as of 2026-09-09: `NOT STARTED`

Target placement is architecture. It is not as-built fact until live evidence and server records prove it.

## HX foundation inherited by HX-10

- LAN: `192.168.50.0/24`
- Gateway: `192.168.50.1`
- Infrastructure DNS: HX-1 at `192.168.50.200`
- AD domain: `hx.local.arpa`
- Kerberos realm: `HX.LOCAL.ARPA`
- Domain client pattern: SSSD / realmd / adcli
- Deployment: native Ubuntu Linux + systemd
- Containers: not used unless explicitly approved by the infrastructure owner
- Normal application UI access: direct native host/port
- HX-7 NGINX: dev/test rendering only, not normal ecosystem routing

Do not let generic Qdrant deployment-option guidance replace these owner-approved HX decisions.

## Qdrant role in HX

Qdrant is the vector-state foundation for later retrieval/memory workloads. BASE validation proves Qdrant itself before those downstream integrations are introduced.

Current proof sequence:

1. Qdrant core deterministic vector lifecycle.
2. Native Web UI live-state companion proof.
3. Qdrant MCP companion proof.
4. Cleanup + cleanup verification.
5. Reboot persistence + retained evidence.

Later consumers include LightRAG and Mem0, which may use Qdrant only after Qdrant has current accepted PASS evidence.

## Retrieval-model placement

HX-4 owns the shared retrieval inference plane:

- BGE-M3 — primary/default embedding model, 1024 dimensions.
- Nomic Embed Text v1.5 — alternate/benchmark embedding model at its accepted dimension.
- BGE-family reranker — exact checkpoint/runtime must be pinned before its smoke test becomes executable.

HX collection-integrity rule:

- never mix embeddings from different model identities in the same Qdrant collection;
- model changes require a new collection and complete re-embedding.

This policy remains authoritative even though Qdrant supports more flexible vector-schema patterns.

## Base-vs-integration boundary

During Qdrant BASE build:

- prove native Qdrant service/storage/API/UI/MCP behavior;
- use synthetic/disposable smoke data;
- do not ingest production corpus;
- do not require LightRAG or Mem0;
- do not establish permanent application bindings;
- do not create a separate test Qdrant instance;
- do not make network/security changes merely to satisfy a generic vendor deployment pattern.

Permanent schemas/collections, RAG ingestion, agent bindings, production model wiring, and end-to-end application integration belong to the later integration program unless explicitly promoted by owner decision.
