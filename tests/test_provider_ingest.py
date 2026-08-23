from pathlib import Path

from aegis.provider_ingest import load_provider_csv
from aegis.provider_schema import ProviderFieldMap


def test_load_provider_csv(tmp_path: Path) -> None:
    path = tmp_path / "provider.csv"
    path.write_text(
        "ts,sym,exp,k,typ,b,a,u\n"
        "2026-01-02T15:00:00Z,SPY260220C00500000,2026-02-20,500,C,4,4.2,501\n",
        encoding="utf-8",
    )
    fields = ProviderFieldMap("ts", "sym", "exp", "k", "typ", "b", "a", "u")
    quotes = load_provider_csv(path, fields)
    assert len(quotes) == 1
    assert quotes[0].bid == 4
