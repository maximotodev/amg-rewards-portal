import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_submit_receipt_multipart():
    # Create a dummy image in memory
    file_content = b"fake-image-binary-content"
    file = io.BytesIO(file_content)
    
    # Multipart uses 'data' for fields and 'files' for the binary
    payload = {
        "user_id": "AMG_TEST_USER",
        "merchant_name": "Test Store",
        "total_amount": "50.00",
        "purchase_date": "2024-01-01"
    }
    
    files = {"image": ("test.jpg", file, "image/jpeg")}
    
    response = client.post("/api/v1/receipts", data=payload, files=files)
    
    assert response.status_code == 201
    assert response.json()["merchant_name"] == "Test Store"
    assert response.json()["points_earned"] == 500

def test_duplicate_prevention():
    # Submit the same content twice to trigger our 409 Conflict logic
    file_content = b"duplicate-check-content"
    payload = {
        "user_id": "AMG_TEST_USER",
        "merchant_name": "Unique Store",
        "total_amount": "10.00",
        "purchase_date": "2024-01-01"
    }
    
    # First submission
    client.post("/api/v1/receipts", data=payload, files={"image": ("1.jpg", io.BytesIO(file_content), "image/jpeg")})
    
    # Second submission (Same user + same image content)
    response = client.post("/api/v1/receipts", data=payload, files={"image": ("2.jpg", io.BytesIO(file_content), "image/jpeg")})
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Duplicate receipt detected."