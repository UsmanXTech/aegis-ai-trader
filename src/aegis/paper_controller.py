from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .execution import MultiLegOrder
from .paper_gateway import SubmittedOrder


class PaperGateway(Protocol):
    def submit_order(self, order_request: object) -> SubmittedOrder: ...
    def get_order(self, order_id: str) -> object: ...


@dataclass(frozen=True)
class ExecutionResult:
    submitted: bool
    order_id: str | None
    status: str
    reason: str


class PaperExecutionController:
    """Final paper-only gate between prepared trades and Alpaca."""

    def __init__(self, gateway: PaperGateway) -> None:
        self.gateway = gateway

    def submit(self, order: MultiLegOrder, payload: dict, *, approved: bool) -> ExecutionResult:
        if not approved:
            return ExecutionResult(False, None, "rejected", "risk approval required")
        if order.qty < 1 or len(order.legs) < 2 or len(order.legs) > 4:
            return ExecutionResult(False, None, "rejected", "invalid multi-leg order")

        submitted = self.gateway.submit_order(payload)
        return ExecutionResult(True, submitted.order_id, submitted.status, "submitted to paper account")

    def status(self, order_id: str) -> str:
        order = self.gateway.get_order(order_id)
        return str(getattr(order, "status", "unknown"))
