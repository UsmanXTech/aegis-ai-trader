from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from .optimization import OptimizationScore, StrategyParameters, WalkForwardOptimizer


@dataclass(frozen=True)
class ResearchReport:
    training_ranked: tuple[OptimizationScore, ...]
    validation_ranked: tuple[OptimizationScore, ...]

    @property
    def best_parameters(self) -> StrategyParameters | None:
        return self.validation_ranked[0].parameters if self.validation_ranked else None


class ResearchRunner:
    """Connect a concrete strategy evaluator to training and validation datasets."""

    def __init__(self, evaluator: Callable[[Sequence[Any], StrategyParameters], tuple[float, float, int]]) -> None:
        self.optimizer = WalkForwardOptimizer(evaluator)

    def run(
        self,
        training: Sequence[Any],
        validation: Sequence[Any],
        parameter_grid: dict[str, Sequence[Any]],
        *,
        finalists: int = 5,
    ) -> ResearchReport:
        ranked = self.optimizer.optimize(training, parameter_grid)
        selected = ranked[:max(1, finalists)]
        validation_ranked = self.optimizer.evaluate_out_of_sample(validation, selected)
        return ResearchReport(tuple(ranked), tuple(validation_ranked))
