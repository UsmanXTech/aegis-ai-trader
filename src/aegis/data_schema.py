from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HistoricalOptionRecord:
    timestamp: str
    underlying: str
    symbol: str
    expiration: date
    strike: float
    option_type: str
    bid: float
    ask: float
    last: float | None
    underlying_price: float
    volume: int = 0
    open_interest: int = 0
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    implied_volatility: float | None = None

    def validate(self) -> None:
        if self.option_type not in {"C", "P"}:
            raise ValueError("option_type must be C or P")
        if self.strike <= 0 or self.underlying_price <= 0:
            raise ValueError("strike and underlying price must be positive")
        if self.bid < 0 or self.ask < self.bid:
            raise ValueError("invalid bid/ask")
        if self.volume < 0 or self.open_interest < 0:
            raise ValueError("volume and open interest cannot be negative")


def records_to_rows(records: list[HistoricalOptionRecord]) -> list[dict[str, object]]:
    for record in records:
        record.validate()
    return [record.__dict__.copy() for record in records]
