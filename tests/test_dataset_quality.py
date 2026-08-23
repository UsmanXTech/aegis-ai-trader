from datetime import date

from aegis.dataset_quality import assess_quotes
from aegis.options_backtest import HistoricalOptionQuote


def quote(symbol: str, timestamp: str, bid: float = 1.0, ask: float = 1.2) -> HistoricalOptionQuote:
    return HistoricalOptionQuote(timestamp, symbol, date(2026, 9, 18), 500, "C", bid, ask, 501)


def test_quality_report_is_usable() -> None:
    report = assess_quotes([quote("A", "2026-01-01T00:00:00Z"), quote("B", "2026-01-02T00:00:00Z")])
    assert report.usable
    assert report.rows == 2
    assert report.unique_symbols == 2


def test_quality_report_detects_crossed_quotes_and_duplicates() -> None:
    rows = [quote("A", "2026-01-01T00:00:00Z", 2, 1), quote("A", "2026-01-01T00:00:00Z", 2, 1)]
    report = assess_quotes(rows)
    assert not report.usable
    assert report.crossed_quotes == 2
    assert report.duplicate_keys == 1
