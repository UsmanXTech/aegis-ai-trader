from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator

from .options_backtest import HistoricalOptionQuote


REQUIRED_COLUMNS = (
    "timestamp",
    "symbol",
    "expiration",
    "strike",
    "option_type",
    "bid",
    "ask",
    "underlying_price",
)


@dataclass(frozen=True)
class HistoricalOptionsDataset:
    quotes: tuple[HistoricalOptionQuote, ...]

    @property
    def symbols(self) -> tuple[str, ...]:
        return tuple(sorted({quote.symbol for quote in self.quotes}))

    @property
    def timestamps(self) -> tuple[str, ...]:
        return tuple(sorted({quote.timestamp for quote in self.quotes}))


class HistoricalOptionsCsvLoader:
    """Load the repository's normalized historical-options CSV format.

    Raw provider-specific files should be normalized before being passed here.
    The loader deliberately accepts only the fields required by the deterministic
    backtest engine so provider-specific assumptions stay outside the engine.
    """

    def load(self, path: str | Path) -> HistoricalOptionsDataset:
        csv_path = Path(path)
        with csv_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            columns = tuple(reader.fieldnames or ())
            missing = [column for column in REQUIRED_COLUMNS if column not in columns]
            if missing:
                raise ValueError(f"missing required columns: {', '.join(missing)}")

            quotes = tuple(self._parse_row(row, reader.line_num) for row in reader)

        if not quotes:
            raise ValueError("historical options dataset is empty")
        return HistoricalOptionsDataset(quotes)

    def _parse_row(self, row: dict[str, str | None], line_number: int) -> HistoricalOptionQuote:
        try:
            timestamp = str(row["timestamp"] or "").strip()
            symbol = str(row["symbol"] or "").strip()
            option_type = str(row["option_type"] or "").strip().upper()
            if not timestamp or not symbol:
                raise ValueError("timestamp and symbol are required")
            if option_type not in {"C", "P", "CALL", "PUT"}:
                raise ValueError("option_type must be C, P, CALL, or PUT")

            expiration = date.fromisoformat(str(row["expiration"]))
            strike = float(str(row["strike"]))
            bid = float(str(row["bid"]))
            ask = float(str(row["ask"]))
            underlying_price = float(str(row["underlying_price"]))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid historical options row at CSV line {line_number}: {exc}") from exc

        if strike <= 0 or underlying_price <= 0:
            raise ValueError(f"CSV line {line_number}: strike and underlying_price must be positive")
        if bid < 0 or ask < 0 or ask < bid:
            raise ValueError(f"CSV line {line_number}: invalid bid/ask")

        normalized_type = "C" if option_type in {"C", "CALL"} else "P"
        return HistoricalOptionQuote(
            timestamp=timestamp,
            symbol=symbol,
            expiration=expiration,
            strike=strike,
            option_type=normalized_type,
            bid=bid,
            ask=ask,
            underlying_price=underlying_price,
        )
