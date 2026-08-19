from dataclasses import dataclass

from .domain import OptionStrategy


@dataclass(frozen=True)
class OptionLeg:
    symbol: str
    side: str
    position_intent: str
    ratio_qty: int = 1


@dataclass(frozen=True)
class MultiLegOrder:
    strategy: OptionStrategy
    legs: tuple[OptionLeg, ...]
    qty: int = 1
    limit_price: float | None = None


class PaperExecutionService:
    """Builds Alpaca-compatible MLeg orders without enabling live trading."""

    def build_order(self, order: MultiLegOrder) -> dict:
        if order.qty < 1:
            raise ValueError("order quantity must be positive")
        if len(order.legs) < 2:
            raise ValueError("multi-leg strategy requires at least two legs")
        if len(order.legs) > 4:
            raise ValueError("Alpaca MLeg orders support at most four legs")

        payload = {
            "order_class": "mleg",
            "qty": str(order.qty),
            "type": "limit" if order.limit_price is not None else "market",
            "time_in_force": "day",
            "legs": [
                {
                    "symbol": leg.symbol,
                    "side": leg.side,
                    "ratio_qty": str(leg.ratio_qty),
                    "position_intent": leg.position_intent,
                }
                for leg in order.legs
            ],
        }
        if order.limit_price is not None:
            payload["limit_price"] = str(order.limit_price)
        return payload
