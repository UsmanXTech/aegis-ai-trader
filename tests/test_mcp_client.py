from __future__ import annotations

import sys
from pathlib import Path

from aegis.mcp_client import AlpacaMcpClient


def _server_script(tmp_path: Path) -> Path:
    script = tmp_path / "fake_mcp.py"
    script.write_text(
        """
import json
import sys

for line in sys.stdin:
    request = json.loads(line)
    method = request.get("method")
    if method == "initialize":
        result = {
            "protocolVersion": "2025-06-18",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "fake", "version": "0.0.1"},
        }
        print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
    elif method == "notifications/initialized":
        continue
    elif method == "tools/list":
        result = {"tools": [{"name": "account", "description": "Get account"}]}
        print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
""",
        encoding="utf-8",
    )
    return script


def test_initialize_and_list_tools(tmp_path: Path) -> None:
    script = _server_script(tmp_path)
    client = AlpacaMcpClient(command=(sys.executable, str(script)))
    try:
        initialized = client.initialize()
        assert initialized["protocolVersion"] == "2025-06-18"
        tools = client.list_tools()
        assert tools["tools"][0]["name"] == "account"
    finally:
        client.stop()
