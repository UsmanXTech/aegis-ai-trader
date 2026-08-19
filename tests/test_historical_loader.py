from aegis.historical_loader import HistoricalOptionsLoader


def test_load_csv(tmp_path) -> None:
    path = tmp_path / "options.csv"
    path.write_text(
        "timestamp,underlying,symbol,expiration,strike,option_type,bid,ask,last,underlying_price,volume,open_interest\n"
        "2026-01-02T15:00:00Z,SPY,SPY260220C00500000,2026-02-20,500,C,2,2.2,2.1,505,100,1000\n",
        encoding="utf-8",
    )
    records = HistoricalOptionsLoader().load_csv(path)
    assert len(records) == 1
    assert records[0].symbol == "SPY260220C00500000"
    assert records[0].open_interest == 1000
