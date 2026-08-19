import pytest

from aegis.paper_gateway import AlpacaPaperGateway


def payload() -> dict:
    return {
        "order_class": "mleg",
        "qty": "1",
        "type": "limit",
        "limit_price": "1.25",
        "time_in_force": "day",
        "legs": [
            {
                "symbol": "SPY260918C00650000",
                "ratio_qty": "1",
                "side": "buy",
                "position_intent": "buy_to_open",
            },
            {
                "symbol": "SPY260918C00655000",
                "ratio_qty": "1",
                "side": "sell",
                "position_intent": "sell_to_open",
            },
        ],
    }


def test_converts_mleg_payload_to_sdk_request() -> None:
    request = AlpacaPaperGateway.to_sdk_request(payload())
    assert request.qty == 1
    assert float(request.limit_price) == 1.25
    assert len(request.legs) == 2
    assert str(request.legs[0].position_intent.value) == "buy_to_open"
    assert str(request.legs[1].side.value) == "sell"


def test_rejects_non_mleg_payload() -> None:
    data = payload()
    data["order_class"] = "simple"
    with pytest.raises(ValueError, match="only MLeg"):
        AlpacaPaperGateway.to_sdk_request(data)
