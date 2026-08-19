from .domain import MarketRegime, TradeDecision, TradeProposal
from .risk import RiskEngine
from .strategies import MarketSnapshot, StrategySelector


class AegisAgent:
    """Coordinates signal interpretation, strategy selection and risk approval."""

    def __init__(self, risk_engine: RiskEngine | None = None) -> None:
        self.selector = StrategySelector()
        self.risk_engine = risk_engine or RiskEngine()

    def evaluate(
        self,
        *,
        symbol: str,
        snapshot: MarketSnapshot,
        max_loss: float,
        max_profit: float,
        thesis: str,
        account_equity: float,
        portfolio_risk_pct: float,
        daily_loss_pct: float,
        open_positions: int,
    ) -> TradeDecision:
        strategy = self.selector.select(snapshot)
        proposal = TradeProposal(
            symbol=symbol,
            strategy=strategy,
            regime=snapshot.regime,
            confidence=snapshot.confidence,
            max_loss=max_loss,
            max_profit=max_profit,
            thesis=thesis,
        )
        risk = self.risk_engine.evaluate(
            proposal,
            account_equity=account_equity,
            portfolio_risk_pct=portfolio_risk_pct,
            daily_loss_pct=daily_loss_pct,
            open_positions=open_positions,
        )
        return TradeDecision(proposal=proposal, risk=risk)
