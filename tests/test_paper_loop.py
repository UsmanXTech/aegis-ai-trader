from aegis.paper_loop import AutonomousPaperLoop, PaperLoopConfig


def test_loop_runs_configured_cycles() -> None:
    calls: list[int] = []
    loop = AutonomousPaperLoop(lambda: calls.append(1), PaperLoopConfig(interval_seconds=1, max_cycles=3))
    assert loop.run() == 3
    assert len(calls) == 3
