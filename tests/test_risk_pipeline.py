from aegis.greeks import Greeks
from aegis.options_risk import OptionsRiskEngine
from aegis.quote_intelligence import OptionQuote
from aegis.risk_pipeline import TradeRiskPipeline


def make_quote(**changes):
    values = dict(
        symbol="SPY250919C00500000",
        bid=2.0,
        ask=2.1,
        last=2.05,
        greeks=Greeks(delta=0.5, gamma=0.02, theta=-0.03, vega=0.1, implied_volatility=0.25),
        open_interest=1000,
    )
    values.update(changes)
    return OptionQuote(**values)


def test_pipeline_approves_safe_quote() -> None:
    result = TradeRiskPipeline().evaluate(make_quote())
    assert result.approved
    assert result.reasons == ()


def test_pipeline_rejects_before_execution() -> None:
    result = TradeRiskPipeline().evaluate(make_quote(ask=3.0))
    assert not result.approved
    assert "bid/ask spread too wide" in result.reasons
