from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class StrategyParameters:
    min_dte: int
    max_dte: int
    long_delta: float
    short_delta: float
    take_profit_pct: float
    max_loss_pct: float


@dataclass(frozen=True)
class OptimizationScore:
    parameters: StrategyParameters
    return_pct: float
    max_drawdown_pct: float
    trades: int
    score: float


class WalkForwardOptimizer:
    """Grid-search parameters on training data, then evaluate finalists out-of-sample."""

    def __init__(self, evaluator: Callable[[Sequence[object], StrategyParameters], tuple[float, float, int]]) -> None:
        self.evaluator = evaluator

    def optimize(self, training_data: Sequence[object], parameter_grid: dict[str, Iterable[object]]) -> list[OptimizationScore]:
        keys = tuple(parameter_grid)
        candidates = []
        for values in product(*(parameter_grid[key] for key in keys)):
            params = StrategyParameters(**dict(zip(keys, values)))
            ret, drawdown, trades = self.evaluator(training_data, params)
            score = ret - drawdown * 0.5 + min(trades, 50) * 0.05
            candidates.append(OptimizationScore(params, ret, drawdown, trades, score))
        return sorted(candidates, key=lambda item: item.score, reverse=True)

    def evaluate_out_of_sample(self, data: Sequence[object], finalists: Sequence[OptimizationScore]) -> list[OptimizationScore]:
        results = []
        for finalist in finalists:
            ret, drawdown, trades = self.evaluator(data, finalist.parameters)
            results.append(OptimizationScore(finalist.parameters, ret, drawdown, trades, ret - drawdown * 0.5))
        return sorted(results, key=lambda item: item.score, reverse=True)
