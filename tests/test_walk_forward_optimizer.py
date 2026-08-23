from datetime import date

from aegis.options_backtest import HistoricalOptionQuote
from aegis.walk_forward_optimizer import optimize_walk_forward


def q(ts: str, symbol: str, bid: float, ask: float) -> HistoricalOptionQuote:
    return HistoricalOptionQuote(ts, symbol, date(2026, 9, 25), 500 if symbol == "LONG" else 505, "C", bid, ask, 501)


def test_walk_forward_uses_train_best_on_test() -> None:
    rows = []
    for i in range(6):
        ts = f"2026-01-0{i + 1}T15:00:00Z"
        rows.append((ts, [q(ts, "LONG", 4 + i * 0.2, 4.2 + i * 0.2), q(ts, "SHORT", 2, 2.1)]))
    result = optimize_walk_forward(rows, "LONG", "SHORT", train_size=3, test_size=2, take_profit_values=[0.25, 0.5], stop_loss_values=[0.25, 0.5])
    assert len(result) == 1
    assert "take_profit_pct" in result[0].train_best
