# Crawl4AI MCP review

Review date: 2026-09-09

## HX requirement

HX-17 is assigned Crawl4AI + Crawl4AI MCP. The product-specific MCP companion is part of the parent application's BASE build and must independently pass `smoke-tests/mcp-companion-smoke-test.md` after Crawl4AI core D3 PASS.

`docs/04-application-standards/MCP-STANDARD.md` controls the HX boundary:

- product-specific MCP ships with its parent application during base build;
- independent MCP smoke proof is required;
- agent/Harness/Open WebUI/workflow client registration is later integration work;
- HX-15 FastMCP is not a prerequisite.

## Current official upstream MCP source

Official Crawl4AI current source contains:

- `deploy/docker/mcp_bridge.py`;
- `deploy/docker/server.py`, which attaches the MCP bridge;
- self-hosted server docs exposing MCP transports/tools through that server.

Current v0.9.3 release notes also state the `mcp` dependency is capped below 2 because `mcp_bridge` depends on the v1 low-level API.

This is authoritative evidence for current upstream MCP behavior and version sensitivity.

## HX conflict

The official implementation is structurally part of the Docker/self-hosted server tree. HX currently prohibits containerized workloads unless the owner changes the rule.

Therefore:

- official MCP behavior/source -> `ACCEPT + ADAPT` as vendor expertise;
- Docker server deployment -> `REJECT_FOR_HX`;
- copying the Docker server files into a native service -> not automatically approved; `OWNER_DECISION_REQUIRED`;
- exact native MCP package/dependency/mode/transport/listener/systemd unit -> `OWNER_DECISION_REQUIRED`;
- server auth/TLS/CORS/Redis/egress/reverse-proxy defaults -> `OWNER_DECISION_REQUIRED` if proposed for HX;
- downstream MCP client registration -> `REFERENCE_ONLY` for BASE.

Do not claim HX lacks an assigned MCP requirement. The requirement is established; the **implementation is not yet selected**.

## D4 acceptance

D4 requires accepted D3 Crawl4AI PASS and must use the generic MCP companion authority to prove at minimum:

- MCP protocol negotiation/connectivity in the selected transport;
- tool discovery;
- one safe known-answer tool call tied to the parent Crawl4AI capability;
- expected structured response;
- cleanup/evidence;
- reboot/service persistence where applicable before HX-17 closes BASE.

The future HX-17 runbook must state exactly how the selected companion is installed and invoked before D4 is executable.
