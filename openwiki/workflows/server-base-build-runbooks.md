---
type: workflow
title: Server base-build runbooks
description: The executable path that stands a server up — one implementation of each numbered block with thin per-server wrappers, a host guard that refuses the wrong machine, pinned and checksum-verified downloads, shared helpers for users, venvs and units, and a validation contract of exactly two questions.
tags: [runbooks, build, shell, systemd, host-guard, checksums, installation]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-44d77985ad29194abad2384a
    resource: repo://.coderabbit.yaml
  - id: openwiki-source-12296e6451a9d695ef6c70ca
    resource: repo://docs/03-runbooks/common/01-base-admin-network-updates.sh
  - id: openwiki-source-55cb761e338a12f96fbe21bc
    resource: repo://docs/03-runbooks/common/02-domain-nvidia.sh
  - id: openwiki-source-5897c3741a9751cc69ea4fa4
    resource: repo://docs/03-runbooks/common/03-storage-ollama.sh
  - id: openwiki-source-d887b0ccaa992fce33fa5814
    resource: repo://docs/03-runbooks/common/10-postgresql.sh
  - id: openwiki-source-45924c2e46a6dbd9a7d521f8
    resource: repo://docs/03-runbooks/common/hx-app-lib.sh
  - id: openwiki-source-667355bbf619c0e53d4f76d4
    resource: repo://docs/03-runbooks/common/hx-base.env
  - id: openwiki-source-9b2252f54c6c4dcf2a153991
    resource: repo://docs/03-runbooks/HX-9/01-base-admin-network-updates.sh
  - id: openwiki-source-d2e11c3bbc0251d9415096b4
    resource: repo://docs/03-runbooks/README.md
  - id: openwiki-source-3bc721c8c10557b77c613ac1
    resource: repo://docs/03-runbooks/RUN-SHEET.md
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Server base-build runbooks

`docs/03-runbooks/` is the only place in the repository where code runs as root
on a real machine. It is organised so that the same build happens the same way
on every host, and so that running the wrong block on the wrong server stops
instead of doing damage.

## Layout: one implementation, thin wrappers

```text
docs/03-runbooks/
├── common/                  one implementation of every block
│   ├── hx-base.env          pins, LAN facts, host guard, verified fetch
│   ├── hx-app-lib.sh        shared application helpers
│   ├── 01-base-admin-network-updates.sh
│   ├── 02-domain-nvidia.sh
│   ├── 03-storage-ollama.sh
│   └── 10-<app>.sh          one per application
├── HX-4/ … HX-17/           five-line wrappers
└── RUN-SHEET.md             the whole build day on one page
```

A per-server wrapper is five lines: strict shell settings and an `exec` of the
common block with its own host name. Both invocations are equivalent:

```bash
./docs/03-runbooks/HX-9/01-base-admin-network-updates.sh
./docs/03-runbooks/common/01-base-admin-network-updates.sh hx-9
```

The wrappers, runbook README and server record for a new host are scaffolded by
`tools/hx-doc/hx-new-server` rather than copied by hand.

## The host guard

Every block sources `hx-base.env` and calls `hx_require_host` before doing
anything else. It compares the short hostname against the expected one and exits
if they differ, then resolves the server's expected address through the
generated fleet lookup — failing if the host has no recorded address. That is
the guard against running one server's block on another, and the review
configuration requires it to come first in any runbook script.

The base block then verifies the machine matches the recorded baseline before
changing anything: the expected address on the interface, the expected default
gateway, and the fleet's DNS server in the resolver configuration. A mismatch
stops the build with a distinct exit code.

## The three base blocks

**Block 1 — identity, sudo, updates.** Verifies network identity, installs the
admin sudo policy through a temporary file validated with `visudo` before it is
moved into place, then confirms passwordless sudo actually took effect with an
explicit test — under strict shell settings a trailing status echo would never
run. It disables the host firewall, which is the decided posture rather than an
oversight, checks SSH, applies updates and reboots.

**Block 2 — domain and driver.** Installs the domain client packages, joins the
realm if not already joined, and requires domain user resolution to succeed. It
then installs the pinned NVIDIA driver, or warns explicitly when no pin is set
before taking the current archive version. Reboots.

**Block 3 — storage and Ollama, inference hosts only.** Re-verifies domain, GPU
and failed units, requires the dedicated storage to be mounted, and refuses to
continue if that mount already holds content. It refuses outright to run
unpinned: an unpinned install put whatever shipped that day on the machine,
which is not a baseline a server record can state. After installing it writes a
systemd drop-in for the model path, the listener and cloud behaviour, then
compares the *installed* version against the pin and stops on a mismatch —
proving the pin rather than assuming it.

Block 3 is skipped on non-inference hosts.

## Application blocks

Each application has one block, `common/10-<app>.sh`, taking a host name.
Sources are constrained by the package-source rule — PyPI, npm, a GitHub
release, an upstream source tarball, a direct binary, or Hugging Face — and the
Ubuntu archive appears only for build toolchains and library headers, always
with a comment saying so.

Not everything becomes a service. Docling, Crawl4AI, Deep Agents, FastMCP and
Mem0 are libraries or CLIs; those blocks install and prove the runtime, and the
thing that gets a unit is the companion MCP server or a small local service.

The PostgreSQL block is a good illustration of the house style. It installs only
the toolchain from apt, downloads the official source tarball, verifies it
against the pinned hash and stops on a mismatch, builds and installs under a
dedicated prefix, creates the service user, runs `initdb` only when no cluster
exists, writes and enables a unit, validates, and prints a closing summary. Two
of its guards are worth copying: after editing the listener setting with `sed`
it *greps for the resulting value*, because `sed` reports success when it
matched nothing; and its access-rule check matches an **active** rule rather than
the text anywhere in the file, because a commented-out line contains the address
range too and would have satisfied a looser test while leaving no rule in force.

## Shared helpers

`hx-base.env` and `hx-app-lib.sh` hold the pieces every block reuses.

`hx_fetch_verified` downloads to a destination and refuses the artifact unless
it matches a recorded SHA-256. It refuses outright when no hash is recorded, and
on a mismatch it deletes the downloaded file so a later step cannot pick up
something that failed its check. It exists because only one block verified a
checksum while everything else took whatever the server sent on the day, and a
release asset can be replaced in place.

`hx_ollama_install` reimplements what the vendor installer does, from a verified
archive. The vendor script cannot be given a local file: it streams the release
archive straight into `sudo tar -x` with no checksum, so verifying the installer
itself proves nothing about the gigabytes it then unpacks as root. The
replacement also renames the previous installation aside instead of deleting it
first, and restores it if extraction fails — a checksum rules out a bad archive
but not a disk-space or I/O failure part way through, and the vendor's
delete-first window leaves an inference server with no Ollama and nothing to go
back to. It writes byte-for-byte the same unit the vendor writes, so
server-specific settings stay in the drop-in.

`hx_app_lib.sh` provides the rest: a system user with its home, a virtual
environment with one pinned package installed into it, a systemd unit written
from a template and enabled, and a start check that waits for a port then
confirms the unit is active and enabled.

`hx_app_done` prints the closing summary, and its signature carries a fix worth
knowing. It used to take a unit name unconditionally, so five blocks that create
no unit told the operator to run a status check on a unit that does not exist —
a command that could only fail. Passing `NONE` now makes the fourth argument the
reboot check to run instead, and it is required. The documentation checker
enforces the other half of that rule: a block may only name a unit it actually
creates.

## The validation contract

Validation here is deliberately minimal, and the helper library says so in its
own header: **does the service start, and does it survive a reboot.** Nothing
else is checked, and more is added only when explicitly asked. The review
configuration repeats the instruction to reviewers, who are told not to ask for
more.

The run sheet's step 5 is exactly that: check active and enabled, reboot, check
active again, using whatever unit or command the block printed.

Deeper proof is not absent — it is a different subsystem. Known-answer testing,
cleanup verification and retained evidence belong to
[the smoke-test run lifecycle](smoke-test-run-lifecycle.md).

## Build day

```bash
tools/hx-doc/hx-preflight        # from anywhere, before touching a machine
```

Every server then follows the same six steps: block 1 with a reboot, block 2
with a reboot, block 3 on inference hosts, the application block, validate
across a reboot, and record it. A dead pin found by preflight costs a minute;
found mid-build it costs the morning.

Recording it is not optional and not last-minute: the closing summary printed by
each block tells the operator to record the installed version in the server
record and set the state and gate in the fleet TSV, then regenerate. See
[server records and evidence retention](../operations/server-records-and-evidence-retention.md).

## What a runbook may not do

The scripts must not alter hostname, address, DNS, gateway, partitions or mounts
without explicit owner approval, and old unmounted disks are not touched at all.
Server-specific model and application steps are added only when finalised and
executed — a runbook is not a place to stage an intention.
