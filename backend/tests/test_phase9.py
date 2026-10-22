import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_insights_distribution(client):
    response = client.get("/api/insights/distribution")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        item = data[0]
        assert "insight_type" in item
        assert "entity_type" in item
        assert "count" in item
        assert item["count"] >= 0

def test_insights_pagination_and_search(client):
    # Test base endpoint
    response = client.get("/api/insights?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert isinstance(data["items"], list)

    # Test search with empty results guarantee (random string)
    response_empty = client.get("/api/insights?search=xyz123randomnotfound")
    assert response_empty.status_code == 200
    empty_data = response_empty.json()
    assert empty_data["total"] == 0
    assert len(empty_data["items"]) == 0

    # Test filters
    response_filter = client.get("/api/insights?insight_type=RISK&entity_type=STUDENT")
    assert response_filter.status_code == 200
    filter_data = response_filter.json()
    if filter_data["items"]:
        for item in filter_data["items"]:
            assert item["insight_type"] == "RISK"
            assert item["entity_type"] == "STUDENT"
