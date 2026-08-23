from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class DatasetQualityReport:
    rows: int
    unique_symbols: int
    invalid_quotes: int
    missing_bid_ask: int
    crossed_quotes: int
    duplicate_keys: int
    coverage_start: str | None
    coverage_end: str | None

    @property
    def usable(self) -> bool:
        return self.rows > 0 and self.invalid_quotes == 0 and self.crossed_quotes == 0


def assess_quotes(quotes: Iterable[HistoricalOptionQuote]) -> DatasetQualityReport:
    rows = list(quotes)
    seen: set[tuple[str, str]] = set()
    duplicates = 0
    invalid = 0
    missing = 0
    crossed = 0
    for quote in rows:
        key = (quote.timestamp, quote.symbol)
        if key in seen:
            duplicates += 1
        seen.add(key)
        if quote.bid < 0 or quote.ask < 0 or quote.ask < quote.bid or quote.strike <= 0 or quote.underlying_price <= 0:
            invalid += 1
        if quote.bid <= 0 or quote.ask <= 0:
            missing += 1
        if quote.ask < quote.bid:
            crossed += 1
    timestamps = sorted(q.timestamp for q in rows)
    return DatasetQualityReport(
        rows=len(rows),
        unique_symbols=len({q.symbol for q in rows}),
        invalid_quotes=invalid,
        missing_bid_ask=missing,
        crossed_quotes=crossed,
        duplicate_keys=duplicates,
        coverage_start=timestamps[0] if timestamps else None,
        coverage_end=timestamps[-1] if timestamps else None,
    )
