from __future__ import annotations

from typing import Any, Callable

from .option_contracts import parse_occ_symbol
from .options_backtest import HistoricalOptionQuote


class AlpacaHistoricalOptionsClient:
    """REST adapter for Alpaca historical option quotes.

    Alpaca option quote records provide quote timestamp/bid/ask; underlying prices
    are not part of the option quote record, so callers must provide a resolver
    when Aegis requires the underlying price for a given quote.
    """

    BASE_URL = "https://data.alpaca.markets/v1beta1/options/quotes"

    def __init__(self, api_key: str, secret_key: str, session: Any = None) -> None:
        if not api_key or not secret_key:
            raise ValueError("Alpaca API credentials are required")
        if session is None:
            import requests
            session = requests.Session()
        self.session = session
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key,
        }

    def historical_quotes(
        self,
        symbols: list[str],
        start: str,
        end: str,
        *,
        limit: int = 10000,
        feed: str = "indicative",
        underlying_price_resolver: Callable[[str, str], float] | None = None,
    ) -> list[HistoricalOptionQuote]:
        if not symbols:
            return []
        params: dict[str, Any] = {
            "symbols": ",".join(symbols),
            "start": start,
            "end": end,
            "limit": limit,
            "feed": feed,
            "sort": "asc",
        }
        quotes: list[HistoricalOptionQuote] = []
        while True:
            response = self.session.get(self.BASE_URL, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()
            for symbol, rows in payload.get("quotes", {}).items():
                for row in rows:
                    quotes.append(self._to_quote(symbol, row, underlying_price_resolver))
            token = payload.get("next_page_token")
            if not token:
                break
            params["page_token"] = token
        return quotes

    @staticmethod
    def _to_quote(
        symbol: str,
        row: dict[str, Any],
        underlying_price_resolver: Callable[[str, str], float] | None,
    ) -> HistoricalOptionQuote:
        contract = parse_occ_symbol(symbol)
        timestamp = str(row["t"])
        if underlying_price_resolver is None:
            raise ValueError("underlying_price_resolver is required for Alpaca option quote normalization")
        underlying_price = float(underlying_price_resolver(contract.underlying, timestamp))
        return HistoricalOptionQuote(
            timestamp=timestamp,
            symbol=symbol,
            expiration=contract.expiration,
            strike=contract.strike,
            option_type=contract.option_type,
            bid=float(row["bp"]),
            ask=float(row["ap"]),
            underlying_price=underlying_price,
        )
