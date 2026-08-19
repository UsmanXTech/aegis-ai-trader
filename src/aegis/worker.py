from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Sequence

from .chain_normalizer import normalize_option_chain
from .live_scan import scan_symbol
from .options import OptionCandidate
from .runner import PaperRunCoordinator, RunResult
from .scanner import UnderlyingSnapshot


@dataclass(frozen=True)
class WorkerConfig:
    symbols: tuple[str, ...] = ("SPY", "QQQ", "IWM")
    interval_seconds: int = 900
    days_forward: int = 45
    max_cycles: int | None = None


class PaperScanWorker:
    """Repeatedly scans markets and prepares paper trades.

    Order submission is intentionally not performed here. A future execution
    worker must explicitly opt into submission after the paper-only checks.
    """

    def __init__(self, coordinator: PaperRunCoordinator | None = None) -> None:
        self.coordinator = coordinator or PaperRunCoordinator()

    def run_cycle(
        self,
        *,
        api_key: str,
        secret_key: str,
        symbol: str,
        underlying: UnderlyingSnapshot,
        account_equity: float,
        portfolio_risk_pct: float,
        daily_loss_pct: float,
        open_positions: int,
    ) -> RunResult:
        chain = scan_symbol(
            api_key,
            secret_key,
            symbol,
            days_forward=45,
            strike_low=underlying.price * 0.80,
            strike_high=underlying.price * 1.20,
        )
        candidates: Sequence[OptionCandidate] = normalize_option_chain(chain)
        return self.coordinator.run_once(
            underlying,
            candidates,
            account_equity=account_equity,
            portfolio_risk_pct=portfolio_risk_pct,
            daily_loss_pct=daily_loss_pct,
            open_positions=open_positions,
        )

    def loop(self, *, config: WorkerConfig, cycle: Callable[[str], RunResult]) -> None:
        """Run a bounded/unbounded polling loop supplied with a safe cycle callback."""
        cycles = 0
        while config.max_cycles is None or cycles < config.max_cycles:
            for symbol in config.symbols:
                cycle(symbol)
            cycles += 1
            if config.max_cycles is not None and cycles >= config.max_cycles:
                break
            time.sleep(config.interval_seconds)
