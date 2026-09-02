from __future__ import annotations

from pathlib import Path
from typing import Callable

from .alpaca_historical import AlpacaHistoricalOptionsClient


def build_dataset(
    client: AlpacaHistoricalOptionsClient,
    symbols: list[str],
    start: str,
    end: str,
    output: str | Path,
    *,
    feed: str = "indicative",
    underlying_price_resolver: Callable[[str, str], float],
) -> int:
    """Fetch option quotes and write the canonical Aegis CSV."""
    quotes = client.historical_quotes(
        symbols,
        start,
        end,
        feed=feed,
        underlying_price_resolver=underlying_price_resolver,
    )
    valid = [q for q in quotes if q.underlying_price > 0]
    if not valid:
        raise ValueError("no quotes with usable underlying prices were returned")

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("timestamp,symbol,expiration,strike,option_type,bid,ask,underlying_price\n")
        for q in valid:
            handle.write(
                f"{q.timestamp},{q.symbol},{q.expiration.isoformat()},{q.strike},"
                f"{q.option_type},{q.bid},{q.ask},{q.underlying_price}\n"
            )
    return len(valid)
