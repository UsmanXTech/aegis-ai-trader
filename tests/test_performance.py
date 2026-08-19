from aegis.performance import build_report


def test_performance_report() -> None:
    report = build_report(
        10_000,
        [10_000, 10_100, 9_900, 10_300],
        [100, -200, 400],
    )
    assert report.ending_equity == 10_300
    assert report.closed_trades == 3
    assert report.winning_trades == 2
    assert report.losing_trades == 1
    assert report.win_rate_pct == 200 / 3 * 100
    assert report.max_drawdown_pct > 0
