from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class McpCallResult:
    raw: dict[str, Any]


class AlpacaMcpClient:
    """JSON-RPC stdio adapter with MCP initialization and tool discovery."""

    def __init__(self, command: Sequence[str] = ("uvx", "alpaca-mcp-server", "serve")) -> None:
        self.command = tuple(command)
        self._process: subprocess.Popen[str] | None = None
        self._request_id = 0
        self._initialized = False

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
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=5)
            self._process = None
        self._initialized = False

    def _send(self, method: str, params: dict[str, Any] | None = None) -> McpCallResult:
        self.start()
        if self._process is None or self._process.stdin is None or self._process.stdout is None:
            raise RuntimeError("MCP process is unavailable")

        self._request_id += 1
        request_id = self._request_id
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {},
        }
        self._process.stdin.write(json.dumps(request) + "\n")
        self._process.stdin.flush()

        while True:
            line = self._process.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed stdout")
            response = json.loads(line)
            if response.get("id") != request_id:
                continue
            if "error" in response:
                raise RuntimeError(str(response["error"]))
            return McpCallResult(response)

    def _notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        self.start()
        if self._process is None or self._process.stdin is None:
            raise RuntimeError("MCP process is unavailable")
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }
        self._process.stdin.write(json.dumps(notification) + "\n")
        self._process.stdin.flush()

    def call(self, method: str, params: dict[str, Any] | None = None) -> McpCallResult:
        """Call an MCP method after initialization."""
        if method != "initialize" and not self._initialized:
            self.initialize()
        return self._send(method, params)

    def initialize(self) -> dict[str, Any]:
        """Perform the MCP initialization handshake and return server capabilities."""
        result = self._send(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "aegis-ai-trader", "version": "0.1.0"},
            },
        ).raw["result"]
        self._notify("notifications/initialized")
        self._initialized = True
        return result

    def list_tools(self) -> dict[str, Any]:
        """Return the tools exposed by the configured MCP server."""
        return self.call("tools/list").raw["result"]
