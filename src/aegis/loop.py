from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class LoopConfig:
    interval_seconds: int = 60
    max_cycles: int | None = None


class PaperTradingLoop:
    """Runs read/analyze cycles; order submission remains behind the paper gate."""

    def __init__(self, cycle: Callable[[], object], config: LoopConfig | None = None) -> None:
        self.cycle = cycle
        self.config = config or LoopConfig()
        if self.config.interval_seconds < 1:
            raise ValueError("interval_seconds must be positive")
        if self.config.max_cycles is not None and self.config.max_cycles < 1:
            raise ValueError("max_cycles must be positive when specified")

    def run(self) -> int:
        cycles = 0
        while self.config.max_cycles is None or cycles < self.config.max_cycles:
            self.cycle()
            cycles += 1
            if self.config.max_cycles is None or cycles < self.config.max_cycles:
                time.sleep(self.config.interval_seconds)
        return cycles
