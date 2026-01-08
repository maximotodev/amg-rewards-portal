import hashlib
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app.models.receipt import Receipt, ReceiptStatus
from app.schemas.receipt import ReceiptCreate
from app.repositories.receipts import ReceiptRepository

UPLOAD_DIR = Path("uploads")

class ReceiptService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReceiptRepository(db)
        UPLOAD_DIR.mkdir(exist_ok=True)

    def calculate_points(self, amount: float) -> int:
        return int(amount * 10)

    async def _process_image(self, image: UploadFile) -> tuple[str, str]:
        """Internal helper to handle file validation and hashing."""
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPEG and PNG are supported")

        content = await image.read()
        fingerprint = hashlib.sha256(content).hexdigest()

        file_ext = ".jpg" if image.content_type == "image/jpeg" else ".png"
        image_key = f"{uuid.uuid4().hex}{file_ext}"
        (UPLOAD_DIR / image_key).write_bytes(content)
        
        return image_key, fingerprint

    async def process_submission(self, data: ReceiptCreate, image: UploadFile) -> Receipt:
        # 1. Process Image
        image_key, fingerprint = await self._process_image(image)

        # 2. Map to Model
        points = self.calculate_points(data.total_amount)
        new_receipt = Receipt(
            **data.model_dump(),
            points_earned=points,
            status=ReceiptStatus.pending,
            image_key=image_key,
            image_fingerprint=fingerprint
        )

        # 3. Persist
        try:
            return self.repo.create(new_receipt)
        except Exception as e:
            # Handle duplicate fingerprint (Fraud Detection)
            if "uq_user_receipt_hash" in str(e) or "1062" in str(e):
                raise HTTPException(status_code=409, detail="Duplicate receipt detected.")
            raise e
