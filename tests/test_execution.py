import pytest

from aegis.domain import OptionStrategy
from aegis.execution import MultiLegOrder, OptionLeg, PaperExecutionService


def test_builds_bull_call_spread_payload() -> None:
    order = MultiLegOrder(
        strategy=OptionStrategy.BULL_CALL_SPREAD,
        legs=(
            OptionLeg("SPY_CALL_1", "buy", "buy_to_open"),
            OptionLeg("SPY_CALL_2", "sell", "sell_to_open"),
        ),
        qty=1,
        limit_price=1.25,
    )
    payload = PaperExecutionService().build_order(order)
    assert payload["order_class"] == "mleg"
    assert payload["type"] == "limit"
    assert payload["time_in_force"] == "day"
    assert len(payload["legs"]) == 2


def test_rejects_single_leg() -> None:
    order = MultiLegOrder(
        strategy=OptionStrategy.BULL_CALL_SPREAD,
        legs=(OptionLeg("SPY_CALL", "buy", "buy_to_open"),),
    )
    with pytest.raises(ValueError, match="at least two"):
        PaperExecutionService().build_order(order)


def test_rejects_more_than_four_legs() -> None:
    legs = tuple(OptionLeg(f"LEG{i}", "buy", "buy_to_open") for i in range(5))
    order = MultiLegOrder(strategy=OptionStrategy.LONG_STRADDLE, legs=legs)
    with pytest.raises(ValueError, match="at most four"):
        PaperExecutionService().build_order(order)
