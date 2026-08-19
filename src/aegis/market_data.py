from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from alpaca.data.enums import DataFeed, OptionsFeed
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import OptionChainRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from .options import OptionCandidate


@dataclass(frozen=True)
class UnderlyingSnapshot:
    symbol: str
    close: float
    vwap: float | None
    volume: int
    timestamp: datetime


def _parse_occ_symbol(symbol: str) -> tuple[float, date, str]:
    """Parse standard 21-character OCC option symbols."""
    if len(symbol) != 21:
        raise ValueError(f"unsupported option symbol format: {symbol}")
    option_type = symbol[12]
    if option_type not in {"C", "P"}:
        raise ValueError(f"invalid option type in symbol: {symbol}")
    expiration = datetime.strptime(symbol[6:12], "%y%m%d").date()
    strike = int(symbol[13:21]) / 1000
    return strike, expiration, option_type


class AlpacaMarketData:
    """Read-only Alpaca market-data gateway for the agent."""

    def __init__(self, api_key: str, secret_key: str) -> None:
        if not api_key or not secret_key:
            raise ValueError("Alpaca credentials are required")
        self.stock = StockHistoricalDataClient(api_key, secret_key)
        self.options = OptionHistoricalDataClient(api_key, secret_key)

    def latest_daily_bars(self, symbol: str, start: datetime, end: datetime | None = None):
        request = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
            feed=DataFeed.IEX,
        )
        return self.stock.get_stock_bars(request)

    def option_chain(
        self,
        symbol: str,
        *,
        expiration_start: date | None = None,
        expiration_end: date | None = None,
        strike_low: float | None = None,
        strike_high: float | None = None,
    ) -> list[OptionCandidate]:
        request = OptionChainRequest(
            underlying_symbol=symbol,
            feed=OptionsFeed.INDICATIVE,
            expiration_date_gte=expiration_start,
            expiration_date_lte=expiration_end,
            strike_price_gte=strike_low,
            strike_price_lte=strike_high,
        )
        snapshots = self.options.get_option_chain(request)
        result: list[OptionCandidate] = []
        for symbol, snapshot in snapshots.items():
            quote = snapshot.latest_quote
            if quote is None:
                continue
            try:
                strike, expiration, option_type = _parse_occ_symbol(symbol)
            except ValueError:
                continue
            result.append(
                OptionCandidate(
                    symbol=symbol,
                    strike=strike,
                    expiration=expiration,
                    option_type=option_type,
                    bid=float(quote.bid_price or 0),
                    ask=float(quote.ask_price or 0),
                    open_interest=int(snapshot.open_interest or 0),
                    delta=(float(snapshot.greeks.delta) if snapshot.greeks and snapshot.greeks.delta is not None else None),
                    implied_volatility=(float(snapshot.implied_volatility) if snapshot.implied_volatility is not None else None),
                )
            )
        return result
