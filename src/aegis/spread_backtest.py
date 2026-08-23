from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .options_backtest import HistoricalOptionQuote, OptionLeg, OptionsBacktestEngine


@dataclass(frozen=True)
class SpreadTrade:
    entry_timestamp: str
    exit_timestamp: str
    entry_value: float
    exit_value: float
    pnl: float
    reason: str


class BullCallSpreadBacktester:
    """Backtest a long-call/short-call debit spread over normalized quotes."""

    def __init__(self, *, engine: OptionsBacktestEngine | None = None) -> None:
        self.engine = engine or OptionsBacktestEngine()

    def run(
        self,
        snapshots: Iterable[tuple[str, list[HistoricalOptionQuote]]],
        long_symbol: str,
        short_symbol: str,
        *,
        take_profit_pct: float = 0.50,
        stop_loss_pct: float = 0.50,
    ) -> list[SpreadTrade]:
        if take_profit_pct <= 0 or stop_loss_pct <= 0:
            raise ValueError("exit percentages must be positive")

        ordered = sorted(snapshots, key=lambda item: datetime.fromisoformat(item[0].replace("Z", "+00:00")))
        legs = [OptionLeg(long_symbol, "buy"), OptionLeg(short_symbol, "sell")]
        if len(ordered) < 2:
            return []

        entry_ts, entry_quotes = ordered[0]
        entry = self.engine.price_spread(entry_quotes, legs)
        if entry <= 0:
            raise ValueError("spread entry debit must be positive")

        trades: list[SpreadTrade] = []
        for timestamp, quotes in ordered[1:]:
            mark = self.engine.mark_to_mid(quotes, legs)
            pnl = mark - entry
            if pnl >= entry * take_profit_pct:
                trades.append(SpreadTrade(entry_ts, timestamp, entry, mark, pnl, "TAKE_PROFIT"))
                return trades
            if pnl <= -entry * stop_loss_pct:
                trades.append(SpreadTrade(entry_ts, timestamp, entry, mark, pnl, "STOP_LOSS"))
                return trades

        timestamp, quotes = ordered[-1]
        mark = self.engine.mark_to_mid(quotes, legs)
        trades.append(SpreadTrade(entry_ts, timestamp, entry, mark, mark - entry, "END_OF_DATA"))
        return trades
