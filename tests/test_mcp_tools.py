from aegis.mcp_tools import AlpacaMcpTrading
from aegis.mcp_client import McpCallResult
from aegis.order_builder import MultiLegOrderBuilder


class FakeMcp:
    def call(self, method, params=None):
        assert method == "place_order"
        assert params["legs"][0]["side"] == "buy"
        return McpCallResult({"result": {"id": "paper-order-1"}})


def test_submit_multileg_paper_order() -> None:
    order = MultiLegOrderBuilder().build_debit_spread("LONG", "SHORT", debit_limit=2.15)
    result = AlpacaMcpTrading(FakeMcp()).submit_multileg(order)
    assert result.response.raw["result"]["id"] == "paper-order-1"


def test_live_order_is_blocked() -> None:
    order = MultiLegOrderBuilder().build_debit_spread("LONG", "SHORT", debit_limit=2.15)
    live_order = order.__class__(order.legs, order.order_type, order.limit_price, order.time_in_force, False)
    try:
        AlpacaMcpTrading(FakeMcp()).submit_multileg(live_order)
    except PermissionError:
        return
    raise AssertionError("live order must be blocked")
