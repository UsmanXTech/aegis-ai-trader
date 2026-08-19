from __future__ import annotations

from dataclasses import dataclass

from .greeks import Greeks, GreeksRisk, scale_greeks


@dataclass(frozen=True)
class OptionQuote:
    symbol: str
    bid: float
    ask: float
    last: float
    greeks: Greeks
    open_interest: int = 0

    @property
    def midpoint(self) -> float:
        if self.bid > 0 and self.ask >= self.bid:
            return (self.bid + self.ask) / 2
        return self.last

    @property
    def spread_pct(self) -> float:
        midpoint = self.midpoint
        return ((self.ask - self.bid) / midpoint * 100) if midpoint > 0 else 100.0


def quote_risk(quote: OptionQuote, quantity: float = 1) -> GreeksRisk:
    return scale_greeks(quote.greeks, quantity)
