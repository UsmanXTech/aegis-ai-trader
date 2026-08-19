from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AccountSnapshot:
    equity: float
    cash: float
    daily_pnl: float
    open_positions: int


class TradingGateway(Protocol):
    """Interface used by Aegis; concrete Alpaca transport is isolated here."""

    def get_account(self) -> AccountSnapshot: ...

    def submit_order(self, *, symbol: str, qty: int, side: str) -> str: ...


class AlpacaPaperGateway:
    """Paper-trading adapter placeholder.

    The network client is deliberately not constructed until credentials are
    explicitly supplied. This keeps tests and local development offline-safe.
    """

    def __init__(self, api_key: str, secret_key: str, base_url: str) -> None:
        if not api_key or not secret_key:
            raise ValueError("Alpaca paper credentials are required")
        if "paper-api.alpaca.markets" not in base_url:
            raise ValueError("Aegis currently permits only the Alpaca paper endpoint")
        self.base_url = base_url
        self._api_key = api_key
        self._secret_key = secret_key

    def get_account(self) -> AccountSnapshot:
        raise NotImplementedError("Connect the official Alpaca SDK/API client in the next stage")

    def submit_order(self, *, symbol: str, qty: int, side: str) -> str:
        raise NotImplementedError("Order execution is intentionally disabled until paper integration")
