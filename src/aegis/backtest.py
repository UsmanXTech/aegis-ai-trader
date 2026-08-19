from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class BacktestBar:
    timestamp: str
    underlying: str
    price: float
    signal: float


@dataclass(frozen=True)
class BacktestTrade:
    entry_time: str
    exit_time: str
    entry_price: float
    exit_price: float
    pnl: float


@dataclass(frozen=True)
class BacktestResult:
    starting_equity: float
    ending_equity: float
    total_return_pct: float
    trades: tuple[BacktestTrade, ...]
    max_drawdown_pct: float


class BacktestEngine:
    """Minimal event-driven engine with explicit costs and no look-ahead."""

    def __init__(self, *, commission_per_trade: float = 0.0, slippage_bps: float = 0.0) -> None:
        if commission_per_trade < 0 or slippage_bps < 0:
            raise ValueError("cost parameters cannot be negative")
        self.commission = commission_per_trade
        self.slippage = slippage_bps / 10_000

    def run(
        self,
        bars: Iterable[BacktestBar],
        *,
        starting_equity: float,
        signal: Callable[[BacktestBar], int],
    ) -> BacktestResult:
        if starting_equity <= 0:
            raise ValueError("starting equity must be positive")
        equity = starting_equity
        peak = equity
        max_drawdown = 0.0
        open_trade: tuple[str, float] | None = None
        trades: list[BacktestTrade] = []

        for bar in bars:
            action = signal(bar)
            if open_trade is None and action > 0:
                open_trade = (bar.timestamp, bar.price * (1 + self.slippage))
            elif open_trade is not None and action <= 0:
                entry_time, entry_price = open_trade
                exit_price = bar.price * (1 - self.slippage)
                pnl = exit_price - entry_price - self.commission
                equity += pnl
                trades.append(BacktestTrade(entry_time, bar.timestamp, entry_price, exit_price, pnl))
                open_trade = None
                peak = max(peak, equity)
                max_drawdown = max(max_drawdown, (peak - equity) / peak * 100)

        return BacktestResult(
            starting_equity=starting_equity,
            ending_equity=equity,
            total_return_pct=(equity - starting_equity) / starting_equity * 100,
            trades=tuple(trades),
            max_drawdown_pct=max_drawdown,
        )
