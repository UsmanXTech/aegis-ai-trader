from datetime import date

from aegis.provider_schema import ProviderFieldMap, map_provider_row


def test_maps_provider_row() -> None:
    quote = map_provider_row({
        "ts": "2026-01-02T15:00:00Z", "sym": "SPY260220C00500000", "exp": "2026-02-20",
        "k": 500, "typ": "c", "b": 4, "a": 4.2, "u": 501,
    }, ProviderFieldMap("ts", "sym", "exp", "k", "typ", "b", "a", "u"))
    assert quote.symbol == "SPY260220C00500000"
    assert quote.expiration == date(2026, 2, 20)
    assert quote.option_type == "C"
