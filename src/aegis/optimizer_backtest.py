from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .optimizer import OptimizationResult, grid_optimize
from .spread_backtest import BullCallSpreadBacktester
from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class ParameterOptimization:
    results: tuple[OptimizationResult, ...]


def optimize_exit_parameters(
    snapshots: Iterable[tuple[str, list[HistoricalOptionQuote]]],
    long_symbol: str,
    short_symbol: str,
    take_profit_values: Iterable[float],
    stop_loss_values: Iterable[float],
) -> ParameterOptimization:
    snapshots = list(snapshots)
    engine = BullCallSpreadBacktester()

    def evaluate(params: dict[str, float]) -> float:
        trades = engine.run(
            snapshots,
            long_symbol,
            short_symbol,
            take_profit_pct=params["take_profit_pct"],
            stop_loss_pct=params["stop_loss_pct"],
        )
        return sum(trade.pnl for trade in trades)

    results = grid_optimize(
        {"take_profit_pct": take_profit_values, "stop_loss_pct": stop_loss_values},
        evaluate,
    )
    return ParameterOptimization(tuple(results))
