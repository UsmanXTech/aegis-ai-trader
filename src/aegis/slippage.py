from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TransactionCostModel:
    slippage_bps: float = 5.0
    commission_per_contract: float = 0.0
    contract_multiplier: int = 100

    def entry_cost(self, debit: float, contracts: int = 1) -> float:
        if debit < 0 or contracts < 1:
            raise ValueError("debit must be non-negative and contracts must be positive")
        slipped = debit * (1.0 + self.slippage_bps / 10_000.0)
        return slipped * self.contract_multiplier * contracts + self.commission_per_contract * 2 * contracts

    def exit_value(self, mark: float, contracts: int = 1) -> float:
        if mark < 0 or contracts < 1:
            raise ValueError("mark must be non-negative and contracts must be positive")
        slipped = mark * (1.0 - self.slippage_bps / 10_000.0)
        return slipped * self.contract_multiplier * contracts - self.commission_per_contract * 2 * contracts
