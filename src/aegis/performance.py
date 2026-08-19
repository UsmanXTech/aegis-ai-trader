from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class PerformanceReport:
    starting_equity: float
    ending_equity: float
    total_return_pct: float
    closed_trades: int
    winning_trades: int
    losing_trades: int
    win_rate_pct: float
    profit_factor: float
    max_drawdown_pct: float


def build_report(starting_equity: float, equity_curve: list[float], trade_pnls: list[float]) -> PerformanceReport:
    if starting_equity <= 0:
        raise ValueError("starting equity must be positive")
    if not equity_curve:
        equity_curve = [starting_equity]

    ending = equity_curve[-1]
    total_return = (ending - starting_equity) / starting_equity * 100
    winners = sum(p > 0 for p in trade_pnls)
    losers = sum(p < 0 for p in trade_pnls)
    gross_profit = sum(p for p in trade_pnls if p > 0)
    gross_loss = -sum(p for p in trade_pnls if p < 0)
    profit_factor = gross_profit / gross_loss if gross_loss else (float("inf") if gross_profit else 0.0)

    peak = equity_curve[0]
    max_drawdown = 0.0
    for equity in equity_curve:
        peak = max(peak, equity)
        if peak:
            max_drawdown = max(max_drawdown, (peak - equity) / peak * 100)

    closed = len(trade_pnls)
    return PerformanceReport(
        starting_equity=starting_equity,
        ending_equity=ending,
        total_return_pct=total_return,
        closed_trades=closed,
        winning_trades=winners,
        losing_trades=losers,
        win_rate_pct=(winners / closed * 100) if closed else 0.0,
        profit_factor=profit_factor,
        max_drawdown_pct=max_drawdown,
    )
