from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .agent import AegisAgent
from .journal import TradeJournal
from .options import OptionCandidate
from .scanner import MarketScanner, UnderlyingSnapshot
from .trade_pipeline import PreparedTrade, TradePipeline


@dataclass(frozen=True)
class RunResult:
    symbol: str
    action: str
    reason: str
    prepared_trade: PreparedTrade | None = None


class PaperRunCoordinator:
    """Runs one complete analysis cycle without directly placing an order."""

    def __init__(
        self,
        *,
        agent: AegisAgent | None = None,
        scanner: MarketScanner | None = None,
        pipeline: TradePipeline | None = None,
        journal: TradeJournal | None = None,
    ) -> None:
        self.agent = agent or AegisAgent()
        self.scanner = scanner or MarketScanner()
        self.pipeline = pipeline or TradePipeline()
        self.journal = journal or TradeJournal()

    def run_once(
        self,
        underlying: UnderlyingSnapshot,
        candidates: Sequence[OptionCandidate],
        *,
        account_equity: float,
        portfolio_risk_pct: float,
        daily_loss_pct: float,
        open_positions: int,
        max_loss_hint: float = 0.0,
        max_profit_hint: float = 0.0,
        thesis: str = "Generated from deterministic market signals.",
    ) -> RunResult:
        scan = self.scanner.scan(underlying)
        decision = self.agent.evaluate(
            symbol=underlying.symbol,
            snapshot=scan.market,
            max_loss=max_loss_hint,
            max_profit=max_profit_hint,
            thesis=thesis,
            account_equity=account_equity,
            portfolio_risk_pct=portfolio_risk_pct,
            daily_loss_pct=daily_loss_pct,
            open_positions=open_positions,
        )
        self.journal.append("decision", decision)

        if not decision.risk.approved:
            result = RunResult(underlying.symbol, "REJECT", "; ".join(decision.risk.reasons))
            self.journal.append("rejected", result)
            return result

        try:
            prepared = self.pipeline.prepare_spread(
                decision,
                candidates,
                underlying_price=underlying.price,
                account_equity=account_equity,
                portfolio_risk_pct=portfolio_risk_pct,
                daily_loss_pct=daily_loss_pct,
                open_positions=open_positions,
            )
        except ValueError as exc:
            result = RunResult(underlying.symbol, "REJECT", str(exc))
            self.journal.append("rejected", result)
            return result

        result = RunResult(underlying.symbol, "PREPARED", "paper order payload validated", prepared)
        self.journal.append("prepared", result)
        return result
