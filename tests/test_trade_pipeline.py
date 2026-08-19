from datetime import date

import pytest

from aegis.agent import AegisAgent
from aegis.domain import MarketRegime, OptionStrategy
from aegis.options import OptionCandidate
from aegis.strategies import MarketSnapshot
from aegis.trade_pipeline import TradePipeline


def c(symbol, strike, typ, bid, ask):
    return OptionCandidate(
        symbol=symbol,
        strike=strike,
        expiration=date(2026, 9, 18),
        option_type=typ,
        bid=bid,
        ask=ask,
        open_interest=2000,
        delta=0.5 if typ == "call" else -0.5,
    )


def test_pipeline_builds_approved_paper_payload() -> None:
    decision = AegisAgent().evaluate(
        symbol="SPY",
        snapshot=MarketSnapshot(MarketRegime.BULLISH, 0.9, 0.18, 0.10),
        max_loss=1,
        max_profit=1,
        thesis="bullish test",
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    prepared = TradePipeline().prepare_spread(
        decision,
        [c("C100", 100, "call", 5.0, 5.2), c("C105", 105, "call", 3.4, 3.6)],
        underlying_price=103,
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    assert prepared.payload["order_class"] == "mleg"
    assert prepared.payload["qty"] == "1"
    assert len(prepared.payload["legs"]) == 2
    assert prepared.selection.max_loss > 0


def test_pipeline_refuses_rejected_decision() -> None:
    decision = AegisAgent().evaluate(
        symbol="SPY",
        snapshot=MarketSnapshot(MarketRegime.BULLISH, 0.2, 0.18, 0.10),
        max_loss=1,
        max_profit=1,
        thesis="low confidence",
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
    )
    with pytest.raises(ValueError, match="risk engine"):
        TradePipeline().prepare_spread(
            decision,
            [c("C100", 100, "call", 5.0, 5.2), c("C105", 105, "call", 3.4, 3.6)],
            underlying_price=103,
            account_equity=10_000,
            portfolio_risk_pct=0,
            daily_loss_pct=0,
            open_positions=0,
        )
