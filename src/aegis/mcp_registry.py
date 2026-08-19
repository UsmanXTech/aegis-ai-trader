from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class McpTool:
    name: str
    description: str
    input_schema: dict[str, Any]


class McpToolRegistry:
    """Index MCP tools and resolve candidates without hard-coding vendor names."""

    def __init__(self, result: dict[str, Any]) -> None:
        self.tools = tuple(
            McpTool(
                name=str(tool["name"]),
                description=str(tool.get("description", "")),
                input_schema=dict(tool.get("inputSchema", {})),
            )
            for tool in result.get("tools", [])
            if "name" in tool
        )
        self._by_name = {tool.name: tool for tool in self.tools}

    def get(self, name: str) -> McpTool:
        try:
            return self._by_name[name]
        except KeyError as exc:
            raise KeyError(f"MCP tool not available: {name}") from exc

    def find(self, *keywords: str) -> list[McpTool]:
        terms = tuple(term.lower() for term in keywords)
        return [
            tool for tool in self.tools
            if all(term in f"{tool.name} {tool.description}".lower() for term in terms)
        ]
