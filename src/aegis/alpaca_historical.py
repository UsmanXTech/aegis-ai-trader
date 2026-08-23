from __future__ import annotations

from datetime import date
from typing import Any

from .options_backtest import HistoricalOptionQuote


class AlpacaHistoricalOptionsClient:
    """Small REST adapter for Alpaca historical option quotes.

    Credentials are read from environment variables and never stored in the repository.
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

    def historical_quotes(self, symbols: list[str], start: str, end: str, *, limit: int = 10000, feed: str = "indicative") -> list[HistoricalOptionQuote]:
        if not symbols:
            return []
        params = {"symbols": ",".join(symbols), "start": start, "end": end, "limit": limit, "feed": feed, "sort": "asc"}
        quotes: list[HistoricalOptionQuote] = []
        while True:
            response = self.session.get(self.BASE_URL, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()
            for symbol, rows in payload.get("quotes", {}).items():
                for row in rows:
                    quotes.append(self._to_quote(symbol, row))
            token = payload.get("next_page_token")
            if not token:
                break
            params["page_token"] = token
        return quotes

    @staticmethod
    def _to_quote(symbol: str, row: dict[str, Any]) -> HistoricalOptionQuote:
        # Contract metadata is not guaranteed in the quote response, so symbol parsing
        # is intentionally delegated to the existing OCC parser in options_backtest.
        from .options_backtest import parse_occ_symbol
        contract = parse_occ_symbol(symbol)
        return HistoricalOptionQuote(
            timestamp=str(row.get("t")),
            symbol=symbol,
            expiration=contract.expiration,
            strike=contract.strike,
            option_type=contract.option_type,
            bid=float(row["bp"]),
            ask=float(row["ap"]),
            underlying_price=float(row.get("underlying_price", 0.0)),
        )
