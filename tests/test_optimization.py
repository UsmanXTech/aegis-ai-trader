from aegis.optimization import StrategyParameters, WalkForwardOptimizer


def evaluator(data, params: StrategyParameters):
    # Deterministic fixture: closer-to-target parameters perform better.
    distance = abs(params.long_delta - 0.6) + abs(params.short_delta - 0.3)
    return (10 - distance * 10, 4 + distance * 10, 20)


def test_optimizer_ranks_best_parameters_first() -> None:
    optimizer = WalkForwardOptimizer(evaluator)
    results = optimizer.optimize(
        [1, 2, 3],
        {
            "min_dte": [7],
            "max_dte": [30],
            "long_delta": [0.5, 0.6],
            "short_delta": [0.3, 0.4],
            "take_profit_pct": [0.5],
            "max_loss_pct": [1.0],
        },
    )
    assert results[0].parameters.long_delta == 0.6
    assert results[0].parameters.short_delta == 0.3


def test_out_of_sample_evaluation() -> None:
    optimizer = WalkForwardOptimizer(evaluator)
    params = StrategyParameters(7, 30, 0.6, 0.3, 0.5, 1.0)
    finalist = optimizer.optimize([1], {k: [getattr(params, k)] for k in params.__dataclass_fields__})[0]
    results = optimizer.evaluate_out_of_sample([2], [finalist])
    assert results[0].trades == 20
