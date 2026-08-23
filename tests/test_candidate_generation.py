from datetime import date

from aegis.candidate_generation import generate_bull_call_candidates
from aegis.options_backtest import HistoricalOptionQuote


def q(symbol: str, strike: float, bid: float, ask: float) -> HistoricalOptionQuote:
    return HistoricalOptionQuote("2026-01-02T15:00:00Z", symbol, date(2026, 2, 20), strike, "C", bid, ask, 501)


def test_generates_valid_debit_spread() -> None:
    result = generate_bull_call_candidates([q("A", 500, 4, 4.2), q("B", 505, 1.8, 2.0)])
    assert len(result) == 1
    assert result[0].debit == 2.4
    assert result[0].width == 5


def test_rejects_non_positive_debit() -> None:
    result = generate_bull_call_candidates([q("A", 500, 4, 4.2), q("B", 505, 4.3, 4.5)])
    assert result == []
