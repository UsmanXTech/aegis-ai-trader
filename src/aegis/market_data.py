from dataclasses import dataclass
from datetime import date, datetime

from alpaca.data.enums import DataFeed, OptionsFeed
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import OptionChainRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame


@dataclass(frozen=True)
class UnderlyingSnapshot:
    symbol: str
    close: float
    vwap: float | None
    volume: int
    timestamp: datetime


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
    ):
        request = OptionChainRequest(
            underlying_symbol=symbol,
            feed=OptionsFeed.INDICATIVE,
            expiration_date_gte=expiration_start,
            expiration_date_lte=expiration_end,
            strike_price_gte=strike_low,
            strike_price_lte=strike_high,
        )
        return self.options.get_option_chain(request)
