from __future__ import annotations

from datetime import date
from typing import Any, Iterable

from .options import OptionCandidate


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def normalize_option_chain(chain: Any) -> list[OptionCandidate]:
    """Convert Alpaca option-chain snapshots into Aegis candidates.

    The adapter intentionally accepts both SDK model objects and dictionaries,
    making the selection layer independent from Alpaca transport details.
    """
    items: Iterable[Any]
    if isinstance(chain, dict):
        items = chain.values()
    elif hasattr(chain, "data") and isinstance(chain.data, dict):
        items = chain.data.values()
    else:
        items = chain or []

    candidates: list[OptionCandidate] = []
    for item in items:
        symbol = str(_value(item, "symbol", ""))
        details = _value(item, "details", item)
        quote = _value(item, "latest_quote", _value(item, "quote", item))
        greeks = _value(item, "greeks", item)

        if not symbol:
            continue

        expiration = _value(details, "expiration_date")
        strike = _value(details, "strike_price")
        option_type = _value(details, "type", "")
        bid = _value(quote, "bid_price", _value(quote, "bid", 0.0))
        ask = _value(quote, "ask_price", _value(quote, "ask", 0.0))
        open_interest = _value(details, "open_interest", _value(item, "open_interest", 0))
        delta = _value(greeks, "delta")
        iv = _value(greeks, "implied_volatility", _value(item, "implied_volatility"))

        if isinstance(expiration, str):
            expiration = date.fromisoformat(expiration[:10])
        if expiration is None or strike is None:
            continue

        candidates.append(
            OptionCandidate(
                symbol=symbol,
                strike=float(strike),
                expiration=expiration,
                option_type=str(option_type).lower(),
                bid=float(bid or 0),
                ask=float(ask or 0),
                open_interest=int(open_interest or 0),
                delta=float(delta) if delta is not None else None,
                implied_volatility=float(iv) if iv is not None else None,
            )
        )
    return candidates
