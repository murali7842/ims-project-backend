import enum
from pydantic import BaseModel
from datetime import datetime, date

from src.app.models.payment import Payment


class PaymentSortBy(str, enum.Enum):
    ID = "id"
    AMOUNT_PAID = "amount_paid"
    PAYMENT_DATE = "payment_date"

class CreatePaymentSch(BaseModel):
    student_id : int
    amount_paid : float
    payment_date : datetime
    payment_mode : str
    remarks : str

class UpdatePaymentSch(CreatePaymentSch):
    id: int

class GetPaymentSch(BaseModel):
    id: int
    student_id: int
    amount_paid: float
    payment_date: date | None
    payment_mode: str
    remarks: str | None

    @staticmethod
    def from_entity(payment: Payment) -> "GetPaymentSch":
        return GetPaymentSch(
            id=payment.id,
            student_id=payment.student_id,
            amount_paid=payment.amount_paid,
            payment_date=payment.payment_date,
            payment_mode=payment.payment_mode,
            remarks=payment.remarks
        )
