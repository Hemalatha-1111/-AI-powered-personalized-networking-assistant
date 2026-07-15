import pytest 
from fastapi.testclient import TestClient 
from backend.main import app
client = TestClient(app)
def test_analyze_event_endpoint():
    response = client.post("/analyze-event", json={
        "description": "We are hosting an advanced machine learning conference discussing python models.",
        "labels": ["Technology", "Healthcare"]
    })
    assert response.status_code == 200
    assert "themes" in response.json()
def test_fact_check_endpoint():
    response = client.get("/fact-check?topic=Python (programming language)")
    assert response.status_code == 200
    assert response.json()["verified"] == True