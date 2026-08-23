from aegis.alpaca_historical import AlpacaHistoricalOptionsClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
    def raise_for_status(self):
        pass
    def json(self):
        return self.payload


class FakeSession:
    def __init__(self):
        self.calls = []
    def get(self, url, **kwargs):
        self.calls.append(kwargs)
        if len(self.calls) == 1:
            return FakeResponse({"quotes": {"SPY260220C00500000": [{"t": "2026-01-02T15:00:00Z", "bp": 4.0, "ap": 4.2, "underlying_price": 501}]}, "next_page_token": "next"})
        return FakeResponse({"quotes": {"SPY260220C00500000": [{"t": "2026-01-02T16:00:00Z", "bp": 4.1, "ap": 4.3, "underlying_price": 502}]}})


def test_alpaca_historical_paginates_and_maps() -> None:
    session = FakeSession()
    client = AlpacaHistoricalOptionsClient("key", "secret", session=session)
    quotes = client.historical_quotes(["SPY260220C00500000"], "2026-01-02", "2026-01-03")
    assert len(quotes) == 2
    assert quotes[0].bid == 4.0
    assert session.calls[1]["params"]["page_token"] == "next"
