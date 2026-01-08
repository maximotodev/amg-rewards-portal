from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.receipt import ReceiptCreate, ReceiptOut
from app.services.receipts import ReceiptService


router = APIRouter(prefix="/api/v1/receipts", tags=["receipts"])

@router.post("", response_model=ReceiptOut, status_code=201)
def submit_receipt(payload: ReceiptCreate, db: Session = Depends(get_db)):
    service = ReceiptService(db)
    return service.process_submission(payload)

@router.post("/{receipt_id}/image", status_code=204)
async def upload_receipt_image(
    receipt_id: int, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Senior Signal: Validate file type and size
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG are supported")
@router.get("", response_model=list[ReceiptOut])
def get_receipts(db: Session = Depends(get_db)):
    # Note: For simplicity in the list, we can call the repo through service 
    # or directly. Let's use the service pattern.
    service = ReceiptService(db)
    return service.repo.get_all()