from __future__ import annotations

from dataclasses import dataclass

from .option_contracts import OptionContract, parse_occ_symbol
from .position_sync import PositionRecord


@dataclass(frozen=True)
class EnrichedPosition:
    position: PositionRecord
    contract: OptionContract
    intrinsic_value: float
    moneyness: str


def enrich_position(position: PositionRecord, underlying_price: float) -> EnrichedPosition:
    contract = parse_occ_symbol(position.symbol)
    if contract.option_type == "C":
        intrinsic = max(underlying_price - contract.strike, 0.0)
    else:
        intrinsic = max(contract.strike - underlying_price, 0.0)
    if underlying_price == contract.strike:
        moneyness = "ATM"
    elif intrinsic > 0:
        moneyness = "ITM"
    else:
        moneyness = "OTM"
    return EnrichedPosition(position, contract, intrinsic, moneyness)
