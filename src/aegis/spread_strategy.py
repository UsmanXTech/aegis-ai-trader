from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .options_backtest import HistoricalOptionQuote, OptionLeg, OptionsBacktestEngine


@dataclass(frozen=True)
class SpreadRules:
    min_dte: int = 7
    max_dte: int = 45
    long_delta_target: float = 0.60
    short_delta_target: float = 0.30
    take_profit_pct: float = 0.50
    max_loss_pct: float = 1.00


@dataclass(frozen=True)
class SpreadTradeResult:
    strategy: str
    entry_timestamp: str
    exit_timestamp: str
    entry_debit: float
    exit_value: float
    pnl: float
    exit_reason: str


def _dte(expiration: date, timestamp_date: date) -> int:
    return (expiration - timestamp_date).days


class DefinedRiskSpreadStrategy:
    def __init__(self, rules: SpreadRules | None = None, engine: OptionsBacktestEngine | None = None) -> None:
        self.rules = rules or SpreadRules()
        self.engine = engine or OptionsBacktestEngine()

    def evaluate_exit(self, entry_debit: float, current_value: float) -> str:
        if entry_debit <= 0:
            raise ValueError("entry debit must be positive")
        pnl = entry_debit - current_value
        if pnl >= entry_debit * self.rules.take_profit_pct:
            return "take_profit"
        if pnl <= -entry_debit * self.rules.max_loss_pct:
            return "max_loss"
        return "hold"

    def build_bull_call(self, long_symbol: str, short_symbol: str) -> tuple[OptionLeg, ...]:
        return (OptionLeg(long_symbol, "buy"), OptionLeg(short_symbol, "sell"))

    def build_bear_put(self, long_symbol: str, short_symbol: str) -> tuple[OptionLeg, ...]:
        return (OptionLeg(long_symbol, "buy"), OptionLeg(short_symbol, "sell"))
