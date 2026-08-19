from datetime import date

from aegis.option_contracts import parse_occ_symbol


def test_parse_occ_call() -> None:
    contract = parse_occ_symbol("SPY250919C00500000")
    assert contract.underlying == "SPY"
    assert contract.option_type == "C"
    assert contract.strike == 500.0
    assert contract.expiration == date(2025, 9, 19)


def test_reject_invalid_symbol() -> None:
    try:
        parse_occ_symbol("SPY-invalid")
    except ValueError:
        return
    raise AssertionError("invalid option symbol should fail")
