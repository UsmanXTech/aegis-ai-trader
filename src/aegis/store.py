from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class AegisStore:
    """Small local SQLite store for decisions, orders, positions and P&L."""

    def __init__(self, path: str | Path = "data/aegis.db") -> None:
        self.path = str(path)
        parent = Path(self.path).parent
        if str(parent) not in ("", "."):
            parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_events_type_time
                    ON events(event_type, created_at);
                """
            )

    def append(self, event_type: str, payload: Any) -> int:
        encoded = json.dumps(payload, default=str, separators=(",", ":"))
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO events(event_type, payload) VALUES (?, ?)",
                (event_type, encoded),
            )
            return int(cursor.lastrowid)

    def recent(self, event_type: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        if limit < 1:
            raise ValueError("limit must be positive")
        with self._connect() as db:
            if event_type:
                rows = db.execute(
                    "SELECT * FROM events WHERE event_type = ? ORDER BY id DESC LIMIT ?",
                    (event_type, limit),
                ).fetchall()
            else:
                rows = db.execute(
                    "SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,)
                ).fetchall()
        return [dict(row) for row in rows]
