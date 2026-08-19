from aegis.loop import LoopConfig, PaperTradingLoop


def test_loop_runs_configured_cycles() -> None:
    calls = []
    loop = PaperTradingLoop(lambda: calls.append(1), LoopConfig(interval_seconds=1, max_cycles=3))
    assert loop.run() == 3
    assert len(calls) == 3
