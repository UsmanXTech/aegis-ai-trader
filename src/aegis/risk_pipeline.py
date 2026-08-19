from __future__ import annotations

from dataclasses import dataclass

from .options_risk import OptionsRiskDecision, OptionsRiskEngine
from .quote_intelligence import OptionQuote, quote_risk


@dataclass(frozen=True)
class RiskPipelineDecision:
    approved: bool
    options: OptionsRiskDecision
    reasons: tuple[str, ...]


class TradeRiskPipeline:
    """Mandatory deterministic options gate before an order can be prepared."""

    def __init__(self, options_engine: OptionsRiskEngine | None = None) -> None:
        self.options_engine = options_engine or OptionsRiskEngine()

    def evaluate(self, quote: OptionQuote, quantity: float = 1) -> RiskPipelineDecision:
        exposure = quote_risk(quote, quantity)
        options = self.options_engine.evaluate(quote, exposure)
        return RiskPipelineDecision(
            approved=options.approved,
            options=options,
            reasons=options.reasons,
        )
