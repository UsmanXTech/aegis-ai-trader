from aegis.idempotency import OrderIdempotencyRegistry


def test_duplicate_decision_returns_existing_submission() -> None:
    registry = OrderIdempotencyRegistry()
    first = registry.register("decision-1", "client-1")
    second = registry.register("decision-1", "client-2")
    assert first == second


def test_submission_tracking() -> None:
    registry = OrderIdempotencyRegistry()
    registry.register("decision-1", "client-1")
    result = registry.mark_submitted("decision-1", "broker-1")
    assert result.broker_order_id == "broker-1"
    assert result.status == "submitted"
