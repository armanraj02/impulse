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

def test_insights_pagination_and_search(client):
    response = client.get("/api/insights?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_student_risk_pagination(client):
    response = client.get("/api/students/risk?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_attendance_students_pagination(client):
    response = client.get("/api/attendance/students?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_academic_students_pagination(client):
    response = client.get("/api/academic/students?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_course_performance_pagination(client):
    response = client.get("/api/courses/performance?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_feedback_module_pagination(client):
    response = client.get("/api/feedback/module?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_feedback_instructor_pagination(client):
    response = client.get("/api/feedback/instructor?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data

def test_insights_filters_empty_result(client):
    response = client.get("/api/insights?insight_type=NONEXISTENT_TYPE&entity_type=NONEXISTENT")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0
