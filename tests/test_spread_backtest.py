from aegis.options_backtest import HistoricalOptionQuote
from aegis.spread_backtest import BullCallSpreadBacktester


def q(ts: str, symbol: str, bid: float, ask: float) -> HistoricalOptionQuote:
    return HistoricalOptionQuote(
        timestamp=ts,
        symbol=symbol,
        expiration=__import__("datetime").date(2026, 9, 25),
        strike=500 if symbol == "LONG" else 505,
        option_type="C",
        bid=bid,
        ask=ask,
        underlying_price=501,
    )


def test_take_profit_lifecycle() -> None:
    backtester = BullCallSpreadBacktester()
    snapshots = [
        ("2026-01-02T15:00:00Z", [q("x", "LONG", 4.0, 4.2), q("x", "SHORT", 2.0, 2.1)]),
        ("2026-01-02T16:00:00Z", [q("x", "LONG", 5.5, 5.7), q("x", "SHORT", 2.0, 2.1)]),
    ]
    trades = backtester.run(snapshots, "LONG", "SHORT", take_profit_pct=0.5)
    assert len(trades) == 1
    assert trades[0].reason == "TAKE_PROFIT"
    assert trades[0].pnl == 155.0


def test_end_of_data_exit() -> None:
    backtester = BullCallSpreadBacktester()
    snapshots = [
        ("2026-01-02T15:00:00Z", [q("x", "LONG", 4.0, 4.2), q("x", "SHORT", 2.0, 2.1)]),
        ("2026-01-02T16:00:00Z", [q("x", "LONG", 4.1, 4.3), q("x", "SHORT", 2.0, 2.2)]),
    ]
    trades = backtester.run(snapshots, "LONG", "SHORT")
    assert trades[0].reason == "END_OF_DATA"
    assert trades[0].pnl == 5.0
