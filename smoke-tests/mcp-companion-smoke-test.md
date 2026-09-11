# Product MCP Companion Smoke Test

## 1. Title & Purpose

Product-specific MCP servers are companion capabilities installed with their parent HX applications. This reusable smoke test validates that an MCP server can be reached by a real client, advertise its tools, execute one safe tool, and return a known expected value.

**Scope:** MCP protocol/tool proof only. The parent application's core function is validated by its own component smoke test.

## 2. Prerequisites

- The parent application has already passed its core smoke test far enough to provide a safe MCP target.
- The product-specific MCP server is installed and running in its accepted native configuration.
- The test runner has a current MCP client. The reference procedure uses FastMCP Client because it handles protocol negotiation automatically.
- Before execution, define one **benign/read-only or smoke-namespaced** tool and its known expected output.
- Set:

```bash
export MCP_SOURCE="http://<mcp-host>:<port>/mcp"
export MCP_TOOL="<safe-tool-name>"
export MCP_ARGS_JSON='{}'
export MCP_EXPECT="<known-expected-text>"
```

- Do not put secrets inside `MCP_ARGS_JSON` if the console output will be retained as evidence.
- No container is required.

## 3. Test Steps

1. Save as `mcp_companion_smoke.py`:

```python
import asyncio
import json
import os
from pathlib import Path
from fastmcp import Client

SOURCE_TEXT = os.environ["MCP_SOURCE"]
TOOL = os.environ["MCP_TOOL"]
ARGS = json.loads(os.environ.get("MCP_ARGS_JSON", "{}"))
EXPECT = os.environ["MCP_EXPECT"]
SOURCE = SOURCE_TEXT if "://" in SOURCE_TEXT else Path(SOURCE_TEXT)

async def main():
    async with Client(SOURCE, mode="auto") as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools}
        assert TOOL in names, f"tool {TOOL!r} not advertised: {sorted(names)}"

        result = await client.call_tool(TOOL, ARGS)
        blob = json.dumps(result.data, default=str)
        if EXPECT not in blob:
            blob += " " + " ".join(
                getattr(item, "text", "") for item in result.content
            )
        assert EXPECT in blob, f"expected value not returned: {blob}"

        print(
            f"MCP_COMPANION_SMOKE_PASS protocol={client.protocol_version} tool={TOOL}"
        )

asyncio.run(main())
```

2. Run:

```bash
python3 mcp_companion_smoke.py
```

3. Record parent application, MCP implementation/version, source/endpoint, negotiated protocol version, safe tool, non-secret arguments, expected value, timestamp, and output.

4. If the chosen tool creates a smoke-namespaced object, remove that object using the parent application's normal cleanup method.

## 4. Sample Data

The exact tool varies by product. Define a known-answer contract before the test, for example:

```text
MCP_TOOL=<read-only-or-smoke-tool>
MCP_ARGS_JSON=<non-secret synthetic arguments>
MCP_EXPECT=HX-MCP-SMOKE-9271
```

The test must exercise a real tool call. Tool discovery alone is not sufficient.

## 5. Expected Output

```text
MCP_COMPANION_SMOKE_PASS protocol=<negotiated-version> tool=<safe-tool-name>
```

Pass means the client negotiates successfully, the required tool is advertised, the tool executes, and the known expected result is returned.

The reference client uses automatic protocol negotiation so the test does not hard-code a legacy `initialize` handshake.

## 6. Cleanup / Teardown

- Delete only smoke-namespaced data created by the selected tool, if any.
- Remove disposable client scripts/workspace after evidence capture.
- Do not unregister or delete the accepted product MCP service.
- Do not create permanent agent/client registrations during this smoke test.

**MCP registration with DeepSeek Harness, Deep Agents, Open WebUI, n8n, or other consumers remains integration-phase work.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the discovery listing and the tool result.

Record the parent service and its version, the negotiated protocol version,
the tool exercised, the expected result returned, and confirmation that only
smoke-namespaced data was deleted and no permanent registration was created.
