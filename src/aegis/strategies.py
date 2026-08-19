from dataclasses import dataclass

from .domain import MarketRegime, OptionStrategy


@dataclass(frozen=True)
class MarketSnapshot:
    regime: MarketRegime
    confidence: float
    implied_volatility: float
    expected_move: float
    event_risk: bool = False


class StrategySelector:
    """Deterministic first-pass options strategy selection."""

    def select(self, snapshot: MarketSnapshot) -> OptionStrategy:
        if snapshot.confidence < 0.60:
            return OptionStrategy.NO_TRADE

        if snapshot.event_risk and snapshot.implied_volatility < snapshot.expected_move:
            return OptionStrategy.LONG_STRADDLE

        if snapshot.regime is MarketRegime.BULLISH:
            return OptionStrategy.BULL_CALL_SPREAD

        if snapshot.regime is MarketRegime.BEARISH:
            return OptionStrategy.BEAR_PUT_SPREAD

        return OptionStrategy.NO_TRADE
