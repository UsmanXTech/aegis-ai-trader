from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .store import AegisStore


@dataclass(frozen=True)
class AccountState:
    equity: float
    cash: float
    buying_power: float
    daily_pnl: float
    open_positions: int


class AccountSynchronizer:
    """Normalize an Alpaca account client into Aegis events."""

    def __init__(self, client: Any, store: AegisStore) -> None:
        self.client = client
        self.store = store

    def sync(self) -> AccountState:
        account = self.client.get_account()
        positions = self.client.get_all_positions()
        equity = float(account.equity)
        last_equity = float(getattr(account, "last_equity", equity))
        state = AccountState(
            equity=equity,
            cash=float(account.cash),
            buying_power=float(account.buying_power),
            daily_pnl=equity - last_equity,
            open_positions=len(positions),
        )
        self.store.append("account", asdict(state))
        return state
