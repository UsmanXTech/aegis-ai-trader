from aegis.optimization import StrategyParameters
from aegis.strategy_optimizer import StrategyEvaluation, select_robust_finalist


def evaluator(data, params: StrategyParameters):
    distance = abs(params.long_delta - 0.6) + abs(params.short_delta - 0.3)
    return StrategyEvaluation(12 - distance * 10, 3 + distance * 10, 25)


def test_selects_robust_finalist() -> None:
    results = select_robust_finalist(
        [1, 2],
        [3, 4],
        {
            "min_dte": [7], "max_dte": [30],
            "long_delta": [0.5, 0.6], "short_delta": [0.3, 0.4],
            "take_profit_pct": [0.5], "max_loss_pct": [1.0],
        },
        evaluator,
        finalists=2,
    )
    assert results
    assert results[0].parameters.long_delta == 0.6
    assert results[0].parameters.short_delta == 0.3
