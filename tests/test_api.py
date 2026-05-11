from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():

    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_market_analysis():

    response = client.get("/market-analysis")

    assert response.status_code == 200

    data = response.json()

    assert "total_articles" in data or "error" in data