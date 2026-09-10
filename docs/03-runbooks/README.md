# Runbooks

Current approved execution runbooks only. Archive superseded runbooks; do not
keep multiple active variants.

## Layout

```text
docs/03-runbooks/
├── common/                  one implementation of the shared base blocks
│   ├── hx-base.env          version pins, LAN facts, host -> IP map, host guard
│   ├── 01-base-admin-network-updates.sh
│   ├── 02-domain-nvidia.sh
│   └── 03-storage-ollama.sh
├── HX-4/                    thin wrappers that call common/ with the host name
└── HX-5/                    thin wrappers plus the HX-5-only CentCom bootstrap
```

Run a block from its server directory, or call the common block directly:

```bash
./docs/03-runbooks/HX-4/01-base-admin-network-updates.sh
./docs/03-runbooks/common/01-base-admin-network-updates.sh hx-4
```

Every common block calls `hx_require_host` first and refuses to run on any
server other than the one named. That is the guard against running HX-4's block
on HX-5.

## The three common base blocks

1. Identity, network and DNS validation, admin sudo policy, apt update/upgrade,
   then reboot.
2. Domain join, SSSD, domain user resolution, pinned NVIDIA driver, then reboot.
3. Domain/GPU/storage re-validation, pinned Ollama, systemd override, listener
   and API proof.

## Application install blocks

Each application has one block in `common/`, named `10-<app>.sh`, taking the
host name. They are written once and called from the server's runbook
directory, the same way the base blocks are.

| Host | Block | Source |
|---|---|---|
| HX-6 | `10-omniroute.sh` | npm, on Node from the official binary tarball |
| HX-7 | `10-nginx.sh` | nginx.org stable source, built natively |
| HX-8 | `10-open-webui.sh` | PyPI |
| HX-9 | `10-postgresql.sh` | PGDG vendor repository — see the note in the block |
| HX-9 | `10-redis.sh` | GitHub release source, built natively |
| HX-10 | `10-qdrant.sh` | prebuilt Linux binary from the GitHub release |
| HX-11 | `10-lightrag.sh` | PyPI |
| HX-12 | `10-deep-agents.sh` | PyPI |
| HX-13 | `10-mem0.sh` | PyPI |
| HX-14 | `10-n8n.sh` | npm, on Node from the official binary tarball |
| HX-15 | `10-fastmcp.sh` | PyPI |
| HX-16 | `10-docling.sh` | PyPI plus Hugging Face for Granite-Docling |
| HX-17 | `10-crawl4ai.sh` | PyPI |

Shared helpers live in `common/hx-app-lib.sh`: a service user, a venv, a
systemd unit, a start check, and a Node installer that verifies the official
checksum.

Some applications are libraries or CLIs rather than daemons — Docling,
Crawl4AI, Deep Agents, FastMCP and Mem0. Those blocks install and prove the
runtime; the thing that gets a unit is the companion MCP server or a small
local service, and each block says so.

Validation is deliberately minimal everywhere: the service starts, and it
survives a reboot.

## Version pins

`common/hx-base.env` holds `HX_OLLAMA_VERSION` and `HX_NVIDIA_PKG_VERSION`.
They default to the versions HX-2 and HX-3 closed on, so a newly built server
matches the recorded fleet baseline instead of silently taking whatever shipped
that morning.

Block 3 verifies the installed Ollama version against the pin and stops on a
mismatch. To move the fleet forward: change the pin here, build, then record the
resolved version in that server's record. Clearing a pin accepts the current
upstream release, and the resolved version must then be recorded in the server
record before that server can close.

## Runbook shape

A server gets a **scripted** runbook when its build is the common base pattern
plus deterministic steps. It gets a **prose** runbook when the sequence needs
judgement at implementation time, such as pinning a package version that does
not exist yet. HX-12 is prose for that reason. A prose runbook states its
version references as "planning reference as of <date>" and requires the exact
version to be pinned in the server record at implementation time.

## Rules

The scripts must not alter hostname/IP/DNS/gateway/partitions/mounts unless the
owner explicitly approves that change. Old unmounted disks are not touched.
Server-specific model and application installation is added only when finalised
and executed.
