from .domain import OptionStrategy, TradeDecision
from .execution import MultiLegOrder, OptionLeg


class ExecutionPolicy:
    """Converts approved strategy decisions into explicitly constrained orders."""

    ALLOWED = {
        OptionStrategy.BULL_CALL_SPREAD,
        OptionStrategy.BEAR_PUT_SPREAD,
        OptionStrategy.LONG_STRADDLE,
    }

    def create_order(
        self,
        decision: TradeDecision,
        *,
        legs: tuple[OptionLeg, ...],
        qty: int = 1,
        limit_price: float | None = None,
    ) -> MultiLegOrder:
        if not decision.risk.approved:
            raise ValueError("risk engine rejected this trade")
        if decision.proposal.strategy not in self.ALLOWED:
            raise ValueError("strategy is not enabled for execution")
        if not legs:
            raise ValueError("option legs are required")

        return MultiLegOrder(
            strategy=decision.proposal.strategy,
            legs=legs,
            qty=qty,
            limit_price=limit_price,
        )
