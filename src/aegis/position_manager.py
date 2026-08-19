from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class PositionState:
    symbol: str
    order_id: str
    opened_at: datetime
    status: str = "pending"
    exit_reason: str | None = None


class PositionManager:
    """In-memory lifecycle state; persistent storage will be added later."""

    def __init__(self) -> None:
        self._positions: dict[str, PositionState] = {}

    def register(self, symbol: str, order_id: str) -> PositionState:
        state = PositionState(symbol=symbol, order_id=order_id, opened_at=datetime.now(timezone.utc))
        self._positions[order_id] = state
        return state

    def update(self, order_id: str, status: str) -> PositionState:
        state = self._positions[order_id]
        updated = PositionState(
            symbol=state.symbol,
            order_id=state.order_id,
            opened_at=state.opened_at,
            status=status,
            exit_reason=state.exit_reason,
        )
        self._positions[order_id] = updated
        return updated

    def close(self, order_id: str, reason: str) -> PositionState:
        state = self._positions[order_id]
        updated = PositionState(
            symbol=state.symbol,
            order_id=state.order_id,
            opened_at=state.opened_at,
            status="closed",
            exit_reason=reason,
        )
        self._positions[order_id] = updated
        return updated

    def get(self, order_id: str) -> PositionState | None:
        return self._positions.get(order_id)

    def active_count(self) -> int:
        return sum(state.status not in {"closed", "canceled", "rejected", "expired"} for state in self._positions.values())
