from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .mcp_client import AlpacaMcpClient, McpCallResult
from .order_builder import MultiLegOrder


@dataclass(frozen=True)
class PaperExecutionResult:
    response: McpCallResult
    order: MultiLegOrder


class AlpacaMcpTrading:
    """Named tool adapter; actual MCP tool names remain configurable."""

    def __init__(self, client: AlpacaMcpClient, *, submit_tool: str = "place_order") -> None:
        self.client = client
        self.submit_tool = submit_tool

    def submit_multileg(self, order: MultiLegOrder) -> PaperExecutionResult:
        if not order.paper_only:
            raise PermissionError("Aegis MCP adapter only permits paper orders")
        payload: dict[str, Any] = {
            "order_type": order.order_type,
            "limit_price": order.limit_price,
            "time_in_force": order.time_in_force,
            "legs": [
                {"symbol": leg.symbol, "side": leg.side, "quantity": leg.quantity}
                for leg in order.legs
            ],
        }
        response = self.client.call(self.submit_tool, payload)
        return PaperExecutionResult(response, order)
