from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from src.app.config.db_config import Base
from src.app.models.base import Auditable
from src.app.models.enum import StudentStatus, PaymentStatus


class Student(Base, Auditable):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    address: Mapped[str] = mapped_column(String)
    guardian_name:Mapped[str] = mapped_column(String, nullable=True)
    guardian_phone:Mapped[str] = mapped_column(String, nullable=True)
    fee_amount: Mapped[float] = mapped_column(default=0.0)  # Total course fee
    paid_amount: Mapped[float] = mapped_column(default=0.0)  # Total paid so far
    balance_amount: Mapped[float] = mapped_column(default=0.0)  # fee_amount - paid_amount
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SQLAlchemyEnum(PaymentStatus, native_enum=False, length=20)
    )
    status: Mapped[StudentStatus] = mapped_column(
        SQLAlchemyEnum(StudentStatus, name="student_status", create_type=False)
    )

    # Foreign Keys
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id", ondelete="CASCADE"))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))
    batch_id: Mapped[int] = mapped_column(ForeignKey("batch.id", ondelete="CASCADE"))

    # Relationships
    institution: Mapped["Institution"] = relationship("Institution")
    course: Mapped["Course"] = relationship("Course")
    batch: Mapped["Batch"] = relationship("Batch")
    attempts: Mapped[list["StudentAssessmentAttempt"]] = relationship(
        "StudentAssessmentAttempt", back_populates="student")

    def refresh_payment_status(self) -> None:
        """Recompute balance and payment status from fee_amount and paid_amount"""
        self.balance_amount = max(self.fee_amount - self.paid_amount, 0)  # no negatives

        if self.paid_amount == 0:
            self.payment_status = PaymentStatus.UNPAID
        elif self.paid_amount < self.fee_amount:
            self.payment_status = PaymentStatus.PARTIALLY_PAID
        else:
            self.payment_status = PaymentStatus.PAID