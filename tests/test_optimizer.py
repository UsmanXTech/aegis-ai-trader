from aegis.optimizer import grid_optimize


def test_grid_optimizer_ranks_best_first() -> None:
    results = grid_optimize(
        {"take_profit": [0.25, 0.50], "stop_loss": [0.25, 0.50]},
        lambda p: p["take_profit"] - p["stop_loss"],
    )
    assert results[0].parameters == {"take_profit": 0.50, "stop_loss": 0.25}
    assert results[0].score == 0.25
    assert len(results) == 4
