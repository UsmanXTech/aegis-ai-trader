from pathlib import Path

from aegis.research_pipeline import run_bull_call_research


def test_research_pipeline(tmp_path: Path) -> None:
    path = tmp_path / "quotes.csv"
    path.write_text(
        "timestamp,symbol,expiration,strike,option_type,bid,ask,underlying_price\n"
        "2026-01-02T15:00:00Z,LONG,2026-09-25,500,C,4.0,4.2,501\n"
        "2026-01-02T15:00:00Z,SHORT,2026-09-25,505,C,2.0,2.1,501\n"
        "2026-01-02T16:00:00Z,LONG,2026-09-25,500,C,5.5,5.7,506\n"
        "2026-01-02T16:00:00Z,SHORT,2026-09-25,505,C,2.0,2.1,506\n",
        encoding="utf-8",
    )
    result = run_bull_call_research(path, "LONG", "SHORT")
    assert result.trades == 1
    assert result.report.closed_trades == 1
    assert result.report.ending_equity == 10155.0
