from sqlalchemy import String, Integer, Date, DateTime, Enum, Numeric, func, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base
import enum

class ReceiptStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"

class Receipt(Base):
    __tablename__ = "receipts"
    __table_args__ = (
        UniqueConstraint("user_id", "image_fingerprint", name="uq_user_receipt_hash"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    merchant_name: Mapped[str] = mapped_column(String(120))
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    purchase_date: Mapped[str] = mapped_column(Date)
    status: Mapped[ReceiptStatus] = mapped_column(Enum(ReceiptStatus), default=ReceiptStatus.pending)
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    
    # New Production Fields
    image_key: Mapped[str | None] = mapped_column(String(255))
    image_fingerprint: Mapped[str | None] = mapped_column(String(64), index=True)
    
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())