from dataclasses import dataclass
from datetime import date

from aegis.selection_filters import SelectionFilters, filter_candidates


@dataclass(frozen=True)
class Candidate:
    expiration: date
    bid: float
    ask: float
    open_interest: int


def test_filters_dte_liquidity_and_spread() -> None:
    as_of = date(2026, 1, 1)
    candidates = [
        Candidate(date(2026, 1, 20), 2.0, 2.1, 1000),
        Candidate(date(2026, 1, 2), 2.0, 2.1, 1000),
        Candidate(date(2026, 1, 20), 2.0, 3.0, 1000),
        Candidate(date(2026, 1, 20), 2.0, 2.1, 10),
    ]
    result = filter_candidates(
        candidates,
        as_of=as_of,
        filters=SelectionFilters(min_dte=7, max_dte=30, min_open_interest=100, max_spread_pct=8),
    )
    assert len(result) == 1
