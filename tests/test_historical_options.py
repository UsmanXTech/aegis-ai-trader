from pathlib import Path

import pytest

from aegis.historical_options import HistoricalOptionsCsvLoader


def test_load_normalized_csv(tmp_path: Path) -> None:
    path = tmp_path / "options.csv"
    path.write_text(
        "timestamp,symbol,expiration,strike,option_type,bid,ask,underlying_price\n"
        "2026-01-02T15:00:00Z,SPY260220C00500000,2026-02-20,500,C,4.0,4.2,505\n"
        "2026-01-02T15:00:00Z,SPY260220C00505000,2026-02-20,505,call,2.0,2.1,505\n",
        encoding="utf-8",
    )
    dataset = HistoricalOptionsCsvLoader().load(path)
    assert len(dataset.quotes) == 2
    assert dataset.quotes[0].option_type == "C"
    assert dataset.symbols == ("SPY260220C00500000", "SPY260220C00505000")


def test_missing_columns_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("symbol,bid,ask\nSPY,1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        HistoricalOptionsCsvLoader().load(path)


def test_invalid_quote_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text(
        "timestamp,symbol,expiration,strike,option_type,bid,ask,underlying_price\n"
        "2026-01-02T15:00:00Z,SPY,2026-02-20,500,C,4.2,4.0,505\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="invalid bid/ask"):
        HistoricalOptionsCsvLoader().load(path)
