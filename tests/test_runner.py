from pathlib import Path

from aegis.options import OptionCandidate
from aegis.runner import PaperRunCoordinator
from aegis.scanner import UnderlyingSnapshot


def candidates() -> list[OptionCandidate]:
    return [
        OptionCandidate("SPY260925C00500000", 500, __import__("datetime").date(2026, 9, 25), "call", 5.0, 5.2, 2500, 0.55),
        OptionCandidate("SPY260925C00505000", 505, __import__("datetime").date(2026, 9, 25), "call", 3.4, 3.6, 2200, 0.35),
    ]


def test_runner_prepares_bull_call_spread(tmp_path: Path) -> None:
    runner = PaperRunCoordinator()
    runner.journal.path = tmp_path / "trades.jsonl"
    result = runner.run_once(
        UnderlyingSnapshot("SPY", 501, 500, 495, 0.04, 0.18, 0.10),
        candidates(),
        account_equity=10_000,
        portfolio_risk_pct=0,
        daily_loss_pct=0,
        open_positions=0,
        max_loss_hint=100,
        max_profit_hint=200,
    )
    assert result.action == "PREPARED"
    assert result.prepared_trade is not None
    assert (tmp_path / "trades.jsonl").exists()
