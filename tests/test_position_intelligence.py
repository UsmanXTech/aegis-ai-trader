from aegis.position_intelligence import ExitReason, PositionExitEngine, PositionState


def make(**changes) -> PositionState:
    values = dict(
        symbol="SPY",
        entry_debit=200.0,
        current_debit=150.0,
        max_loss=200.0,
        max_profit=300.0,
        days_to_expiration=10,
        signal_confidence=0.8,
        entry_confidence=0.8,
    )
    values.update(changes)
    return PositionState(**values)


def test_take_profit() -> None:
    result = PositionExitEngine().evaluate(make(current_debit=90.0))
    assert result.exit
    assert result.reason is ExitReason.TAKE_PROFIT


def test_expiration_protection() -> None:
    result = PositionExitEngine().evaluate(make(days_to_expiration=1))
    assert result.exit
    assert result.reason is ExitReason.EXPIRATION


def test_signal_invalidation() -> None:
    result = PositionExitEngine().evaluate(make(signal_confidence=0.2))
    assert result.exit
    assert result.reason is ExitReason.SIGNAL_INVALIDATED


def test_hold() -> None:
    result = PositionExitEngine().evaluate(make(current_debit=180.0))
    assert not result.exit
    assert result.reason is ExitReason.HOLD
