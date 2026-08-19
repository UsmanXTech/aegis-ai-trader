from dataclasses import dataclass

from .contract_selector import ContractSelector, SpreadSelection
from .domain import TradeDecision
from .execution import MultiLegOrder, PaperExecutionService
from .risk import RiskEngine


@dataclass(frozen=True)
class PreparedTrade:
    decision: TradeDecision
    selection: SpreadSelection
    order: MultiLegOrder
    payload: dict


class TradePipeline:
    """Turns an approved agent decision into a validated paper-order payload."""

    def __init__(
        self,
        *,
        selector: ContractSelector | None = None,
        execution: PaperExecutionService | None = None,
        risk_engine: RiskEngine | None = None,
    ) -> None:
        self.selector = selector or ContractSelector()
        self.execution = execution or PaperExecutionService()
        self.risk_engine = risk_engine or RiskEngine()

    def prepare_spread(
        self,
        decision: TradeDecision,
        candidates,
        *,
        underlying_price: float,
        account_equity: float,
        portfolio_risk_pct: float,
        daily_loss_pct: float,
        open_positions: int,
    ) -> PreparedTrade:
        if not decision.risk.approved:
            raise ValueError("trade decision was rejected by the risk engine")

        selection = self.selector.select_spread(
            decision.proposal.strategy,
            candidates,
            underlying_price=underlying_price,
        )

        refreshed_risk = self.risk_engine.evaluate(
            decision.proposal.model_copy(
                update={
                    "max_loss": selection.max_loss,
                    "max_profit": selection.max_profit,
                }
            ),
            account_equity=account_equity,
            portfolio_risk_pct=portfolio_risk_pct,
            daily_loss_pct=daily_loss_pct,
            open_positions=open_positions,
        )
        if not refreshed_risk.approved:
            raise ValueError(f"spread rejected by risk engine: {refreshed_risk.reasons}")

        final_decision = decision.model_copy(update={
            "proposal": decision.proposal.model_copy(update={
                "max_loss": selection.max_loss,
                "max_profit": selection.max_profit,
            }),
            "risk": refreshed_risk,
        })
        order = self.selector.to_order(selection)
        payload = self.execution.build_order(order)
        return PreparedTrade(final_decision, selection, order, payload)
