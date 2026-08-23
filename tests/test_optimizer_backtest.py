from aegis.optimizer_backtest import optimize_exit_parameters
from aegis.options_backtest import HistoricalOptionQuote


def q(ts: str, symbol: str, bid: float, ask: float) -> HistoricalOptionQuote:
    from datetime import date
    return HistoricalOptionQuote(ts, symbol, date(2026, 9, 25), 500 if symbol == "LONG" else 505, "C", bid, ask, 501)


def test_optimizer_uses_spread_backtest() -> None:
    snapshots = [
        ("2026-01-02T15:00:00Z", [q("x", "LONG", 4, 4.2), q("x", "SHORT", 2, 2.1)]),
        ("2026-01-02T16:00:00Z", [q("x", "LONG", 5.5, 5.7), q("x", "SHORT", 2, 2.1)]),
    ]
    result = optimize_exit_parameters(snapshots, "LONG", "SHORT", [0.25, 0.50], [0.25, 0.50])
    assert len(result.results) == 4
    assert result.results[0].score >= result.results[-1].score
