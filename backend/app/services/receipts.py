from sqlalchemy.orm import Session
from app.models.receipt import Receipt, ReceiptStatus
from app.schemas.receipt import ReceiptCreate
from app.repositories.receipts import ReceiptRepository

class ReceiptService:
    def __init__(self, db: Session):
        self.repo = ReceiptRepository(db)

    def calculate_points(self, amount: float) -> int:
        # AMG Logic: 10 points per dollar
        return int(amount * 10)

    def process_submission(self, data: ReceiptCreate) -> Receipt:
        # Business Logic: Point calculation happens here
        points = self.calculate_points(data.total_amount)
        
        new_receipt = Receipt(
            **data.model_dump(),
            points_earned=points,
            status=ReceiptStatus.pending
        )
        return self.repo.create(new_receipt)