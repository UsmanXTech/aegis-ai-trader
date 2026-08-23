from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path

from .research_pipeline import run_bull_call_research


@dataclass(frozen=True)
class ExperimentConfig:
    csv_path: str
    long_symbol: str
    short_symbol: str
    take_profit_pct: float = 0.50
    stop_loss_pct: float = 0.50


def run_experiment(config: ExperimentConfig, output: str | Path) -> None:
    result = run_bull_call_research(
        config.csv_path,
        config.long_symbol,
        config.short_symbol,
        take_profit_pct=config.take_profit_pct,
        stop_loss_pct=config.stop_loss_pct,
    )
    payload = {"config": asdict(config), "result": asdict(result.report), "trades": result.trades}
    Path(output).write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
