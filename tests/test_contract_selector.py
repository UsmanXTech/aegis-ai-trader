from datetime import date

import pytest

from aegis.contract_selector import ContractSelector
from aegis.domain import OptionStrategy
from aegis.options import OptionCandidate


def candidate(symbol: str, strike: float, option_type: str, bid: float, ask: float, oi: int = 1500):
    return OptionCandidate(
        symbol=symbol,
        strike=strike,
        expiration=date(2026, 9, 18),
        option_type=option_type,
        bid=bid,
        ask=ask,
        open_interest=oi,
        delta=0.5 if option_type == "call" else -0.5,
    )


def test_selects_bull_call_spread() -> None:
    selector = ContractSelector()
    result = selector.select_spread(
        OptionStrategy.BULL_CALL_SPREAD,
        [
            candidate("C100", 100, "call", 5.0, 5.2),
            candidate("C105", 105, "call", 2.8, 3.0),
            candidate("C110", 110, "call", 1.0, 1.2),
        ],
        underlying_price=103,
    )
    assert result.long_leg.strike < result.short_leg.strike
    assert result.estimated_debit > 0
    assert result.max_profit > 0


def test_rejects_missing_candidates() -> None:
    with pytest.raises(ValueError):
        ContractSelector().select_spread(
            OptionStrategy.BULL_CALL_SPREAD,
            [],
            underlying_price=100,
        )
