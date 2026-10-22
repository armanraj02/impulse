from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_departments_performance():
    response = client.get("/api/departments/performance")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "department_id" in data[0]
        assert "average_attendance_percentage" in data[0]

def test_batches_performance():
    response = client.get("/api/batches/performance")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "batch_id" in data[0]
        assert "average_attendance_percentage" in data[0]

def test_sections_performance():
    response = client.get("/api/sections/performance")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "section_id" in data[0]
        assert "average_attendance_percentage" in data[0]
