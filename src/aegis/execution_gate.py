from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Any

from .risk_pipeline import TradeRiskPipeline, RiskPipelineDecision
from .quote_intelligence import OptionQuote


class PaperExecutor(Protocol):
    def submit(self, payload: dict[str, Any]) -> Any: ...


@dataclass(frozen=True)
class GatedExecutionResult:
    submitted: bool
    risk: RiskPipelineDecision
    response: Any = None


class GatedPaperExecutor:
    """Hard boundary preventing an order from reaching execution without risk approval."""

    def __init__(self, executor: PaperExecutor, risk: TradeRiskPipeline | None = None) -> None:
        self.executor = executor
        self.risk = risk or TradeRiskPipeline()

    def submit(self, quote: OptionQuote, payload: dict[str, Any], quantity: float = 1) -> GatedExecutionResult:
        decision = self.risk.evaluate(quote, quantity)
        if not decision.approved:
            return GatedExecutionResult(False, decision)
        if payload.get("paper_only") is not True:
            raise PermissionError("paper_only=true is required")
        return GatedExecutionResult(True, decision, self.executor.submit(payload))
