import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app
from app.database import Base, get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_attendance_overview(client):
    response = client.get("/api/attendance/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "students_below_75" in data
    assert "average_attendance" in data
    assert data["total_students"] >= 0
    assert data["students_below_75"] >= 0
    assert 0 <= data["average_attendance"] <= 100

def test_academic_overview(client):
    response = client.get("/api/academic/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "students_below_50" in data
    assert "average_academic" in data
    assert data["total_students"] >= 0
    assert data["students_below_50"] >= 0
    assert 0 <= data["average_academic"] <= 100

def test_attendance_students_pagination(client):
    response = client.get("/api/attendance/students?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["items"]) <= 5
    assert "total" in data

def test_academic_students_pagination(client):
    response = client.get("/api/academic/students?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["items"]) <= 5
    assert "total" in data

def test_attendance_students_filter_department(client):
    # Try a department filter (assume department 1 exists)
    response = client.get("/api/attendance/students?department_id=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        # Verify that all returned students belong to branch_id 1
        for item in data["items"]:
            assert item["branch_id"] == 1

def test_academic_students_filter_department(client):
    response = client.get("/api/academic/students?department_id=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        for item in data["items"]:
            assert item["branch_id"] == 1

def test_attendance_students_filter_batch(client):
    response = client.get("/api/attendance/students?batch_id=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        for item in data["items"]:
            assert item["batch_id"] == 1
