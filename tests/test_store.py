from aegis.store import AegisStore


def test_store_round_trip(tmp_path) -> None:
    store = AegisStore(tmp_path / "aegis.db")
    event_id = store.append("decision", {"symbol": "SPY", "approved": True})

    assert event_id == 1
    events = store.recent("decision")
    assert len(events) == 1
    assert '"symbol":"SPY"' in events[0]["payload"]
