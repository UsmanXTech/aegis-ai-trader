from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol


class AgentCycle(Protocol):
    def __call__(self) -> object: ...


@dataclass(frozen=True)
class PaperLoopConfig:
    interval_seconds: int = 60
    max_cycles: int | None = None


class AutonomousPaperLoop:
    """Orchestrate analysis cycles while leaving execution behind the paper/risk gate."""

    def __init__(self, cycle: AgentCycle, config: PaperLoopConfig | None = None) -> None:
        self.cycle = cycle
        self.config = config or PaperLoopConfig()
        if self.config.interval_seconds < 1:
            raise ValueError("interval_seconds must be positive")
        if self.config.max_cycles is not None and self.config.max_cycles < 1:
            raise ValueError("max_cycles must be positive")

    def run(self) -> int:
        import time

        completed = 0
        while self.config.max_cycles is None or completed < self.config.max_cycles:
            self.cycle()
            completed += 1
            if self.config.max_cycles is None or completed < self.config.max_cycles:
                time.sleep(self.config.interval_seconds)
        return completed
