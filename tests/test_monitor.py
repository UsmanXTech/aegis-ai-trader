from types import SimpleNamespace

from aegis.monitor import MonitoredStatus, is_terminal, snapshot_order


def make_order(status="filled", filled_qty="1", qty="1", avg="2.50"):
    return SimpleNamespace(
        id="order-1",
        status=status,
        filled_qty=filled_qty,
        qty=qty,
        filled_avg_price=avg,
    )


def test_filled_order_is_terminal() -> None:
    snapshot = snapshot_order(make_order())
    assert snapshot.status is MonitoredStatus.FILLED
    assert snapshot.filled_qty == 1
    assert is_terminal(snapshot)


def test_open_order_is_not_terminal() -> None:
    snapshot = snapshot_order(make_order(status="open", filled_qty="0"))
    assert snapshot.status is MonitoredStatus.OPEN
    assert not is_terminal(snapshot)


def test_unknown_status_is_safe() -> None:
    snapshot = snapshot_order(make_order(status="future_status"))
    assert snapshot.status is MonitoredStatus.UNKNOWN
