from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class McpCallResult:
    raw: dict[str, Any]


class AlpacaMcpClient:
    """Small JSON-RPC stdio adapter for an Alpaca MCP server process.

    The server command is injected so deployments can use uvx, a local binary,
    or another approved launcher. Credentials are intentionally not stored here.
    """

    def __init__(self, command: Sequence[str] = ("uvx", "alpaca-mcp-server", "serve")) -> None:
        self.command = tuple(command)
        self._process: subprocess.Popen[str] | None = None
        self._request_id = 0

    def start(self) -> None:
        if self._process is not None:
            return
        self._process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def stop(self) -> None:
        if self._process is not None:
            self._process.terminate()
            self._process = None

    def call(self, method: str, params: dict[str, Any] | None = None) -> McpCallResult:
        self.start()
        if self._process is None or self._process.stdin is None or self._process.stdout is None:
            raise RuntimeError("MCP process is unavailable")
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params or {},
        }
        self._process.stdin.write(json.dumps(request) + "\n")
        self._process.stdin.flush()
        line = self._process.stdout.readline()
        if not line:
            raise RuntimeError("MCP server closed stdout")
        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(str(response["error"]))
        return McpCallResult(response)
