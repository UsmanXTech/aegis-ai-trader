from aegis.spread_strategy import DefinedRiskSpreadStrategy


def test_bull_call_legs() -> None:
    legs = DefinedRiskSpreadStrategy().build_bull_call("LONG", "SHORT")
    assert [leg.side for leg in legs] == ["buy", "sell"]


def test_take_profit() -> None:
    strategy = DefinedRiskSpreadStrategy()
    assert strategy.evaluate_exit(200, 90) == "take_profit"


def test_max_loss() -> None:
    strategy = DefinedRiskSpreadStrategy()
    assert strategy.evaluate_exit(200, 410) == "max_loss"


def test_hold() -> None:
    strategy = DefinedRiskSpreadStrategy()
    assert strategy.evaluate_exit(200, 180) == "hold"
