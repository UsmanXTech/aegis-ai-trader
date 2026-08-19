from __future__ import annotations

from pathlib import Path
from typing import Any

from .data_adapter import OptionsDataAdapter
from .data_schema import HistoricalOptionRecord


class HistoricalOptionsLoader:
    def __init__(self, adapter: OptionsDataAdapter | None = None) -> None:
        self.adapter = adapter or OptionsDataAdapter()

    def load_csv(self, path: str | Path) -> list[HistoricalOptionRecord]:
        import csv

        file_path = Path(path)
        with file_path.open("r", newline="", encoding="utf-8") as handle:
            return self.adapter.normalize(csv.DictReader(handle))

    def load_parquet(self, path: str | Path) -> list[HistoricalOptionRecord]:
        try:
            import pandas as pd
        except ImportError as exc:
            raise RuntimeError("Parquet loading requires pandas") from exc
        frame = pd.read_parquet(Path(path))
        return self.adapter.normalize(frame.to_dict(orient="records"))
