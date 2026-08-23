from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .research_pipeline import ResearchResult


def write_research_summary(result: ResearchResult, path: str | Path) -> None:
    payload = {
        "trades": result.trades,
        "rejected_quotes": result.rejected_quotes,
        "report": asdict(result.report),
    }
    Path(path).write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
