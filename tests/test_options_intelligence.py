from aegis.options_intelligence import enrich_position
from aegis.position_sync import PositionRecord


def make(symbol: str) -> PositionRecord:
    return PositionRecord(symbol, 1, 2.0, 230.0, 30.0, 15.0, "long", "now")


def test_itm_call() -> None:
    result = enrich_position(make("SPY250919C00500000"), 510.0)
    assert result.contract.strike == 500
    assert result.contract.option_type == "C"
    assert result.intrinsic_value == 10
    assert result.moneyness == "ITM"


def test_otm_call() -> None:
    result = enrich_position(make("SPY250919C00500000"), 490.0)
    assert result.intrinsic_value == 0
    assert result.moneyness == "OTM"
