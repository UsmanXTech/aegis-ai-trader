from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .dataset_quality import validate_quotes
from .historical_options import HistoricalOptionsCsvLoader
from .performance import PerformanceReport, build_report
from .spread_backtest import BullCallSpreadBacktester


@dataclass(frozen=True)
class ResearchResult:
    report: PerformanceReport
    trades: int
    rejected_quotes: int


def run_bull_call_research(
    csv_path: str | Path,
    long_symbol: str,
    short_symbol: str,
    *,
    take_profit_pct: float = 0.50,
    stop_loss_pct: float = 0.50,
) -> ResearchResult:
    quotes = HistoricalOptionsCsvLoader().load(csv_path)
    quality = validate_quotes(quotes)
    valid = quality.valid_quotes
    snapshots: dict[str, list] = {}
    for quote in valid:
        snapshots.setdefault(quote.timestamp, []).append(quote)
    ordered = sorted(snapshots.items())
    trades = BullCallSpreadBacktester().run(
        ordered,
        long_symbol,
        short_symbol,
        take_profit_pct=take_profit_pct,
        stop_loss_pct=stop_loss_pct,
    )
    curve = [10_000.0]
    for trade in trades:
        curve.append(curve[-1] + trade.pnl)
    report = build_report(10_000.0, curve, [trade.pnl for trade in trades])
    return ResearchResult(report=report, trades=len(trades), rejected_quotes=quality.rejected_count)
