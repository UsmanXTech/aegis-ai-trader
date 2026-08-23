from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class BullCallCandidate:
    long: HistoricalOptionQuote
    short: HistoricalOptionQuote
    debit: float
    width: float


def generate_bull_call_candidates(
    quotes: Iterable[HistoricalOptionQuote],
    *,
    min_width: float = 1.0,
    max_width: float = 10.0,
    min_dte: int = 7,
    max_dte: int = 60,
) -> list[BullCallCandidate]:
    grouped: dict[tuple[str, date, float], HistoricalOptionQuote] = {}
    for quote in quotes:
        key = (quote.timestamp, quote.expiration, quote.strike)
        grouped.setdefault(key, quote)

    calls = [q for q in grouped.values() if q.option_type.upper() == "C" and q.ask > 0 and q.bid >= 0]
    result: list[BullCallCandidate] = []
    for long in calls:
        dte = (long.expiration - date.fromisoformat(long.timestamp[:10])).days
        if not min_dte <= dte <= max_dte:
            continue
        for short in calls:
            if short.timestamp != long.timestamp or short.expiration != long.expiration:
                continue
            if short.strike <= long.strike:
                continue
            width = short.strike - long.strike
            if not min_width <= width <= max_width:
                continue
            debit = long.ask - short.bid
            if debit <= 0 or debit >= width:
                continue
            result.append(BullCallCandidate(long, short, debit, width))
    return result
