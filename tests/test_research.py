from aegis.optimization import StrategyParameters
from aegis.research import ResearchRunner


def evaluator(data, params: StrategyParameters):
    distance = abs(params.long_delta - 0.6) + abs(params.short_delta - 0.3)
    return 10 - distance * 10, 4 + distance * 5, 20


def test_research_runner_produces_validation_leaderboard() -> None:
    report = ResearchRunner(evaluator).run(
        [1, 2, 3], [4, 5],
        {
            "min_dte": [7], "max_dte": [30],
            "long_delta": [0.5, 0.6], "short_delta": [0.3, 0.4],
            "take_profit_pct": [0.5], "max_loss_pct": [1.0],
        },
        finalists=2,
    )
    assert len(report.training_ranked) == 4
    assert len(report.validation_ranked) == 2
    assert report.best_parameters is not None
