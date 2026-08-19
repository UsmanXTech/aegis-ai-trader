from __future__ import annotations

from fastapi import FastAPI, Query

from .store import AegisStore

app = FastAPI(title="Aegis AI Trader API", version="0.1.0")
store = AegisStore()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "paper"}


@app.get("/api/v1/events")
def events(
    event_type: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
) -> list[dict]:
    return store.recent(event_type=event_type, limit=limit)


@app.get("/api/v1/decisions")
def decisions(limit: int = Query(default=50, ge=1, le=500)) -> list[dict]:
    return store.recent(event_type="decision", limit=limit)


@app.get("/api/v1/orders")
def orders(limit: int = Query(default=50, ge=1, le=500)) -> list[dict]:
    return store.recent(event_type="order", limit=limit)


@app.get("/api/v1/positions")
def positions(limit: int = Query(default=50, ge=1, le=500)) -> list[dict]:
    return store.recent(event_type="position", limit=limit)


@app.get("/api/v1/pnl")
def pnl(limit: int = Query(default=100, ge=1, le=500)) -> list[dict]:
    return store.recent(event_type="pnl", limit=limit)
