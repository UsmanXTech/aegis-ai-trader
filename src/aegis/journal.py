from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class TradeJournal:
    """Small append-only JSONL journal for reproducible paper-trading runs."""

    def __init__(self, path: str | Path = "data/trades.jsonl") -> None:
        self.path = Path(path)

    def append(self, event: str, payload: Any) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "payload": asdict(payload) if is_dataclass(payload) else payload,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, default=str, separators=(",", ":")) + "\n")
