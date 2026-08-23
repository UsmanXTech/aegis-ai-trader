from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Mapping

from .provider_schema import ProviderFieldMap, map_provider_row
from .provider_validation import validate_provider_rows
from .options_backtest import HistoricalOptionQuote


def load_provider_csv(path: str | Path, fields: ProviderFieldMap = ProviderFieldMap()) -> list[HistoricalOptionQuote]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    errors = validate_provider_rows(rows, fields)
    if errors:
        raise ValueError("invalid provider dataset: " + "; ".join(errors[:10]))
    return [map_provider_row(row, fields) for row in rows]


def normalize_rows(rows: Iterable[Mapping[str, object]], fields: ProviderFieldMap = ProviderFieldMap()) -> list[HistoricalOptionQuote]:
    rows = list(rows)
    errors = validate_provider_rows(rows, fields)
    if errors:
        raise ValueError("invalid provider rows: " + "; ".join(errors[:10]))
    return [map_provider_row(row, fields) for row in rows]
