from sqlalchemy import String, Integer, Date, DateTime, Numeric, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base
import enum

class ReceiptStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"

class Receipt(Base):
    __tablename__ = "receipts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    merchant_name: Mapped[str] = mapped_column(String(120))
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    purchase_date: Mapped[str] = mapped_column(Date)
    status: Mapped[ReceiptStatus] = mapped_column(Enum(ReceiptStatus), default=ReceiptStatus.pending)
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())