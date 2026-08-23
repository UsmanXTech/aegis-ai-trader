from __future__ import annotations

import argparse
from pathlib import Path

from .provider_ingest import load_provider_csv
from .provider_schema import ProviderFieldMap


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize a provider options CSV")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    quotes = load_provider_csv(args.input, ProviderFieldMap())
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        handle.write("timestamp,symbol,expiration,strike,option_type,bid,ask,underlying_price\n")
        for q in quotes:
            handle.write(f"{q.timestamp},{q.symbol},{q.expiration.isoformat()},{q.strike},{q.option_type},{q.bid},{q.ask},{q.underlying_price}\n")
    print(f"normalized={len(quotes)} output={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
