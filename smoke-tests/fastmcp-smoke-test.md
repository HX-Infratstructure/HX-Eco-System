# FastMCP Smoke Test

## 1. Title & Purpose

FastMCP on HX-15 is the shared/custom MCP development and runtime capability. This smoke test validates that FastMCP can expose a small custom tool over MCP, allow a client to discover that tool, execute it, and return a deterministic structured result.

**Scope:** FastMCP custom-server capability only. Product-specific MCP servers remain part of their parent applications.

## 2. Prerequisites

- FastMCP is installed natively in the accepted HX-15 Python environment.
- Python is available in the same environment.
- The temporary HTTP test port is available and reachable from the test runner.
- Set the accepted URL if different from the example:

```bash
export FASTMCP_URL="http://192.168.50.215:18015/mcp"
```

- No production backend, external model, database, or container is required.

## 3. Test Steps

1. Save as `fastmcp_smoke_server.py` in the disposable workspace:

```python
from fastmcp import FastMCP

mcp = FastMCP("HX FastMCP Smoke")

@mcp.tool
def echo_smoke(token: str) -> dict:
    return {"status": "PASS", "token": token}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=18015)
```

2. Start the temporary server using the accepted Python environment.

3. Save as `fastmcp_smoke_client.py`:

```python
import asyncio
import os
from fastmcp import Client

TOKEN = "HX-FASTMCP-SMOKE-9271"
URL = os.environ.get("FASTMCP_URL", "http://192.168.50.215:18015/mcp")

async def main():
    async with Client(URL, mode="auto") as client:
        tools = await client.list_tools()
        assert "echo_smoke" in {tool.name for tool in tools}, tools

        result = await client.call_tool("echo_smoke", {"token": TOKEN})
        assert result.data["status"] == "PASS", result.data
        assert result.data["token"] == TOKEN, result.data

        print(
            f"FASTMCP_SMOKE_PASS protocol={client.protocol_version} token={TOKEN}"
        )

asyncio.run(main())
```

4. Run:

```bash
python3 fastmcp_smoke_client.py
```

5. Record FastMCP version, negotiated MCP protocol version, endpoint, tool name, execution timestamp, and console output.

## 4. Sample Data

```text
Tool:  echo_smoke
Input: HX-FASTMCP-SMOKE-9271
Expected structured result:
{"status":"PASS","token":"HX-FASTMCP-SMOKE-9271"}
```

## 5. Expected Output

A passing run prints a line similar to:

```text
FASTMCP_SMOKE_PASS protocol=<negotiated-version> token=HX-FASTMCP-SMOKE-9271
```

Pass means the client connects, protocol negotiation succeeds, `echo_smoke` appears in tool discovery, the tool executes, and the exact structured known-answer result is returned.

## 6. Cleanup / Teardown

1. Stop the temporary FastMCP smoke server.
2. Confirm the temporary test port is no longer listening.
3. Remove `fastmcp_smoke_server.py`, `fastmcp_smoke_client.py`, and the disposable workspace after evidence capture.
4. Retain the accepted FastMCP installation and normal HX-15 service configuration.

**Do not register this temporary tool as a permanent HX MCP service. No containers are created by this test.**
