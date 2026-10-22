from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_students_risk():
    response = client.get("/api/students/risk")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    
    # We should have one row per student (if we paginated, page_size=10)
    assert len(data["items"]) <= 10
    
    # Total should be around 5000 (all students)
    assert data["total"] > 4000
    
    first = data["items"][0]
    assert "student_id" in first
    assert "risk_category" in first
    assert "risk_reason" in first

def test_get_students_risk_distribution():
    response = client.get("/api/students/risk/distribution")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) > 0
    categories = [item["category"] for item in data]
    assert "High Risk" in categories
    assert "No Risk" in categories
    
def test_students_risk_filters():
    # Test High Risk
    response = client.get("/api/students/risk?risk_category=High Risk")
    assert response.status_code == 200
    data = response.json()
    
    for item in data["items"]:
        assert item["risk_category"] == "High Risk"
        
    # Test No Risk
    response = client.get("/api/students/risk?risk_category=No Risk")
    assert response.status_code == 200
    data = response.json()
    
    for item in data["items"]:
        assert item["risk_category"] == "No Risk"
        
    # Test section filter
    response = client.get("/api/students/risk?section_id=1")
    assert response.status_code == 200
    
def test_students_risk_search():
    response = client.get("/api/students/risk?search=Tarak")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        # Should match either name or usn
        match = any("Tarak" in str(i["student_name"]) or "Tarak" in str(i["usn"]) for i in data["items"])
        assert match
