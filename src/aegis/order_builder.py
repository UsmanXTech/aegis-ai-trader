from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class OrderLeg:
    symbol: str
    side: Literal["buy", "sell"]
    quantity: int = 1


@dataclass(frozen=True)
class MultiLegOrder:
    legs: tuple[OrderLeg, ...]
    order_type: Literal["market", "limit"]
    limit_price: float | None
    time_in_force: str
    paper_only: bool = True


class MultiLegOrderBuilder:
    def build_debit_spread(
        self,
        long_symbol: str,
        short_symbol: str,
        *,
        debit_limit: float,
        quantity: int = 1,
    ) -> MultiLegOrder:
        if not long_symbol or not short_symbol or long_symbol == short_symbol:
            raise ValueError("spread requires two distinct option symbols")
        if debit_limit <= 0 or quantity < 1:
            raise ValueError("debit and quantity must be positive")
        return MultiLegOrder(
            legs=(OrderLeg(long_symbol, "buy", quantity), OrderLeg(short_symbol, "sell", quantity)),
            order_type="limit",
            limit_price=debit_limit,
            time_in_force="day",
            paper_only=True,
        )
