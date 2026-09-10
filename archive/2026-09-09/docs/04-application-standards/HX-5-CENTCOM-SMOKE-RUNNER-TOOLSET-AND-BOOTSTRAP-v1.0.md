---
document: HX-5 CentCom Smoke-Runner Toolset and Bootstrap Standard
status: current
version: 1.0
date: 2026-09-09
scope: HX-5 smoke-runner client tooling and bootstrap
authority: HX-Eco-System clean rebuild
---

# HX-5 CentCom — Smoke-Runner Toolset and Bootstrap Standard

## 1. Purpose

This standard defines the permanent **client-side test toolset on HX-5 CentCom** and the bootstrap used to activate it as the HX Eco-System remote smoke-test runner.

It implements, but does not replace, `HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`.

```text
component smoke-test authority = /smoke-tests/<component>-smoke-test.md
execution/process authority     = HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md
runner implementation          = tools/hx-smoke-runner/
bootstrap execution artifact   = docs/03-runbooks/HX-5/04-centcom-smoke-runner-bootstrap.sh
```

The runner remains **AI-centric**: instructions, deterministic commands, known boundaries, evidence rules, and executable helpers live in the repository so a coding/infrastructure agent can recover the intended workflow without reconstructing it from chat history.

## 2. Permanent HX-5 toolset

### Ubuntu packages

Install only client/development utilities required by the smoke-test catalog:

| Package | Purpose |
|---|---|
| `postgresql-client` | `psql` client for HX-9 PostgreSQL |
| `redis-tools` | `redis-cli` client for HX-9 Redis |
| `curl` | HTTP/API probes and deterministic REST smoke calls |
| `jq` | JSON response extraction/validation |
| `git` | authoritative repository checkout, commit identity, evidence staging |
| `openssh-client` | exception-path remote command execution where local SUT execution is intrinsic |
| `python3` | standard-library smoke scripts and runner helpers |
| `python3-venv` | isolated permanent CentCom runner environment |
| `python3-pip` | controlled Python dependency installation inside the runner venv |
| `ca-certificates` | normal HTTPS package/API trust support |

Do **not** install PostgreSQL server, Redis server, Qdrant, LightRAG, n8n, Docling, Crawl4AI, or other SUT workloads on HX-5 merely to test them.

### Python runner environment

Default:

```text
HX_SMOKE_VENV=$HOME/.venvs/hx-smoke-runner
```

Pinned accepted dependencies are stored in:

```text
tools/hx-smoke-runner/requirements.txt
```

Accepted pins on 2026-09-09:

```text
fastmcp==4.0.3
playwright==1.62.0
```

FastMCP provides the current MCP client used for product-specific MCP discovery and safe tool calls. Playwright Python provides deterministic headless Chromium UI evidence.

### Version policy

- Ubuntu client packages follow the supported Ubuntu 24.04 package stream; record the installed versions during activation.
- Python runner packages are pinned for reproducibility.
- Before intentionally upgrading a pinned Python runner dependency, verify current upstream stable, review breaking changes, update `requirements.txt`, run `hx-smoke-doctor`, and commit the new accepted pin.
- Do not silently float Python dependencies to `latest` during a component test.

## 3. HX-5 paths

Defaults:

```bash
export HX_ECO_REPO="${HX_ECO_REPO:-$HOME/src/HX-Eco-System}"
export HX_SMOKE_ROOT="${HX_SMOKE_ROOT:-$HOME/hx-smoke-runs}"
export HX_SMOKE_VENV="${HX_SMOKE_VENV:-$HOME/.venvs/hx-smoke-runner}"
```

`HX_ECO_REPO` must be an already-authenticated checkout of `HX-Infratstructure/HX-Eco-System`. The bootstrap does **not** embed a PAT or create a new secret-management path.

`HX_SMOKE_ROOT` contains disposable test runs. It is not repository authority.

## 4. Repository-provided runner commands

After bootstrap, HX-5 exposes these commands through `$HOME/.local/bin`:

| Command | Function |
|---|---|
| `hx-smoke-doctor` | validate the CentCom client toolchain and headless Chromium |
| `hx-smoke-doctor --remote` | additionally prove a known-good remote inference call to already-PASS HX-2 |
| `hx-smoke-new` | create a timestamped disposable run workspace and manifest from a committed smoke-test authority |
| `hx-smoke-ui-capture` | capture direct-LAN UI evidence only after expected live text is visible |
| `hx-smoke-promote` | validate normalized status/cleanup, screen obvious secrets, and promote selected evidence into `docs/05-evidence/` |

The helper scripts do not change the SUT configuration by themselves.

## 5. Bootstrap procedure

Execute only after HX-5 base/domain/GPU, Ollama/Ornith, and reboot-persistence gates are accepted.

From the authenticated repository checkout:

```bash
cd "$HX_ECO_REPO"
bash docs/03-runbooks/HX-5/04-centcom-smoke-runner-bootstrap.sh
```

The bootstrap:

1. verifies it is running on `hx-5`;
2. requires an existing authenticated repository checkout;
3. installs the Ubuntu client packages listed above;
4. creates the dedicated Python venv;
5. installs the pinned FastMCP and Playwright dependencies;
6. installs Playwright's Chromium runtime and required OS libraries;
7. links the repository-owned helper commands into `$HOME/.local/bin`;
8. creates/protects `HX_SMOKE_ROOT`;
9. does **not** modify firewall, DNS, routing, NFS, application-server packages, or SUT configuration.

Then run:

```bash
export PATH="$HOME/.local/bin:$PATH"
hx-smoke-doctor
hx-smoke-doctor --remote
```

The second command uses the already-proven HX-2 Ollama endpoint by default and requires the exact known answer:

```text
HX-CENTCOM-RUNNER-PASS
```

Defaults may be overridden with non-secret environment variables:

```bash
export HX_SMOKE_PROBE_OLLAMA_URL="http://192.168.50.202:11434"
export HX_SMOKE_PROBE_MODEL="qwen-x:qwen3.8-27b-q6_k"
```

Passing the doctor does not mark HX-5 DeepSeek Harness PASS. It activates only the CentCom smoke-runner capability.

## 6. Disposable run creation and manifest

Example:

```bash
RUN_DIR="$(hx-smoke-new hx-9 postgresql postgresql-smoke-test.md 192.168.50.209)"
cd "$RUN_DIR"
```

`hx-smoke-new` refuses to start from an untracked or locally modified smoke-test authority. It records:

- run ID and UTC start;
- operator and runner host;
- SUT host/IP;
- component;
- smoke-test file;
- repository commit SHA;
- smoke-test SHA-256;
- placeholders for component version, endpoint, and final status.

This prevents an agent from quietly changing PASS criteria in the same run that uses them.

## 7. Browser/UI evidence method

The standard automated browser is **Playwright-managed headless Chromium on HX-5**.

Use it only when the component smoke-test authority requires browser/UI proof:

```bash
hx-smoke-ui-capture \
  "http://<sut-ip>:<port>/" \
  "<expected live backend text>" \
  "$RUN_DIR/evidence/supporting/ui-live-state.png"
```

A screenshot is accepted only after the expected visible text is present. A page title, HTTP 200, or generic login page alone is not sufficient when the component requires proof of live backend state.

The helper also writes a `.meta.txt` sidecar containing UTC time, runner, final URL, page title, expected visible text, and `UI_CAPTURE=PASS`.

Rules:

- use the application's direct LAN UI; do not insert HX-7 NGINX unless NGINX itself is the SUT;
- do not persist a browser profile, cookies, or authentication state as repository evidence;
- do not put credentials in command lines retained as evidence;
- product-specific authenticated navigation remains defined by the applicable smoke test or an explicit implementation-time procedure;
- if a UI cannot be safely automated generically, capture the visual proof from the operator workstation and place only the resulting non-secret evidence in the HX-5 run bundle.

## 8. Evidence promotion

Before promotion, normalize two files in the run workspace:

```text
evidence/result.txt
  FUNCTIONAL=PASS|FAIL|NOT_EXECUTABLE
  STATUS=IN_PROGRESS
  SUMMARY=<short explanation>

cleanup/cleanup.txt
  CLEANUP=PASS|NOT_APPLICABLE|FAIL
  DETAIL=<short explanation>
```

Then:

```bash
hx-smoke-promote "$RUN_DIR" PASS
```

For `PASS`, promotion requires:

```text
FUNCTIONAL=PASS
AND
CLEANUP=PASS or NOT_APPLICABLE
```

The promotion helper:

1. verifies the run came from `HX_SMOKE_ROOT`;
2. reads SUT/component/run identity from the manifest;
3. refuses PASS when functional or cleanup gates are incomplete;
4. screens the promotion set for obvious credential patterns;
5. stamps final status and UTC end time;
6. copies only the normalized retained bundle and selected supporting evidence to:

```text
docs/05-evidence/<sut>/<component>/<run-id>/
```

7. **does not auto-commit**.

An agent or operator reviews the promoted evidence and commits it explicitly. This keeps repository changes visible and prevents an execution helper from becoming an unreviewed Git authority.

## 9. AI-agent operating context

Scoped instructions live at:

```text
tools/hx-smoke-runner/AGENTS.md
```

Any AI agent preparing or executing a smoke test must read, in order:

1. root `AGENTS.md`;
2. `docs/00-control/CURRENT-STATE.md`;
3. `docs/00-control/BUILD-STATE.md`;
4. relevant server record and runbook;
5. `HX-5-SMOKE-TEST-PROCESS-AND-PROCEDURES.md`;
6. the component's current `/smoke-tests/*.md` authority;
7. `tools/hx-smoke-runner/AGENTS.md`.

If the smoke-test authority appears defective, stale, or inconsistent with live evidence, stop the run. Correct the authority in a separate reviewed change, commit it, then start a **new run ID**. Never modify acceptance criteria inside an in-progress run workspace.

## 10. What this standard deliberately does not do

It does not:

- install or configure SUT workloads;
- create permanent cross-service integrations;
- create firewall, TLS, DNS, NFS, or routing policy;
- store PATs/passwords/API keys in the repository;
- install a container runtime;
- auto-commit evidence;
- make DeepSeek Harness a prerequisite for infrastructure smoke testing;
- replace the individual component smoke-test authorities.

## 11. Activation evidence

When actually installed on HX-5, capture at minimum:

```text
psql --version
redis-cli --version
curl --version
jq --version
git --version
ssh -V
python3 --version
FastMCP installed version
Playwright installed version
Chromium launch PASS
hx-smoke-doctor --remote PASS
```

Only after live execution may the HX-5 server record and `BUILD-STATE.md` state that the CentCom smoke-runner capability is active.
