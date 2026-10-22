from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_courses_performance_endpoint():
    response = client.get("/api/courses/performance")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    
    # Test pagination bounds
    assert data["page"] == 1
    assert data["page_size"] == 10

def test_courses_performance_filtering():
    # Filter by department_id
    response = client.get("/api/courses/performance?department_id=1")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["department_id"] == 1

def test_feedback_module_endpoint():
    response = client.get("/api/feedback/module")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        # Verify rating is on 0-5 scale
        rating = item.get("average_rating")
        if rating is not None:
            assert 0 <= rating <= 5
        # Verify non-negative response counts
        responses = item.get("rating_responses")
        if responses is not None:
            assert responses >= 0

def test_feedback_module_filtering():
    response = client.get("/api/feedback/module?course_id=1")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["course_id"] == 1

def test_feedback_instructor_endpoint():
    response = client.get("/api/feedback/instructor")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        # Verify rating is on 0-5 scale
        rating = item.get("average_rating")
        if rating is not None:
            assert 0 <= rating <= 5
        # Verify non-negative response counts
        responses = item.get("rating_responses")
        if responses is not None:
            assert responses >= 0
