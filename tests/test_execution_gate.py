from aegis.execution_gate import GatedPaperExecutor
from aegis.quote_intelligence import OptionQuote
from aegis.greeks import Greeks


class FakeExecutor:
    def submit(self, payload):
        return {"id": "paper-1"}


def make_quote():
    return OptionQuote("SPY260918C00500000", 2.0, 2.1, 2.05, Greeks(implied_volatility=0.25), 1000)


def test_safe_order_reaches_executor():
    result = GatedPaperExecutor(FakeExecutor()).submit(make_quote(), {"paper_only": True})
    assert result.submitted
    assert result.response["id"] == "paper-1"


def test_live_order_is_blocked():
    try:
        GatedPaperExecutor(FakeExecutor()).submit(make_quote(), {"paper_only": False})
    except PermissionError:
        return
    raise AssertionError("live execution must be blocked")
