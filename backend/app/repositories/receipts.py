from sqlalchemy.orm import Session
from app.models.receipt import Receipt

class ReceiptRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, receipt: Receipt) -> Receipt:
        self.db.add(receipt)
        self.db.commit()
        self.db.refresh(receipt)
        return receipt

    def get_all(self, limit: int = 100):
        return self.db.query(Receipt).order_by(Receipt.created_at.desc()).limit(limit).all()
