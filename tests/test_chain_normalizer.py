from datetime import date

from aegis.chain_normalizer import normalize_option_chain


def test_normalizes_sdk_like_snapshot() -> None:
    chain = {
        "XYZ260918C00100000": {
            "symbol": "XYZ260918C00100000",
            "details": {
                "expiration_date": date(2026, 9, 18),
                "strike_price": "100",
                "type": "call",
                "open_interest": "1500",
            },
            "latest_quote": {"bid_price": "2.00", "ask_price": "2.20"},
            "greeks": {"delta": "0.52", "implied_volatility": "0.31"},
        }
    }
    result = normalize_option_chain(chain)
    assert len(result) == 1
    assert result[0].symbol == "XYZ260918C00100000"
    assert result[0].strike == 100
    assert result[0].expiration == date(2026, 9, 18)
    assert result[0].delta == 0.52
    assert result[0].open_interest == 1500
