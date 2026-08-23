from __future__ import annotations

from pathlib import Path

from .alpaca_historical import AlpacaHistoricalOptionsClient
from .options_backtest import HistoricalOptionQuote


def build_dataset(
    client: AlpacaHistoricalOptionsClient,
    symbols: list[str],
    start: str,
    end: str,
    output: str | Path,
    *,
    feed: str = "indicative",
) -> int:
    """Fetch option quotes and write the canonical Aegis CSV.

    Underlying prices must be supplied by the upstream adapter; this builder
    refuses quotes that have no usable underlying price because the backtester
    relies on that field for chain/risk analysis.
    """
    quotes = client.historical_quotes(symbols, start, end, feed=feed)
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
