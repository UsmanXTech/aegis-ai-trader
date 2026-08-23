from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Iterable


@dataclass(frozen=True)
class OptimizationResult:
    parameters: dict[str, float]
    score: float


def grid_optimize(
    parameter_grid: dict[str, Iterable[float]],
    evaluate: Callable[[dict[str, float]], float],
    *,
    maximize: bool = True,
) -> list[OptimizationResult]:
    names = list(parameter_grid)
    values = [list(parameter_grid[name]) for name in names]
    if any(not items for items in values):
        raise ValueError("parameter grid values must not be empty")
    results = [
        OptimizationResult(dict(zip(names, combo)), float(evaluate(dict(zip(names, combo)))))
        for combo in product(*values)
    ]
    return sorted(results, key=lambda item: item.score, reverse=maximize)
