from datetime import date

from aegis.market_data import _parse_occ_symbol


def test_parse_occ_call_symbol() -> None:
    strike, expiration, option_type = _parse_occ_symbol("AAPL260918C00200000")
    assert strike == 200.0
    assert expiration == date(2026, 9, 18)
    assert option_type == "C"


def test_parse_occ_put_symbol() -> None:
    strike, expiration, option_type = _parse_occ_symbol("SPY261218P00500000")
    assert strike == 500.0
    assert expiration == date(2026, 12, 18)
    assert option_type == "P"
