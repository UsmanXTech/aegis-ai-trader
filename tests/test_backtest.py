from aegis.backtest import BacktestBar, BacktestEngine


def test_backtest_profit_and_costs() -> None:
    bars = [
        BacktestBar("t1", "SPY", 100, 1),
        BacktestBar("t2", "SPY", 110, 1),
        BacktestBar("t3", "SPY", 105, 0),
    ]
    result = BacktestEngine(commission_per_trade=1, slippage_bps=10).run(
        bars, starting_equity=10_000, signal=lambda bar: 1 if bar.timestamp != "t3" else 0
    )
    assert len(result.trades) == 1
    assert result.ending_equity < 10_009
    assert result.ending_equity > 10_003


def test_backtest_rejects_invalid_equity() -> None:
    try:
        BacktestEngine().run([], starting_equity=0, signal=lambda _: 0)
    except ValueError:
        return
    raise AssertionError("invalid equity should fail")
