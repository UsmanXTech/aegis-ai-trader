from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class AlpacaMCPClient(Protocol):
    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...


@dataclass(frozen=True)
class MCPExecutionPolicy:
    paper_only: bool = True
    require_risk_approval: bool = True


class AlpacaMCPGateway:
    """Small adapter keeping Aegis independent of a particular MCP client."""

    def __init__(self, client: AlpacaMCPClient, policy: MCPExecutionPolicy | None = None) -> None:
        self.client = client
        self.policy = policy or MCPExecutionPolicy()

    def account(self) -> Any:
        return self.client.call_tool("get_account", {})

    def positions(self) -> Any:
        return self.client.call_tool("get_all_positions", {})

    def orders(self, limit: int = 50) -> Any:
        if limit < 1:
            raise ValueError("limit must be positive")
        return self.client.call_tool("get_orders", {"limit": limit})

    def submit_approved_order(self, order: dict[str, Any], *, risk_approved: bool) -> Any:
        if self.policy.require_risk_approval and not risk_approved:
            raise PermissionError("risk approval required before order submission")
        if self.policy.paper_only and order.get("paper") is not True:
            raise PermissionError("paper-only policy requires paper=true")
        return self.client.call_tool("place_order", order)
