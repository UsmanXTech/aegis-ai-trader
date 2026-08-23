from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .optimizer import OptimizationResult


def write_optimizer_report(results: Iterable[OptimizationResult], path: str | Path, *, top_n: int = 10) -> None:
    if top_n < 1:
        raise ValueError("top_n must be positive")
    rows = [{"parameters": result.parameters, "score": result.score} for result in list(results)[:top_n]]
    Path(path).write_text(json.dumps(rows, indent=2), encoding="utf-8")
