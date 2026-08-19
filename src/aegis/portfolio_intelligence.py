from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .position_intelligence import ExitDecision, PositionExitEngine, PositionState
from .position_sync import PositionRecord


@dataclass(frozen=True)
class PositionInsight:
    position: PositionRecord
    exit: ExitDecision
    days_to_expiration: int | None


@dataclass(frozen=True)
class PortfolioSnapshot:
    total_market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    positions: tuple[PositionInsight, ...]
    exits_required: int


class PortfolioIntelligence:
    def __init__(self, exit_engine: PositionExitEngine | None = None) -> None:
        self.exit_engine = exit_engine or PositionExitEngine()

    def analyze(
        self,
        positions: Iterable[PositionRecord],
        *,
        metadata: dict[str, tuple[float, float, int]] | None = None,
    ) -> PortfolioSnapshot:
        rows: list[PositionInsight] = []
        total_value = 0.0
        total_pnl = 0.0
        total_cost = 0.0

        for position in positions:
            total_value += position.market_value
            total_pnl += position.unrealized_pnl
            total_cost += position.avg_entry_price * abs(position.qty)
            entry, max_loss, days = (metadata or {}).get(
                position.symbol, (position.avg_entry_price, 0.0, 999)
            )
            state = PositionState(
                symbol=position.symbol,
                entry_debit=entry,
                current_debit=max(
                    entry - position.unrealized_pnl / max(abs(position.qty), 1),
                    0.01,
                ),
                max_loss=max_loss,
                max_profit=0.0,
                days_to_expiration=days,
                signal_confidence=1.0,
                entry_confidence=1.0,
            )
            rows.append(PositionInsight(position, self.exit_engine.evaluate(state), days))

        return PortfolioSnapshot(
            total_market_value=total_value,
            unrealized_pnl=total_pnl,
            unrealized_pnl_pct=(total_pnl / total_cost * 100) if total_cost else 0.0,
            positions=tuple(rows),
            exits_required=sum(item.exit.exit for item in rows),
        )