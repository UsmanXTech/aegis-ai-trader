from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class DatasetInventory:
    quotes: int
    symbols: int
    timestamps: int
    start: str | None
    end: str | None


def inventory(quotes: Iterable[HistoricalOptionQuote]) -> DatasetInventory:
    rows = list(quotes)
    timestamps = sorted(q.timestamp for q in rows)
    return DatasetInventory(
        quotes=len(rows),
        symbols=len({q.symbol for q in rows}),
        timestamps=len(set(timestamps)),
        start=timestamps[0] if timestamps else None,
        end=timestamps[-1] if timestamps else None,
    )
