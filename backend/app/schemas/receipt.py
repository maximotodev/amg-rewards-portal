from pydantic import BaseModel, Field, ConfigDict # Added ConfigDict
from datetime import date
from typing import Literal

class ReceiptCreate(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=64)
    merchant_name: str = Field(..., min_length=2, max_length=120)
    total_amount: float = Field(..., gt=0)
    purchase_date: date

class ReceiptOut(BaseModel):
    # Professional Pydantic V2 configuration
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    merchant_name: str
    total_amount: float
    purchase_date: date
    status: str
    points_earned: int