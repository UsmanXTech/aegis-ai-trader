from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderClass, OrderSide, OrderStatus, PositionIntent, TimeInForce
from alpaca.trading.requests import GetOrdersRequest, LimitOrderRequest, OptionLegRequest

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

    @staticmethod
    def to_sdk_request(payload: dict[str, Any]) -> LimitOrderRequest:
        """Convert Aegis's JSON-compatible MLeg payload into an alpaca-py request."""
        if payload.get("order_class") != "mleg":
            raise ValueError("paper gateway currently accepts only MLeg option orders")
        if payload.get("type") != "limit":
            raise ValueError("MLeg paper execution currently requires a limit order")

        legs = [
            OptionLegRequest(
                symbol=str(leg["symbol"]),
                ratio_qty=float(leg["ratio_qty"]),
                side=OrderSide(str(leg["side"]).lower()),
                position_intent=PositionIntent(str(leg["position_intent"]).lower()),
            )
            for leg in payload.get("legs", [])
        ]
        return LimitOrderRequest(
            qty=float(payload["qty"]),
            limit_price=float(payload["limit_price"]),
            order_class=OrderClass.MLEG,
            time_in_force=TimeInForce.DAY,
            legs=legs,
        )

    def submit_order(self, order_request: Any) -> SubmittedOrder:
        """Submit an already risk-approved request to the paper account."""
        request = self.to_sdk_request(order_request) if isinstance(order_request, dict) else order_request
        order = self._client.submit_order(order_data=request)
        return SubmittedOrder(order_id=str(order.id), status=str(order.status))

    def get_order(self, order_id: str) -> Any:
        return self._client.get_order_by_id(order_id)

    def open_orders(self) -> list[Any]:
        request = GetOrdersRequest(status=OrderStatus.OPEN, nested=True)
        return list(self._client.get_orders(filter=request))
