from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from .store import AegisStore


@dataclass(frozen=True)
class PositionRecord:
    symbol: str
    qty: float
    avg_entry_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    side: str
    synced_at: str


class PositionSynchronizer:
    """Persist the broker's current positions as normalized Aegis events."""

    def __init__(self, client: Any, store: AegisStore) -> None:
        self.client = client
        self.store = store

    def sync(self) -> list[PositionRecord]:
        now = datetime.now(timezone.utc).isoformat()
        records: list[PositionRecord] = []
        for position in self.client.get_all_positions():
            record = PositionRecord(
                symbol=str(position.symbol),
                qty=float(position.qty),
                avg_entry_price=float(position.avg_entry_price),
                market_value=float(position.market_value),
                unrealized_pnl=float(position.unrealized_pl),
                unrealized_pnl_pct=float(position.unrealized_plpc) * 100,
                side=str(position.side),
                synced_at=now,
            )
            records.append(record)
            self.store.append("position", asdict(record))
        return records


class OrderSynchronizer:
    """Persist recent broker orders without assuming submission equals a fill."""

    def __init__(self, client: Any, store: AegisStore) -> None:
        self.client = client
        self.store = store

    def sync(self, *, limit: int = 50) -> list[dict[str, Any]]:
        if limit < 1:
            raise ValueError("limit must be positive")
        orders = self.client.get_orders(limit=limit)
        records: list[dict[str, Any]] = []
        for order in orders:
            record = {
                "id": str(order.id),
                "symbol": str(order.symbol),
                "status": str(order.status),
                "side": str(order.side),
                "qty": str(order.qty),
                "filled_qty": str(order.filled_qty),
                "order_class": str(order.order_class),
                "submitted_at": str(order.submitted_at),
                "filled_at": str(order.filled_at) if order.filled_at else None,
            }
            records.append(record)
            self.store.append("order", record)
        return records
