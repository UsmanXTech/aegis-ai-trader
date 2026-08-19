from dataclasses import dataclass

from aegis.execution import MultiLegOrder, OptionLeg
from aegis.domain import OptionStrategy
from aegis.paper_controller import PaperExecutionController


@dataclass
class FakeSubmitted:
    order_id: str = "paper-123"
    status: str = "accepted"


class FakeGateway:
    def __init__(self) -> None:
        self.submitted = None

    def submit_order(self, order_request):
        self.submitted = order_request
        return FakeSubmitted()

    def get_order(self, order_id):
        return FakeSubmitted(order_id=order_id, status="filled")


def test_rejected_trade_never_reaches_gateway():
    gateway = FakeGateway()
    controller = PaperExecutionController(gateway)
    order = MultiLegOrder(
        strategy=OptionStrategy.BULL_CALL_SPREAD,
        legs=(
            OptionLeg("SPY260918C00650000", "buy", "buy_to_open"),
            OptionLeg("SPY260918C00655000", "sell", "sell_to_open"),
        ),
    )
    result = controller.submit(order, {"order_class": "mleg"}, approved=False)
    assert not result.submitted
    assert gateway.submitted is None


def test_approved_trade_is_submitted():
    gateway = FakeGateway()
    controller = PaperExecutionController(gateway)
    order = MultiLegOrder(
        strategy=OptionStrategy.BULL_CALL_SPREAD,
        legs=(
            OptionLeg("SPY260918C00650000", "buy", "buy_to_open"),
            OptionLeg("SPY260918C00655000", "sell", "sell_to_open"),
        ),
    )
    result = controller.submit(order, {"order_class": "mleg"}, approved=True)
    assert result.submitted
    assert result.order_id == "paper-123"
    assert gateway.submitted == {"order_class": "mleg"}
    assert controller.status("paper-123") == "filled"
