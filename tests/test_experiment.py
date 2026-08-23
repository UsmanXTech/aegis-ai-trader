from pathlib import Path

from aegis.experiment import ExperimentConfig, run_experiment


def test_experiment_writes_result(tmp_path: Path) -> None:
    csv = tmp_path / "quotes.csv"
    csv.write_text(
        "timestamp,symbol,expiration,strike,option_type,bid,ask,underlying_price\n"
        "2026-01-02T15:00:00Z,LONG,2026-09-25,500,C,4.0,4.2,501\n"
        "2026-01-02T15:00:00Z,SHORT,2026-09-25,505,C,2.0,2.1,501\n"
        "2026-01-02T16:00:00Z,LONG,2026-09-25,500,C,5.5,5.7,506\n"
        "2026-01-02T16:00:00Z,SHORT,2026-09-25,505,C,2.0,2.1,506\n",
        encoding="utf-8",
    )
    out = tmp_path / "result.json"
    run_experiment(ExperimentConfig(str(csv), "LONG", "SHORT"), out)
    assert out.exists()
    assert "config" in out.read_text(encoding="utf-8")
