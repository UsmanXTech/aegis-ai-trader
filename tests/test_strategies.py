from aegis.domain import MarketRegime, OptionStrategy
from aegis.strategies import MarketSnapshot, StrategySelector


selector = StrategySelector()


def test_low_confidence_does_not_trade() -> None:
    snapshot = MarketSnapshot(MarketRegime.BULLISH, 0.59, 0.2, 0.1)
    assert selector.select(snapshot) is OptionStrategy.NO_TRADE


def test_bullish_selects_call_spread() -> None:
    snapshot = MarketSnapshot(MarketRegime.BULLISH, 0.8, 0.2, 0.1)
    assert selector.select(snapshot) is OptionStrategy.BULL_CALL_SPREAD


def test_bearish_selects_put_spread() -> None:
    snapshot = MarketSnapshot(MarketRegime.BEARISH, 0.8, 0.2, 0.1)
    assert selector.select(snapshot) is OptionStrategy.BEAR_PUT_SPREAD


def test_event_with_low_iv_selects_straddle() -> None:
    snapshot = MarketSnapshot(MarketRegime.NEUTRAL, 0.8, 0.05, 0.2, event_risk=True)
    assert selector.select(snapshot) is OptionStrategy.LONG_STRADDLE
