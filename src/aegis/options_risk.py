from __future__ import annotations

from dataclasses import dataclass

from .greeks import GreeksRisk
from .quote_intelligence import OptionQuote


@dataclass(frozen=True)
class OptionsRiskLimits:
    max_abs_delta: float = 150.0
    max_abs_gamma: float = 50.0
    max_abs_theta: float = 100.0
    max_abs_vega: float = 200.0
    max_spread_pct: float = 8.0
    min_open_interest: int = 100
    min_iv: float = 0.01
    max_iv: float = 3.0


@dataclass(frozen=True)
class OptionsRiskDecision:
    approved: bool
    reasons: tuple[str, ...]


class OptionsRiskEngine:
    def __init__(self, limits: OptionsRiskLimits | None = None) -> None:
        self.limits = limits or OptionsRiskLimits()

    def evaluate(self, quote: OptionQuote, exposure: GreeksRisk) -> OptionsRiskDecision:
        reasons: list[str] = []
        if abs(exposure.delta_exposure) > self.limits.max_abs_delta:
            reasons.append("delta exposure exceeded")
        if abs(exposure.gamma_exposure) > self.limits.max_abs_gamma:
            reasons.append("gamma exposure exceeded")
        if abs(exposure.theta_exposure) > self.limits.max_abs_theta:
            reasons.append("theta exposure exceeded")
        if abs(exposure.vega_exposure) > self.limits.max_abs_vega:
            reasons.append("vega exposure exceeded")
        if quote.spread_pct > self.limits.max_spread_pct:
            reasons.append("bid/ask spread too wide")
        if quote.open_interest < self.limits.min_open_interest:
            reasons.append("open interest too low")
        if not self.limits.min_iv <= quote.greeks.implied_volatility <= self.limits.max_iv:
            reasons.append("implied volatility outside allowed range")
        return OptionsRiskDecision(not reasons, tuple(reasons))
