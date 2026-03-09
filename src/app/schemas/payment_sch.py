from pydantic import BaseModel
from datetime import datetime

class CreatePaymentSch(BaseModel):
    student_id : int
    amount_paid : float
    payment_date : datetime
    payment_mode : str
    remarks : str