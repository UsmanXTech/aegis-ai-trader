from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .optimizer_backtest import optimize_exit_parameters
from .options_backtest import HistoricalOptionQuote


@dataclass(frozen=True)
class WalkForwardOptimizationResult:
    train_best: dict[str, float]
    test_score: float


def optimize_walk_forward(
    snapshots: Iterable[tuple[str, list[HistoricalOptionQuote]]],
    long_symbol: str,
    short_symbol: str,
    *,
    train_size: int,
    test_size: int,
    take_profit_values: Iterable[float],
    stop_loss_values: Iterable[float],
) -> list[WalkForwardOptimizationResult]:
    rows = sorted(snapshots, key=lambda item: item[0])
    if train_size < 1 or test_size < 1:
        raise ValueError("train_size and test_size must be positive")
    results: list[WalkForwardOptimizationResult] = []
    start = 0
    while start + train_size + test_size <= len(rows):
        train = rows[start : start + train_size]
        test = rows[start + train_size : start + train_size + test_size]
        optimized = optimize_exit_parameters(
            train,
            long_symbol,
            short_symbol,
            take_profit_values,
            stop_loss_values,
        )
        if not optimized.results:
            start += test_size
            continue
        best = optimized.results[0].parameters
        test_trades = optimize_exit_parameters(
            test,
            long_symbol,
            short_symbol,
            [best["take_profit_pct"]],
            [best["stop_loss_pct"]],
        )
        score = test_trades.results[0].score if test_trades.results else 0.0
        results.append(WalkForwardOptimizationResult(best, score))
        start += test_size
    return results
