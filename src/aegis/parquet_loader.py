from __future__ import annotations

from pathlib import Path

from .historical_options import HistoricalOptionsCsvLoader
from .options_backtest import HistoricalOptionQuote


class HistoricalOptionsParquetLoader:
    """Load normalized historical options data from Parquet."""

    def load(self, path: str | Path) -> list[HistoricalOptionQuote]:
        try:
            import pandas as pd
        except ImportError as exc:
            raise RuntimeError("Parquet loading requires pandas and a parquet engine") from exc

        frame = pd.read_parquet(path)
        required = set(HistoricalOptionsCsvLoader.REQUIRED_COLUMNS)
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")

        quotes: list[HistoricalOptionQuote] = []
        for row in frame.to_dict(orient="records"):
            quotes.append(
                HistoricalOptionQuote(
                    timestamp=str(row["timestamp"]),
                    symbol=str(row["symbol"]),
                    expiration=row["expiration"],
                    strike=float(row["strike"]),
                    option_type=str(row["option_type"]).upper(),
                    bid=float(row["bid"]),
                    ask=float(row["ask"]),
                    underlying_price=float(row["underlying_price"]),
                )
            )
        return quotes
