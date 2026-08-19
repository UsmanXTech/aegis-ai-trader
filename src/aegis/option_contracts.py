from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re


_OCC = re.compile(r"^(?P<root>[A-Z0-9.]{1,6})(?P<date>\d{6})(?P<type>[CP])(?P<strike>\d{8})$")


@dataclass(frozen=True)
class OptionContract:
    symbol: str
    underlying: str
    expiration: date
    option_type: str
    strike: float

    @property
    def days_to_expiration(self) -> int:
        return (self.expiration - date.today()).days


def parse_occ_symbol(symbol: str) -> OptionContract:
    match = _OCC.match(symbol.strip().upper())
    if not match:
        raise ValueError(f"unsupported OCC option symbol: {symbol}")
    expiration = date(
        2000 + int(match.group("date")[:2]),
        int(match.group("date")[2:4]),
        int(match.group("date")[4:6]),
    )
    return OptionContract(
        symbol=symbol.strip().upper(),
        underlying=match.group("root"),
        expiration=expiration,
        option_type=match.group("type"),
        strike=int(match.group("strike")) / 1000,
    )
