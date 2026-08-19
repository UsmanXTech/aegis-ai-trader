from aegis.agent import AegisAgent
from aegis.domain import MarketRegime, OptionStrategy
from aegis.strategies import MarketSnapshot


def test_agent_approves_safe_bullish_trade() -> None:
    result = AegisAgent().evaluate(
        symbol="SPY",
        snapshot=MarketSnapshot(MarketRegime.BULLISH, 0.85, 0.18, 0.10),
        max_loss=100,
        max_profit=220,
        thesis="Bullish regime with favorable risk/reward.",
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    assert result.proposal.strategy is OptionStrategy.BULL_CALL_SPREAD
    assert result.risk.approved


def test_agent_rejects_low_confidence() -> None:
    result = AegisAgent().evaluate(
        symbol="SPY",
        snapshot=MarketSnapshot(MarketRegime.BULLISH, 0.40, 0.18, 0.10),
        max_loss=100,
        max_profit=220,
        thesis="Insufficient confidence.",
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    assert result.proposal.strategy is OptionStrategy.NO_TRADE
    assert not result.risk.approved
