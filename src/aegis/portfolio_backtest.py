from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .performance import PerformanceReport, build_report
from .spread_backtest import SpreadTrade


@dataclass(frozen=True)
class PortfolioBacktestResult:
    starting_equity: float
    ending_equity: float
    equity_curve: tuple[float, ...]
    trades: tuple[SpreadTrade, ...]
    report: PerformanceReport


def backtest_portfolio(
    trades: Iterable[SpreadTrade],
    *,
    starting_equity: float = 10_000.0,
    max_concurrent_trades: int = 1,
) -> PortfolioBacktestResult:
    if starting_equity <= 0:
        raise ValueError("starting equity must be positive")
    if max_concurrent_trades < 1:
        raise ValueError("max_concurrent_trades must be positive")

    ordered = sorted(trades, key=lambda trade: trade.exit_timestamp)
    equity = starting_equity
    curve = [equity]
    accepted: list[SpreadTrade] = []
    active: list[SpreadTrade] = []

    for trade in ordered:
        active = [item for item in active if item.exit_timestamp > trade.entry_timestamp]
        if len(active) >= max_concurrent_trades:
            continue
        accepted.append(trade)
        active.append(trade)
        equity += trade.pnl
        curve.append(equity)

    report = build_report(starting_equity, curve, [trade.pnl for trade in accepted])
    return PortfolioBacktestResult(
        starting_equity=starting_equity,
        ending_equity=equity,
        equity_curve=tuple(curve),
        trades=tuple(accepted),
        report=report,
    )
