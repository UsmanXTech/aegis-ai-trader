from __future__ import annotations

from datetime import date
from typing import Any, Iterable

from .data_schema import HistoricalOptionRecord


class OptionsDataAdapter:
    """Map provider-specific dictionaries into the Aegis historical schema."""

    def normalize(self, rows: Iterable[dict[str, Any]]) -> list[HistoricalOptionRecord]:
        records: list[HistoricalOptionRecord] = []
        for row in rows:
            record = HistoricalOptionRecord(
                timestamp=str(row["timestamp"]),
                underlying=str(row["underlying"]),
                symbol=str(row["symbol"]),
                expiration=self._date(row["expiration"]),
                strike=float(row["strike"]),
                option_type=str(row["option_type"]).upper(),
                bid=float(row["bid"]),
                ask=float(row["ask"]),
                last=float(row["last"]) if row.get("last") is not None else None,
                underlying_price=float(row["underlying_price"]),
                volume=int(row.get("volume", 0)),
                open_interest=int(row.get("open_interest", 0)),
                delta=self._float(row.get("delta")),
                gamma=self._float(row.get("gamma")),
                theta=self._float(row.get("theta")),
                vega=self._float(row.get("vega")),
                implied_volatility=self._float(row.get("implied_volatility")),
            )
            record.validate()
            records.append(record)
        return records

    @staticmethod
    def _date(value: Any) -> date:
        if isinstance(value, date):
            return value
        return date.fromisoformat(str(value))

    @staticmethod
    def _float(value: Any) -> float | None:
        return None if value is None else float(value)
