from aegis.order_builder import MultiLegOrderBuilder


def test_build_debit_spread() -> None:
    order = MultiLegOrderBuilder().build_debit_spread("LONG", "SHORT", debit_limit=2.15)
    assert order.paper_only
    assert order.order_type == "limit"
    assert order.limit_price == 2.15
    assert [(leg.symbol, leg.side) for leg in order.legs] == [("LONG", "buy"), ("SHORT", "sell")]


def test_rejects_invalid_spread() -> None:
    try:
        MultiLegOrderBuilder().build_debit_spread("X", "X", debit_limit=2)
    except ValueError:
        return
    raise AssertionError("invalid spread should fail")
