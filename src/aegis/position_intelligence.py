from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ExitReason(StrEnum):
    TAKE_PROFIT = "take_profit"
    MAX_LOSS = "max_loss"
    EXPIRATION = "expiration"
    SIGNAL_INVALIDATED = "signal_invalidated"
    HOLD = "hold"


@dataclass(frozen=True)
class PositionState:
    symbol: str
    entry_debit: float
    current_debit: float
    max_loss: float
    max_profit: float
    days_to_expiration: int
    signal_confidence: float
    entry_confidence: float

    @property
    def pnl(self) -> float:
        return self.entry_debit - self.current_debit

    @property
    def pnl_pct(self) -> float:
        if self.entry_debit <= 0:
            return 0.0
        return self.pnl / self.entry_debit * 100


@dataclass(frozen=True)
class ExitDecision:
    exit: bool
    reason: ExitReason
    rationale: str


class PositionExitEngine:
    """Deterministic exit layer; AI cannot override hard loss/expiry rules."""

    def __init__(self, *, take_profit_pct: float = 50.0, confidence_floor: float = 0.45) -> None:
        self.take_profit_pct = take_profit_pct
        self.confidence_floor = confidence_floor

    def evaluate(self, position: PositionState) -> ExitDecision:
        if position.days_to_expiration <= 1:
            return ExitDecision(True, ExitReason.EXPIRATION, "expiration protection")

        if position.max_loss > 0 and position.pnl <= -position.max_loss:
            return ExitDecision(True, ExitReason.MAX_LOSS, "maximum defined loss reached")

        if position.max_profit > 0 and position.pnl >= position.max_profit:
            return ExitDecision(True, ExitReason.TAKE_PROFIT, "maximum defined profit reached")

        if position.pnl_pct >= self.take_profit_pct:
            return ExitDecision(True, ExitReason.TAKE_PROFIT, "take-profit threshold reached")

        if position.signal_confidence < self.confidence_floor:
            return ExitDecision(True, ExitReason.SIGNAL_INVALIDATED, "signal confidence fell below floor")

        return ExitDecision(False, ExitReason.HOLD, "position remains within exit policy")
