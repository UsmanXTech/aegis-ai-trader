from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OptionCandidate:
    symbol: str
    strike: float
    expiration: date
    option_type: str
    bid: float
    ask: float
    open_interest: int
    delta: float | None = None
    implied_volatility: float | None = None

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2

    @property
    def spread_pct(self) -> float:
        if self.mid <= 0:
            return 1.0
        return (self.ask - self.bid) / self.mid


def score_candidate(candidate: OptionCandidate, *, target_delta: float = 0.50) -> float:
    """Liquidity-first score for selecting a contract; no trade is executed here."""
    liquidity = min(candidate.open_interest / 1000, 1.0)
    spread_quality = max(0.0, 1.0 - candidate.spread_pct)
    delta_quality = 0.0
    if candidate.delta is not None:
        delta_quality = max(0.0, 1.0 - abs(abs(candidate.delta) - target_delta) / target_delta)
    return 0.45 * liquidity + 0.40 * spread_quality + 0.15 * delta_quality
