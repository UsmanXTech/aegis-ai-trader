from pathlib import Path

from aegis.alpaca_dataset_builder import build_dataset
from aegis.options_backtest import HistoricalOptionQuote


class FakeClient:
    def historical_quotes(self, symbols, start, end, *, feed):
        return [HistoricalOptionQuote("2026-01-02T15:00:00Z", "SPY260220C00500000", __import__("datetime").date(2026, 2, 20), 500, "C", 4, 4.2, 501)]


def test_build_dataset(tmp_path: Path) -> None:
    output = tmp_path / "options.csv"
    count = build_dataset(FakeClient(), ["SPY260220C00500000"], "2026-01-02", "2026-01-03", output)
    assert count == 1
    assert "SPY260220C00500000" in output.read_text(encoding="utf-8")
