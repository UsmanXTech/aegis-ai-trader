from datetime import date

import pandas as pd

from aegis.parquet_loader import HistoricalOptionsParquetLoader


def test_load_parquet(tmp_path) -> None:
    path = tmp_path / "quotes.parquet"
    pd.DataFrame(
        [{
            "timestamp": "2026-01-02T15:00:00Z",
            "symbol": "SPY260220C00500000",
            "expiration": date(2026, 2, 20),
            "strike": 500,
            "option_type": "C",
            "bid": 4.0,
            "ask": 4.2,
            "underlying_price": 501,
        }]
    ).to_parquet(path)
    quotes = HistoricalOptionsParquetLoader().load(path)
    assert len(quotes) == 1
    assert quotes[0].symbol == "SPY260220C00500000"
