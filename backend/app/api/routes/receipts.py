from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.receipt import ReceiptCreate, ReceiptOut
from app.services.receipts import create_receipt_logic
from app.models.receipt import Receipt

router = APIRouter(prefix="/api/v1/receipts", tags=["receipts"])

@router.post("", response_model=ReceiptOut, status_code=201)
def submit_receipt(payload: ReceiptCreate, db: Session = Depends(get_db)):
    return create_receipt_logic(db, payload)

@router.get("", response_model=list[ReceiptOut])
def get_receipts(db: Session = Depends(get_db)):
    return db.query(Receipt).order_by(Receipt.created_at.desc()).all()
