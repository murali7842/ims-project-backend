from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum, DateTime, ForeignKey, Integer, Float, Date
from src.app.config.db_config import Base
from src.app.models.base import Auditable


class Payment(Base, Auditable):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    amount_paid : Mapped[float] = mapped_column(Float, nullable=False)
    payment_date :Mapped[int] = mapped_column(Date, nullable=True)
    payment_mode : Mapped[str] = mapped_column(String, default="Cash")
    remarks : Mapped[str] = mapped_column(String, nullable=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))

    student: Mapped["Student"] = relationship("Student")


    # Relationships
    # student = relationship("Student", back_populates="payments")
