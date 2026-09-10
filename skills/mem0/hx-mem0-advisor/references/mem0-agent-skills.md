# Official Mem0 Agent Skills — HX Disposition

## Reviewed catalog

Official source:

```text
Repository: mem0ai/mem0
Path: skills/
Reviewed main: 02f7a9b2c4fe38dedb96631e48c85c74ad58b605
Catalog count: 6 skills
```

Mem0 defines two categories: three reference skills and three pipeline skills. Pipeline skills can create branches/files, install dependencies, run code, or migrate projects and therefore require stronger HX execution gating.

## Disposition table

| Upstream skill | Upstream purpose | HX disposition | HX rule |
|---|---|---|---|
| `mem0` | Python/TypeScript SDKs, Platform + OSS, framework integrations | `ADAPT` | Use OSS/self-hosted guidance for HX-13. Platform examples remain reference only unless owner-approved. |
| `mem0-cli` | Terminal workflows for Mem0 CLI | `REFERENCE_ONLY` | Current guidance is Platform/API-key oriented and may mint/use hosted credentials. Do not make it a BASE dependency without runbook approval. |
| `mem0-vercel-ai-sdk` | `@mem0/vercel-ai-provider` / Vercel AI SDK | `REFERENCE_ONLY` | Useful for application development; not HX-13 BASE runtime authority. |
| `mem0-integrate` | TDD pipeline that wires Mem0 into an existing repo | `REFERENCE_ONLY` | Creates feature branch and `.mem0-integration/` artifacts. Use only on an explicitly authorized target application repo; never as hidden HX infrastructure execution authority. |
| `mem0-test-integration` | Verifies output of `mem0-integrate` | `REFERENCE_ONLY` | Useful developer verification, but not the HX Mem0 smoke-test authority and may exercise live hosted credentials. |
| `mem0-oss-to-platform` | Migrates OSS `Memory` to hosted `MemoryClient` | `REJECT_FOR_HX_RUNTIME` | Directly conflicts with current native/self-hosted HX-13 architecture unless the owner explicitly changes that decision. |

## Important upstream behavior

### `mem0`

The official reference skill is Platform-first in its main flow but explicitly includes OSS/self-hosted `Memory`. For HX-13, load the OSS/client references and current official component docs; do not let Platform defaults rewrite placement.

### `mem0-cli`

The current skill describes `mem0 init --agent` and hosted API-key workflows. This is potentially useful for developer tooling but is not required for self-hosted HX-13 BASE.

### `mem0-integrate`

The pipeline's useful principles include additive integration, opt-in feature flags, no breakage, minimal dependencies, separable commits, and test-first work. Those principles can inform HX application integration later. Its repository-writing actions remain subordinate to the target repo's own governance.

### `mem0-test-integration`

The upstream skill explicitly says it catches compile/runtime bugs rather than logical integration errors. HX validation must still prove the current known-answer memory lifecycle and cleanup contract.

### `mem0-oss-to-platform`

This skill intentionally removes self-hosted vector/LLM/embedder configuration and replaces `Memory` with hosted `MemoryClient`. That is the opposite of the current HX-13 role and therefore cannot auto-trigger for HX runtime work.

## Coding-assistant plugin distinction

Mem0 also ships integration/plugin code for coding assistants. The reviewed portable `integrations/mem0-agent-plugin` declares:

```text
name: mem0
version: 0.3.1
purpose: cross-session memory and token savings for coding agents
MCP transport: stdio via Python mcp_server.py
```

This is a separate capability from the HX-13 application/runtime role. Do not equate installing a coding-agent plugin with building or validating HX-13.

## Update trigger

Re-review this reference when:

- `mem0ai/mem0` changes SDK major versions;
- the skill catalog count/behavior changes materially;
- the official plugin/MCP architecture changes;
- HX selects an exact Mem0 MCP implementation;
- HX changes from self-hosted OSS to another deployment model.
