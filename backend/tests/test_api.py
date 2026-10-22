from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "FastAPI is running"}

def test_overview():
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "average_academic_performance" in data
    
def test_departments():
    response = client.get("/api/departments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_courses_pagination():
    response = client.get("/api/courses?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) <= 2

def test_students_search():
    response = client.get("/api/students?search=test")
    assert response.status_code == 200
    
def test_feedback():
    response = client.get("/api/feedback")
    assert response.status_code in (200, 404) # 404 is fine if table empty
