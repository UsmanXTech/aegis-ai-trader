from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class DatasetQualityReport:
    quotes: int
    symbols: int
    timestamps: int
    expirations: int
    invalid_quotes: int
    duplicate_keys: int


def summarize_quotes(quotes: list[HistoricalOptionQuote]) -> DatasetQualityReport:
    keys = [(q.timestamp, q.symbol) for q in quotes]
    duplicates = len(keys) - len(set(keys))
    invalid = sum(1 for q in quotes if q.bid < 0 or q.ask < q.bid or q.ask <= 0 or q.strike <= 0)
    return DatasetQualityReport(
        quotes=len(quotes),
        symbols=len({q.symbol for q in quotes}),
        timestamps=len({q.timestamp for q in quotes}),
        expirations=len({q.expiration for q in quotes}),
        invalid_quotes=invalid,
        duplicate_keys=duplicates,
    )
