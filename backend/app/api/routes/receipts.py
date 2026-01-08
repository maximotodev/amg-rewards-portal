from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.receipt import ReceiptCreate, ReceiptOut
from app.services.receipts import ReceiptService

router = APIRouter(prefix="/api/v1/receipts", tags=["receipts"])

@router.post("", response_model=ReceiptOut, status_code=201)
async def submit_receipt(
    user_id: Annotated[str, Form()],
    merchant_name: Annotated[str, Form()],
    total_amount: Annotated[float, Form()],
    purchase_date: Annotated[str, Form()],
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Construct schema from form-data
    payload = ReceiptCreate(
        user_id=user_id,
        merchant_name=merchant_name,
        total_amount=total_amount,
        purchase_date=purchase_date
    )
    
    service = ReceiptService(db)
    return await service.process_submission(payload, image)

@router.get("", response_model=list[ReceiptOut])
def get_receipts(db: Session = Depends(get_db)):
    service = ReceiptService(db)
    return service.repo.get_all()
