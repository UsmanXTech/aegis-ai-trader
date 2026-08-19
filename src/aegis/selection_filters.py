from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from .options import OptionCandidate


@dataclass(frozen=True)
class SelectionFilters:
    min_dte: int = 7
    max_dte: int = 45
    min_open_interest: int = 100
    max_spread_pct: float = 8.0


def filter_candidates(
    candidates: Iterable[OptionCandidate],
    *,
    as_of: date,
    filters: SelectionFilters | None = None,
) -> list[OptionCandidate]:
    rules = filters or SelectionFilters()
    if rules.min_dte < 0 or rules.max_dte < rules.min_dte:
        raise ValueError("invalid DTE range")
    result: list[OptionCandidate] = []
    for candidate in candidates:
        dte = (candidate.expiration - as_of).days
        midpoint = (candidate.bid + candidate.ask) / 2 if candidate.ask >= candidate.bid else 0.0
        spread_pct = ((candidate.ask - candidate.bid) / midpoint * 100) if midpoint > 0 else 100.0
        if not rules.min_dte <= dte <= rules.max_dte:
            continue
        if getattr(candidate, "open_interest", 0) < rules.min_open_interest:
            continue
        if spread_pct > rules.max_spread_pct:
            continue
        result.append(candidate)
    return result
