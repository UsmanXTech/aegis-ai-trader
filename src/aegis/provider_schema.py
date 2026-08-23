from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Mapping

from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class ProviderFieldMap:
    timestamp: str = "timestamp"
    symbol: str = "symbol"
    expiration: str = "expiration"
    strike: str = "strike"
    option_type: str = "option_type"
    bid: str = "bid"
    ask: str = "ask"
    underlying_price: str = "underlying_price"


def map_provider_row(row: Mapping[str, object], fields: ProviderFieldMap = ProviderFieldMap()) -> HistoricalOptionQuote:
    expiration = row[fields.expiration]
    if isinstance(expiration, str):
        expiration = date.fromisoformat(expiration)
    if not isinstance(expiration, date):
        raise ValueError("expiration must be a date or ISO date string")
    return HistoricalOptionQuote(
        timestamp=str(row[fields.timestamp]),
        symbol=str(row[fields.symbol]),
        expiration=expiration,
        strike=float(row[fields.strike]),
        option_type=str(row[fields.option_type]).upper(),
        bid=float(row[fields.bid]),
        ask=float(row[fields.ask]),
        underlying_price=float(row[fields.underlying_price]),
    )
