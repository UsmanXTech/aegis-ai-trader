import pytest

from aegis.agent import AegisAgent
from aegis.domain import MarketRegime
from aegis.execution import OptionLeg
from aegis.order_policy import ExecutionPolicy
from aegis.strategies import MarketSnapshot


def test_policy_requires_risk_approval() -> None:
    decision = AegisAgent().evaluate(
        symbol="SPY",
        snapshot=MarketSnapshot(MarketRegime.BULLISH, 0.4, 0.2, 0.1),
        max_loss=100,
        max_profit=200,
        thesis="low confidence",
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    with pytest.raises(ValueError, match="risk engine rejected"):
        ExecutionPolicy().create_order(
            decision,
            legs=(OptionLeg("A", "buy", "buy_to_open"), OptionLeg("B", "sell", "sell_to_open")),
        )
