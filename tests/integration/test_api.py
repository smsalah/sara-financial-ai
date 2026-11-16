import pytest
from fastapi.testclient import TestClient
from src.interfaces.api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Sara Financial AI API"

def test_audit_endpoint_smoke():
    payload = {
        "query": "Check ERP status for Zumzum Enterprise Solutions UK",
        "thread_id": "api_pytest_thread"
    }
    response = client.post("/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["thread_id"] == "api_pytest_thread"
    assert len(data["response"]) > 0
