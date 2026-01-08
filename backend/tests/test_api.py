from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "version" in data

def test_submit_receipt_validation():
    # Test invalid data (too short merchant name)
    bad_data = {
        "user_id": "test_user",
        "merchant_name": "A", 
        "total_amount": 10.0,
        "purchase_date": "2024-01-01"
    }
    response = client.post("/api/v1/receipts", json=bad_data)
    assert response.status_code == 422