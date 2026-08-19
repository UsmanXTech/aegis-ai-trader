from aegis.domain import MarketRegime, OptionStrategy, TradeProposal
from aegis.risk import RiskEngine, RiskLimits


def proposal(max_loss: float = 100.0) -> TradeProposal:
    return TradeProposal(
        symbol="SPY",
        strategy=OptionStrategy.BULL_CALL_SPREAD,
        regime=MarketRegime.BULLISH,
        confidence=0.8,
        max_loss=max_loss,
        max_profit=200.0,
        thesis="test",
    )


def test_approves_trade_inside_limits() -> None:
    decision = RiskEngine().evaluate(
        proposal(),
        account_equity=10_000,
        portfolio_risk_pct=1.0,
        daily_loss_pct=0.5,
        open_positions=1,
    )
    assert decision.approved
    assert decision.reasons == []


def test_rejects_position_risk() -> None:
    engine = RiskEngine(RiskLimits(max_position_risk_pct=1.0))
    decision = engine.evaluate(
        proposal(101.0),
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    assert not decision.approved
    assert "maximum position risk exceeded" in decision.reasons


def test_rejects_after_daily_loss_limit() -> None:
    decision = RiskEngine().evaluate(
        proposal(),
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=3.0,
        open_positions=0,
    )
    assert not decision.approved
    assert "daily loss limit reached" in decision.reasons
