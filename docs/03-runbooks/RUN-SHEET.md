---
document: HX Build Day Run Sheet
status: current
date: 2026-09-10
authority: HX-Eco-System clean rebuild
---

# Build Day Run Sheet

One page for the whole day. Every command is exact. Every block refuses to run
on the wrong host, so a mistyped server name stops rather than damages.

Validation is two questions everywhere: **does it start, and does it survive a
reboot.** Nothing more.

---

## Before you touch a machine

From anywhere, including a laptop:

```bash
cd ~/src/HX-Eco-System
git pull
tools/hx-doc/hx-preflight
```

Once the smoke phase starts, also confirm the step may run at all:

```bash
tools/hx-doc/hx-proof --ready B2
```

Expect `all clear`. If anything FAILS, fix the pin in
`docs/03-runbooks/common/hx-base.env` before starting. A dead link found here
costs a minute; found mid-build it costs the morning.

---

## The shape of every server

Identical for all of them. Two reboots, then the application.

| Step | Block | Reboots | Roughly |
|---|---|---|---|
| 1 | `common/01-base-admin-network-updates.sh` | yes | 10-20 min |
| 2 | `common/02-domain-nvidia.sh` | yes | 10-15 min |
| 3 | `common/03-storage-ollama.sh` | no | 5 min |
| 4 | the application block | no | varies |
| 5 | validate: starts, then reboot, then starts | yes | 5 min |
| 6 | record it | no | 5 min |

Step 3 is inference hosts only. Skip it on HX-6 through HX-17.

Call each block with the host name, or run the wrapper from the server's own
runbook directory. Both do the same thing.

```bash
cd ~/src/HX-Eco-System/docs/03-runbooks
./common/01-base-admin-network-updates.sh hx-4

# or, equivalently:
cd ~/src/HX-Eco-System/docs/03-runbooks/HX-4
./01-base-admin-network-updates.sh
```

### Step 5 — validation

```bash
systemctl is-active <unit> && systemctl is-enabled <unit>
sudo reboot
# once it is back:
systemctl is-active <unit>
```

### Step 6 — record it

```bash
$EDITOR docs/02-server-records/HX-4.md      # fill every section
$EDITOR docs/00-control/hx-fleet.tsv        # state -> PASS, gate -> CLOSED
tools/hx-doc/hx-fleet                       # regenerate the tables
tools/hx-doc/hx-render-html
tools/hx-doc/hx-doc-check && tools/hx-doc/hx-record-check
git add -A && git commit && git push
```

The record needs the **source URI and the full SHA-256** of anything you
downloaded. An unknown value is written `UNRESOLVED`, never left blank.

---

## Build order

Dependency-driven. Do not reorder without a reason.

| # | Host | Application | Block |
|---:|---|---|---|
| 1 | HX-4 | Meta-X: GPT-OSS 20B, BGE-M3, Nomic, reranker | `common/04-reranker.sh hx-4` |
| 2 | HX-5 | CentCom / Ornith inference | base blocks only |
| 3 | HX-9 | PostgreSQL 18.6 | `common/10-postgresql.sh hx-9` |
| 4 | HX-9 | Redis 8.10.1 | `common/10-redis.sh hx-9` |
| 5 | HX-10 | Qdrant 1.19.1 | `common/10-qdrant.sh hx-10` |
| 6 | HX-6 | OmniRoute 3.8.50 | `common/10-omniroute.sh hx-6` |
| 7 | HX-15 | FastMCP 4.0.3 | `common/10-fastmcp.sh hx-15` |
| 8 | HX-5 | DeepSeek Harness | see the HX-5 runbook |
| 9 | HX-7 | NGINX 1.30.4 | `common/10-nginx.sh hx-7` |
| 10 | HX-16 | Docling 2.126.0 + Granite-Docling | `common/10-docling.sh hx-16` |
| 11 | HX-17 | Crawl4AI 0.9.3 | `common/10-crawl4ai.sh hx-17` |
| 12 | HX-11 | LightRAG 1.5.7 | `common/10-lightrag.sh hx-11` |
| 13 | HX-13 | Mem0 2.0.20 | `common/10-mem0.sh hx-13` |
| 14 | HX-12 | Deep Agents 0.7.13 | `common/10-deep-agents.sh hx-12` |
| 15 | HX-14 | n8n 2.38.6 | `common/10-n8n.sh hx-14` |
| 16 | HX-8 | Open WebUI 0.11.3 | `common/10-open-webui.sh hx-8` |

### Separate from the build order

The two closed inference servers move to the fleet Ollama pin. Run on each host:

```bash
./docs/03-runbooks/common/90-ollama-upgrade.sh hx-2
./docs/03-runbooks/common/90-ollama-upgrade.sh hx-3
```

Models are not re-downloaded. Update the Ollama version in each record after.

---

## Things that will stop you, and what to do

**HX-4 reranker.** First start downloads the model, so allow a few minutes
before the health check answers. The block already waits.

**HX-6 OmniRoute.** The product discovers hundreds of providers by default.
Before HX-6 closes, build the explicit provider allowlist and the explicit
model allowlist. Discovery is not approval — that is D-010, and it is the
reason this server exists.

**HX-9.** Two applications on one host. They close separately. PostgreSQL
builds from source, so allow time for `make`. Set the postgres role password
before anything connects over the LAN, and do not put it in the repository.

**HX-13 Mem0.** Mem0 is a library, not a daemon. It has no unit until you
decide whether it runs inside the assigned MCP server or behind a small local
service. That decision is not made yet.

**HX-16, HX-17, HX-12, HX-15.** These install libraries or CLIs, not services.
The base install proves the runtime. The thing that gets a unit is the
companion MCP server, which is a separate gate.

**HX-11 LightRAG.** Set the embedding and LLM bindings in the unit environment
before the smoke test: HX-4 for BGE-M3, and one approved HX Ollama endpoint.

---

## Two records to backfill

Both need a live host, so do them on the first day you have access:

**HX-2** — the Hugging Face repository the Qwen3.8-27B GGUF came from. The hash
is recorded; the origin is not. Recover it from shell history or the download
record.

**HX-3** — the full artifact SHA-256. Only the 12-character layer prefix was
recorded.

```bash
ollama show --modelfile coder-x:qwen3-coder-30b-q6_k
ls -l /srv/ollama/models/blobs/
```

Downstream smoke tests cite both servers as prior PASS evidence, so these close
before the smoke phase starts.

---

## At the end of the day

```bash
tools/hx-doc/hx-doc-check
tools/hx-doc/hx-record-check
tools/hx-doc/hx-fleet --check
git status
```

Anything a server needs that is not yet decided goes in that server's record as
`UNRESOLVED`, not in someone's memory.
