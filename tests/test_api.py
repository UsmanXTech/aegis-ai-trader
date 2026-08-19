from fastapi.testclient import TestClient

from aegis.api import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "paper"}


def test_events_endpoint() -> None:
    response = client.get("/api/v1/events?limit=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
