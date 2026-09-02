from __future__ import annotations

import argparse
import os

from .alpaca_dataset_builder import build_dataset
from .alpaca_historical import AlpacaHistoricalOptionsClient


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a normalized Aegis dataset from Alpaca option quotes")
    parser.add_argument("--symbols", required=True, help="Comma-separated OCC option symbols")
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--feed", default="indicative")
    parser.add_argument("--underlying-price", type=float, required=True,
                        help="Temporary fixed underlying price for a small connectivity smoke test only")
    args = parser.parse_args()

    key = os.environ.get("ALPACA_API_KEY")
    secret = os.environ.get("ALPACA_SECRET_KEY")
    if not key or not secret:
        raise SystemExit("Set ALPACA_API_KEY and ALPACA_SECRET_KEY before running this command.")

    client = AlpacaHistoricalOptionsClient(key, secret)
    count = build_dataset(
        client,
        [item.strip() for item in args.symbols.split(",") if item.strip()],
        args.start,
        args.end,
        args.output,
        feed=args.feed,
        underlying_price_resolver=lambda _symbol, _timestamp: args.underlying_price,
    )
    print(f"normalized_quotes={count} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
