from __future__ import annotations

import argparse

from .research_pipeline import run_bull_call_research


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an Aegis bull-call historical research backtest")
    parser.add_argument("csv", help="normalized historical options CSV")
    parser.add_argument("long_symbol")
    parser.add_argument("short_symbol")
    parser.add_argument("--take-profit", type=float, default=0.50)
    parser.add_argument("--stop-loss", type=float, default=0.50)
    args = parser.parse_args()

    result = run_bull_call_research(
        args.csv,
        args.long_symbol,
        args.short_symbol,
        take_profit_pct=args.take_profit,
        stop_loss_pct=args.stop_loss,
    )
    report = result.report
    print(f"trades={result.trades}")
    print(f"ending_equity={report.ending_equity:.2f}")
    print(f"return_pct={report.total_return_pct:.2f}")
    print(f"win_rate_pct={report.win_rate_pct:.2f}")
    print(f"profit_factor={report.profit_factor:.2f}")
    print(f"max_drawdown_pct={report.max_drawdown_pct:.2f}")
    print(f"rejected_quotes={result.rejected_quotes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
