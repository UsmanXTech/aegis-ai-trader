from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubmissionRecord:
    decision_id: str
    client_order_id: str
    broker_order_id: str | None = None
    status: str = "created"


class OrderIdempotencyRegistry:
    """Prevent duplicate broker submissions for the same trading decision."""

    def __init__(self) -> None:
        self._records: dict[str, SubmissionRecord] = {}

    def register(self, decision_id: str, client_order_id: str) -> SubmissionRecord:
        if decision_id in self._records:
            return self._records[decision_id]
        record = SubmissionRecord(decision_id, client_order_id)
        self._records[decision_id] = record
        return record

    def mark_submitted(self, decision_id: str, broker_order_id: str) -> SubmissionRecord:
        current = self._records[decision_id]
        updated = SubmissionRecord(
            decision_id=current.decision_id,
            client_order_id=current.client_order_id,
            broker_order_id=broker_order_id,
            status="submitted",
        )
        self._records[decision_id] = updated
        return updated

    def get(self, decision_id: str) -> SubmissionRecord | None:
        return self._records.get(decision_id)
