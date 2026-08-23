from __future__ import annotations

from typing import Iterable, Mapping

from .provider_schema import ProviderFieldMap


def validate_provider_rows(rows: Iterable[Mapping[str, object]], fields: ProviderFieldMap = ProviderFieldMap()) -> list[str]:
    errors: list[str] = []
    required = [fields.timestamp, fields.symbol, fields.expiration, fields.strike, fields.option_type, fields.bid, fields.ask, fields.underlying_price]
    for index, row in enumerate(rows):
        for field in required:
            if field not in row or row[field] in (None, ""):
                errors.append(f"row {index}: missing {field}")
        if fields.bid in row and fields.ask in row:
            try:
                bid = float(row[fields.bid])
                ask = float(row[fields.ask])
                if bid < 0 or ask < bid:
                    errors.append(f"row {index}: invalid bid/ask")
            except (TypeError, ValueError):
                errors.append(f"row {index}: non-numeric bid/ask")
    return errors
