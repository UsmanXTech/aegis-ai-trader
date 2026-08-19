from __future__ import annotations

from datetime import date, timedelta

from .market_data import AlpacaMarketData


def scan_symbol(
    api_key: str,
    secret_key: str,
    symbol: str,
    *,
    days_forward: int = 45,
    strike_low: float | None = None,
    strike_high: float | None = None,
):
    """Fetch current underlying bars and an indicative option chain.

    This function is read-only. It does not submit, replace, or cancel orders.
    """
    market = AlpacaMarketData(api_key, secret_key)
    today = date.today()
    chain = market.option_chain(
        symbol,
        expiration_start=today + timedelta(days=7),
        expiration_end=today + timedelta(days=days_forward),
        strike_low=strike_low,
        strike_high=strike_high,
    )
    return chain
