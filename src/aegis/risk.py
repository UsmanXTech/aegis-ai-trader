from dataclasses import dataclass

from .domain import RiskDecision, TradeProposal


@dataclass(frozen=True)
class RiskLimits:
    max_position_risk_pct: float = 2.0
    max_portfolio_risk_pct: float = 10.0
    max_daily_loss_pct: float = 3.0
    max_open_positions: int = 5


class RiskEngine:
    """Deterministic authorization layer; the AI cannot override these rules."""

    def __init__(self, limits: RiskLimits | None = None) -> None:
        self.limits = limits or RiskLimits()

    def evaluate(
        self,
        proposal: TradeProposal,
        *,
        account_equity: float,
        portfolio_risk_pct: float,
        daily_loss_pct: float,
        open_positions: int,
    ) -> RiskDecision:
        reasons: list[str] = []

        if account_equity <= 0:
            reasons.append("account equity must be positive")
        if proposal.max_loss > account_equity * self.limits.max_position_risk_pct / 100:
            reasons.append("maximum position risk exceeded")
        if portfolio_risk_pct + (proposal.max_loss / max(account_equity, 1) * 100) > self.limits.max_portfolio_risk_pct:
            reasons.append("maximum portfolio risk exceeded")
        if daily_loss_pct >= self.limits.max_daily_loss_pct:
            reasons.append("daily loss limit reached")
        if open_positions >= self.limits.max_open_positions:
            reasons.append("maximum open positions reached")
        if proposal.strategy.value == "no_trade":
            reasons.append("strategy explicitly rejected")

        return RiskDecision(approved=not reasons, reasons=reasons)
