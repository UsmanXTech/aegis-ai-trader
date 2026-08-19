from dataclasses import dataclass
from datetime import date

from .domain import MarketRegime, TradeDecision
from .strategies import MarketSnapshot


@dataclass(frozen=True)
class UnderlyingSnapshot:
    symbol: str
    price: float
    fast_sma: float
    slow_sma: float
    momentum: float
    implied_volatility: float
    expected_move: float
    event_risk: bool = False


@dataclass(frozen=True)
class ScanResult:
    as_of: date
    underlying: UnderlyingSnapshot
    market: MarketSnapshot


class MarketScanner:
    """Pure decision-input builder; networking remains in the Alpaca adapter."""

    def scan(self, snapshot: UnderlyingSnapshot) -> ScanResult:
        if snapshot.price <= 0:
            raise ValueError("underlying price must be positive")
        if snapshot.fast_sma > snapshot.slow_sma and snapshot.momentum > 0:
            regime = MarketRegime.BULLISH
        elif snapshot.fast_sma < snapshot.slow_sma and snapshot.momentum < 0:
            regime = MarketRegime.BEARISH
        else:
            regime = MarketRegime.NEUTRAL

        distance = abs(snapshot.fast_sma - snapshot.slow_sma) / max(snapshot.price, 1.0)
        momentum_strength = min(abs(snapshot.momentum), 1.0)
        confidence = min(0.99, 0.50 + distance * 5 + momentum_strength * 0.35)
        if regime is MarketRegime.NEUTRAL:
            confidence = min(confidence, 0.55)

        return ScanResult(
            as_of=date.today(),
            underlying=snapshot,
            market=MarketSnapshot(
                regime=regime,
                confidence=confidence,
                implied_volatility=snapshot.implied_volatility,
                expected_move=snapshot.expected_move,
                event_risk=snapshot.event_risk,
            ),
        )
