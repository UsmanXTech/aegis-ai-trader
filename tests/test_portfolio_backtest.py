from aegis.portfolio_backtest import backtest_portfolio
from aegis.spread_backtest import SpreadTrade


def trade(entry: str, exit: str, pnl: float) -> SpreadTrade:
    return SpreadTrade(entry, exit, 200.0, 200.0 + pnl, pnl, "TEST")


def test_portfolio_accumulates_non_overlapping_trades() -> None:
    result = backtest_portfolio(
        [trade("2026-01-01T10:00:00Z", "2026-01-01T11:00:00Z", 100), trade("2026-01-01T12:00:00Z", "2026-01-01T13:00:00Z", -50)]
    )
    assert result.ending_equity == 10050
    assert result.report.closed_trades == 2


def test_portfolio_respects_concurrency_limit() -> None:
    result = backtest_portfolio(
        [trade("2026-01-01T10:00:00Z", "2026-01-01T13:00:00Z", 100), trade("2026-01-01T11:00:00Z", "2026-01-01T12:00:00Z", 200)],
        max_concurrent_trades=1,
    )
    assert len(result.trades) == 1
    assert result.ending_equity == 10100
