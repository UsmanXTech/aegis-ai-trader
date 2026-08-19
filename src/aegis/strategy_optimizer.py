from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .optimization import OptimizationScore, StrategyParameters, WalkForwardOptimizer


@dataclass(frozen=True)
class StrategyEvaluation:
    return_pct: float
    max_drawdown_pct: float
    trades: int


def make_spread_optimizer(
    evaluator,
) -> WalkForwardOptimizer:
    """Adapt a concrete spread backtest into the generic walk-forward optimizer."""
    def wrapped(data: Sequence[object], params: StrategyParameters) -> tuple[float, float, int]:
        result = evaluator(data, params)
        if isinstance(result, StrategyEvaluation):
            return result.return_pct, result.max_drawdown_pct, result.trades
        return result.return_pct, result.max_drawdown_pct, result.trades

    return WalkForwardOptimizer(wrapped)


def select_robust_finalist(
    training: Sequence[object],
    validation: Sequence[object],
    parameter_grid: dict[str, Iterable[object]],
    evaluator,
    finalists: int = 5,
) -> list[OptimizationScore]:
    optimizer = make_spread_optimizer(evaluator)
    ranked = optimizer.optimize(training, parameter_grid)[:finalists]
    return optimizer.evaluate_out_of_sample(validation, ranked)
