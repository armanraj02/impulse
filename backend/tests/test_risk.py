from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_risk_distribution():
    response = client.get("/api/students/risk/distribution")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "category" in data[0]
        assert "count" in data[0]
        assert "percentage" in data[0]
