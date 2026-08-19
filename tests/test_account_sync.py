from types import SimpleNamespace

from aegis.account_sync import AccountSynchronizer
from aegis.store import AegisStore


class FakeClient:
    def get_account(self):
        return SimpleNamespace(equity="10100", cash="9000", buying_power="18000", last_equity="10000")

    def get_all_positions(self):
        return [object(), object()]


def test_sync_persists_account_state(tmp_path) -> None:
    store = AegisStore(tmp_path / "aegis.db")
    state = AccountSynchronizer(FakeClient(), store).sync()
    assert state.equity == 10100
    assert state.daily_pnl == 100
    assert state.open_positions == 2
    assert len(store.recent("account")) == 1
