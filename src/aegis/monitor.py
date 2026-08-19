from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class MonitoredStatus(StrEnum):
    OPEN = "open"
    ACCEPTED = "accepted"
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class OrderSnapshot:
    order_id: str
    status: MonitoredStatus
    filled_qty: float
    qty: float
    filled_avg_price: float | None


def snapshot_order(order: Any) -> OrderSnapshot:
    raw_status = str(order.status).lower().split(".")[-1]
    try:
        status = MonitoredStatus(raw_status)
    except ValueError:
        status = MonitoredStatus.UNKNOWN

    filled_qty = float(order.filled_qty or 0)
    qty = float(order.qty or 0)
    avg_price = order.filled_avg_price

    return OrderSnapshot(
        order_id=str(order.id),
        status=status,
        filled_qty=filled_qty,
        qty=qty,
        filled_avg_price=float(avg_price) if avg_price is not None else None,
    )


def is_terminal(snapshot: OrderSnapshot) -> bool:
    return snapshot.status in {
        MonitoredStatus.FILLED,
        MonitoredStatus.CANCELED,
        MonitoredStatus.REJECTED,
        MonitoredStatus.EXPIRED,
    }
