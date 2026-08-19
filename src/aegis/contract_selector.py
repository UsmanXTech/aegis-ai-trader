from dataclasses import dataclass

from .domain import OptionStrategy
from .execution import MultiLegOrder, OptionLeg
from .options import OptionCandidate, score_candidate


@dataclass(frozen=True)
class SpreadSelection:
    strategy: OptionStrategy
    long_leg: OptionCandidate
    short_leg: OptionCandidate
    estimated_debit: float
    max_loss: float
    max_profit: float


class ContractSelector:
    """Selects liquid option pairs and converts them into defined-risk spreads."""

    def select_spread(
        self,
        strategy: OptionStrategy,
        candidates: list[OptionCandidate],
        *,
        underlying_price: float,
    ) -> SpreadSelection:
        if strategy not in (OptionStrategy.BULL_CALL_SPREAD, OptionStrategy.BEAR_PUT_SPREAD):
            raise ValueError("spread selection currently supports call and put spreads only")
        if not candidates:
            raise ValueError("no option candidates supplied")
        if underlying_price <= 0:
            raise ValueError("underlying price must be positive")

        option_type = "call" if strategy is OptionStrategy.BULL_CALL_SPREAD else "put"
        pool = [
            c for c in candidates
            if c.option_type.lower() == option_type and c.bid >= 0 and c.ask >= c.bid
        ]
        if len(pool) < 2:
            raise ValueError("at least two valid contracts of the required type are needed")

        pool.sort(key=score_candidate, reverse=True)
        best_pair: tuple[OptionCandidate, OptionCandidate, float] | None = None

        for i, first in enumerate(pool):
            for second in pool[i + 1 :]:
                if first.expiration != second.expiration:
                    continue
                if strategy is OptionStrategy.BULL_CALL_SPREAD:
                    long_leg, short_leg = sorted((first, second), key=lambda c: c.strike)
                else:
                    long_leg, short_leg = sorted((first, second), key=lambda c: c.strike, reverse=True)
                width = abs(short_leg.strike - long_leg.strike)
                if width <= 0:
                    continue
                debit = max(0.0, long_leg.ask - short_leg.bid)
                if debit <= 0 or debit >= width:
                    continue
                quality = score_candidate(long_leg) + score_candidate(short_leg)
                if best_pair is None or quality > best_pair[2]:
                    best_pair = (long_leg, short_leg, quality)

        if best_pair is None:
            raise ValueError("no valid defined-risk spread found")

        long_leg, short_leg, _ = best_pair
        debit = max(0.0, long_leg.ask - short_leg.bid)
        width = abs(short_leg.strike - long_leg.strike)
        max_loss = debit * 100
        max_profit = max(0.0, width - debit) * 100
        return SpreadSelection(strategy, long_leg, short_leg, debit, max_loss, max_profit)

    def to_order(self, selection: SpreadSelection, *, qty: int = 1) -> MultiLegOrder:
        if selection.strategy is OptionStrategy.BULL_CALL_SPREAD:
            legs = (
                OptionLeg(selection.long_leg.symbol, "buy", "buy_to_open"),
                OptionLeg(selection.short_leg.symbol, "sell", "sell_to_open"),
            )
        elif selection.strategy is OptionStrategy.BEAR_PUT_SPREAD:
            legs = (
                OptionLeg(selection.long_leg.symbol, "buy", "buy_to_open"),
                OptionLeg(selection.short_leg.symbol, "sell", "sell_to_open"),
            )
        else:
            raise ValueError("unsupported strategy")
        return MultiLegOrder(
            strategy=selection.strategy,
            legs=legs,
            qty=qty,
            limit_price=round(selection.estimated_debit, 2),
        )
