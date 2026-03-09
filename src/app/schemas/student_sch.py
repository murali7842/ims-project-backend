from pydantic import BaseModel, EmailStr
from src.app.models.enum import StudentStatus, PaymentStatus


class CreateStudentSch(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: str
    guardian_name: str
    guardian_phone: str
    status : StudentStatus
    institution_id: int
    course_id: int
    batch_id: int
