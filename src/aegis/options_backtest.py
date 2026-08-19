from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class HistoricalOptionQuote:
    timestamp: str
    symbol: str
    expiration: date
    strike: float
    option_type: str
    bid: float
    ask: float
    underlying_price: float

    @property
    def midpoint(self) -> float:
        if self.bid > 0 and self.ask >= self.bid:
            return (self.bid + self.ask) / 2
        return max(self.bid, self.ask)


@dataclass(frozen=True)
class OptionLeg:
    symbol: str
    side: str  # buy/sell
    quantity: int = 1


@dataclass(frozen=True)
class SpreadSnapshot:
    timestamp: str
    legs: tuple[OptionLeg, ...]
    net_debit: float
    max_loss: float
    max_profit: float | None


class OptionsBacktestEngine:
    """Deterministic mark-to-mid simulator for multi-leg option strategies."""

    def __init__(self, *, slippage_bps: float = 0.0, commission_per_contract: float = 0.0) -> None:
        if slippage_bps < 0 or commission_per_contract < 0:
            raise ValueError("cost parameters cannot be negative")
        self.slippage = slippage_bps / 10_000
        self.commission = commission_per_contract

    def price_spread(self, quotes: Iterable[HistoricalOptionQuote], legs: Iterable[OptionLeg]) -> float:
        by_symbol = {quote.symbol: quote for quote in quotes}
        value = 0.0
        contracts = 0
        for leg in legs:
            quote = by_symbol.get(leg.symbol)
            if quote is None:
                raise ValueError(f"missing historical quote: {leg.symbol}")
            # Buy at ask, sell at bid, with a deterministic adverse slippage adjustment.
            if leg.side == "buy":
                price = quote.ask * (1 + self.slippage)
                value += price * leg.quantity
            elif leg.side == "sell":
                price = quote.bid * (1 - self.slippage)
                value -= price * leg.quantity
            else:
                raise ValueError(f"invalid leg side: {leg.side}")
            contracts += abs(leg.quantity)
        return value * 100 + contracts * self.commission

    def mark_to_mid(self, quotes: Iterable[HistoricalOptionQuote], legs: Iterable[OptionLeg]) -> float:
        by_symbol = {quote.symbol: quote for quote in quotes}
        value = 0.0
        for leg in legs:
            quote = by_symbol.get(leg.symbol)
            if quote is None:
                raise ValueError(f"missing historical quote: {leg.symbol}")
            sign = 1 if leg.side == "buy" else -1
            value += sign * quote.midpoint * leg.quantity * 100
        return value
