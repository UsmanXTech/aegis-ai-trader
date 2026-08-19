from datetime import date

from aegis.options_backtest import HistoricalOptionQuote, OptionLeg, OptionsBacktestEngine


def quote(symbol: str, bid: float, ask: float) -> HistoricalOptionQuote:
    return HistoricalOptionQuote(
        timestamp="2026-01-02T15:00:00Z",
        symbol=symbol,
        expiration=date(2026, 2, 20),
        strike=500.0,
        option_type="C",
        bid=bid,
        ask=ask,
        underlying_price=505.0,
    )


def test_bull_call_spread_price_and_mark() -> None:
    quotes = [quote("LONG", 4.0, 4.2), quote("SHORT", 2.0, 2.1)]
    legs = [OptionLeg("LONG", "buy"), OptionLeg("SHORT", "sell")]
    engine = OptionsBacktestEngine()
    assert engine.price_spread(quotes, legs) == 220
    assert engine.mark_to_mid(quotes, legs) == 205


def test_missing_quote_fails() -> None:
    try:
        OptionsBacktestEngine().mark_to_mid([], [OptionLeg("MISSING", "buy")])
    except ValueError:
        return
    raise AssertionError("missing quote should fail")
