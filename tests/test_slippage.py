import pytest

from aegis.slippage import TransactionCostModel


def test_entry_cost_applies_slippage_and_commission() -> None:
    model = TransactionCostModel(slippage_bps=10, commission_per_contract=0.5)
    assert model.entry_cost(2.0) == pytest.approx(201.0)


def test_exit_value_applies_slippage_and_commission() -> None:
    model = TransactionCostModel(slippage_bps=10, commission_per_contract=0.5)
    assert model.exit_value(3.0) == pytest.approx(299.0)
