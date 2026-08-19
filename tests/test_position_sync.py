from types import SimpleNamespace

from aegis.position_sync import OrderSynchronizer, PositionSynchronizer
from aegis.store import AegisStore


class FakeClient:
    def get_all_positions(self):
        return [
            SimpleNamespace(
                symbol="SPY250919C00500000",
                qty="1",
                avg_entry_price="2.10",
                market_value="230",
                unrealized_pl="20",
                unrealized_plpc="0.0952",
                side="long",
            )
        ]

    def get_orders(self, limit=50):
        return [
            SimpleNamespace(
                id="order-1",
                symbol="SPY250919C00500000",
                status="filled",
                side="buy",
                qty="1",
                filled_qty="1",
                order_class="mleg",
                submitted_at="2026-08-19T10:00:00Z",
                filled_at="2026-08-19T10:00:02Z",
            )
        ]


def test_position_sync(tmp_path) -> None:
    store = AegisStore(tmp_path / "aegis.db")
    records = PositionSynchronizer(FakeClient(), store).sync()
    assert records[0].symbol == "SPY250919C00500000"
    assert records[0].unrealized_pnl == 20
    assert len(store.recent("position")) == 1


def test_order_sync(tmp_path) -> None:
    store = AegisStore(tmp_path / "aegis.db")
    records = OrderSynchronizer(FakeClient(), store).sync()
    assert records[0]["status"] == "filled"
    assert records[0]["filled_qty"] == "1"
    assert len(store.recent("order")) == 1
