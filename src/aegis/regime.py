from dataclasses import dataclass

from .domain import MarketRegime


@dataclass(frozen=True)
class RegimeInput:
    price: float
    sma_fast: float
    sma_slow: float
    momentum_pct: float


class RegimeDetector:
    """Simple deterministic baseline; later replaced/enriched by agent features."""

    def detect(self, data: RegimeInput) -> tuple[MarketRegime, float]:
        if data.price <= 0 or data.sma_fast <= 0 or data.sma_slow <= 0:
            return MarketRegime.UNKNOWN, 0.0

        bullish = data.price > data.sma_fast > data.sma_slow and data.momentum_pct > 0
        bearish = data.price < data.sma_fast < data.sma_slow and data.momentum_pct < 0

        if bullish:
            confidence = min(0.99, 0.60 + abs(data.momentum_pct) / 20)
            return MarketRegime.BULLISH, confidence
        if bearish:
            confidence = min(0.99, 0.60 + abs(data.momentum_pct) / 20)
            return MarketRegime.BEARISH, confidence
        return MarketRegime.NEUTRAL, 0.50
