from sqlalchemy.orm import Session
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate

def calculate_points(amount: float) -> int:
    # AMG Logic: 10 points per dollar
    return int(amount * 10)

def create_receipt_logic(db: Session, data: ReceiptCreate) -> Receipt:
    new_receipt = Receipt(
        **data.model_dump(),
        points_earned=calculate_points(data.total_amount)
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return new_receipt