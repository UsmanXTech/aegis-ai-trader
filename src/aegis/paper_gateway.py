from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderStatus
from alpaca.trading.requests import GetOrdersRequest

from .alpaca_adapter import AccountSnapshot


@dataclass(frozen=True)
class SubmittedOrder:
    order_id: str
    status: str


class AlpacaPaperGateway:
    """Thin, paper-only wrapper around the official Alpaca TradingClient."""

    def __init__(self, api_key: str, secret_key: str) -> None:
        if not api_key or not secret_key:
            raise ValueError("Alpaca paper credentials are required")
        self._client = TradingClient(api_key, secret_key, paper=True)

    def get_account(self) -> AccountSnapshot:
        account = self._client.get_account()
        positions = self._client.get_all_positions()
        daily_pnl = float(account.equity) - float(account.last_equity)
        return AccountSnapshot(
            equity=float(account.equity),
            cash=float(account.cash),
            daily_pnl=daily_pnl,
            open_positions=len(positions),
        )

    def submit_order(self, order_request: Any) -> SubmittedOrder:
        """Submit an already risk-approved request to the paper account."""
        order = self._client.submit_order(order_data=order_request)
        return SubmittedOrder(order_id=str(order.id), status=str(order.status))

    def get_order(self, order_id: str) -> Any:
        return self._client.get_order_by_id(order_id)

    def open_orders(self) -> list[Any]:
        request = GetOrdersRequest(status=OrderStatus.OPEN, nested=True)
        return list(self._client.get_orders(filter=request))
