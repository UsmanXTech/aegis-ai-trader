from aegis.greeks import Greeks
from aegis.options_risk import OptionsRiskEngine
from aegis.quote_intelligence import OptionQuote, quote_risk


def quote(**kwargs):
    values = dict(
        symbol="SPY250919C00500000",
        bid=2.0,
        ask=2.1,
        last=2.05,
        greeks=Greeks(delta=0.5, gamma=0.02, theta=-0.03, vega=0.1, implied_volatility=0.25),
        open_interest=1000,
    )
    values.update(kwargs)
    return OptionQuote(**values)


def test_approves_liquid_contract() -> None:
    result = OptionsRiskEngine().evaluate(quote(), quote_risk(quote().greeks if False else quote()))
    assert result.approved


def test_rejects_wide_spread() -> None:
    result = OptionsRiskEngine().evaluate(quote(ask=2.5), quote_risk(quote()))
    assert not result.approved
    assert "bid/ask spread too wide" in result.reasons


def test_rejects_low_open_interest() -> None:
    result = OptionsRiskEngine().evaluate(quote(open_interest=10), quote_risk(quote()))
    assert not result.approved
    assert "open interest too low" in result.reasons
