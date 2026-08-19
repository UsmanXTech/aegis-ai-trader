from aegis.data_adapter import OptionsDataAdapter


def test_normalizes_provider_row() -> None:
    records = OptionsDataAdapter().normalize([
        {
            "timestamp": "2026-01-02T15:00:00Z",
            "underlying": "SPY",
            "symbol": "SPY260220C00500000",
            "expiration": "2026-02-20",
            "strike": 500,
            "option_type": "c",
            "bid": 2.0,
            "ask": 2.2,
            "last": 2.1,
            "underlying_price": 505,
            "volume": 100,
            "open_interest": 1000,
            "delta": 0.6,
        }
    ])
    assert records[0].option_type == "C"
    assert records[0].expiration.isoformat() == "2026-02-20"
    assert records[0].delta == 0.6


def test_rejects_bad_market_data() -> None:
    try:
        OptionsDataAdapter().normalize([
            {
                "timestamp": "x", "underlying": "SPY", "symbol": "X",
                "expiration": "2026-02-20", "strike": 0, "option_type": "C",
                "bid": 2, "ask": 2, "underlying_price": 500,
            }
        ])
    except ValueError:
        return
    raise AssertionError("invalid market data should fail validation")
