from aegis.greeks import Greeks, scale_greeks
from aegis.quote_intelligence import OptionQuote


def test_greeks_scale_by_contract_multiplier() -> None:
    risk = scale_greeks(Greeks(delta=0.5, gamma=0.02, theta=-0.03, vega=0.1), 2)
    assert risk.delta_exposure == 100
    assert risk.gamma_exposure == 4
    assert risk.theta_exposure == -6
    assert risk.vega_exposure == 20


def test_quote_midpoint_and_spread() -> None:
    quote = OptionQuote(
        symbol="SPY250919C00500000",
        bid=2.0,
        ask=2.2,
        last=2.1,
        greeks=Greeks(delta=0.5),
        open_interest=1000,
    )
    assert quote.midpoint == 2.1
    assert round(quote.spread_pct, 4) == round((0.2 / 2.1) * 100, 4)
