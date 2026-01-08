import pytest
from app.services.receipts import ReceiptService

def test_calculate_points():
    # We don't need a DB for this test!
    service = ReceiptService(db=None) 
    assert service.calculate_points(10.50) == 105
    assert service.calculate_points(0) == 0
    assert service.calculate_points(100) == 1000

def test_points_rounding():
    service = ReceiptService(db=None)
    # Ensure float precision doesn't break our integers
    assert service.calculate_points(10.555) == 105